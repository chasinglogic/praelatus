package v1

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"
	"strings"

	"github.com/gorilla/mux"
	"github.com/praelatus/praelatus/api/middleware"
	"github.com/praelatus/praelatus/api/utils"
	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/store"
)

func ticketRouter(router *mux.Router) {
	router.HandleFunc("/tickets", GetAllTickets).Methods("GET")

	router.HandleFunc("/tickets/{key}", GetTicket).Methods("GET")
	router.HandleFunc("/tickets/{key}", RemoveTicket).Methods("DELETE")
	router.HandleFunc("/tickets/{key}", UpdateTicket).Methods("PUT")

	router.HandleFunc("/tickets/{key}/transition", TransitionTicket).Methods("POST")

	router.HandleFunc("/tickets/{project_key}", CreateTicket).Methods("POST")

	router.HandleFunc("/tickets/{key}/comments", GetComments).Methods("GET")
	router.HandleFunc("/tickets/{key}/comments", CreateComment).Methods("POST")

	router.HandleFunc("/tickets/comments/{id}", UpdateComment).Methods("PUT")
	router.HandleFunc("/tickets/comments/{id}", RemoveComment).Methods("DELETE")
}

// GetTicket will get a ticket by the ticket key
func GetTicket(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	key := vars["key"]
	preload := r.FormValue("preload")

	tk := &models.Ticket{
		Key: key,
	}

	u := middleware.GetUserSession(r)
	if u == nil {
		u = &models.User{ID: 0}
	}

	err := Store.Tickets().Get(*u, tk)
	if err != nil {
		log.Println(err.Error())

		if err == store.ErrNotFound {
			w.WriteHeader(404)
			w.Write(utils.APIError("ticket not found"))
			return
		}

		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		return
	}

	if strings.Contains(preload, "comments") {
		cm, err := Store.Tickets().GetComments(*u, tk.Project, *tk)
		if err != nil && err != store.ErrNotFound {
			w.WriteHeader(500)
			w.Write(utils.APIError("failed to retrieve comments"))
			log.Println(err)
			return
		}

		tk.Comments = cm
	}

	utils.SendJSON(w, tk)
}

// GetAllTickets will get all the tickets for this instance
func GetAllTickets(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		u = &models.User{ID: 0}
	}

	tks, err := Store.Tickets().GetAll(*u)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError("failed to retrieve tickets from the database"))
		log.Println(err)
		return
	}

	utils.SendJSON(w, tks)
}

// CreateTicket will create a ticket in the database and send the json
// representation of the ticket back
func CreateTicket(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	pkey := vars["project_key"]

	u := middleware.GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to create a ticket"))
		return
	}

	var tk models.Ticket

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&tk)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("invalid body"))
		log.Println(err)
		return
	}

	err = Store.Tickets().New(models.Project{Key: pkey}, &tk)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, tk)
}

// RemoveTicket will remove the ticket with the given key from the database
func RemoveTicket(w http.ResponseWriter, r *http.Request) {
	key := r.Context().Value("key").(string)

	u := middleware.GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to remove a ticket"))
		return
	}

	tk := &models.Ticket{Key: key}

	err := Store.Tickets().Get(*u, tk)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		return
	}

	err = Store.Tickets().Remove(*u, tk.Project, *tk)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		return
	}

	w.Write([]byte{})
}

// UpdateTicket will update the ticket indicated by given key using the json
// from the body of the request
func UpdateTicket(w http.ResponseWriter, r *http.Request) {
	key := r.Context().Value("key").(string)

	u := middleware.GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to update a ticket"))
		return
	}

	var tk models.Ticket

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&tk)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	if tk.Key == "" {
		tk.Key = key
	}

	err = Store.Tickets().Save(*u, tk.Project, tk)
	if err != nil {
		utils.APIErr(w, 500, err.Error())
		return
	}

	w.Write(utils.Success())
}

// GetComments will get the comments for the ticket indicated by the ticket key
// in the url
func GetComments(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	key := vars["key"]

	u := middleware.GetUserSession(r)
	if u == nil {
		u = &models.User{ID: 0}
	}

	tk := &models.Ticket{Key: key}
	err := Store.Tickets().Get(*u, tk)
	if tk.ID == 0 {
		utils.APIErr(w, 404, "ticket not found")
		return
	}

	if err != nil {
		utils.APIErr(w, 500, err.Error())
		return
	}

	comments, err := Store.Tickets().GetComments(*u, tk.Project, *tk)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, comments)
}

// UpdateComment will update the comment with the given ID
func UpdateComment(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		utils.APIErr(w, 403, "you must be logged in to update a comment")
		return
	}

	var cm models.Comment

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&cm)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	if cm.ID == 0 {
		vars := mux.Vars(r)
		id, _ := strconv.Atoi(vars["id"])
		cm.ID = int64(id)
	}

	tk := &models.Ticket{Key: cm.TicketKey}
	err := Store.Tickets().Get(*u, tk)
	if tk.ID == 0 {
		utils.APIErr(w, 404, "ticket not found")
		return
	}

	if err != nil {
		utils.APIErr(w, 500, err.Error())
		return
	}

	err = Store.Tickets().SaveComment(cm)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	w.Write([]byte{})
}

// RemoveComment will remove the ticket with the given key from the database
func RemoveComment(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to update a ticket"))
		return
	}

	vars := mux.Vars(r)
	id, _ := strconv.Atoi(vars["id"])

	err := Store.Tickets().RemoveComment(models.Comment{ID: int64(id)})
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	w.Write([]byte{})
}

// CreateComment will add a comment to the ticket indicated in the url
func CreateComment(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to update a ticket"))
		return
	}

	var cm models.Comment

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&cm)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	vars := mux.Vars(r)
	key := vars["key"]
	err = Store.Tickets().NewComment(models.Ticket{Key: key}, &cm)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, cm)
}

// TransitionTicket will perform the given transition on the ticket indicated by {key}
func TransitionTicket(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to transition a ticket"))
		return
	}

	tk := &models.Ticket{
		Key: mux.Vars(r)["key"],
	}

	err := Store.Tickets().Get(tk)
	if err != nil {
		if err == store.ErrNotFound {
			w.WriteHeader(http.StatusNotFound)
			w.Write(utils.APIError("no ticket with that key"))
			return
		}

		w.WriteHeader(http.StatusInternalServerError)
		w.Write(utils.APIError(err.Error()))
		return
	}

	transition, valid := tk.Transition(r.FormValue("name"))
	if !valid {
		w.WriteHeader(http.StatusBadRequest)
		w.Write(utils.APIError("not a valid transition for ticket"))
		return
	}

	err = Store.Tickets().ExecuteTransition(tk, transition)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(err.Error()))
		return
	}

	utils.SendJSON(w, tk)
}
