// Package pg implements all of the appropriate interfaces to be used
// as a store.Store, store.SQLStore, store.Migrater, and
// store.Droppable for a Postgres database
package pg

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	"github.com/lib/pq"
	"github.com/praelatus/praelatus/models/permission"
	"github.com/praelatus/praelatus/store"
	"github.com/praelatus/praelatus/store/pg/migrations"
)

// rowScanner is used internally so we can take a sql.Row or sql.Rows in some
// of the utility functions
type rowScanner interface {
	Scan(dest ...interface{}) error
}

// Store implements the store.Store and store.SQLStore interface for a postgres DB.
type Store struct {
	db          *sql.DB
	replicas    []sql.DB
	users       *UserStore
	projects    *ProjectStore
	fields      *FieldStore
	workflows   *WorkflowStore
	tickets     *TicketStore
	types       *TypeStore
	labels      *LabelStore
	statuses    *StatusStore
	teams       *TeamStore
	permissions *PermissionStore
	roles       *RoleStore
}

// New connects to the postgres database provided and returns a store
// that's connected. It will stop execution of the program if unable to connect
// to the database.
func New(conn string, replicas ...string) *Store {
	d, err := sql.Open("postgres", conn)
	if err != nil {
		fmt.Println("Invalid database url:", err)
		os.Exit(1)
	}

	err = d.Ping()
	if err != nil {
		fmt.Println("Error connecting to postgres:", err)
		os.Exit(1)
	}

	s := &Store{
		db:          d,
		replicas:    []sql.DB{},
		users:       &UserStore{d},
		projects:    &ProjectStore{d},
		fields:      &FieldStore{d},
		tickets:     &TicketStore{d},
		labels:      &LabelStore{d},
		workflows:   &WorkflowStore{d},
		types:       &TypeStore{d},
		statuses:    &StatusStore{d},
		teams:       &TeamStore{d},
		permissions: &PermissionStore{d},
		roles:       &RoleStore{d},
	}

	return s
}

// Users returns the underlying UserStore for a postgres DB
func (pg *Store) Users() store.UserStore {
	return pg.users
}

// Teams returns the underlying TeamStore for a postgres DB
func (pg *Store) Teams() store.TeamStore {
	return pg.teams
}

// Fields returns the underlying FieldStore for a postgres DB
func (pg *Store) Fields() store.FieldStore {
	return pg.fields
}

// Tickets returns the underlying TicketStore for a postgres DB
func (pg *Store) Tickets() store.TicketStore {
	return pg.tickets
}

// Types returns the underlying TypeStore for a postgres DB
func (pg *Store) Types() store.TypeStore {
	return pg.types
}

// Projects returns the underlying ProjectStore for a postgres DB
func (pg *Store) Projects() store.ProjectStore {
	return pg.projects
}

// Statuses returns the underlying StatusStore for a postgres DB
func (pg *Store) Statuses() store.StatusStore {
	return pg.statuses
}

// Workflows returns the underlying WorkflowStore for a postgres DB
func (pg *Store) Workflows() store.WorkflowStore {
	return pg.workflows
}

// Labels returns the underlying LabelStore for a postgres DB
func (pg *Store) Labels() store.LabelStore {
	return pg.labels
}

// Permissions returns the underlying PermissionStore for a postgres DB
func (pg *Store) Permissions() store.PermissionStore {
	return pg.permissions
}

// Roles returns the underlying RoleStore for a postgres DB
func (pg *Store) Roles() store.RoleStore {
	return pg.roles
}

// Conn implements store.SQLStore for postgres db
func (pg *Store) Conn() *sql.DB {
	return pg.db
}

// Drop implements store.SQLStore for postgres db
func (pg *Store) Drop() error {
	_, err := pg.db.Exec("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
	return err
}

// Migrate implements store.SQLStore for postgres db
func (pg *Store) Migrate() error {
	return migrations.RunMigrations(pg.db)
}

// checkIfAdmin will return true if the given userID references a user
// who is a system admin
func checkIfAdmin(db *sql.DB, userID int64) bool {
	var isAdmin bool

	row := db.QueryRow(`SELECT is_admin FROM users WHERE id = $1`,
		userID)

	err := row.Scan(&isAdmin)
	if err != nil {
		handlePqErr(err)
		return false
	}

	return isAdmin
}

// checkPermission will check on the given db that the user with
// userID has the permission permName on the project indicated by
// projectID returning a boolean
func checkPermission(db *sql.DB, permName permission.Permission, projectID, userID int64) bool {
	var id int64

	row := db.QueryRow(`
SELECT p.id FROM projects AS p
FULL JOIN project_permission_schemes AS 
     project_scheme ON p.id = project_scheme.project_id
LEFT JOIN permission_schemes AS scheme ON scheme.id = project_scheme.permission_scheme_id
LEFT JOIN permission_scheme_permissions AS perms ON perms.scheme_id = project_scheme.permission_scheme_id
LEFT JOIN permissions AS perm ON perm.id = perms.perm_id
LEFT JOIN roles AS r ON perms.role_id = r.id
LEFT JOIN user_roles AS roles ON roles.role_id = perms.role_id
LEFT JOIN users AS u ON roles.user_id = u.id
WHERE p.id = $1
AND
(
    (select is_admin from users where users.id = $2 and users.is_admin = true) 
    OR
    (perm.name = $4 AND roles.user_id = $3)
)
`,
		projectID, userID, userID, permName)

	err := row.Scan(&id)
	if err != nil {
		fmt.Println("Error checking perm", err)
		handlePqErr(err)
		return false
	}

	if id != 0 {
		return true
	}

	return false
}

// toPqErr converts an error to a pq.Error so we can access more info about what
// happened.
func toPqErr(e error) *pq.Error {
	if err, ok := e.(*pq.Error); ok {
		return err
	}

	return nil
}

// handlePqErr takes an error converts it to a pq.Error if appropriate and will
// return the appropriate store error, if no handling matches it will just
// return the error as it is.
func handlePqErr(e error) store.Error {
	if e == nil {
		return nil
	}

	if e == sql.ErrNoRows {
		return store.ErrNotFound
	}

	pqe := toPqErr(e)
	if pqe == nil {
		return store.Err{Err: e}
	}

	log.Printf("DATABASE: [%v] %s\n", pqe.Code, pqe.Message)

	if pqe.Code == "23505" {
		return store.ErrDuplicateEntry
	}

	return store.Err{Err: e}
}
