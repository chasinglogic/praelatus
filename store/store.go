// Package store defines the interfaces we use for storing and
// retrieving models. Managing data this way allows us to easily
// compose and change the way/s that we store our models without
// changing the rest of the application.  (i.e. we can support
// multiple databases much more easily because of this
// architecture). Any method which takes a pointer to a model will
// modify that model in some way (usually filling out the missing
// data) otherwise the method simply uses the provided model for
// reference.
//
// All methods which take a non pointer requires an ID is non-zero on
// that model.  Additionally, any model which contains other models
// (i.e. a Ticket has a User as the reporter and assignee) requires
// that those submodels contain their ID's.
//
// All methods which take a models.User as their first argument and
// are not part of UserStore represent an "Action". An Action is
// anything which requires a permissions check and the underlying
// store will take care of checking the permissions of the user for
// you. However some calls to the store should still be protected by
// simple authentication but require no permission schemes. Those
// checks should be performed in the HTTP handler for simplicity and
// performance.
package store

import (
	"database/sql"
	"errors"

	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/models/permission"
)

var (
	// ErrDuplicateEntry is returned when a unique constraint is
	// violated.
	ErrDuplicateEntry = Err{
		Err: errors.New("duplicate entry attempted"),
	}

	// ErrNotFound is returned when an invalid resource is given
	// or searched for
	ErrNotFound = Err{
		Err: errors.New("no such resource"),
	}

	// ErrNoSession is returned when a session does not exist in
	// the SessionStore
	ErrNoSession = Err{
		Err: errors.New("no session found"),
	}

	// ErrSessionInvalid is returned when a session has timed out
	ErrSessionInvalid = Err{
		Err: errors.New("session invalid"),
	}

	// ErrPermissionDenied is returned when the given user does
	// not have permission to perform the action requested
	ErrPermissionDenied = Err{
		Err: errors.New("permission denied"),
	}
)

// Error wraps the primitive error so that handlers can tell if the
// reason was invalid input or not to provide better error messages to
// the client
type Error interface {
	Error() string
	InvalidInput() bool
}

// Err is used to wrap store errors which are not invalid input
type Err struct {
	Err error
}

func (e Err) Error() string {
	return e.Err.Error()
}

// InvalidInput returns a boolean false indicating this is not an
// invalid input error
func (e Err) InvalidInput() bool {
	return false
}

// ErrInvalidInput is used to indicate an error is caused by invalid
// input, i.e. not a valid role name
type ErrInvalidInput struct {
	Err error
}

func (e ErrInvalidInput) Error() string {
	return e.Err.Error()
}

// InvalidInput returns a boolean true indicating this is an
// invalid input error
func (e ErrInvalidInput) InvalidInput() bool {
	return true
}

// Store is implemented by any struct that has the ability to store
// all of the available models in Praelatus
type Store interface {
	Users() UserStore
	Teams() TeamStore
	Labels() LabelStore
	Fields() FieldStore
	Tickets() TicketStore
	Types() TypeStore
	Projects() ProjectStore
	Statuses() StatusStore
	Workflows() WorkflowStore
	Permissions() PermissionStore
	Roles() RoleStore
}

// SQLStore is implemented by any store which wants to provide a
// direct sql.DB connection to the database this is useful when
// migrating and testing
type SQLStore interface {
	Conn() *sql.DB
}

// Droppable is implemented by any store which allows for all of the
// data to be wiped, this is useful for testing and debugging
type Droppable interface {
	Drop() error
}

// Migrater is implemented by any store which requires setup to be run
// for example creating tables in a sql database or setting up
// collections in a mongodb
type Migrater interface {
	Migrate() error
}

// SessionStore is implemented by any struct supporting a simple key
// value store, preferably a fast one as this is used for storing user
// sessions
type SessionStore interface {
	Get(string) (models.Session, error)
	Set(string, models.Session) error

	GetRaw(string) ([]byte, error)
	SetRaw(string, []byte) error

	Remove(string) error
}

// FieldStore contains methods for storing and retrieving Fields and
// FieldValues
type FieldStore interface {
	Get(*models.Field) error
	GetAll() ([]models.Field, error)

	GetForScreen(models.User, models.Project, models.TicketType) ([]models.Field, error)
	AddToProject(models.User, models.Project, *models.Field, ...models.TicketType) error

	New(*models.Field) error
	Create(models.User, *models.Field) error
	Save(models.User, models.Field) error
	Remove(models.User, models.Field) error
}

