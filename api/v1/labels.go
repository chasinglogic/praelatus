package v1

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
	"github.com/praelatus/praelatus/api/utils"
	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/store"
)

func labelRouter(router *mux.Router) {
	router.HandleFunc("", GetAllLabels).Methods("GET")
	router.HandleFunc("", CreateLabel).Methods("POST")

	router.HandleFunc("/search", SearchLabels).Methods("GET")
	router.HandleFunc("/{id}", GetLabel).Methods("GET")
	router.HandleFunc("/{id}", DeleteLabel).Methods("DELETE")
	router.HandleFunc("/{id}", UpdateLabel).Methods("PUT")
}

// GetAllLabels will return a JSON array of all labels from the store.
func GetAllLabels(w http.ResponseWriter, r *http.Request) {
	labels, err := Store.Labels().GetAll()
	if err != nil {
		w.WriteHeader(500)
		w.Write([]byte(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, labels)
}

// GetLabel will return a JSON representation of a label
func GetLabel(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	lbl := &models.Label{}

	i, err := strconv.Atoi(id)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("invalid id"))
		log.Println(err)
		return
	}

	lbl.ID = int64(i)

	err = Store.Labels().Get(lbl)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		return
	}

	utils.SendJSON(w, lbl)
}

// CreateLabel creates a label in the db and return a JSON object of
func CreateLabel(w http.ResponseWriter, r *http.Request) {
	var lbl models.Label

	u := middleware.GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to create a label"))
		return
	}

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&lbl)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("malformed json"))
		log.Println(err)
		return
	}

	err = Store.Labels().New(&lbl)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, lbl)
}

// UpdateLabel updates the label in the db and returns a message indicating
// success or failure.
func UpdateLabel(w http.ResponseWriter, r *http.Request) {
	var lbl models.Label

	u := middleware.GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to create a label"))
		return
	}

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&lbl)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("malformed json"))
		log.Println(err)
		return
	}

	if lbl.ID == 0 {
		vars := mux.Vars(r)
		id := vars["id"]
		i, err := strconv.Atoi(id)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write(utils.APIError(http.StatusText(http.StatusBadRequest)))
			return
		}

		lbl.ID = int64(i)
	}

	err = Store.Labels().Save(lbl)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, lbl)
}

// DeleteLabel deletes labels from the db and returns a response indicating
// success of failure.
func DeleteLabel(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	i, err := strconv.Atoi(id)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError("invalid id"))
		log.Println(err)
		return
	}

	err = Store.Labels().Remove(models.Label{ID: int64(i)})
	if err != nil {
		w.WriteHeader(500)
		w.Write([]byte(err.Error()))
		return
	}

	w.Write([]byte("Label successfully deleted"))
}

// SearchLabels will take a url param of query and try to find a label
// with the given name
func SearchLabels(w http.ResponseWriter, r *http.Request) {
	query := r.FormValue("query")

	labels, err := Store.Labels().Search(query)
	if err != nil {
		if err == store.ErrNotFound {
			w.WriteHeader(http.StatusNotFound)
			w.Write(utils.APIError("No labels match that query"))
			return
		}

		w.WriteHeader(http.StatusInternalServerError)
		w.Write(utils.APIError(err.Error()))
		return
	}

	utils.SendJSON(w, labels)
}
