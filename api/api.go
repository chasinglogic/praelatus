// Package api has our routers and handler methods for all of the available api
// routes
package api

import (
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/praelatus/praelatus/config"
	"github.com/praelatus/praelatus/store"

	"github.com/praelatus/praelatus/api/v1"
)

func index() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/",
		func(w http.ResponseWriter, r *http.Request) {
			http.ServeFile(w, r, "client/index.html")
		})

	mux.Handle("/static/",
		http.StripPrefix("/client/", http.FileServer(http.Dir("client/static"))))

	return mux
}

func routes(router *mux.Router) http.HandleFunc {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		rs := []string{}

		SendJSON(w, rs)
	})
}

// New will start running the api on the given port
func New(store store.Store, ss store.SessionStore) *mux.Router {
	context := config.ContextPath()

	middleware.Cache = ss

	router := mux.NewRouter()
	api := router.PathPrefix(context + "/api").Subrouter()
	v1r := router.PathPrefix(context + "/v1/api").Subrouter()

	// setup v1 of api
	v1.Store = store
	v1.V1Routes(api)
	v1.V1Routes(v1r)

	router.Handle(context+"/", index())

	api.Walk(func(route *mux.Route, router *mux.Router, ancestors []*mux.Route) error {
		t, err := route.GetPathTemplate()
		if err != nil {
			return err
		}
		fmt.Println(t)
		return nil
	})

	router.Walk(func(route *mux.Route, router *mux.Router, ancestors []*mux.Route) error {
		t, err := route.GetPathTemplate()
		if err != nil {
			return err
		}
		fmt.Println(t)
		return nil
	})

	return loadMw(router, DefaultMiddleware...)
}
