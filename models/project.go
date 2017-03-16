package models

import "time"

// PermissionLevel represents a permission level.
type PermissionLevel string

// Permission Levels
const (
	Admin       PermissionLevel = "ADMIN"
	Contributor                 = "CORE"
	Viewer                      = "USER"
)

// Project is the model used to represent a project in the database.
type Project struct {
	ID          int64     `json:"id"`
	CreatedDate time.Time `json:"created_date"`
	Name        string    `json:"name"`
	Key         string    `json:"key"`
	Lead        User      `json:"lead"`
	Homepage    string    `json:"homepage,omitempty"`
	IconURL     string    `json:"icon_url,omitempty"`
	Repo        string    `json:"repo,omitempty"`
}

func (p *Project) String() string {
	return jsonString(p)
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
