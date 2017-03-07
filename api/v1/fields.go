package v1

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
	"github.com/praelatus/praelatus/api/utils"
	"github.com/praelatus/praelatus/models"
)

func fieldRouter() *mux.Router {
	router := mux.NewRouter()

	router.HandleFunc("/", GetAllFields).Methods("GET")
	router.HandleFunc("/", CreateField).Methods("POST")

	router.HandleFunc("/{id}", GetField).Methods("GET")
	router.HandleFunc("/{id}", UpdateField).Methods("PUT")
	router.HandleFunc("/{id}", DeleteField).Methods("DELETE")

	return router
}

// GetAllFields will retrieve all fields from the DB and send a JSON response
func GetAllFields(w http.ResponseWriter, r *http.Request) {
	u := GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to view all fields"))
		return
	}

	fields, err := Store.Fields().GetAll()
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, fields)
}

// CreateField will create a field in the database based on the JSON sent by the
// client
func CreateField(w http.ResponseWriter, r *http.Request) {
	var t models.Field

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

	err = Store.Fields().New(&t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, t)
}

// GetField will return the json representation of a field in the database
func GetField(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	i, err := strconv.Atoi(id)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("invalid id"))
		log.Println(err)
		return
	}

	t := models.Field{ID: int64(i)}

	err = Store.Fields().Get(&t)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, t)
}

// UpdateField will update a project based on the JSON representation sent to
// the API
func UpdateField(w http.ResponseWriter, r *http.Request) {
	var t models.Field

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

	err = Store.Fields().Save(t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, t)
}

// DeleteField will remove the project indicated by the id passed in as a
// url parameter
func DeleteField(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	u := GetUserSession(r)
	if u == nil || !u.IsAdmin {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in as a system administrator to create a project"))
		return
	}

	i, err := strconv.Atoi(id)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("invalid id"))
		log.Println(err)
		return
	}

	err = Store.Fields().Remove(models.Field{ID: int64(i)})
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	w.Write([]byte{})
}
