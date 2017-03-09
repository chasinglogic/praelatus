package middleware

import (
	"net/http"

	"github.com/praelatus/praelatus/store"
)

// Cache is the global session store used in our middleware.
var Cache store.SessionStore

// LoadMw will wrap the given http.Handler in the DefaultMiddleware
func LoadMw(handler http.Handler) http.Handler {
	h := handler

	for _, m := range DefaultMiddleware {
		h = m(h)
	}

	return h
}

// DefaultMiddleware is the default middleware stack for Praelatus
var DefaultMiddleware = []func(http.Handler) http.Handler{
	Logger,
}
