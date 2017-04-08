package pg

import (
	"database/sql"
	"fmt"

	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/models/permission"
	"github.com/praelatus/praelatus/store"
)

// PermissionStore contains methods for storing, retrieving, and
// manipulating permissions, roles, and permission schemes in a
// Postgres DB
type PermissionStore struct {
	db *sql.DB
}

func (ps *PermissionStore) fillPermissions(p *models.PermissionScheme) error {
	var roles []models.Role

	rows, err := ps.db.Query(`SELECT id, name FROM roles`)
	if err != nil {
		return handlePqErr(err)
	}

	for rows.Next() {
		var role models.Role

		err = rows.Scan(&role.ID, &role.Name)
		if err != nil {
			return handlePqErr(err)
		}

		roles = append(roles, role)
	}

	for _, r := range roles {
		var permissions []permission.Permission

		rows, err := ps.db.Query(`
SELECT perm.name FROM permissions AS perm
JOIN permission_scheme_permissions AS scheme ON scheme.perm_id = perm.id
WHERE scheme.scheme_id = $1 AND scheme.role_id = $2
`,
			p.ID, r.ID)
		if err != nil {
			return handlePqErr(err)
		}

		for rows.Next() {
			var perm permission.Permission

			err = rows.Scan(&perm)
			if err != nil {
				return handlePqErr(err)
			}

			permissions = append(permissions, perm)
		}

		p.Permissions[r.Name] = permissions
	}

	return nil
}

// Get will return a permission scheme from the database
func (ps *PermissionStore) Get(u models.User, p *models.PermissionScheme) error {
	if !ps.IsAdmin(u) {
		return store.ErrPermissionDenied
	}

	err := ps.db.QueryRow(`
SELECT id, name, description FROM permission_schemes
WHERE id = $1 OR name = $2
`,
		p.ID, p.Name).
		Scan(&p.ID, &p.Name, &p.Description)

	if err != nil {
		return handlePqErr(err)
	}

	p.Permissions = make(map[string][]permission.Permission)
	return ps.fillPermissions(p)
}

// GetAll will return all permission schemes from the database
func (ps *PermissionStore) GetAll(u models.User) ([]models.PermissionScheme, error) {
	if !ps.IsAdmin(u) {
		return nil, store.ErrPermissionDenied
	}

	rows, err := ps.db.Query(`SELECT id, name, description FROM permission_schemes`)
	if err != nil {
		return nil, handlePqErr(err)
	}

	var schemes []models.PermissionScheme

	for rows.Next() {
		var p models.PermissionScheme
		p.Permissions = make(map[string][]permission.Permission)

		err = rows.Scan(&p.ID, &p.Name, &p.Description)
		if err != nil {
			return schemes, handlePqErr(err)
		}

		err = ps.fillPermissions(&p)
		if err != nil {
			return schemes, handlePqErr(err)
		}

		schemes = append(schemes, p)
	}

	return schemes, nil
}

// New will create the given permission scheme in the database and
// update the ID on the given permission scheme once it's returned
// from the database
func (ps *PermissionStore) New(p *models.PermissionScheme) store.Error {
	tx, err := ps.db.Begin()
	if err != nil {
		return store.Err{Err: err}
	}

	err = tx.QueryRow(`
INSERT INTO permission_schemes (name, description)
VALUES ($1, $2)
RETURNING id;
`,
		p.Name, p.Description).
		Scan(&p.ID)

	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	for role := range p.Permissions {
		var roleID int64

		err = tx.
			QueryRow("SELECT id FROM roles WHERE name = $1", role).
			Scan(&roleID)
		if roleID == 0 {
			tx.Rollback()
			fmt.Println(err)
			return store.ErrInvalidInput{Err: fmt.Errorf("%s is not a valid role", role)}
		}

		if err != nil {
			tx.Rollback()
			return handlePqErr(err)
		}

		for _, perm := range p.Permissions[role] {
			var permID int64

			err = tx.
				QueryRow("SELECT id FROM permissions WHERE name = $1", perm).
				Scan(&permID)
			if permID == 0 {
				tx.Rollback()
				return store.ErrInvalidInput{
					Err: fmt.Errorf("%s is not a valid permission", perm),
				}
			}

			if err != nil {
				tx.Rollback()
				return handlePqErr(err)
			}

			_, err = tx.Exec(`
INSERT INTO permission_scheme_permissions (scheme_id, role_id, perm_id)
VALUES ($1, $2, $3)`,
				p.ID, roleID, permID)
			if err != nil {
				tx.Rollback()
				return handlePqErr(err)
			}
		}
	}

	return handlePqErr(tx.Commit())
}

