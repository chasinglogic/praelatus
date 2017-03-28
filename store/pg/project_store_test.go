package pg_test

import (
	"testing"

	"github.com/praelatus/praelatus/models"
)

func TestProjectGet(t *testing.T) {
	p := &models.Project{ID: 1}
	e := s.Projects().Get(models.User{ID: 1}, p)
	failIfErr("Project Get", t, e)

	if p.Key == "" {
		t.Errorf("Expected: TEST Got: %s\n", p.Key)
	}

	p = &models.Project{Key: "TEST"}
	e = s.Projects().Get(models.User{ID: 1}, p)
	failIfErr("Project Get", t, e)

	if p.ID == 0 {
		t.Errorf("Expected: 1 Got: %d\n", p.ID)
	}
}

func TestProjectGetAll(t *testing.T) {
	p, e := s.Projects().GetAll(models.User{ID: 1})
	failIfErr("Project Get All", t, e)

	if p == nil || len(p) == 0 {
		t.Error("Expected to get some projects and got nil instead.")
	}
}

func TestProjectSave(t *testing.T) {
	p := &models.Project{ID: 1}
	e := s.Projects().Get(models.User{ID: 1}, p)
	failIfErr("Project Save", t, e)

	p.IconURL = "TEST"

	e = s.Projects().Save(*p)
	failIfErr("Project Save", t, e)

	p = &models.Project{ID: 1}
	e = s.Projects().Get(models.User{ID: 1}, p)
	failIfErr("Project Save", t, e)

	if p.IconURL != "TEST" {
		t.Errorf("Expected project to have iconURL TEST got %s\n", p.IconURL)
	}
}

func TestProjectRemove(t *testing.T) {
	p := &models.Project{ID: 3}
	e := s.Projects().Remove(*p)
	failIfErr("Project Remove", t, e)
}
