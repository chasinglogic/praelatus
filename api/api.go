// Package api has our routers and handler methods for all of the available api
// routes
package api

import (
	"net/http"

	"github.com/gorilla/mux"
	"github.com/praelatus/praelatus/config"
	"github.com/praelatus/praelatus/store"

	"github.com/praelatus/praelatus/api/middleware"
	"github.com/praelatus/praelatus/api/utils"
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

func routes(router *mux.Router) http.HandlerFunc {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		rs := []string{}

		router.Walk(func(route *mux.Route, router *mux.Router, ancestors []*mux.Route) error {
			t, err := route.GetPathTemplate()
			if err != nil {
				return err
			}

			rs = append(rs, t)
			return nil
		})

		utils.SendJSON(w, rs)
	})
}

// Routes will return the mux.Router which contains all of the api routes
func Routes() *mux.Router {
	context := config.ContextPath()

	router := mux.NewRouter()
	api := router.PathPrefix(context + "/api").Subrouter()
	v1r := router.PathPrefix(context + "/api/v1").Subrouter()

	// setup v1 routes
	v1.V1Routes(v1r)

	// setup latest routes
	v1.V1Routes(api)

	// setup routes endpoints
	v1r.HandleFunc("/routes", routes(v1r)).Methods("GET")
	api.HandleFunc("/routes", routes(api)).Methods("GET")

	router.Handle(context+"/", index())
	router.HandleFunc("/routes", routes(router)).Methods("GET")

	return router
}

// New will start running the api on the given port
func New(store store.Store, ss store.SessionStore) http.Handler {

	middleware.Cache = ss
	// setup v1 of api
	v1.Store = store

	router := Routes()

	return middleware.LoadMw(router)
}
