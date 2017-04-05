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

// Get will return a permission scheme from the database
func (ps *PermissionStore) Get(u models.User, p *models.PermissionScheme) error {
	if !ps.IsAdmin(u) {
		return store.ErrPermissionDenied
	}

	return nil
}

// GetAll will return all permission schemes from the database
func (ps *PermissionStore) GetAll(u models.User) ([]models.PermissionScheme, error) {
	if !ps.IsAdmin(u) {
		return nil, store.ErrPermissionDenied
	}

	return nil, nil
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
		var roleID *int64

		err = tx.
			QueryRow("SELECT id FROM roles WHERE name = $1", role).
			Scan(roleID)
		if err != nil {
			return store.Err{Err: err}
		}

		if roleID == nil {
			tx.Rollback()
			return store.ErrInvalidInput{Err: fmt.Errorf("%s is not a valid role", role)}
		}

		for _, perm := range p.Permissions[role] {
			var permID *int64

			err = tx.
				QueryRow("SELECT id FROM permissions WHERE name = $1", perm).
				Scan(permID)
			if err != nil {
				tx.Rollback()
				return store.Err{Err: err}
			}

			if permID == nil {
				tx.Rollback()
				return store.ErrInvalidInput{
					Err: fmt.Errorf("%s is not a valid permission", perm),
				}
			}

			_, err = tx.Exec(`
INSERT INTO permission_scheme_permissions (scheme_id, role_id, perm_id)
VALUES ($1, $2, $3)`,
				p.ID, roleID, permID)
			if err != nil {
				tx.Rollback()
				return store.Err{Err: err}
			}
		}
	}

	return nil
}

// Create is the action version of new, verifying that the user is an
// admin before creating the scheme
func (ps *PermissionStore) Create(u models.User, p *models.PermissionScheme) error {
	if !ps.IsAdmin(u) {
		return store.ErrPermissionDenied
	}

	return ps.New(p)
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
