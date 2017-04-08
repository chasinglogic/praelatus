// Package v1 contains all of the routes and handlers for v1 of the
// API
package v1

import (
	"github.com/gorilla/mux"
	"github.com/praelatus/praelatus/store"
)

// Store is the global store used in our HTTP handlers.
var Store store.Store

// Routes will set up the appropriate routes on the given mux.Router
func Routes(router *mux.Router) {
	labelRouter(router)
	fieldRouter(router)
	projectRouter(router)
	teamRouter(router)
	ticketRouter(router)
	typeRouter(router)
	userRouter(router)
	workflowRouter(router)
	roleRouter(router)
	permissionSchemeRouter(router)
}
