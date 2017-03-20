package pg

import (
	"database/sql"
	"encoding/json"

	"github.com/praelatus/praelatus/models"
)

// ProjectStore contains methods for storing and retrieving Projects from a
// Postgres DB
type ProjectStore struct {
	db *sql.DB
}

func intoProject(row rowScanner, p *models.Project) error {
	var lead models.User
	var ljson json.RawMessage

	err := row.Scan(&p.ID, &p.CreatedDate, &p.Name, &p.Key,
		&p.Homepage, &p.IconURL, &p.Repo, &ljson)
	if err != nil {
		return err
	}

	err = json.Unmarshal(ljson, &lead)
	p.Lead = lead

	return err
}

// Get gets a project by it's ID in a postgres DB.
func (ps *ProjectStore) Get(p *models.Project) error {
	row := ps.db.QueryRow(`
SELECT p.id, created_date, name, 
       key, homepage, icon_url, repo,
       json_build_object('id', lead.id, 
                         'username', lead.username,  
                         'email', lead.email,  
                         'full_name', lead.full_name,  
                         'profile_picture', lead.profile_picture) AS lead
FROM projects  AS p
JOIN users AS lead ON lead.id = p.lead_id
WHERE p.id = $1
OR p.key = $2;
`,
		p.ID, p.Key)

	err := intoProject(row, p)
	return handlePqErr(err)
}

// GetAll returns all projects
func (ps *ProjectStore) GetAll() ([]models.Project, error) {
	var projects []models.Project

	rows, err := ps.db.Query(`
SELECT p.id, p.created_date, p.name, 
       p.key, p.repo, p.homepage, p.icon_url, 
       json_build_object('id', lead.id, 
                         'username', lead.username,  
                         'email', lead.email,  
                         'full_name', lead.full_name,  
                         'profile_picture', lead.profile_picture) AS lead
FROM projects AS p
JOIN users AS lead ON p.lead_id = lead.id;
`)

	if err != nil {
		return projects, handlePqErr(err)
	}

	for rows.Next() {
		var p models.Project

		err = intoProject(rows, &p)
		if err != nil {
			return projects, handlePqErr(err)
		}

		projects = append(projects, p)
	}

	return projects, nil
}

// GetAllByPermission returns all projects that the given user has access to
func (ps *ProjectStore) GetAllByPermission(u models.User) ([]models.Project, error) {
	var projects []models.Project

	rows, err := ps.db.Query(`
SELECT p.id, p.created_date, p.name, 
       p.key, p.repo, p.homepage, p.icon_url, 
       json_build_object('id', lead.id, 
                         'username', lead.username,  
                         'email', lead.email,  
                         'full_name', lead.full_name,  
                         'profile_picture', lead.profile_picture) AS lead
FROM projects AS p
JOIN users AS lead ON p.lead_id = lead.id
JOIN permissions AS perm ON p.id = perm.project_id
JOIN users AS u ON perm.user_id = u.id
WHERE (
    (perm.user_id = $1 AND perm.level > 0)
    OR u.is_admin = true
) 
OR perm.level < 0;
`,
		u.ID)

	if err != nil {
		return projects, handlePqErr(err)
	}

	for rows.Next() {
		var p models.Project

		err = intoProject(rows, &p)
		if err != nil {
			return projects, handlePqErr(err)
		}

		projects = append(projects, p)
	}

	return projects, nil
}

// New creates a new Project in the database.
func (ps *ProjectStore) New(project *models.Project) error {
	err := ps.db.QueryRow(`
INSERT INTO projects (name, key, repo, homepage, icon_url, lead_id) 
VALUES ($1, $2, $3, $4, $5, $6)
RETURNING id;
`,
		project.Name, project.Key, project.Repo, project.Homepage,
		project.IconURL, project.Lead.ID).
		Scan(&project.ID)

	return handlePqErr(err)
}

// Save updates a Project in the database.
func (ps *ProjectStore) Save(project models.Project) error {
	_, err := ps.db.Exec(`
UPDATE projects SET 
(name, key, repo, homepage, icon_url, lead_id) 
= ($1, $2, $3, $4, $5, $6)
WHERE projects.id = $7;
`,
		project.Name, project.Key, project.Repo, project.Homepage,
		project.IconURL, project.Lead.ID, project.ID)

	return handlePqErr(err)
}

// Remove updates a Project in the database.
func (ps *ProjectStore) Remove(project models.Project) error {
	tx, err := ps.db.Begin()
	if err != nil {
		return handlePqErr(err)
	}

	_, err = tx.Exec(`
DELETE FROM field_tickettype_project WHERE project_id = $1;
`,
		project.ID)

	if err != nil {
		return handlePqErr(tx.Rollback())
	}

	_, err = tx.Exec(`
DELETE FROM permissions WHERE project_id = $1;
`,
		project.ID)

	if err != nil {
		return handlePqErr(tx.Rollback())
	}

	_, err = tx.Exec(`
DELETE FROM field_values
WHERE ticket_id in(SELECT id FROM tickets WHERE project_id = $1);
`,
		project.ID)

	if err != nil {
		return handlePqErr(tx.Rollback())
	}

	_, err = tx.Exec(`
DELETE FROM tickets_labels 
WHERE ticket_id in(SELECT id FROM tickets WHERE project_id = $1);
`,
		project.ID)

	if err != nil {
		return handlePqErr(tx.Rollback())
	}

	_, err = tx.Exec(`DELETE FROM tickets WHERE project_id = $1;`,
		project.ID)

	if err != nil {
		tx.Rollback()
		return handlePqErr(tx.Rollback())
	}

	_, err = tx.Exec(`DELETE FROM projects WHERE id = $1;`,
		project.ID)

	if err != nil {
		return handlePqErr(tx.Rollback())
	}

	return handlePqErr(tx.Commit())
}
