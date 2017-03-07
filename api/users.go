package api

import (
	"encoding/json"
	"log"
	"net/http"
	"time"

	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/store"
	"github.com/pressly/chi"
)

func userRouter() chi.Router {
	router := chi.NewRouter()

	router.Get("/current_user", CurrentUser)

	router.Put("/:username", UpdateUser)
	router.Delete("/:username", DeleteUser)
	router.Get("/search", SearchUsers)
	router.Get("/:username", GetUser)
	router.Get("/", GetAllUsers)
	router.Post("/", CreateUser)

	router.Post("/sessions", CreateSession)
	router.Get("/sessions", RefreshSession)

	return router
}

// TokenResponse is used when logging in or signing up, it will return a
// generated token plus the user model for use by the client.
type TokenResponse struct {
	Token string      `json:"token"`
	User  models.User `json:"user"`
}

// GetUser will get a user from the database by the given username
func GetUser(w http.ResponseWriter, r *http.Request) {
	u := models.User{
		Username: chi.URLParam(r, "username"),
	}

	err := Store.Users().Get(&u)
	if err != nil {
		if err == store.ErrNotFound {
			w.WriteHeader(404)
			w.Write(apiError("No user exists with that username."))
			return
		}

		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	u.Password = ""

	sendJSON(w, u)
}

// GetAllUsers will return the json encoded array of all users in the given
// store
func GetAllUsers(w http.ResponseWriter, r *http.Request) {
	u := GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(apiError("you must be logged in to view other users"))
		return
	}

	users, err := Store.Users().GetAll()
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	for i := range users {
		users[i].Password = ""
		users[i].Settings = nil
	}

	sendJSON(w, users)
}

// SearchUsers will return the json encoded array of all users in the given
// store which match the provided query
func SearchUsers(w http.ResponseWriter, r *http.Request) {
	u := GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(apiError("you must be logged in to view other users"))
		return
	}

	query := r.FormValue("query")

	users, err := Store.Users().Search(query)
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	for i := range users {
		users[i].Password = ""
		users[i].Settings = nil
	}

	sendJSON(w, users)
}

// CreateUser will take the JSON given and attempt to
func CreateUser(w http.ResponseWriter, r *http.Request) {
	var u models.User

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&u)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	usr, err := models.NewUser(u.Username, u.Password, u.FullName, u.Email, false)
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	err = Store.Users().New(usr)
	if err != nil {
		if err == store.ErrDuplicateEntry {
			w.WriteHeader(400)
			w.Write(apiError(err.Error()))
			return
		}

		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	err = SetUserSession(*usr, r)
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	usr.Password = ""
	sendJSON(w, usr)
}

// UpdateUser will update a user in the database, it will reject the call if
// the user sending is not the user being updated or if the user sending is not
// a sys admin
func UpdateUser(w http.ResponseWriter, r *http.Request) {
	var u models.User

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&u)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	if u.Username == "" {
		u.Username = chi.URLParam(r, "username")
	}

	err = Store.Users().Save(u)
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	sendJSON(w, u)
}

// DeleteUser will remove a user from the database by setting is_inactive = 1
// can only be used by sys admins
func DeleteUser(w http.ResponseWriter, r *http.Request) {
	var u models.User

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&u)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	if u.Username == "" {
		u.Username = chi.URLParam(r, "username")
	}

	err = Store.Users().Remove(u)
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	w.Write([]byte(""))
}

// CreateSession will log in a user and create a jwt token for the current
// session
func CreateSession(w http.ResponseWriter, r *http.Request) {
	type loginRequest struct {
		Username string `json:"username"`
		Password string `json:"password"`
	}

	var l loginRequest

	decode := json.NewDecoder(r.Body)
	err := decode.Decode(&l)
	if err != nil {
		w.WriteHeader(400)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	u := models.User{Username: l.Username}

	err = Store.Users().Get(&u)
	if err != nil {
		if err == store.ErrNotFound {
			w.WriteHeader(404)
			w.Write(apiError("No user exists with that username."))
			return
		}

		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	if u.CheckPw([]byte(l.Password)) {
		u.Password = ""
		err := SetUserSession(u, r)
		if err != nil {
			w.WriteHeader(500)
			w.Write(apiError(err.Error()))
			log.Println(err)
			return

		}

		sendJSON(w, u)

		return
	}

	w.WriteHeader(401)
	w.Write(apiError("invalid password", "password"))
}

// RefreshSession will reset the expiration on the current session
func RefreshSession(w http.ResponseWriter, r *http.Request) {
	cookie, err := r.Cookie("PRAESESSION")
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError(err.Error()))
		log.Println(err)
		return
	}

	duration, _ := time.ParseDuration("3h")
	cookie.Expires = time.Now().Add(duration)
	r.AddCookie(cookie)

	w.Write([]byte{})
}

// CurrentUser will return the user object for the currently logged in user
func CurrentUser(w http.ResponseWriter, r *http.Request) {
	u := GetUserSession(r)
	if u != nil {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write(apiError("you are not logged in"))
		return
	}

	sendJSON(w, u)
}
