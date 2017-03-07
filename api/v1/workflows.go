package v1

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/praelatus/praelatus/models"
	"github.com/pressly/chi"
)

func workflowRouter() chi.Router {
	router := chi.NewRouter()

	router.Get("/", GetAllWorkflows)

	// Because of how chi does routing the id is actually the project key
	router.Post("/:id", CreateWorkflow)

	router.Get("/:id", GetWorkflow)
	router.Put("/:id", UpdateWorkflow)
	router.Delete("/:id", RemoveWorkflow)

	return router
}

// GetAllWorkflows will retrieve all workflows from the DB and send a JSON response
func GetAllWorkflows(w http.ResponseWriter, r *http.Request) {
	u := GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to view all workflows"))
		return
	}

	workflows, err := Store.Workflows().GetAll()
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, workflows)
}

// CreateWorkflow will create a workflow in the database based on the JSON sent by the
// client
func CreateWorkflow(w http.ResponseWriter, r *http.Request) {
	var t models.Workflow

	u := GetUserSession(r)
	if u == nil || !u.IsAdmin {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in as a system administrator to create a project"))
		return
	}

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("malformed json"))
		log.Println(err)
		return
	}

	// Because of how chi does routing the id is actually the project key
	p := models.Project{Key: chi.URLParam(r, "id")}

	err = Store.Projects().Get(&p)
	if err != nil {
		w.WriteHeader(404)
		w.Write(utils.APIError("project with that key does not exist"))
		log.Println(err)
		return
	}

	err = Store.Workflows().New(p, &t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, t)
}

// GetWorkflow will return the json representation of a workflow in the database
func GetWorkflow(w http.ResponseWriter, r *http.Request) {
	i, err := strconv.Atoi(chi.URLParam(r, "id"))
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("invalid id"))
		log.Println(err)
		return
	}

	t := models.Workflow{ID: int64(i)}

	err = Store.Workflows().Get(&t)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, t)
}

// UpdateWorkflow will update a project based on the JSON representation sent to
// the API
func UpdateWorkflow(w http.ResponseWriter, r *http.Request) {
	var t models.Workflow

	u := GetUserSession(r)
	if u == nil || !u.IsAdmin {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in as a system administrator to create a project"))
		return
	}

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("invalid body"))
		log.Println(err)
		return
	}

	if t.ID == 0 {
		id := chi.URLParam(r, "id")
		i, err := strconv.Atoi(id)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write(utils.APIError(http.StatusText(http.StatusBadRequest)))
			return
		}

		t.ID = int64(i)
	}

	p := models.Project{Key: r.Context().Value("pkey").(string)}

	err = Store.Projects().Get(&p)
	if err != nil {
		w.WriteHeader(404)
		w.Write(utils.APIError("project with that key does not exist"))
		log.Println(err)
		return
	}

	err = Store.Workflows().New(p, &t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, t)
}

// RemoveWorkflow will remove the project indicated by the id passed in as a
// url parameter
func RemoveWorkflow(w http.ResponseWriter, r *http.Request) {
	u := GetUserSession(r)
	if u == nil || !u.IsAdmin {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in as a system administrator to create a project"))
		return
	}

	i, err := strconv.Atoi(chi.URLParam(r, "id"))
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("invalid id"))
		log.Println(err)
		return
	}

	err = Store.Workflows().Remove(models.Workflow{ID: int64(i)})
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	w.Write([]byte{})
}
