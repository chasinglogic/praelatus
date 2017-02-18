package api

import (
	"crypto/rand"
	"encoding/base64"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/securecookie"
	"github.com/praelatus/praelatus/models"
)

var hashKey = genSecKey(64)
var blockKey = genSecKey(32)
var sec = securecookie.New(hashKey, blockKey)

func genSecKey(leng int) []byte {
	b := make([]byte, leng)
	_, err := rand.Read(b)

	// if we can't generate secure strings fail out
	if err != nil {
		panic(err)
	}

	return b
}

// DefaultMiddleware is the default middleware stack for Praelatus
var DefaultMiddleware = []func(http.Handler) http.Handler{
	Logger,
}

// GetUser will check the given http.Request for a session token and if found
// it will return the corresponding user.
func GetUserSession(r *http.Request) *models.User {
	cookie, err := r.Cookie("PRAESESSION")
	if err != nil {
		log.Println("Error getting cookie:", err)
		return nil
	}

	var id string
	if err := sec.Decode("PRAESESSION", cookie.Value, &id); err != nil {
		log.Println("Error decoding cookie:", err)
		return nil
	}

	user, err := Cache.Get(id)

	if err != nil {
		log.Println("Error fetching session from store: ", err)
		return nil
	}

	return &user
}

func SetUserSession(u models.User, r *http.Request) error {
	id := generateSessionID()
	encoded, err := sec.Encode("PRAESESSION", id)
	if err != nil {
		return err
	}

	duration, _ := time.ParseDuration("3h")
	c := http.Cookie{
		Name:    "PRAESESSION",
		Value:   encoded,
		Expires: time.Now().Add(duration),
		Secure:  true,
	}

	r.AddCookie(&c)
	return Cache.Set(id, u)
}

func generateSessionID() string {
	b := genSecKey(32)
	return base64.URLEncoding.EncodeToString(b)
}

// LoggedResponseWriter wraps http.ResponseWriter so we can capture the status
// code for logging
type LoggedResponseWriter struct {
	status int
	http.ResponseWriter
}

// Status will return the status code used in this request.
func (w *LoggedResponseWriter) Status() int {
	return w.status
}

// WriteHeader implements http.ResponseWriter adding our custom functionality
// to it
func (w *LoggedResponseWriter) WriteHeader(code int) {
	w.status = code
	w.ResponseWriter.WriteHeader(code)
}

func (w *LoggedResponseWriter) Write(b []byte) (int, error) {
	if w.status == 0 {
		w.WriteHeader(200)
	}

	return w.ResponseWriter.Write(b)
}

// Logger will log a request and any information about the request, it should
// be the first middleware in any chain.
func Logger(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		lrw := &LoggedResponseWriter{0, w}

		lrw.Header().Add("Access-Control-Allow-Origin", "*")

		next.ServeHTTP(lrw, r)

		log.Printf("|%s| [%d] %s %s",
			r.Method, lrw.Status(), r.URL.Path, time.Since(start).String())
	})
}
