package v1_test

import (
	"bytes"
	"encoding/json"
	"net/http/httptest"
	"testing"

	"github.com/praelatus/praelatus/models"
)

func TestGetTicket(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/tickets/TEST-1", nil)

	router.ServeHTTP(w, r)

	var tk models.Ticket

	e := json.Unmarshal(w.Body.Bytes(), &tk)
	if e != nil {
		t.Errorf("Failed with error %s", e.Error())
	}

	if tk.Key != "TEST-1" {
		t.Errorf("Expected TEST-1 Got %s", tk.Key)
	}

	t.Log(w.Body)
}

func TestGetTicketPreloadComments(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/tickets/TEST-1?preload=comments", nil)

	router.ServeHTTP(w, r)

	var tk models.Ticket

	e := json.Unmarshal(w.Body.Bytes(), &tk)
	if e != nil {
		t.Errorf("Failed with error %s", e.Error())
	}

	t.Log(w.Body)

	if len(tk.Comments) == 0 {
		t.Errorf("Expected comments got 0 instead.")
		return
	}

	if tk.Key != "TEST-1" {
		t.Errorf("Expected TEST-1 Got %s", tk.Key)
	}
}

func TestGetAllTickets(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/tickets", nil)

	router.ServeHTTP(w, r)

	var tk []models.Ticket

	e := json.Unmarshal(w.Body.Bytes(), &tk)
	if e != nil {
		t.Errorf("Failed with error %s", e.Error())
		t.Log(w.Body)
	}

	t.Log(w.Body)

	if len(tk) != 2 {
		t.Errorf("Expected 2 tickets got %d", len(tk))
		return
	}

	if tk[0].Key != "TEST-1" {
		t.Errorf("Expected TEST-1 Got %s", tk[0].Key)
	}
}

func TestGetAllTicketsByProject(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/projects/TEST/tickets", nil)

	router.ServeHTTP(w, r)

	var tk []models.Ticket

	e := json.Unmarshal(w.Body.Bytes(), &tk)
	if e != nil {
		t.Errorf("Failed with error %s", e.Error())
	}

	t.Log(w.Body)

	if len(tk) != 2 {
		t.Errorf("Expected 2 tickets got %d", len(tk))
		return
	}

	if tk[0].Key != "TEST-1" {
		t.Errorf("Expected TEST-1 Got %s", tk[0].Key)
	}

}

func TestCreateTicket(t *testing.T) {
	tk := models.Ticket{Summary: "Nope"}
	byt, _ := json.Marshal(tk)
	rd := bytes.NewReader(byt)

	w := httptest.NewRecorder()
	r := httptest.NewRequest("POST", "/api/v1/tickets/TEST", rd)
	testLogin(w, r)

	router.ServeHTTP(w, r)

	e := json.Unmarshal(w.Body.Bytes(), &tk)
	if e != nil {
		t.Logf("Failed with error %s", e.Error())
		t.Logf("Received %s", string(w.Body.Bytes()))
		t.Fail()
	}

	if tk.ID != 1 {
		t.Errorf("Expected 1 Got %d", tk.ID)
	}

	t.Log(w.Body)
}

func TestGetComments(t *testing.T) {
	w := httptest.NewRecorder()
	r := httptest.NewRequest("GET", "/api/v1/tickets/TEST-1/comments", nil)

	router.ServeHTTP(w, r)

	var cm []models.Comment

	e := json.Unmarshal(w.Body.Bytes(), &cm)
	if e != nil {
		t.Errorf("Failed with error %s", e.Error())
		t.Log(w.Body)
	}

	if len(cm) != 1 {
		t.Errorf("Expected 1 comment got %d", len(cm))
	}

	t.Log(w.Body)
}

func TestCreateComment(t *testing.T) {
	cm := models.Comment{}
	byt, _ := json.Marshal(cm)
	rd := bytes.NewReader(byt)

	w := httptest.NewRecorder()
	r := httptest.NewRequest("POST", "/api/v1/tickets/TEST-1/comments", rd)
	testLogin(w, r)

	router.ServeHTTP(w, r)

	e := json.Unmarshal(w.Body.Bytes(), &cm)
	if e != nil {
		t.Errorf("Failed with error %s\n", e.Error())
		t.Log(w.Body)
	}

	if cm.ID == 0 {
		t.Errorf("Expected 1 Got %d\n", cm.ID)
	}

	t.Log(w.Body)
}
