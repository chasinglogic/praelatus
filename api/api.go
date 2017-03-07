// Package api has our routers and handler methods for all of the available api
// routes
package api

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
	"github.com/praelatus/praelatus/config"
	"github.com/praelatus/praelatus/store"
	"github.com/pressly/chi"
	"github.com/pressly/chi/docgen"
)

// Store is the global store used in our HTTP handlers.
var Store store.Store

// Cache is the global session store used in our HTTP handlers.
var Cache store.SessionStore

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

func routes(rtr chi.Router) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		jsnStr := docgen.JSONRoutesDoc(rtr)
		w.Write([]byte(jsnStr))
	})
}

// New will start running the api on the given port
func New(store store.Store, ss store.SessionStore) http.Handler {
	Store = store

	Cache = ss

	context := config.ContextPath()

	router := mux.NewRouter()
	api := router.PathPrefix(context + "/api").Subrouter()
	v1r := router.PathPrefix(context + "/v1/api").Subrouter()

	v1.V1Routes(api)
	v1.V1Routes(v1r)

	api.Handle("/fields", fieldRouter())
	api.Handle("/projects", projectRouter())
	api.Handle("/teams", teamRouter())
	api.Handle("/tickets", ticketRouter())
	api.Handle("/types", typeRouter())
	api.Handle("/users", userRouter())
	api.Handle("/workflows", workflowRouter())

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

// Message is a general purpose json struct used primarily for error responses.
type Message struct {
	Field   string `json:"field,omitempty"`
	Message string `json:"message"`
}

func apiError(msg string, fields ...string) []byte {
	e := Message{
		Message: msg,
	}

	if fields != nil {
		e.Field = strings.Join(fields, ",")
	}

	byt, _ := json.Marshal(e)
	return byt
}

func sendJSON(w http.ResponseWriter, v interface{}) {
	resp, err := json.Marshal(v)
	if err != nil {
		w.WriteHeader(500)
		w.Write(apiError("Failed to marshal database response to JSON."))
		log.Println(err)
		return
	}

	w.Write(resp)
}
