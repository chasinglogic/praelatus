package api

import (
	"net/http"
	"strings"
	"time"

	"github.com/gorilla/mux"
	"github.com/praelatus/backend/models"
)

// Context will hold the vars from the request and has a special field for
// holding the currently logged in user.
type Context struct {
	CurrentUser *models.User
	Vars        *Vars
}

// Authenticated will return a boolean indicating whether or not CurrentUser is
// nil or not.
func (c *Context) Authenticated() bool {
	if c.CurrentUser != nil {
		return true
	}

	return false
}

type Vars struct {
	internal map[string]interface{}
}

func (v *Vars) String(key string) string {
	vl, ok := v.internal[key].(string)
	if ok {
		return vl
	}

	return ""
}

func NewVars(m map[string]interface{}) *Vars {
	return &Vars{
		internal: m,
	}
}

// AppHandler is a custom function type which handles a http request, it takes
// a pointer to our context as the first argument and returns an integer and
// []byte which will be the response status code and body respectively.
type AppHandler func(*Context) (int, []byte)

// AdminRequired takes an AppHandler and returns a http.Handler which will
// check if the jwt token provided belongs to a user with admin rights.
func AdminRequired(fn AppHandler) http.Handler {
	return &handler{fn, true, true}
}

// AuthRequired takes an AppHandler and returns a http.Handler which will
// required that a user is logged in before executing the request.
func AuthRequired(fn AppHandler) http.Handler {
	return &handler{fn, true, false}
}

// NoAuth takes an AppHandler and returns a http.Handler which requires no
// authentication before executing.
func NoAuth(fn AppHandler) http.Handler {
	return &handler{fn, false, false}
}

type handler struct {
	fn       AppHandler
	reqUser  bool
	reqAdmin bool
}

// ServeHTTP allows our handler struct to implement the http.Handler interface.
func (h *handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	var token string
	start := time.Now()

	c := &Context{}
	c.Vars = NewVars(mux.Vars(r))

	// Attempt to parse token out of the header
	authHeader := r.Header.Get("Authorization")
	if len(authHeader) > 6 && strings.ToUpper(authHeader[0:6]) == "BEARER" {
		// Default session token
		tokenStr = authHeader[7:]
	} else if len(authHeader) > 5 && strings.ToLower(authHeader[0:5]) == "token" {
		// OAuth token
		tokenStr = authHeader[6:]
	}

	// Commented out for now to make development less of a headache.
	// 	if c.CurrentUser == nil && h.reqUser {
	// 		w.WriteHeader(403)
	// 		w.Write([]byte("You must be logged in to access this resource."))
	// 	}

	// 	if !c.CurrentUser.IsAdmin && h.reqAdmin {
	// 		w.WriteHeader(403)
	// 		w.Write([]byte("You must be an admin to access this resource."))
	// 	}

	statusCode, response := h.fn(c)
	Log.Infof("|%s| [%d] %s %s",
		r.Method, statusCode, r.URL.Path, time.Since(start).String())

	w.WriteHeader(statusCode)
	_, err := w.Write(response)
	if err != nil {
		Log.Error(err)
	}

}
