package api

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/praelatus/backend/models"
	"github.com/pressly/chi"
)

func typeRouter() chi.Router {
	router := chi.NewRouter()

	router.Get("/", GetAllTicketTypes)
	router.Post("/", CreateTicketType)

	router.Get("/:id", GetTicketType)
	router.Put("/:id", UpdateTicketType)
	router.Delete("/:id", RemoveTicketType)

	return router
}

// GetAllTicketTypes will retrieve all types from the DB and send a JSON response
func GetAllTicketTypes(w http.ResponseWriter, r *http.Request) {
	u := mw.GetUser(r.Context())
	if u == nil {
		w.WriteHeader(403)
		w.Write(apiError("you must be logged in to view all types"))
		return
	}

	types, err := Store.Types().GetAll()
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, types)
}

// CreateTicketType will create a type in the database based on the JSON sent by the
// client
func CreateTicketType(w http.ResponseWriter, r *http.Request) {
	var t models.TicketType

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

	err = Store.Types().New(&t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, t)
}

// GetTicketType will return the json representation of a type in the database
func GetTicketType(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "id")

	i, err := strconv.Atoi(id)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError("invalid id"))
		log.Println(err)
		return
	}

	t := models.TicketType{ID: int64(i)}

	err = Store.Types().Get(&t)
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, t)
}

// UpdateTicketType will update a project based on the JSON representation sent to
// the API
func UpdateTicketType(w http.ResponseWriter, r *http.Request) {
	var t models.TicketType

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

	err = Store.Types().Save(t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, t)
}

// RemoveTicketType will remove the project indicated by the id passed in as a
// url parameter
func RemoveTicketType(w http.ResponseWriter, r *http.Request) {
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

	err = Store.Types().Remove(models.TicketType{ID: int64(i)})
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	w.Write([]byte{})
}
