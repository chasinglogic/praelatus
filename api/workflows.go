package api

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/praelatus/backend/models"
	"github.com/praelatus/backend/mw"
	"github.com/pressly/chi"
)

func workflowRouter() chi.Router {
	router := chi.NewRouter()

	router.Get("/", GetAllWorkflows)
	router.Post("/:pkey", CreateWorkflow)

	router.Get("/:id", GetWorkflow)
	router.Put("/:id", UpdateWorkflow)
	router.Delete("/:id", RemoveWorkflow)

	return router
}

// GetAllWorkflows will retrieve all workflows from the DB and send a JSON response
func GetAllWorkflows(w http.ResponseWriter, r *http.Request) {
	u := mw.GetUser(r.Context())
	if u == nil {
		w.WriteHeader(403)
		w.Write(apiError("you must be logged in to view all workflows"))
		return
	}

	workflows, err := Store.Workflows().GetAll()
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, workflows)
}

// CreateWorkflow will create a workflow in the database based on the JSON sent by the
// client
func CreateWorkflow(w http.ResponseWriter, r *http.Request) {
	var t models.Workflow

	u := mw.GetUser(r.Context())
	if u == nil || !u.IsAdmin {
		w.WriteHeader(403)
		w.Write(apiError("you must be logged in as a system administrator to create a project"))
		return
	}

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError("malformed json"))
		log.Println(err)
		return
	}

	p := models.Project{Key: r.Context().Value("pkey").(string)}

	err = Store.Projects().Get(&p)
	if err != nil {
		w.WriteHeader(404)
		w.Write(apiError("project with that key does not exist"))
		log.Println(err)
		return
	}

	err = Store.Workflows().New(p, &t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, t)
}

// GetWorkflow will return the json representation of a workflow in the database
func GetWorkflow(w http.ResponseWriter, r *http.Request) {
	i, err := strconv.Atoi(chi.URLParam(r, "id"))
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError("invalid id"))
		log.Println(err)
		return
	}

	t := models.Workflow{ID: int64(i)}

	err = Store.Workflows().Get(&t)
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, t)
}

// UpdateWorkflow will update a project based on the JSON representation sent to
// the API
func UpdateWorkflow(w http.ResponseWriter, r *http.Request) {
	var t models.Workflow

	u := mw.GetUser(r.Context())
	if u == nil || !u.IsAdmin {
		w.WriteHeader(403)
		w.Write(apiError("you must be logged in as a system administrator to create a project"))
		return
	}

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError("invalid body"))
		log.Println(err)
		return
	}

	if t.ID == 0 {
		id := chi.URLParam(r, "id")
		i, err := strconv.Atoi(id)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write(apiError(http.StatusText(http.StatusBadRequest)))
			return
		}

		t.ID = int64(i)
	}

	p := models.Project{Key: r.Context().Value("pkey").(string)}

	err = Store.Projects().Get(&p)
	if err != nil {
		w.WriteHeader(404)
		w.Write(apiError("project with that key does not exist"))
		log.Println(err)
		return
	}

	err = Store.Workflows().New(p, &t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, t)
}

// RemoveWorkflow will remove the project indicated by the id passed in as a
// url parameter
func RemoveWorkflow(w http.ResponseWriter, r *http.Request) {
	u := mw.GetUser(r.Context())
	if u == nil || !u.IsAdmin {
		w.WriteHeader(403)
		w.Write(apiError("you must be logged in as a system administrator to create a project"))
		return
	}

	i, err := strconv.Atoi(chi.URLParam(r, "id"))
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError("invalid id"))
		log.Println(err)
		return
	}

	err = Store.Workflows().Remove(models.Workflow{ID: int64(i)})
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	w.Write([]byte{})
}
