package middleware

import (
	"encoding/base64"
	"errors"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/securecookie"
	"github.com/praelatus/praelatus/models"
)

var hashKey = securecookie.GenerateRandomKey(64)
var blockKey = securecookie.GenerateRandomKey(32)
var sec = securecookie.New(hashKey, blockKey)

// TODO fix this
// func init() {
// 	bKey, _ := Cache.GetRaw("blockKey")
// 	hKey, _ := Cache.GetRaw("hashKey")

// 	if bKey != nil && hKey != nil {
// 		blockKey = bKey
// 		hashKey = hKey
// 		sec = securecookie.New(hashKey, blockKey)
// 	}

// 	ferr := Cache.SetRaw("hashKey", hashKey)
// 	serr := Cache.SetRaw("blockKey", blockKey)

// 	// We don't really care about the errors just want to be
// 	// notified if there's can issue
// 	if ferr != nil || serr != nil {
// 		log.Println(ferr)
// 		log.Println(serr)
// 	}
// }

func generateSessionID() string {
	b := securecookie.GenerateRandomKey(32)
	return base64.URLEncoding.EncodeToString(b)
}

func getSessionID(r *http.Request) string {
	var encoded string

	cookie, _ := r.Cookie("PRAESESSION")
	if cookie != nil {
		encoded = cookie.Value
	}

	if cookie == nil {
		// if the cookie is not set check the header
		encoded = r.Header.Get("Authorization")
	}

	if encoded == "" {
		return ""
	}

	var id string
	if err := sec.Decode("PRAESESSION", encoded, &id); err != nil {
		log.Println("Error decoding cookie:", err)
		return ""
	}

	return id
}

// GetUserSession will check the given http.Request for a session token and if
// found it will return the corresponding user.
func GetUserSession(r *http.Request) *models.User {
	id := getSessionID(r)
	if id == "" {
		return nil
	}

	sess, err := Cache.Get(id)
	if err != nil {
		log.Println("Error fetching session from store: ", err)
		return nil
	}

	if sess.Expires.Before(time.Now()) {
		// session has expired
		if err := Cache.Remove(id); err != nil {
			log.Println("Error removing from store:", err)
		}

		return nil
	}

	return &sess.User
}

// SetUserSession will generate a secure cookie for user u, will set the cookie
// on the request r and will add the user session to the session store
func SetUserSession(u models.User, w http.ResponseWriter) error {
	id := generateSessionID()
	encoded, err := sec.Encode("PRAESESSION", id)
	if err != nil {
		return err
	}

	exp := time.Now().Add(time.Hour * 3)
	c := http.Cookie{
		Name:    "PRAESESSION",
		Value:   encoded,
		Expires: exp,
		Secure:  true,
	}

	http.SetCookie(w, &c)
	w.Header().Add("Token", encoded)

	sess := models.Session{
		Expires: exp,
		User:    u,
	}

	return Cache.Set(id, sess)
}

// RefreshSession will reset the expiry on the session for the given request
func RefreshSession(r *http.Request) error {
	id := getSessionID(r)
	if id == "" {
		return errors.New("no session on this request")
	}

	sess, err := Cache.Get(id)
	if err != nil {
		return err
	}

	sess.Expires = time.Now().Add(time.Hour * 3)
	return Cache.Set(id, sess)
}
