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

func permissionSchemeRouter(router *mux.Router) {
	router.HandleFunc("/permissionschemes", GetAllPermissionSchemes).Methods("GET")
	router.HandleFunc("/permissionschemes", CreatePermissionScheme).Methods("POST")

	router.HandleFunc("/permissionschemes/{id}", GetPermissionScheme).Methods("GET")
	router.HandleFunc("/permissionschemes/{id}", DeletePermissionScheme).Methods("DELETE")
	router.HandleFunc("/permissionschemes/{id}", UpdatePermissionScheme).Methods("PUT")
}

// GetAllPermissionSchemes will return a JSON array of all permissionSchemes from the store.
func GetAllPermissionSchemes(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		utils.APIErr(w, http.StatusForbidden,
			"you must be logged in as an administrator")
		return
	}

	permissionSchemes, err := Store.Permissions().GetAll(*u)
	if err != nil {
		utils.APIErr(w, utils.GetErrorCode(err), err.Error())
		return
	}

	utils.SendJSON(w, permissionSchemes)
}

// GetPermissionScheme will return a JSON representation of a permissionScheme
func GetPermissionScheme(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		utils.APIErr(w, http.StatusForbidden,
			"you must be logged in as an administrator")
		return
	}

	vars := mux.Vars(r)
	id := vars["id"]

	scheme := models.PermissionScheme{}

	i, _ := strconv.Atoi(id)
	scheme.ID = int64(i)
	scheme.Name = id

	err := Store.Permissions().Get(*u, &scheme)
	if err != nil {
		utils.APIErr(w, utils.GetErrorCode(err), err.Error())
		return
	}

	utils.SendJSON(w, scheme)
}

// CreatePermissionScheme creates a permissionScheme in the db and return a JSON object of
func CreatePermissionScheme(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		utils.APIErr(w, http.StatusForbidden,
			"you must be logged in as an administrator")
		return
	}

	var scheme models.PermissionScheme

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&scheme)
	if err != nil {
		utils.APIErr(w, http.StatusBadRequest, "malformed json")
		return
	}

	err = Store.Permissions().Create(*u, &scheme)
	if err != nil {
		utils.APIErr(w, utils.GetErrorCode(err), err.Error())
		return
	}

	utils.SendJSON(w, scheme)
}

// UpdatePermissionScheme updates the permissionScheme in the db and returns a message indicating
// success or failure.
func UpdatePermissionScheme(w http.ResponseWriter, r *http.Request) {
	u := middleware.GetUserSession(r)
	if u == nil {
		utils.APIErr(w, http.StatusForbidden,
			"you must be logged in as an administrator")
		return
	}

	var scheme models.PermissionScheme

	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&scheme)
	if err != nil {
		utils.APIErr(w, http.StatusBadRequest, "malformed json")
		return
	}

	err = Store.Permissions().Save(*u, scheme)
	if err != nil {
		utils.APIErr(w, utils.GetErrorCode(err), err.Error())
		return
	}

	utils.SendJSON(w, scheme)
}

// DeletePermissionScheme deletes permissionSchemes from the db and returns a response indicating
// success of failure.
func DeletePermissionScheme(w http.ResponseWriter, r *http.Request) {
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

	err = Store.Permissions().Remove(*u, models.PermissionScheme{ID: int64(i)})
	if err != nil {
		utils.APIErr(w, utils.GetErrorCode(err), err.Error())
		return
	}

	w.Write(utils.APIMsg("PermissionScheme successfully deleted"))
}
