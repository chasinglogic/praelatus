package middleware

import (
	"crypto/rand"
	"encoding/base64"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/securecookie"
	"github.com/praelatus/praelatus/models"
)

// Session stores a user with the expiration time of the session
type Session struct {
	Expires time.Time
	User    *models.User
}

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

// GetUserSession will check the given http.Request for a session token and if
// found it will return the corresponding user.
func GetUserSession(r *http.Request) *models.User {
	var encoded string

	cookie, err := r.Cookie("PRAESESSION")
	encoded = cookie.Value
	if err != nil {
		// if the cookie is not set check the header
		encoded = r.Header.Get("Authorization")
		return nil
	}

	if encoded == "" {
		// no session is set
		return nil
	}

	var id string
	if err := sec.Decode("PRAESESSION", encoded, &id); err != nil {
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

// SetUserSession will generate a secure cookie for user u, will set the cookie
// on the request r and will add the user session to the session store
func SetUserSession(u models.User, w http.ResponseWriter) error {
	id := generateSessionID()
	encoded, err := sec.Encode("PRAESESSION", id)
	if err != nil {
		return err
	}

	duration, _ := time.ParseDuration("3h")
	exp := time.Now().Add(duration)
	c := http.Cookie{
		Name:    "PRAESESSION",
		Value:   encoded,
		Expires: exp,
		Secure:  true,
	}

	http.SetCookie(w, &c)
	w.Header().Add("Token", encoded)
	return Cache.Set(id, u)
}

func generateSessionID() string {
	b := genSecKey(32)
	return base64.URLEncoding.EncodeToString(b)
}
