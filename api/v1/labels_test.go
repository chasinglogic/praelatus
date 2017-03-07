package v1

import (
	"bytes"
	"encoding/json"
	"net/http/httptest"
	"testing"

	"github.com/praelatus/praelatus/models"
)

func TestGetLabel(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/labels/1", nil)

	router.ServeHTTP(w, r)

	var p models.Label

	e := json.Unmarshal(w.Body.Bytes(), &p)
	if e != nil {
		t.Errorf("Failed with error %s\n", e.Error())
	}

	if p.ID != 1 {
		t.Errorf("Expected 1 Got %d\n", p.ID)
	}
}

func TestGetAllLabels(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/labels", nil)
	testLogin(r)

	router.ServeHTTP(w, r)

	var p []models.Label

	e := json.Unmarshal(w.Body.Bytes(), &p)
	if e != nil {
		t.Errorf("Failed with error %s\n", e.Error())
	}

	t.Log(w.Body)

	if len(p) != 2 {
		t.Errorf("Expected 2 Got %d\n", len(p))
		return
	}

	if p[0].Name != "mock" {
		t.Errorf("Expected mock Got %s\n", p[0].Name)
	}

}

func TestCreateLabel(t *testing.T) {
	p := models.Label{Name: "Snug"}
	byt, _ := json.Marshal(p)
	rd := bytes.NewReader(byt)

	w := httptest.NewRecorder()
	r := httptest.NewRequest("POST", "/api/v1/labels", rd)
	testAdminLogin(r)

	router.ServeHTTP(w, r)

	e := json.Unmarshal(w.Body.Bytes(), &p)
	if e != nil {
		t.Errorf("Failed with error %s", e.Error())
	}

	if p.ID != 1 {
		t.Errorf("Expected 1 Got %d", p.ID)
	}

	t.Log(w.Body)
}

func TestSearchLabels(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/labels/search?query=fake", nil)
	testLogin(r)

	router.ServeHTTP(w, r)

	var p []models.Label

	e := json.Unmarshal(w.Body.Bytes(), &p)
	if e != nil {
		t.Errorf("Failed with error %s\n", e.Error())
	}

	t.Log(w.Body)

	if len(p) != 1 {
		t.Errorf("Expected 1 Got %d\n", len(p))
		return
	}

	if p[0].Name != "fake" {
		t.Errorf("Expected fake Got %s\n", p[0].Name)
	}
}
