package v1_test

import (
	"bytes"
	"encoding/json"
	"net/http/httptest"
	"testing"

	"github.com/praelatus/praelatus/models"
)

func TestGetTeam(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/teams/1", nil)

	router.ServeHTTP(w, r)

	var p models.Team

	e := json.Unmarshal(w.Body.Bytes(), &p)
	if e != nil {
		t.Errorf("Failed with error %s\n", e.Error())
	}

	if p.ID != 1 {
		t.Errorf("Expected 1 Got %d\n", p.ID)
	}

	t.Log(w.Body)
}

func TestGetAllTeams(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/teams", nil)
	testLogin(r)

	router.ServeHTTP(w, r)

	var p []models.Team

	e := json.Unmarshal(w.Body.Bytes(), &p)
	if e != nil {
		t.Errorf("Failed with error %s\n", e.Error())
	}

	t.Log(w.Body)

	if len(p) != 2 {
		t.Errorf("Expected 2 Got %d\n", len(p))
		return
	}

	if p[0].Name != "A" {
		t.Errorf("Expected A Got %s\n", p[0].Name)
	}
}

func TestCreateTeam(t *testing.T) {
	p := models.Team{Name: "Snug"}
	byt, _ := json.Marshal(p)
	rd := bytes.NewReader(byt)

	w := httptest.NewRecorder()
	r := httptest.NewRequest("POST", "/api/v1/teams", rd)
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
