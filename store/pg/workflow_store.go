package pg

import (
	"database/sql"
	"encoding/json"
	"fmt"

	"github.com/praelatus/praelatus/models"
)

// WorkflowStore contains methods for saving/retrieving workflows from a
// postgres DB
type WorkflowStore struct {
	db *sql.DB
}

// Get gets a workflow from the database
func (ws *WorkflowStore) Get(w *models.Workflow) error {
	row := ws.db.QueryRow(`
SELECT w.id, w.name 
FROM workflows AS w
JOIN workflows_projects AS wkp ON wkp.workflow_id = w.id
JOIN projects AS p ON wkp.project_id = p.id
WHERE w.id = $1 OR w.name = $2`,
		w.ID, w.Name)
	err := row.Scan(&w.ID, &w.Name)
	if err != nil {
		return handlePqErr(err)
	}

	err = ws.getTransitions(w)
	return handlePqErr(err)
}

func getHooks(db *sql.DB, t *models.Transition) error {
	rows, err := db.Query(`
SELECT h.id, endpoint, method, body
FROM hooks AS h
JOIN transitions AS t ON t.id = h.transition_id`)
	if err != nil {
		return err
	}

	for rows.Next() {
		var h models.Hook

		err = rows.Scan(&h.ID, &h.Endpoint, &h.Method, &h.Body)
		if err != nil {
			return err
		}

		t.Hooks = append(t.Hooks, h)
	}

	return nil
}

func transitionsFromRows(db *sql.DB, rows *sql.Rows) ([]models.Transition, error) {
	var transitions []models.Transition

	for rows.Next() {
		var t models.Transition
		var status json.RawMessage

		err := rows.Scan(&t.ID, &t.Name, &status)
		if err != nil {
			return nil, handlePqErr(err)
		}

		err = json.Unmarshal(status, &t.ToStatus)
		if err != nil {
			return nil, handlePqErr(err)
		}

		err = getHooks(db, &t)
		if err != nil {
			return nil, handlePqErr(err)
		}

		transitions = append(transitions, t)
	}

	return transitions, nil
}

func (ws *WorkflowStore) getTransitions(w *models.Workflow) error {
	var statuses []struct {
		ID   int64
		Name string
	}

	rows, err := ws.db.Query(`
SELECT status.id, status.name
FROM workflow_statuses 
JOIN statuses AS status ON status.id = status_id
WHERE workflow_id = $1`,
		w.ID)
	if err != nil {
		return handlePqErr(err)
	}

	defer rows.Close()

	for rows.Next() {
		var s struct {
			ID   int64
			Name string
		}

		err := rows.Scan(&s.ID, &s.Name)
		if err != nil {
			return handlePqErr(err)
		}

		statuses = append(statuses, s)
	}

	for _, fromS := range statuses {

		rows, err = ws.db.Query(`
SELECT t.id, t.name, row_to_json(to_s.*)
FROM transitions AS t
JOIN statuses AS to_s ON to_s.id = t.to_status
WHERE t.from_status = $1
AND t.workflow_id = $2`,
			fromS.ID, w.ID)
		if err != nil {
			return handlePqErr(err)
		}

		if w.Transitions == nil {
			w.Transitions = make(map[string][]models.Transition, 0)
		}

		transitions, err := transitionsFromRows(ws.db, rows)
		if err != nil {
			return err
		}

		w.Transitions[fromS.Name] = transitions
	}

	return nil
}

func workflowsFromRows(rows *sql.Rows, ws *WorkflowStore) ([]models.Workflow, error) {
	var workflows []models.Workflow

	for rows.Next() {
		w := models.Workflow{}

		err := rows.Scan(&w.ID, &w.Name)
		if err != nil {
			return workflows, handlePqErr(err)
		}

		err = ws.getTransitions(&w)
		if err != nil {
			return workflows, handlePqErr(err)
		}

		workflows = append(workflows, w)
	}

	return workflows, nil
}

// GetAll gets all the workflows from the database
func (ws *WorkflowStore) GetAll() ([]models.Workflow, error) {
	rows, err := ws.db.Query("SELECT id, name FROM workflows;")
	if err != nil {
		return nil, handlePqErr(err)
	}

	return workflowsFromRows(rows, ws)
}

// GetByProject gets all the workflows for the given project
func (ws *WorkflowStore) GetByProject(p models.Project) ([]models.Workflow, error) {
	rows, err := ws.db.Query(`
SELECT w.id, w.name 
FROM workflows AS w
JOIN workflows_projects AS wp ON wp.workflow_id = w.id
JOIN projects AS p ON p.id = wp.project_id
WHERE p.id = $1 OR p.key = $2`,
		p.ID, p.Key)
	if err != nil {
		return []models.Workflow{}, handlePqErr(err)
	}

	return workflowsFromRows(rows, ws)
}

// GetForTicket will get the workflow associated with the given ticket
func (ws *WorkflowStore) GetForTicket(t models.Ticket) (models.Workflow, error) {
	var w models.Workflow

	row := ws.db.QueryRow(`
SELECT id, name FROM workflows
WHERE id = $1`,
		t.WorkflowID)
	err := row.Scan(&w.ID, &w.Name)
	if err != nil {
		return w, err
	}

	err = ws.getTransitions(&w)
	return w, err
}