// UserStore contains methods for storing and retrieving Users
type UserStore interface {
	Get(*models.User) error
	GetAll() ([]models.User, error)

	New(*models.User) error
	Save(models.User) error
	Remove(models.User) error

	Search(string) ([]models.User, error)
}

// ProjectStore contains methods for storing and retrieving Projects
type ProjectStore interface {
	Get(models.User, *models.Project) error
	GetAll(models.User) ([]models.Project, error)

	New(*models.Project) error
	Create(models.User, *models.Project) error
	Save(models.User, models.Project) error
	Remove(models.User, models.Project) error

	SetPermissionScheme(models.User, models.Project, models.PermissionScheme) error
}

// TypeStore contains methods for storing and retrieving Ticket Types
type TypeStore interface {
	Get(*models.TicketType) error
	GetAll() ([]models.TicketType, error)

	New(*models.TicketType) error
	Save(models.TicketType) error
	Remove(models.TicketType) error
}

// TicketStore contains methods for storing and retrieving Tickets
type TicketStore interface {
	Get(models.User, *models.Ticket) error
	GetAll(models.User) ([]models.Ticket, error)
	GetAllByProject(models.User, models.Project) ([]models.Ticket, error)

	GetComment(models.User, *models.Comment) error
	GetComments(models.User, models.Project, models.Ticket) ([]models.Comment, error)
	NewComment(models.Ticket, *models.Comment) error
	CreateComment(models.User, models.Project, models.Ticket, *models.Comment) error
	SaveComment(models.User, models.Project, models.Comment) error
	RemoveComment(models.User, models.Project, models.Comment) error

	NextTicketKey(models.Project) string

	ExecuteTransition(models.User, models.Project, *models.Ticket, models.Transition) error

	New(models.Project, *models.Ticket) error
	Create(models.User, models.Project, *models.Ticket) error
	Save(models.User, models.Project, models.Ticket) error
	Remove(models.User, models.Project, models.Ticket) error
}

// TeamStore contains methods for storing and retrieving Teams
type TeamStore interface {
	Get(*models.Team) error
	GetAll() ([]models.Team, error)
	GetForUser(models.User) ([]models.Team, error)

	AddMembers(models.Team, ...models.User) error

	New(*models.Team) error
	Save(models.Team) error
	Remove(models.Team) error
}

// StatusStore contains methods for storing and retrieving Statuses
type StatusStore interface {
	Get(*models.Status) error
	GetAll() ([]models.Status, error)

	New(*models.Status) error
	Save(models.Status) error
	Remove(models.Status) error
}

// WorkflowStore contains methods for storing and retrieving Workflows
type WorkflowStore interface {
	Get(*models.Workflow) error
	GetAll() ([]models.Workflow, error)

	GetByProject(models.Project) ([]models.Workflow, error)
	GetForTicket(models.Ticket) (models.Workflow, error)

	New(models.Project, *models.Workflow) error
	Save(models.Workflow) error
	Remove(models.Workflow) error
}

// LabelStore contains methods for storing and retrieving Labels
type LabelStore interface {
	Get(*models.Label) error
	GetAll() ([]models.Label, error)

	New(*models.Label) error
	Save(models.Label) error
	Remove(models.Label) error

	Search(query string) ([]models.Label, error)
}

// PermissionStore contains methods for storing, retrieving, and
// manipulating permissions, roles, and permission schemes
type PermissionStore interface {
	Get(models.User, *models.PermissionScheme) error
	GetAll(models.User) ([]models.PermissionScheme, error)

	New(*models.PermissionScheme) Error
	Create(models.User, *models.PermissionScheme) error
	Save(models.User, models.PermissionScheme) error
	Remove(models.User, models.PermissionScheme) error

	IsAdmin(models.User) bool
	CheckPermission(permission.Permission, models.Project, models.User) bool
}

// RoleStore contains methods for storing, and retrieving roles
type RoleStore interface {
	Get(*models.Role) error
	GetAll() ([]models.Role, error)

	New(*models.Role) error
	Create(models.User, *models.Role) error
	Save(models.User, models.Role) error
	Remove(models.User, models.Role) error

	GetForUser(models.User) ([]models.Role, error)

	AddUserToRole(models.User, models.User, models.Project, models.Role) error
	GetForProject(models.User, models.Project) ([]models.Role, error)
}
