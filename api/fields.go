package api

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/praelatus/backend/models"
	"github.com/pressly/chi"
)

func fieldRouter() chi.Router {
	router := chi.NewRouter()

	router.Get("/", GetAllFields)
	router.Post("/", CreateField)

	router.Get("/:id", GetField)
	router.Put("/:id", UpdateField)
	router.Delete("/:id", DeleteField)

	return router
}

// GetAllFields will retrieve all fields from the DB and send a JSON response
func GetAllFields(w http.ResponseWriter, r *http.Request) {
	u := GetUser(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(apiError("you must be logged in to view all fields"))
		return
	}

	fields, err := Store.Fields().GetAll()
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, fields)
}

// CreateField will create a field in the database based on the JSON sent by the
// client
func CreateField(w http.ResponseWriter, r *http.Request) {
	var t models.Field

	u := GetUser(r)
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

	err = Store.Fields().New(&t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, t)
}

// GetField will return the json representation of a field in the database
func GetField(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "id")

	i, err := strconv.Atoi(id)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError("invalid id"))
		log.Println(err)
		return
	}

	t := models.Field{ID: int64(i)}

	err = Store.Fields().Get(&t)
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, t)
}

// UpdateField will update a project based on the JSON representation sent to
// the API
func UpdateField(w http.ResponseWriter, r *http.Request) {
	var t models.Field

	u := GetUser(r)
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

	err = Store.Fields().Save(t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, t)
}

// DeleteField will remove the project indicated by the id passed in as a
// url parameter
func DeleteField(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "id")

	u := GetUser(r)
	if u == nil || !u.IsAdmin {
		w.WriteHeader(403)
		w.Write(apiError("you must be logged in as a system administrator to create a project"))
		return
	}

	i, err := strconv.Atoi(id)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError("invalid id"))
		log.Println(err)
		return
	}

	err = Store.Fields().Remove(models.Field{ID: int64(i)})
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	w.Write([]byte{})
}
