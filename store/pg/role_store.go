package pg

import (
	"database/sql"

	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/store"
)

// RoleStore contains methods for storing, and retrieving roles in a
// Postgres DB
type RoleStore struct {
	db *sql.DB
}

func (rs *RoleStore) Get(u models.User, r *models.Role) error {
	if !checkIfAdmin(rs.db, u.ID) {
		return store.ErrPermissionDenied
	}

	return nil
}

func (rs *RoleStore) GetAll(u models.User) ([]models.Role, error) {
	if !checkIfAdmin(rs.db, u.ID) {
		return store.ErrPermissionDenied
	}

	return nil
}

func (rs *RoleStore) New(r *models.Role) error {
	return nil
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

	return nil
}

func (rs *RoleStore) Remove(u models.User, r models.Role) error {
	if !checkIfAdmin(rs.db, u.ID) {
		return store.ErrPermissionDenied
	}

	return nil
}

func (rs *RoleStore) AddUserToRole(userAdding models.User, userToAdd models.User,
	project models.Project, role models.Role) error {
	if !checkIfAdmin(rs.db, userAdding.ID) {
		return store.ErrPermissionDenied
	}

	return nil
}

func (rs *RoleStore) GetForUser(u models.User) ([]models.Role, error) {
	if !checkIfAdmin(rs.db, u.ID) {
		return store.ErrPermissionDenied
	}

	return nil
}
