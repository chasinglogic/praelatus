package v1

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
	"github.com/praelatus/praelatus/api/middleware"
	"github.com/praelatus/praelatus/api/utils"
	"github.com/praelatus/praelatus/models"
)

func workflowRouter(router *mux.Router) {
	router.HandleFunc("/workflows", GetAllWorkflows).Methods("GET")

	router.HandleFunc("/workflows/{id:[0-9]+}", GetWorkflow).Methods("GET")
	router.HandleFunc("/workflows/{id:[0-9]+}", UpdateWorkflow).Methods("PUT")
	router.HandleFunc("/workflows/{id:[0-9]+}", RemoveWorkflow).Methods("DELETE")

	router.HandleFunc("/workflows/{project_key}", CreateWorkflow).Methods("POST")
}

// GetAllWorkflows will retrieve all workflows from the DB and send a JSON response
func GetAllWorkflows(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
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

	u := middleware.GetUserSession(r)
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

	vars := mux.Vars(r)
	p := models.Project{Key: vars["project_key"]}

	err = Store.Projects().Get(*u, &p)
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
	vars := mux.Vars(r)
	i, err := strconv.Atoi(vars["id"])
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

	u := middleware.GetUserSession(r)
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
		vars := mux.Vars(r)
		id := vars["id"]
		i, err := strconv.Atoi(id)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write(utils.APIError(http.StatusText(http.StatusBadRequest)))
			return
		}

		t.ID = int64(i)
	}

	p := models.Project{Key: r.Context().Value("pkey").(string)}

	err = Store.Projects().Get(*u, &p)
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
	u := middleware.GetUserSession(r)
	if u == nil || !u.IsAdmin {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in as a system administrator to create a project"))
		return
	}

	vars := mux.Vars(r)
	i, err := strconv.Atoi(vars["id"])
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
