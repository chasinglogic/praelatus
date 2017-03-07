package v1

import (
	"encoding/json"
	"log"
	"net/http"
	"time"

	"github.com/praelatus/praelatus/api/utils"
	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/store"

	"github.com/gorilla/mux"
)

func userRouter() http.Handler {
	router := mux.NewRouter()

	router.HandleFunc("/", GetAllUsers).Methods("GET")
	router.HandleFunc("/", CreateUser).Methods("POST")

	router.HandleFunc("/current_user", CurrentUser).Methods("GET")

	router.HandleFunc("/sessions", CreateSession).Methods("POST")
	router.HandleFunc("/sessions", RefreshSession).Methods("GET")

	router.HandleFunc("/search", SearchUsers).Methods("GET")

	router.HandleFunc("/{username}", UpdateUser).Methods("PUT")
	router.HandleFunc("/{username}", DeleteUser).Methods("DELETE")
	router.HandleFunc("/{username}", GetUser).Methods("GET")

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
	vars := mux.Vars(r)

	u := models.User{
		Username: vars["username"],
	}

	err := Store.Users().Get(&u)
	if err != nil {
		if err == store.ErrNotFound {
			w.WriteHeader(404)
			w.Write(utils.APIError("No user exists with that username."))
			return
		}

		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	u.Password = ""

	utils.SendJSON(w, u)
}

// GetAllUsers will return the json encoded array of all users in the given
// store
func GetAllUsers(w http.ResponseWriter, r *http.Request) {
	u := GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to view other users"))
		return
	}

	users, err := Store.Users().GetAll()
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	for i := range users {
		users[i].Password = ""
		users[i].Settings = nil
	}

	utils.SendJSON(w, users)
}

// SearchUsers will return the json encoded array of all users in the given
// store which match the provided query
func SearchUsers(w http.ResponseWriter, r *http.Request) {
	u := GetUserSession(r)
	if u == nil {
		w.WriteHeader(403)
		w.Write(utils.APIError("you must be logged in to view other users"))
		return
	}

	query := r.FormValue("query")

	users, err := Store.Users().Search(query)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	for i := range users {
		users[i].Password = ""
		users[i].Settings = nil
	}

	utils.SendJSON(w, users)
}

// CreateUser will take the JSON given and attempt to
func CreateUser(w http.ResponseWriter, r *http.Request) {
	var u models.User

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&u)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	usr, err := models.NewUser(u.Username, u.Password, u.FullName, u.Email, false)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	err = Store.Users().New(usr)
	if err != nil {
		if err == store.ErrDuplicateEntry {
			w.WriteHeader(400)
			w.Write(utils.APIError(err.Error()))
			return
		}

		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	err = SetUserSession(*usr, r)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	usr.Password = ""
	utils.SendJSON(w, usr)
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
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	if u.Username == "" {
		vars := mux.Vars(r)
		u.Username = vars["username"]
	}

	err = Store.Users().Save(u)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	utils.SendJSON(w, u)
}

// DeleteUser will remove a user from the database by setting is_inactive = 1
// can only be used by sys admins
func DeleteUser(w http.ResponseWriter, r *http.Request) {
	var u models.User

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&u)
	if err != nil {
		w.WriteHeader(400)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	if u.Username == "" {
		vars := mux.Vars(r)
		u.Username = vars["username"]
	}

	err = Store.Users().Remove(u)
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
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
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	u := models.User{Username: l.Username}

	err = Store.Users().Get(&u)
	if err != nil {
		if err == store.ErrNotFound {
			w.WriteHeader(404)
			w.Write(utils.APIError("No user exists with that username."))
			return
		}

		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
		log.Println(err)
		return
	}

	if u.CheckPw([]byte(l.Password)) {
		err := SetUserSession(u, r)
		if err != nil {
			w.WriteHeader(500)
			w.Write(utils.APIError(err.Error()))
			log.Println(err)
			return

		}

		u.Password = ""
		utils.SendJSON(w, u)

		return
	}

	w.WriteHeader(401)
	w.Write(utils.APIError("invalid password", "password"))
}

// RefreshSession will reset the expiration on the current session
func RefreshSession(w http.ResponseWriter, r *http.Request) {
	cookie, err := r.Cookie("PRAESESSION")
	if err != nil {
		w.WriteHeader(500)
		w.Write(utils.APIError(err.Error()))
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
		w.Write(utils.APIError("you are not logged in"))
		return
	}

	utils.SendJSON(w, u)
}
