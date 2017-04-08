package v1_test

import (
	"bytes"
	"encoding/json"
	"net/http/httptest"
	"testing"

	"github.com/praelatus/praelatus/api/utils"
	"github.com/praelatus/praelatus/models"
)

func TestGetProject(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/projects/TEST", nil)

	router.ServeHTTP(w, r)

	var p models.Project

	e := json.Unmarshal(w.Body.Bytes(), &p)
	if e != nil {
		t.Errorf("Failed with error %s\n", e.Error())
	}

	if p.Key != "TEST" {
		t.Errorf("Expected TEST-1 Got %s\n", p.Key)
	}

	t.Log(w.Body)
}

func TestGetAllProjects(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/projects", nil)
	testLogin(w, r)

	router.ServeHTTP(w, r)

	var p []models.Project

	e := json.Unmarshal(w.Body.Bytes(), &p)
	if e != nil {
		t.Errorf("Failed with error %s\n", e.Error())
	}

	t.Log(w.Body)

	if len(p) != 2 {
		t.Errorf("Expected 2 Got %d\n", len(p))
		return
	}

	if p[0].Key != "TEST" {
		t.Errorf("Expected TEST-1 Got %s\n", p[0].Key)
	}
}

func TestCreateProject(t *testing.T) {
	p := models.Project{Name: "Grumpy Cat", Key: "NOPE"}
	byt, _ := json.Marshal(p)
	rd := bytes.NewReader(byt)

	w := httptest.NewRecorder()
	r := httptest.NewRequest("POST", "/api/v1/projects", rd)
	testAdminLogin(w, r)

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

func TestSetPermissionScheme(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("POST", "/api/v1/projects/TEST/permissionscheme/1", nil)
	testAdminLogin(w, r)

	router.ServeHTTP(w, r)

	var msg utils.APIMessage

	e := json.Unmarshal(w.Body.Bytes(), &msg)
	if e != nil {
		t.Errorf("Failed with error %s", e.Error())
	}

	if msg.Message != "successfully set permission scheme" {
		t.Errorf("Expected successfully set permission scheme Got: %s\n",
			msg.Message)
	}

	t.Log(w.Body)
}

func TestGetPermissionScheme(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/projects/TEST/permissionscheme", nil)
	testAdminLogin(w, r)

	router.ServeHTTP(w, r)

	var ps models.PermissionScheme

	e := json.Unmarshal(w.Body.Bytes(), &ps)
	if e != nil {
		t.Errorf("Failed with error %s", e.Error())
	}

	if ps.ID == 0 {
		t.Errorf("Expected ID to be set Got %s\n", ps)
	}

	if ps.Name == "" {
		t.Errorf("Expected Name to be set Got %s\n", ps)
	}

	t.Log(w.Body)
}

func TestGetRoles(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/projects/TEST/roles", nil)
	testAdminLogin(w, r)

	router.ServeHTTP(w, r)

	var role []models.Role

	e := json.Unmarshal(w.Body.Bytes(), &role)
	if e != nil {
		t.Errorf("Failed with error %s", e.Error())
	}

	if role[0].ID == 0 {
		t.Errorf("Expected ID to be set Got %s\n", role)
	}

	if role[0].Name == "" {
		t.Errorf("Expected Name to be set Got %s\n", role)
	}

	if role[0].Members == nil {
		t.Error("Expected members to be populated instead got nil")
	}

	t.Log(w.Body)
}

func TestAddUserToRole(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("POST",
		"/api/v1/projects/TEST/roles/1/addUser/1", nil)
	testAdminLogin(w, r)

	router.ServeHTTP(w, r)

	var msg utils.APIMessage

	e := json.Unmarshal(w.Body.Bytes(), &msg)
	if e != nil {
		t.Errorf("Failed with error %s", e.Error())
	}

	if msg.Message != "successfully added user to role" {
		t.Errorf("Expected successfully added user to role Got: %s\n",
			msg.Message)
	}

	t.Log(w.Body)
}
