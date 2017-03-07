package v1

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/praelatus/praelatus/api/utils"
	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/store"
	"github.com/pressly/chi"
)

func ticketRouter() chi.Router {
	router := chi.NewRouter()

	router.Get("/", GetAllTickets)
	router.Get("/:key", GetTicket)
	router.Delete("/:key", RemoveTicket)
	router.Put("/:key", UpdateTicket)

	router.Post("/:key", CreateTicket)

	router.Get("/:key/comments", GetComments)
	router.Post("/:key/comments", CreateComment)

	router.Put("/comments/:id", UpdateComment)
	router.Delete("/comments/:id", RemoveComment)

	return router
}

// GetTicket will get a ticket by the ticket key
func GetTicket(w http.ResponseWriter, r *http.Request) {
	key := chi.URLParam(r, "key")
	preload := r.FormValue("preload")

	tk := &models.Ticket{
		Key: key,
	}

	err := Store.Tickets().Get(tk)
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

	if preload == "comments" {
		cm, err := Store.Tickets().GetComments(*tk)
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
	tks, err := Store.Tickets().GetAll()
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError("failed to retrieve tickets from the database"))
		log.Println(err)
		return
	}

	utils.SendJSON(w, tks)
}

// GetAllTicketsByProject will get all the tickets for a given project
func GetAllTicketsByProject(w http.ResponseWriter, r *http.Request) {
	pkey := chi.URLParam(r, "key")

	tks, err := Store.Tickets().GetAllByProject(models.Project{Key: pkey})
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
	pkey := chi.URLParam(r, "key")

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

	err := Store.Tickets().Remove(models.Ticket{Key: key})
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
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

	err = Store.Tickets().Save(tk)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	w.Write([]byte{})
}

// GetComments will get the comments for the ticket indicated by the ticket key
// in the url
func GetComments(w http.ResponseWriter, r *http.Request) {
	key := chi.URLParam(r, "key")

	comments, err := Store.Tickets().GetComments(models.Ticket{Key: key})
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
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to update a ticket"))
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
		id, _ := strconv.Atoi(chi.URLParam(r, "id"))
		cm.ID = int64(id)
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

	id, _ := strconv.Atoi(chi.URLParam(r, "id"))

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

	key := chi.URLParam(r, "key")
	err = Store.Tickets().NewComment(models.Ticket{Key: key}, &cm)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, cm)
}
