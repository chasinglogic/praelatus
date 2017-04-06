package v1

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
	"github.com/praelatus/praelatus/api/middleware"
	"github.com/praelatus/praelatus/api/utils"
	"github.com/praelatus/praelatus/models"
)

func roleRouter(router *mux.Router) {
	router.HandleFunc("/roles", GetAllRoles).Methods("GET")
	router.HandleFunc("/roles", CreateRole).Methods("POST")

	router.HandleFunc("/roles/{id}", GetRole).Methods("GET")
	router.HandleFunc("/roles/{id}", DeleteRole).Methods("DELETE")
	router.HandleFunc("/roles/{id}", UpdateRole).Methods("PUT")
}

// GetAllRoles will return a JSON array of all roles from the store.
func GetAllRoles(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		utils.APIErr(w, http.StatusUnauthorized,
			"you must be logged in")
		return
	}

	roles, err := Store.Roles().GetAll()
	if err != nil {
		utils.APIErr(w, utils.GetErrorCode(err), err.Error())
		return
	}

	utils.SendJSON(w, roles)
}

// GetRole will return a JSON representation of a role
func GetRole(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		utils.APIErr(w, http.StatusUnauthorized,
			"you must be logged in")
		return
	}

	vars := mux.Vars(r)
	id := vars["id"]

	role := models.Role{}

	i, _ := strconv.Atoi(id)
	role.ID = int64(i)
	role.Name = id

	err := Store.Roles().Get(&role)
	if err != nil {
		utils.APIErr(w, utils.GetErrorCode(err), err.Error())
		return
	}

	utils.SendJSON(w, role)
}

// CreateRole creates a role in the db and return a JSON object of
func CreateRole(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		utils.APIErr(w, http.StatusForbidden,
			"you must be logged in as an administrator")
		return
	}

	var role models.Role

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&role)
	if err != nil {
		utils.APIErr(w, http.StatusBadRequest, "malformed json")
		return
	}

	err = Store.Roles().Create(*u, &role)
	if err != nil {
		utils.APIErr(w, utils.GetErrorCode(err), err.Error())
		return
	}

	utils.SendJSON(w, role)
}

// UpdateRole updates the role in the db and returns a message indicating
// success or failure.
func UpdateRole(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		utils.APIErr(w, http.StatusForbidden,
			"you must be logged in as an administrator")
		return
	}

	var role models.Role

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&role)
	if err != nil {
		utils.APIErr(w, http.StatusBadRequest, "malformed json")
		return
	}

	err = Store.Roles().Save(*u, role)
	if err != nil {
		utils.APIErr(w, utils.GetErrorCode(err), err.Error())
		return
	}

	utils.SendJSON(w, role)
}

// DeleteRole deletes roles from the db and returns a response indicating
// success of failure.
func DeleteRole(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		utils.APIErr(w, http.StatusForbidden,
			"you must be logged in as an administrator")
		return
	}

	vars := mux.Vars(r)
	id := vars["id"]

	i, err := strconv.Atoi(id)
	if err != nil {
		utils.APIErr(w, http.StatusBadRequest, "not a valid id")
		return
	}

	err = Store.Roles().Remove(*u, models.Role{ID: int64(i)})
	if err != nil {
		utils.APIErr(w, utils.GetErrorCode(err), err.Error())
		return
	}

	w.Write(utils.APIMsg("Role successfully deleted"))
}
