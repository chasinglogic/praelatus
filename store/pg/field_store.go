package pg

import (
	"database/sql"
	"errors"

	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/store"
)

// FieldStore contains methods for storing and retrieving Fields and
// FieldValues in a Postgres Database
type FieldStore struct {
	db *sql.DB
}

// Get retrieves a models.Field by ID
func (fs *FieldStore) Get(f *models.Field) error {
	var row *sql.Row

	row = fs.db.QueryRow(`SELECT id, name, data_type FROM fields 
			      WHERE id = $1 OR name = $2`, f.ID, f.Name)
	err := row.Scan(&f.ID, &f.Name, &f.DataType)
	if err != nil {
		return handlePqErr(err)
	}

	if f.DataType == "OPT" {
		fo := models.FieldOption{}
		err = getOpts(fs.db, f.ID, &fo)
		if err != nil {
			return handlePqErr(err)
		}

		f.Options = &fo
	}

	return nil
}

// GetAll will return all fields from the DB
func (fs *FieldStore) GetAll() ([]models.Field, error) {
	var fields []models.Field

	rows, err := fs.db.Query("SELECT id, name, data_type FROM fields;")
	if err != nil {
		return fields, handlePqErr(err)
	}

	for rows.Next() {
		var f models.Field

		err = rows.Scan(&f.ID, &f.Name, &f.DataType)
		if err != nil {
			return fields, handlePqErr(err)
		}

		if f.DataType == "OPT" {
			fo := models.FieldOption{}
			err = getOpts(fs.db, f.ID, &fo)
			if err != nil {
				return fields, handlePqErr(err)
			}

			f.Options = &fo
		}

		fields = append(fields, f)
	}

	return fields, nil
}

// GetByProject retrieves all Fields associated with a project
func (fs *FieldStore) GetByProject(p models.Project, t models.TicketType) ([]models.Field, error) {
	var fields []models.Field

	rows, err := fs.db.Query(`
SELECT fields.id, fields.name, fields.data_type 
FROM fields
JOIN field_tickettype_project AS ftp 
ON fields.id = ftp.field_id
JOIN projects AS p 
ON p.id = ftp.project_id
WHERE p.key = $1;`,
		p.Key)
	if err != nil {
		return fields, handlePqErr(err)
	}

	for rows.Next() {
		var f models.Field

		err = rows.Scan(&f.ID, &f.Name, &f.DataType)
		if err != nil {
			return fields, handlePqErr(err)
		}

		fields = append(fields, f)
	}

	return fields, nil
}

// AddToProject adds a field to a project's tickets
func (fs *FieldStore) AddToProject(u models.User, project models.Project, field *models.Field, ticketTypes ...models.TicketType) error {
	if !checkPermission(fs.db, "ADMIN_PROJECT", u.ID, project.ID) {
		return store.ErrPermissionDenied
	}

	if ticketTypes == nil {
		_, err := fs.db.Exec(`
INSERT INTO field_tickettype_project 
(field_id, project_id) VALUES ($1, $2)
`,
			field.ID, project.ID)
		return handlePqErr(err)
	}

	for _, typ := range ticketTypes {
		_, err := fs.db.Exec(`
INSERT INTO field_tickettype_project
(field_id, project_id, ticket_type_id) 
VALUES ($1, $2, $3)
`,
			field.ID, project.ID, typ.ID, u.ID)
		if err != nil {
			return handlePqErr(err)
		}
	}

	return nil

}

// Save updates an existing field in the database.
func (fs *FieldStore) Save(u models.User, field models.Field) error {
	if !checkIfAdmin(fs.db, u.ID) {
		return store.ErrPermissionDenied
	}

	_, err := fs.db.Exec(`
UPDATE fields SET 
(name, data_type) = ($1, $2) WHERE id = $3;
`,
		field.Name, field.DataType, field.ID)

	return handlePqErr(err)
}

// New creates a new Field in the database.
func (fs *FieldStore) New(field *models.Field) error {
	err := fs.db.QueryRow(`
INSERT INTO fields 
(name, data_type) VALUES ($1, $2)
RETURNING id;`,
		field.Name, field.DataType).
		Scan(&field.ID)
	if err != nil {
		return handlePqErr(err)
	}

	if field.DataType == "OPT" {
		for _, opt := range field.Options.Options {
			_, err = fs.db.Exec(`
INSERT INTO field_options (option, field_id) 
VALUES ($1, $2)
`,
				opt, field.ID)
			if err != nil {
				return handlePqErr(err)
			}
		}
	}

	return handlePqErr(err)
}

// Create will create the field if the given user is a system administrator
func (fs *FieldStore) Create(u models.User, field *models.Field) error {
	if !checkIfAdmin(fs.db, u.ID) {
		return store.ErrPermissionDenied
	}

	return fs.New(field)
}

// Remove updates an existing field in the database.
func (fs *FieldStore) Remove(u models.User, field models.Field) error {
	if !checkIfAdmin(fs.db, u.ID) {
		return store.ErrPermissionDenied
	}

	var c int

	tx, err := fs.db.Begin()
	if err != nil {
		return handlePqErr(err)
	}

	err = tx.QueryRow(`
SELECT COUNT(id) FROM field_values 
WHERE field_id = $1`,
		field.ID).Scan(&c)
	if err != nil {
		return handlePqErr(tx.Rollback())
	}

	if c > 0 {
		tx.Rollback()
		return errors.New("that field is currently in use, refusing to delete")
	}

	_, err = tx.Exec("DELETE FROM fields WHERE id = $1", field.ID)
	if err != nil {
		return handlePqErr(tx.Rollback())
	}

	return handlePqErr(tx.Commit())
}
