package models

import "time"

// Session stores a user with the expiration time of the session
type Session struct {
	Expires time.Time
	User    User
}
