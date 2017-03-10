package bolt

import (
	"testing"
	"time"

	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/store"
)

var s store.SessionStore

func init() {
	s = New("SessionTest.db")
}

func TestGetAndSet(t *testing.T) {
	user, _ := models.NewUser("testuser", "test", "Test Testerson", "test@example.com", false)
	sess := models.Session{
		Expires: time.Now().Add(time.Hour),
		User:    *user,
	}

	err := s.Set("test", sess)
	if err != nil {
		t.Error(err)
	}

	s, err := s.Get("test")
	if err != nil {
		t.Error(err)
	}

	if s.User != *user {
		t.Errorf("Expected %v, got %v", user, s.User)
	}
}
