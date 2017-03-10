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

func typeRouter(router *mux.Router) {
	router.HandleFunc("/types", GetAllTicketTypes).Methods("GET")
	router.HandleFunc("/types", CreateTicketType).Methods("POST")

	router.HandleFunc("/types/{id}", GetTicketType).Methods("GET")
	router.HandleFunc("/types/{id}", UpdateTicketType).Methods("PUT")
	router.HandleFunc("/types/{id}", RemoveTicketType).Methods("DELETE")
}

// GetAllTicketTypes will retrieve all types from the DB and send a JSON response
func GetAllTicketTypes(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to view all types"))
		return
	}

	types, err := Store.Types().GetAll()
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, types)
}

// CreateTicketType will create a type in the database based on the JSON sent by the
// client
func CreateTicketType(w http.ResponseWriter, r *http.Request) {
	var t models.TicketType

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

	err = Store.Types().New(&t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, t)
}

// GetTicketType will return the json representation of a type in the database
func GetTicketType(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	i, err := strconv.Atoi(vars["id"])
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("invalid id"))
		log.Println(err)
		return
	}

	t := models.TicketType{ID: int64(i)}

	err = Store.Types().Get(&t)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, t)
}

// UpdateTicketType will update a project based on the JSON representation sent to
// the API
func UpdateTicketType(w http.ResponseWriter, r *http.Request) {
	var t models.TicketType

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
		i, err := strconv.Atoi(vars["id"])
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write(utils.APIError(http.StatusText(http.StatusBadRequest)))
			return
		}

		t.ID = int64(i)
	}

	err = Store.Types().Save(t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, t)
}

// RemoveTicketType will remove the project indicated by the id passed in as a
// url parameter
func RemoveTicketType(w http.ResponseWriter, r *http.Request) {
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

	err = Store.Types().Remove(models.TicketType{ID: int64(i)})
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	w.Write([]byte{})
}
