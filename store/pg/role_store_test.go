package pg_test

import (
	"testing"

	"github.com/praelatus/praelatus/models"
)

func TestRoleGet(t *testing.T) {
	l := &models.Role{ID: 1}
	e := s.Roles().Get(l)
	failIfErr("Role Get", t, e)

	if l == nil {
		t.Error("Expected a role and got nil instead.")
	}

	if l.Name == "" {
		t.Errorf("Expected role to have name got %s\n", l.Name)
	}
}

func TestRoleGetAll(t *testing.T) {
	l, e := s.Roles().GetAll()
	failIfErr("Role Get All", t, e)

	if l == nil {
		t.Error("Expected to get some roles and got nil instead.")
	}

	if len(l) == 0 {
		t.Errorf("Expected roles to be returned got %d roles instead\n", len(l))
	}
}

func TestRoleSave(t *testing.T) {
	l := models.Role{
		Name: "Rename me!",
	}

	e := s.Roles().New(&l)
	failIfErr("Role Save", t, e)

	l.Name = "SAVE_TEST_ROLE"

	e = s.Roles().Save(models.User{ID: 1}, l)
	failIfErr("Role Save", t, e)

	e = s.Roles().Get(&l)
	failIfErr("Role Save", t, e)

	if l.Name != "SAVE_TEST_ROLE" {
		t.Errorf("Expected: SAVE_TEST_ROLE Got: %s\n", l.Name)
	}
}

func TestRoleRemove(t *testing.T) {
	l := models.Role{
		Name: "Delete me!",
	}

	e := s.Roles().New(&l)
	failIfErr("Role Remove", t, e)

	e = s.Roles().Remove(models.User{ID: 1}, l)
	failIfErr("Role Remove", t, e)
}

func TestAddUserToRoleAndGetForUser(t *testing.T) {
	err := s.Roles().AddUserToRole(models.User{ID: 1},
		models.User{ID: 2}, models.Project{ID: 1}, models.Role{ID: 2})
	failIfErr("Add User to Role", t, err)

	l, e := s.Roles().GetForUser(models.User{ID: 2})
	failIfErr("Role Get All", t, e)

	if l == nil {
		t.Error("Expected to get some roles and got nil instead.")
	}

	if len(l) == 0 {
		t.Errorf("Expected roles to be returned got %d roles instead\n", len(l))
	}
}
