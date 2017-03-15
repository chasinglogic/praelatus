// Package bolt implements a store.SessionStore using a BoltDB as
// the backend
package bolt

import (
	"encoding/json"
	"log"

	"github.com/boltdb/bolt"
	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/store"
)

// SessionStore implements store.SessionStore for a boltdb based cache
type SessionStore struct {
	db *bolt.DB
}

// Remove will remove the given key from the bolt session store
func (c *SessionStore) Remove(key string) error {
	return c.db.Update(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte("sessions"))
		return b.Delete([]byte(key))
	})
}

// Get will get the sesion information for the given session key
func (c *SessionStore) Get(key string) (models.Session, error) {
	var u models.Session
	var jsn []byte

	c.db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte("sessions"))
		jsn = b.Get([]byte(key))
		return nil
	})

	if jsn == nil {
		return u, store.ErrNoSession
	}

	err := json.Unmarshal(jsn, &u)
	return u, err
}

// Set will set the session information for the given session key
func (c *SessionStore) Set(key string, model models.Session) error {
	jsn, err := json.Marshal(model)
	if err != nil {
		return err
	}

	return c.db.Update(func(tx *bolt.Tx) error {
		bucket, err := tx.CreateBucketIfNotExists([]byte("sessions"))
		if err != nil {
			return err
		}

		return bucket.Put([]byte(key), jsn)
	})
}

// New will open boltdb at filename for storing session info in
func New(filename string) store.SessionStore {
	ss := &SessionStore{}
	db, err := bolt.Open(filename, 0600, nil)
	if err != nil {
		log.Panicln("Error starting session db:", err.Error())
	}

	ss.db = db
	return ss
}
