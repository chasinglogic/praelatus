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
// All methods which take a models.User as their first argument
// represent an "Action". An Action is anything which requires a
// permissions check and the underlying store will take care of
// checking the permissions of the user for you. However some calls to
// the store should still be protected by simple authentication but
// require no permission schemes. Those checks should be performed in
// the HTTP handler for simplicity and performance.
package store

import (
	"database/sql"
	"errors"

	"github.com/praelatus/praelatus/models"
)

var (
	// ErrDuplicateEntry is returned when a unique constraint is
	// violated.
	ErrDuplicateEntry = errors.New("duplicate entry attempted")

	// ErrNotFound is returned when an invalid resource is given
	// or searched for
	ErrNotFound = errors.New("no such resource")

	// ErrNoSession is returned when a session does not exist in
	// the SessionStore
	ErrNoSession = errors.New("no session found")

	// ErrSessionInvalid is returned when a session has timed out
	ErrSessionInvalid = errors.New("session invalid")
)

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

	GetByProject(models.Project, models.TicketType) ([]models.Field, error)
	AddToProject(models.User, models.Project, *models.Field, ...models.TicketType) error

	New(models.User, *models.Field) error
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

	New(models.User, *models.Project) error
	Save(models.User, models.Project) error
	Remove(models.User, models.Project) error
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

	GetComments(models.User, models.Ticket) ([]models.Comment, error)
	NewComment(models.User, models.Ticket, *models.Comment) error
	SaveComment(models.User, models.Comment) error
	RemoveComment(models.User, models.Comment) error

	NextTicketKey(models.Project) string

	ExecuteTransition(models.User, *models.Ticket, models.Transition) error

	New(models.User, models.Project, *models.Ticket) error
	Save(models.User, models.Ticket) error
	Remove(models.User, models.Ticket) error
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
