package pg

import "database/sql"

// RoleStore contains methods for storing, and retrieving roles in a
// Postgres DB
type RoleStore struct {
	db *sql.DB
}
