package v1

import (
	"net/http"

	"github.com/praelatus/praelatus/api/middleware"
	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/store"
)

func init() {
	Store, Cache = store.Mock()
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
		&settings,
	}

	err := middleware.middleware.SetUserSession(u, r)
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
		&settings,
	}

	err := middleware.middleware.SetUserSession(u, r)
	if err != nil {
		panic(err)
	}
}