// Create is the action version of new, verifying that the user is an
// admin before creating the scheme
func (ps *PermissionStore) Create(u models.User, p *models.PermissionScheme) error {
	if !ps.IsAdmin(u) {
		return store.ErrPermissionDenied
	}

	return ps.New(p)
}

// Save will update the permission scheme in the database if it exists
func (ps *PermissionStore) Save(u models.User, p models.PermissionScheme) error {
	if !ps.IsAdmin(u) {
		return store.ErrPermissionDenied
	}

	tx, err := ps.db.Begin()
	if err != nil {
		return store.Err{Err: err}
	}

	_, err = tx.Exec(`
UPDATE permission_schemes 
SET (name, description) = ($1, $2)
WHERE id = $3`,
		p.Name, p.Description, p.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	for role := range p.Permissions {
		var roleID int64

		err = tx.
			QueryRow("SELECT id FROM roles WHERE name = $1", role).
			Scan(&roleID)
		if roleID == 0 {
			tx.Rollback()
			return store.ErrInvalidInput{Err: fmt.Errorf("%s is not a valid role", role)}
		}

		if err != nil {
			return handlePqErr(err)
		}

		for _, perm := range p.Permissions[role] {
			var permID int64

			err = tx.
				QueryRow("SELECT id FROM permissions WHERE name = $1", perm).
				Scan(&permID)
			if permID == 0 {
				tx.Rollback()
				return store.ErrInvalidInput{
					Err: fmt.Errorf("%s is not a valid permission", perm),
				}
			}

			if err != nil {
				tx.Rollback()
				return handlePqErr(err)
			}

			_, err = tx.Exec(`
DELETE FROM permission_scheme_permissions WHERE scheme_id = $1
`,
				p.ID)
			if err != nil {
				tx.Rollback()
				return handlePqErr(err)
			}

			_, err = tx.Exec(`
INSERT INTO permission_scheme_permissions (scheme_id, role_id, perm_id) 
VALUES ($1, $2, $3)`,
				p.ID, roleID, permID)
			if err != nil {
				tx.Rollback()
				return handlePqErr(err)
			}
		}
	}

	return handlePqErr(tx.Commit())

}

// Remove will remove the given permission scheme from the database
func (ps *PermissionStore) Remove(u models.User, p models.PermissionScheme) error {
	if !ps.IsAdmin(u) {
		return store.ErrPermissionDenied
	}

	tx, err := ps.db.Begin()
	if err != nil {
		return handlePqErr(err)
	}

	_, err = tx.Exec(`
DELETE FROM permission_scheme_permissions WHERE scheme_id = $1;
`,
		p.ID)
	if err != nil {
		return handlePqErr(err)
	}

	_, err = tx.Exec(`
DELETE FROM project_permission_schemes WHERE permission_scheme_id = $1;
`,
		p.ID)
	if err != nil {
		return handlePqErr(err)
	}

	_, err = tx.Exec(`
DELETE FROM permission_schemes WHERE id = $1;
`,
		p.ID)
	if err != nil {
		return handlePqErr(err)
	}

	return handlePqErr(tx.Commit())
}

// IsAdmin will return a boolean indicating whether the provided user
// is an admin or not
func (ps *PermissionStore) IsAdmin(u models.User) bool {
	return checkIfAdmin(ps.db, u.ID)
}

// CheckPermission will return a boolean indicating whether the
// permission is granted to the given user on the given project
func (ps *PermissionStore) CheckPermission(permission permission.Permission,
	project models.Project, user models.User) bool {
	return checkPermission(ps.db, permission, project.ID, user.ID)
}
