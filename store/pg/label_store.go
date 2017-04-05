package pg

import (
	"database/sql"

	"github.com/praelatus/praelatus/models"
)

// LabelStore contains methods for storing and retrieving Labels from a
// Postgres DB
type LabelStore struct {
	db *sql.DB
}

// Get gets a label from the database
func (ls *LabelStore) Get(l *models.Label) error {
	err := ls.db.QueryRow(`
SELECT id, name FROM labels 
WHERE id = $1 OR name = $2
`,
		l.ID, l.Name).
		Scan(&l.ID, &l.Name)
	return handlePqErr(err)
}

// GetAll gets all the labels from the database
func (ls *LabelStore) GetAll() ([]models.Label, error) {
	var labels []models.Label
	rows, err := ls.db.Query("SELECT id, name FROM labels;")

	for rows.Next() {
		var l models.Label

		err := rows.Scan(&l.ID, &l.Name)
		if err != nil {
			return labels, handlePqErr(err)
		}

		labels = append(labels, l)
	}

	return labels, handlePqErr(err)
}

// New creates a new label in the database
func (ls *LabelStore) New(label *models.Label) error {
	err := ls.db.QueryRow(`
INSERT INTO labels (name) VALUES ($1)
RETURNING id;
`,
		label.Name).
		Scan(&label.ID)
	return handlePqErr(err)
}

// Save updates a label in the database
func (ls *LabelStore) Save(label models.Label) error {
	_, err := ls.db.Exec(`
UPDATE labels SET (name) = ($1) 
WHERE id = $2;
`,
		label.Name, label.ID)
	return handlePqErr(err)
}

// Remove updates a label in the database
func (ls *LabelStore) Remove(label models.Label) error {
	tx, err := ls.db.Begin()
	if err != nil {
		return handlePqErr(err)
	}
	_, err = tx.Exec(`DELETE FROM tickets_labels WHERE label_id = $1;`, label.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	_, err = tx.Exec(`DELETE FROM labels WHERE id = $1;`, label.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	return handlePqErr(tx.Commit())
}

// Search will take a name and search for the closest matching label
// in the store
func (ls *LabelStore) Search(query string) ([]models.Label, error) {
	rows, err := ls.db.Query(`
SELECT id, name FROM labels
WHERE name LIKE $1
`,
		query+"%")
	if err != nil {
		return nil, handlePqErr(err)
	}

	var labels []models.Label

	for rows.Next() {
		var l models.Label

		err = rows.Scan(&l.ID, &l.Name)
		if err != nil {
			return labels, handlePqErr(err)
		}

		labels = append(labels, l)
	}

	return labels, nil
}
