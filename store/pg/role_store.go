package pg

import (
	"database/sql"

	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/models/permission"
	"github.com/praelatus/praelatus/store"
)

// RoleStore contains methods for storing, and retrieving roles in a
// Postgres DB
type RoleStore struct {
	db *sql.DB
}

func (rs *RoleStore) Get(r *models.Role) error {
	err := rs.db.QueryRow(`
SELECT id, name 
FROM roles 
WHERE id = $1 OR name = $2
`,
		r.ID, r.Name).
		Scan(&r.ID, &r.Name)

	return handlePqErr(err)
}

// GetAll will return all roles for this instance of Praelatus
func (rs *RoleStore) GetAll() ([]models.Role, error) {
	rows, err := rs.db.Query("SELECT id, name FROM roles")
	if err != nil {
		return nil, handlePqErr(err)
	}

	var roles []models.Role

	for rows.Next() {
		var r models.Role

		err = rows.Scan(&r.ID, &r.Name)
		if err != nil {
			return roles, handlePqErr(err)
		}

		roles = append(roles, r)
	}

	return roles, nil
}

func (rs *RoleStore) New(r *models.Role) error {
	err := rs.db.QueryRow(`
INSERT INTO roles (name) 
VALUES ($1)
RETURNING id
`,
		r.Name).
		Scan(&r.ID)

	return handlePqErr(err)
}

func (rs *RoleStore) Create(u models.User, r *models.Role) error {
	if !checkIfAdmin(rs.db, u.ID) {
		return store.ErrPermissionDenied
	}

	return rs.New(r)
}

func (rs *RoleStore) Save(u models.User, r models.Role) error {
	if !checkIfAdmin(rs.db, u.ID) {
		return store.ErrPermissionDenied
	}

	_, err := rs.db.Exec(`
UPDATE roles 
SET (name) = ($2)
WHERE id = $1
`,
		r.ID, r.Name)

	return handlePqErr(err)
}

func (rs *RoleStore) Remove(u models.User, r models.Role) error {
	if !checkIfAdmin(rs.db, u.ID) {
		return store.ErrPermissionDenied
	}

	tx, err := rs.db.Begin()
	if err != nil {
		return handlePqErr(err)
	}

	_, err = tx.Exec("DELETE FROM user_roles WHERE role_id = $1",
		r.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	_, err = tx.Exec(`
DELETE FROM permission_scheme_permissions WHERE role_id = $1
`,
		r.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	_, err = tx.Exec("DELETE FROM roles WHERE id = $1",
		r.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	return handlePqErr(tx.Commit())
}

func (rs *RoleStore) AddUserToRole(userAdding models.User, userToAdd models.User,
	project models.Project, role models.Role) error {
	if !checkPermission(rs.db, permission.ADMINPROJECT, project.ID, userAdding.ID) && !checkIfAdmin(rs.db, userAdding.ID) {
		return store.ErrPermissionDenied
	}

	_, err := rs.db.Exec(`
INSERT INTO user_roles (user_id, project_id, role_id)
VALUES ($1, $2, $3)
`,
		userToAdd.ID, project.ID, role.ID)

	return handlePqErr(err)
}

func (rs *RoleStore) GetForUser(u models.User) ([]models.Role, error) {
	var roles []models.Role

	rows, err := rs.db.Query(`
SELECT r.id, r.name, p.id, p.name, p.key
FROM roles AS r
JOIN user_roles AS ur ON ur.role_id = r.id
JOIN users AS u ON u.id = ur.user_id
JOIN projects AS p ON p.id = ur.project_id
WHERE u.id = $1
`,
		u.ID)

	if err != nil {
		return roles, handlePqErr(err)
	}

	for rows.Next() {
		var r models.Role
		r.Project = &models.Project{}

		err := rows.Scan(&r.ID, &r.Name, &r.Project.ID, &r.Project.Key, &r.Project.Name)
		if err != nil {
			return roles, handlePqErr(err)
		}

		roles = append(roles, r)
	}

	return roles, nil
}

// GetForProject will get all of the roles and associated users for
// the given project
func (rs *RoleStore) GetForProject(u models.User, p models.Project) ([]models.Role, error) {
	if !checkPermission(rs.db, "ADMIN_PROJECT", p.ID, u.ID) {
		return nil, store.ErrPermissionDenied
	}

	var roles []models.Role

	rows, err := rs.db.Query(`
SELECT r.id, r.name FROM roles AS r
JOIN user_roles AS ur ON ur.role_id = r.id
JOIN users AS u ON u.id = ur.user_id
JOIN projects AS p ON p.id = ur.project_id
WHERE p.id = $1
`,
		p.ID)

	if err != nil {
		return roles, handlePqErr(err)
	}

	for rows.Next() {
		var r models.Role

		err = rows.Scan(&r.ID, &r.Name)
		if err != nil {
			return roles, handlePqErr(err)
		}

		err = populateMembers(rs.db, p, &r)
		if err != nil {
			return roles, handlePqErr(err)
		}

		roles = append(roles, r)
	}

	return roles, nil
}

func populateMembers(db *sql.DB, p models.Project, r *models.Role) error {
	rows, err := db.Query(`
SELECT u.id, u.username, u.email, u.full_name, 
       u.profile_picture, u.is_admin
FROM users AS u
JOIN user_roles AS ur ON ur.user_id = u.id
WHERE ur.role_id = $1
AND ur.project_id = $2
`,
		r.ID, p.ID)
	if err != nil {
		return err
	}

	for rows.Next() {
		var u models.User

		err = rows.Scan(&u.ID, &u.Username, &u.Email,
			&u.FullName, &u.ProfilePic, &u.IsAdmin)
		if err != nil {
			return err
		}

		r.Members = append(r.Members, u)
	}

	return nil
}
