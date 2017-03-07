package v1_test

import (
	"net/http"

	"github.com/gorilla/mux"
	"github.com/praelatus/praelatus/api"
	"github.com/praelatus/praelatus/api/middleware"
	"github.com/praelatus/praelatus/api/v1"
	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/store"
)

var router *mux.Router

func init() {
	v1.Store, middleware.Cache = store.Mock()
	router = api.Routes()
}

func testLogin(r *http.Request) {
	u := models.User{
		1,
		"foouser",
		"foopass",
		"foo@foo.com",
		"Foo McFooserson",
		"",
		false,
		true,
		&models.Settings{},
	}

	err := middleware.SetUserSession(u, r)
	if err != nil {
		panic(err)
	}
}

func testAdminLogin(r *http.Request) {
	u := models.User{
		1,
		"foouser",
		"foopass",
		"foo@foo.com",
		"Foo McFooserson",
		"",
		true,
		true,
		&models.Settings{},
	}

	err := middleware.SetUserSession(u, r)
	if err != nil {
		panic(err)
	}
}
