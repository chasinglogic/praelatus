package pg_test

import (
	"testing"

	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/store"
)

func TestPermissionStoreGet(t *testing.T) {
	p := &models.PermissionScheme{ID: 1}
	e := s.Permissions().Get(models.User{ID: 1}, p)
	failIfErr("Permission Scheme Get", t, e)

	compareScheme := store.DefaultPermissionScheme
	compareScheme.ID = 1

	if p == nil {
		t.Error("Expected a label and got nil instead")
	}

	if p.String() != compareScheme.String() {
		t.Errorf("Expected: %s Got: %s\n",
			compareScheme.String(), p.String())
	}
}

func TestPermissionStoreGetAll(t *testing.T) {
	p, e := s.Permissions().GetAll(models.User{ID: 1})
	failIfErr("Permission Scheme Get All", t, e)

	if p == nil {
		t.Error("Expected some permission schemes got nil instead.")
	}

	if len(p) == 0 {
		t.Errorf("Expected permission schemes got %d schemes instead.\n",
			len(p))
	}

	return
}

func TestPermissionStoreSave(t *testing.T) {
	p := &models.PermissionScheme{ID: 3}
	e := s.Permissions().Get(models.User{ID: 1}, p)
	failIfErr("Permission Scheme Save: Get", t, e)

	p.Name = "SAVED THIS SCHEME YO"

	e = s.Permissions().Save(models.User{ID: 1}, *p)
	failIfErr("Permission Scheme Save", t, e)

	p = &models.PermissionScheme{ID: 3}
	e = s.Permissions().Get(models.User{ID: 1}, p)
	failIfErr("Permission Scheme Save: Get", t, e)

	if p.Name != "SAVED THIS SCHEME YO" {
		t.Errorf("Expected SAVED THIS SCHEME YO Got: %s\n", p.Name)
	}

	return
}

func TestPermissionStoreRemove(t *testing.T) {
	e := s.Permissions().Remove(models.User{ID: 1}, models.PermissionScheme{ID: 4})
	failIfErr("Permission Scheme Remove", t, e)
}
