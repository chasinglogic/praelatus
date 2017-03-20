package models

import (
	"time"
)

// PermissionLevel represents a permission level.
type PermissionLevel int

// Permission Levels
const (
	Admin       PermissionLevel = 1
	Contributor                 = 2
	Viewer                      = 3
)

func (pl PermissionLevel) String() string {
	switch pl {
	case 1:
		return "ADMIN"
	case 2:
		return "CONTRIBUTOR"
	case 3:
		return "VIEWER"
	default:
		return "ANONYMOUS"
	}
}

// MarshalJSON implements json.Marshaler for our PermissionLevel this
// allows us to store "machine readable" permission levels but give
// "human readable" permission levels to the clients.
func (pl PermissionLevel) MarshalJSON() ([]byte, error) {
	return []byte("\"" + pl.String() + "\""), nil
}

// Permission is used to control user / team access to projects.
type Permission struct {
	ID          int64           `json:"id"`
	CreatedDate time.Time       `json:"created_date"`
	UpdatedDate time.Time       `json:"updated_date"`
	Level       PermissionLevel `json:"level"`
	User        User            `json:"user,omitempty"`
	Team        Team            `json:"team,omitempty"`
}

func (p *Permission) String() string {
	return jsonString(p)
}
