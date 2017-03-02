package pg_test

import (
	"testing"

	_ "github.com/lib/pq"
	"github.com/praelatus/praelatus/models"
)

func TestFieldGet(t *testing.T) {
	f := &models.Field{ID: 1}
	e := s.Fields().Get(f)
	failIfErr("Field Get", t, e)

	if f.Name == "" {
		t.Errorf("Expected a name got %s\n", f.Name)
	}
}

func TestFieldGetAll(t *testing.T) {
	f, e := s.Fields().GetAll()
	failIfErr("Field Get All", t, e)

	if f == nil || len(f) == 0 {
		t.Error("Expected multiple fields and got nil instead.")
	}
}

// func TestFieldGetByProject(t *testing.T) {
// 	p := models.Project{ID: 1}

// 	f, e := s.Fields().GetByProject(p)
// 	failIfErr("Field Get By Project", t, e)

// 	if f == nil || len(f) == 0 {
// 		t.Error("Expected multiple fields and got nil instead.")
// 	}
// }

func TestFieldSave(t *testing.T) {
	f1 := models.Field{
		ID:       2,
		Name:     "Field Save Test",
		DataType: "INT",
	}

	e := s.Fields().Save(f1)
	failIfErr("Field Save", t, e)

	f := &models.Field{ID: 2}
	e = s.Fields().Get(f)
	failIfErr("Field Save", t, e)

	if f.Name != "Field Save Test" {
		t.Errorf("Expected Story Points got: %s\n", f.Name)
	}

	if f.DataType != "INT" {
		t.Errorf("Expected INT got: %s\n", f.DataType)
	}
}

func TestFieldRemove(t *testing.T) {
	f := models.Field{
		ID:   2,
		Name: "TestField2",
	}

	e := s.Fields().Remove(f)
	failIfErr("Field Remove", t, e)
}