// New creates a new workflow in the database
func (ws *WorkflowStore) New(p models.Project, workflow *models.Workflow) error {
	tx, err := ws.db.Begin()
	if err != nil {
		return handlePqErr(err)
	}

	err = tx.QueryRow(`
INSERT INTO workflows (name) 
VALUES ($1)
RETURNING id;`,
		workflow.Name).
		Scan(&workflow.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	_, err = tx.Exec(`
INSERT INTO workflows_projects (workflow_id, project_id) 
VALUES ($1, $2);`,
		workflow.ID, p.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	for fromStatus, transitions := range workflow.Transitions {
		var fromID int64

		err = tx.QueryRow(`SELECT id FROM statuses WHERE name = $1`, fromStatus).
			Scan(&fromID)
		if err != nil {
			tx.Rollback()
			return handlePqErr(err)

		}

		_, err = tx.Exec(`INSERT INTO workflow_statuses 
                                  (workflow_id, status_id) VALUES ($1, $2)`, workflow.ID, fromID)
		if err != nil {
			tx.Rollback()
			return handlePqErr(err)
		}

		for _, t := range transitions {
			err = tx.QueryRow(`INSERT INTO transitions
                                           (name, workflow_id, to_status, from_status)
                                           VALUES ($1, $2, $3, $4)
                                           RETURNING id`, t.Name, workflow.ID, t.ToStatus.ID, fromID).
				Scan(&t.ID)
			if err != nil {
				tx.Rollback()
				return handlePqErr(err)
			}

			if t.Hooks == nil || len(t.Hooks) == 0 {
				continue
			}

			for _, h := range t.Hooks {
				err = tx.QueryRow(`INSERT INTO hooks
       (endpoint, method, body, transition_id)
       VALUES ($1, $2, $3, $4, $5)
       RETURNING id`, h.Endpoint, h.Method, h.Body, t.ID).
					Scan(&h.ID)
				if err != nil {
					tx.Rollback()
					return handlePqErr(err)
				}

			}
		}
	}

	return handlePqErr(tx.Commit())
}

// Save updates a workflow in the database
// and by proxy doesn't support with statuses being changed to
// different statuses
func (ws *WorkflowStore) Save(w models.Workflow) error {
	tx, err := ws.db.Begin()
	if err != nil {
		return handlePqErr(err)
	}

	_, err = tx.Exec(`UPDATE workflows SET (name) = ($1) 
			  WHERE id = $2`, w.Name, w.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	for fromStatus, transitions := range w.Transitions {
		var fromID int64

		err = tx.QueryRow(`SELECT id FROM statuses WHERE name = $1`, fromStatus).
			Scan(&fromID)
		if err != nil {
			tx.Rollback()
			return handlePqErr(err)
		}

		rows, err := tx.Query(`SELECT status_id FROM workflow_statuses WHERE status_id = $1`, fromID)
		rows.Close()
		// check if the status already exists for this workflow
		// and if not then add it
		fmt.Println(fromID)
		if err == sql.ErrNoRows {
			fmt.Println("INSIDE IF")
			_, err = tx.Exec(`INSERT INTO workflow_statuses (workflow_id, status_id)
                                          VALUES ($1, $2)`, w.ID, fromID)
			if err != nil {
				tx.Rollback()
				return handlePqErr(err)
			}
		}

		for _, t := range transitions {
			_, err = tx.Exec(`UPDATE transitions SET
      (name, workflow_id, from_status, to_status)
      = ($1, $2, $3, $4)
      WHERE id = $5`, t.Name, w.ID, t.ToStatus.ID, fromID, t.ID)
			if err != nil {
				tx.Rollback()
				return handlePqErr(err)
			}

			if t.Hooks == nil || len(t.Hooks) == 0 {
				continue
			}

			for _, h := range t.Hooks {
				_, err = tx.Exec(`UPDATE hooks SET
       (endpoint, method, body, transition_id)
       = ($1, $2, $3, $4, $5)
       WHERE id = $6`, h.Endpoint, h.Method, h.Body, t.ID, h.ID)
				if err != nil {
					tx.Rollback()
					return handlePqErr(err)
				}

			}
		}
	}

	return handlePqErr(tx.Commit())
}

// Remove removes a workflow from the database
func (ws *WorkflowStore) Remove(w models.Workflow) error {
	tx, err := ws.db.Begin()
	if err != nil {
		return handlePqErr(err)
	}

	_, err = tx.Exec(`DELETE FROM hooks 
                          WHERE transition_id 
                          in(SELECT id FROM transitions WHERE workflow_id = $1);`, w.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	_, err = tx.Exec(`DELETE FROM workflow_statuses WHERE workflow_id = $1;`, w.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	_, err = tx.Exec(`DELETE FROM transitions WHERE workflow_id = $1;`, w.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	_, err = tx.Exec(`DELETE FROM workflows WHERE id = $1;`, w.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	return handlePqErr(tx.Commit())
}
