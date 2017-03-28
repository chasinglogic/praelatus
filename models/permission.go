package models

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

// PermissionScheme is used to map roles to permissions
type PermissionScheme struct {
	ID          int64               `json:"id"`
	Name        string              `json:"name"`
	Description string              `json:"description"`
	Permissions map[string][]string `json:"permissions"`
}
