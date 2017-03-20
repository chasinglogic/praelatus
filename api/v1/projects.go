package v1

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/praelatus/praelatus/api/middleware"
	"github.com/praelatus/praelatus/api/utils"
	"github.com/praelatus/praelatus/models"
)

func projectRouter(router *mux.Router) {
	router.HandleFunc("/projects", GetAllProjects).Methods("GET")
	router.HandleFunc("/projects", CreateProject).Methods("POST")

	router.HandleFunc("/projects/{key}", GetProject).Methods("GET")
	router.HandleFunc("/projects/{key}/tickets", GetAllTicketsByProject).Methods("GET")
	router.HandleFunc("/projects/{key}", RemoveProject).Methods("DELETE")
	router.HandleFunc("/projects/{key}", UpdateProject).Methods("PUT")

	router.HandleFunc("/projects/{key}/fields/{ticketType}", GetFieldsForScreen)
}

// GetProject will get a project by it's project key
func GetProject(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	key := vars["key"]

	p := models.Project{
		Key: key,
	}

	err := Store.Projects().Get(&p)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, p)
}

// GetAllProjects will get all the projects on this instance that the user has
// permissions to
func GetAllProjects(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)

	if u == nil {
		u = &models.User{ID: 0}
	}

	projects, err := Store.Projects().GetAllByPermission(*u)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, projects)
}

// GetAllTicketsByProject will get all the tickets for a given project
func GetAllTicketsByProject(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	pkey := vars["key"]

	tks, err := Store.Tickets().GetAllByProject(models.Project{Key: pkey})
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError("failed to retrieve tickets from the database"))
		log.Println(err)
		return
	}

	utils.SendJSON(w, tks)
}

// CreateProject will create a project based on the JSON representation sent to
// the API
func CreateProject(w http.ResponseWriter, r *http.Request) {
	var p models.Project

	u := middleware.GetUserSession(r)
	if u == nil || !u.IsAdmin {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in as a system administrator to create a project"))
		return
	}

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&p)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("invalid body"))
		log.Println(err)
		return
	}

	err = Store.Projects().New(&p)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, p)
}

// RemoveProject will remove the project indicated by the key passed in as a
// url parameter
func RemoveProject(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	key := vars["key"]

	u := middleware.GetUserSession(r)
	if u == nil || !u.IsAdmin {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in as a system administrator to create a project"))
		return
	}

	err := Store.Projects().Remove(models.Project{Key: key})
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	w.Write([]byte{})

}

// UpdateProject will update a project based on the JSON representation sent to
// the API
func UpdateProject(w http.ResponseWriter, r *http.Request) {
	var p models.Project

	u := middleware.GetUserSession(r)
	if u == nil || !u.IsAdmin {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in as a system administrator to create a project"))
		return
	}

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&p)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("invalid body"))
		log.Println(err)
		return
	}

	err = Store.Projects().New(&p)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, p)
}

// GetFieldsForScreen will return the appropriate fields based on the given
// project key and ticket type
func GetFieldsForScreen(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	key := vars["key"]
	ticketType := vars["ticketType"]

	w.Write([]byte(key + " " + ticketType))
}
