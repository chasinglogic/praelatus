package pg_test

import (
	"testing"

	"github.com/praelatus/praelatus/models"
)

func TestUserGet(t *testing.T) {
	u := &models.User{ID: 1}
	e := s.Users().Get(u)
	failIfErr("User Get", t, e)

	if u.Username == "" {
		t.Errorf("Expected a username got: %s\n", u.Username)
	}
}

func TestUserSearch(t *testing.T) {
	u, e := s.Users().Search("test")
	failIfErr("User Search", t, e)

	if len(u) == 0 {
		t.Error("Expected to get more than 0 types.")
	}
}

func TestUserGetAll(t *testing.T) {
	u, e := s.Users().GetAll()
	failIfErr("User Get All", t, e)

	if len(u) == 0 {
		t.Error("Expected to get more than 0 types.")
	}
}

func TestUserSave(t *testing.T) {
	u := models.User{ID: 4}
	e := s.Users().Get(&u)
	failIfErr("User Save", t, e)

	u.Username = "SaveUser"

	e = s.Users().Save(u)
	failIfErr("User Save", t, e)

	u = models.User{ID: 4}
	e = s.Users().Get(&u)
	failIfErr("User Save", t, e)

	if u.Username != "SaveUser" {
		t.Errorf("Expected: Test Save User Got: %s\n", u.Username)
	}
}

func TestUserRemove(t *testing.T) {
	u := models.User{ID: 3}
	e := s.Users().Remove(u)
	failIfErr("User Remove", t, e)
}
