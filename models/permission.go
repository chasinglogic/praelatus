package models

import "github.com/praelatus/praelatus/models/permission"

// Role represents a role on a project, the defaults are
// Administrator, Contributor, User, and Anonymous these are user
// configurable. If members is present this means you are looking at
// that role for a given project.
type Role struct {
	ID      int64    `json:"id"`
	Name    string   `json:"name"`
	Project *Project `json:"project,omitempty"`
	Members []User   `json:"members,omitempty"`
}

func (r Role) String() string {
	return jsonString(r)
}

// PermissionScheme is used to map roles to permissions
type PermissionScheme struct {
	ID          int64                              `json:"id"`
	Name        string                             `json:"name"`
	Description string                             `json:"description"`
	Permissions map[string][]permission.Permission `json:"permissions"`
}

func (p PermissionScheme) String() string {
	return jsonString(p)
}

// Permission is a permission in the DB
type Permission struct {
	ID   int64                 `json:"id"`
	Name permission.Permission `json:"name"`
}
