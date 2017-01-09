package api

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/praelatus/backend/models"
	"github.com/praelatus/backend/mw"
	"github.com/pressly/chi"
)

func teamRouter() chi.Router {
	router := chi.NewRouter()

	router.Get("/", GetAllTeams)
	router.Post("/", CreateTeam)

	router.Get("/:id", GetTeam)
	router.Put("/:id", UpdateTeam)
	router.Delete("/:id", RemoveTeam)

	return router
}

// GetAllTeams will retrieve all teams from the DB and send a JSON response
func GetAllTeams(w http.ResponseWriter, r *http.Request) {
	u := mw.GetUser(r.Context())
	if u == nil {
		w.WriteHeader(403)
		w.Write(apiError("you must be logged in to view all teams"))
		return
	}

	teams, err := Store.Teams().GetAll()
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, teams)
}

// CreateTeam will create a team in the database based on the JSON sent by the
// client
func CreateTeam(w http.ResponseWriter, r *http.Request) {
	var t models.Team

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

	err = Store.Teams().New(&t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, t)
}

// GetTeam will return the json representation of a team in the database
func GetTeam(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "id")

	i, err := strconv.Atoi(id)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError("invalid id"))
		log.Println(err)
		return
	}

	t := models.Team{ID: int64(i)}

	err = Store.Teams().Get(&t)
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, t)
}

// UpdateTeam will update a project based on the JSON representation sent to
// the API
func UpdateTeam(w http.ResponseWriter, r *http.Request) {
	var t models.Team

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

	err = Store.Teams().New(&t)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, t)
}

// RemoveTeam will remove the project indicated by the id passed in as a
// url parameter
func RemoveTeam(w http.ResponseWriter, r *http.Request) {
	id := r.Context().Value("id").(string)

	u := mw.GetUser(r.Context())
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

	err = Store.Teams().Remove(models.Team{ID: int64(i)})
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	w.Write([]byte{})
}
