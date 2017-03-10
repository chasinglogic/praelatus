package models

import (
	"crypto/md5"
	"encoding/hex"
	"strings"

	"log"

	"golang.org/x/crypto/bcrypt"
)

// User represents a user of our application
type User struct {
	ID         int64     `json:"id"`
	Username   string    `json:"username"`
	Password   string    `json:"password,omitempty"`
	Email      string    `json:"email"`
	FullName   string    `json:"full_name"`
	ProfilePic string    `json:"profile_picture"`
	IsAdmin    bool      `json:"is_admin,omitempty"`
	IsActive   bool      `json:"is_active,omitempty"`
	Settings   *Settings `json:"settings,omitempty"`
}

// CheckPw will verify if the given password matches for this user. Logs any
// errors it encounters
func (u *User) CheckPw(pw []byte) bool {
	err := bcrypt.CompareHashAndPassword([]byte(u.Password), pw)
	if err == nil {
		return true
	}

	log.Println("Error checking password:", err)
	return false
}

func (u *User) String() string {
	return jsonString(u)
}

// NewUser will create the user after encrypting the password with bcrypt
func NewUser(username, password, fullName, email string, admin bool) (*User, error) {
	pw, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return &User{}, err
	}

	emailHash := md5.Sum([]byte(strings.ToLower(email)))
	eh := hex.EncodeToString(emailHash[:16])

	return &User{
		Username:   username,
		Password:   string(pw),
		Email:      email,
		FullName:   fullName,
		ProfilePic: "https://www.gravatar.com/avatar/" + eh,
		IsAdmin:    admin,
	}, nil
}

// Settings represents an individual users preferences
type Settings struct {
	DefaultProject string `json:"default_project,omitempty"`
	DefaultView    string `json:"default_view,omitempty"`
}
