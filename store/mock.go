package store

import (
	"errors"
	"net/http"
	"time"

	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/models/permission"
)

// Mock will return a mock store and session store to use for testing
func Mock() (Store, SessionStore) {
	return mockStore{},
		mockSessionStore{
			store: make(map[string]*models.User),
		}
}

var loc, _ = time.LoadLocation("")

var router http.Handler

type mockStore struct{}

func (ms mockStore) Users() UserStore {
	return mockUsersStore{}
}

func (ms mockStore) Teams() TeamStore {
	return mockTeamStore{}
}

func (ms mockStore) Labels() LabelStore {
	return mockLabelStore{}
}

func (ms mockStore) Fields() FieldStore {
	return mockFieldStore{}
}

func (ms mockStore) Tickets() TicketStore {
	return mockTicketStore{}
}

func (ms mockStore) Projects() ProjectStore {
	return mockProjectStore{}
}

func (ms mockStore) Types() TypeStore {
	return mockTypeStore{}
}

func (ms mockStore) Statuses() StatusStore {
	return mockStatusStore{}
}

func (ms mockStore) Workflows() WorkflowStore {
	return mockWorkflowStore{}
}

func (ms mockStore) Permissions() PermissionStore {
	return mockPermissionStore{}
}

func (ms mockStore) Roles() RoleStore {
	return mockRoleStore{}
}

type mockUsersStore struct{}

var us, _ = models.NewUser("foouser", "foopass", "Foo McFooserson", "foo@foo.com", false)

func (ms mockUsersStore) Get(u *models.User) error {
	u.ID = 1
	u.IsActive = true
	u.Username = us.Username
	u.Password = us.Password
	u.FullName = us.FullName
	u.Email = us.Email
	return nil
}

// because you can't use a pointer in a struct initializer
var settings = models.Settings{}

func (ms mockUsersStore) GetAll() ([]models.User, error) {
	return []models.User{
		{
			1,
			"foouser",
			"foopass",
			"foo@foo.com",
			"Foo McFooserson",
			"",
			false,
			true,
			&settings,
		},
		{
			2,
			"foouser",
			"foopass",
			"foo@foo.com",
			"Foo McFooserson",
			"",
			false,
			true,
			&settings,
		},
	}, nil
}

func (ms mockUsersStore) Search(query string) ([]models.User, error) {
	if query != "foo" {
		return nil, nil
	}

	return []models.User{
		{
			1,
			"foouser",
			"foopass",
			"foo@foo.com",
			"Foo McFooserson",
			"",
			false,
			true,
			&settings,
		},
		{
			2,
			"foouser",
			"foopass",
			"foo@foo.com",
			"Foo McFooserson",
			"",
			false,
			true,
			&settings,
		},
	}, nil
}

func (ms mockUsersStore) New(u *models.User) error {
	u.ID = 1
	return nil
}

func (ms mockUsersStore) Save(u models.User) error {
	return nil
}

func (ms mockUsersStore) Remove(u models.User) error {
	return nil
}

//A mock TeamStore struct
type mockTeamStore struct{}

func (ms mockTeamStore) Get(t *models.Team) error {
	t.ID = 1
	t.Name = "A"
	t.Lead = models.User{
		1,
		"foouser",
		"foopass",
		"foo@foo.com",
		"Foo McFooserson",
		"",
		false,
		true,
		&settings,
	}
	t.Members = []models.User{
		{
			1,
			"foouser",
			"foopass",
			"foo@foo.com",
			"Foo McFooserson",
			"",
			false,
			true,
			&settings,
		},
		{
			2,
			"foouser",
			"foopass",
			"foo@foo.com",
			"Foo McFooserson",
			"",
			false,
			true,
			&settings,
		},
	}
	return nil
}

func (ms mockTeamStore) GetAll() ([]models.Team, error) {
	return []models.Team{
			{
				ID:   1,
				Name: "A",
				Lead: models.User{
					1,
					"foouser",
					"foopass",
					"foo@foo.com",
					"Foo McFooserson",
					"",
					false,
					true,
					&settings,
				},
				Members: []models.User{
					{
						1,
						"foouser",
						"foopass",
						"foo@foo.com",
						"Foo McFooserson",
						"",
						false,
						true,
						&settings,
					},
					{
						2,
						"foouser",
						"foopass",
						"foo@foo.com",
						"Foo McFooserson",
						"",
						false,
						true,
						&settings,
					},
				},
			},
			{
				ID:   1,
				Name: "A",
				Lead: models.User{
					2,
					"foouser3",
					"foopass",
					"foo@foo3.com",
					"Foo McFooserson3",
					"",
					false,
					true,
					&settings,
				},
				Members: []models.User{
					{
						3,
						"foouser3",
						"foopass",
						"foo@foo3.com",
						"Foo McFooserson3",
						"",
						false,
						true,
						&settings,
					},
					{
						4,
						"foouser4",
						"foopass",
						"foo@foo4.com",
						"Foo McFooserson4",
						"",
						false,
						true,
						&settings,
					},
				},
			},
		},
		nil
}

func (ms mockTeamStore) GetForUser(m models.User) ([]models.Team, error) {
	return []models.Team{
		{
			ID:   1,
			Name: "A",
			Lead: models.User{
				1,
				"foouser",
				"foopass",
				"foo@foo.com",
				"Foo McFooserson",
				"",
				false,
				true,
				&settings,
			},
			Members: []models.User{
				{
					1,
					"foouser",
					"foopass",
					"foo@foo.com",
					"Foo McFooserson",
					"",
					false,
					true,
					&settings,
				},
				{
					2,
					"foouser",
					"foopass",
					"foo@foo.com",
					"Foo McFooserson",
					"",
					false,
					true,
					&settings,
				},
			},
		},
		{
			ID:   1,
			Name: "A",
			Lead: models.User{
				2,
				"foouser3",
				"foopass",
				"foo@foo3.com",
				"Foo McFooserson3",
				"",
				false,
				true,
				&settings,
			},
			Members: []models.User{
				{
					3,
					"foouser3",
					"foopass",
					"foo@foo3.com",
					"Foo McFooserson3",
					"",
					false,
					true,
					&settings,
				},
				{
					4,
					"foouser4",
					"foopass",
					"foo@foo4.com",
					"Foo McFooserson4",
					"",
					false,
					true,
					&settings,
				},
			},
		},
	}, nil
}

func (ms mockTeamStore) AddMembers(m models.Team, u ...models.User) error {
	return nil
}

func (ms mockTeamStore) New(t *models.Team) error {
	t.ID = 1
	return nil
}

func (ms mockTeamStore) Save(t models.Team) error {
	return nil
}

func (ms mockTeamStore) Remove(t models.Team) error {
	return nil
}

//A mock LabelStore struct
type mockLabelStore struct{}

func (ms mockLabelStore) Get(l *models.Label) error {
	l.ID = 1
	l.Name = "mock"
	return nil
}

func (ms mockLabelStore) GetAll() ([]models.Label, error) {
	return []models.Label{
		{
			ID:   1,
			Name: "mock",
		},
		{
			ID:   2,
			Name: "fake",
		},
	}, nil
}

func (ms mockLabelStore) Search(query string) ([]models.Label, error) {
	if query != "fake" {
		return nil, nil
	}

	return []models.Label{
		{
			ID:   2,
			Name: "fake",
		},
	}, nil
}

func (ms mockLabelStore) New(l *models.Label) error {
	l.ID = 1
	return nil
}

func (ms mockLabelStore) Save(l models.Label) error {
	return nil
}

func (ms mockLabelStore) Remove(l models.Label) error {
	return nil
}

//A mock FieldStore struct
type mockFieldStore struct{}

func (mockFieldStore) Get(f *models.Field) error {
	f.ID = 1
	f.Name = "String Field"
	f.DataType = "STRING"
	return nil
}

func (mockFieldStore) GetAll() ([]models.Field, error) {
	return []models.Field{
		{
			ID:       1,
			Name:     "String Field",
			DataType: "STRING",
		},
		{
			ID:       2,
			Name:     "Int Field",
			DataType: "INT",
		},
	}, nil
}

func (mockFieldStore) GetForScreen(u models.User, p models.Project, t models.TicketType) ([]models.Field, error) {
	return []models.Field{
		{
			ID:       1,
			Name:     "String Field",
			DataType: "STRING",
		},
		{
			ID:       2,
			Name:     "Int Field",
			DataType: "INT",
		},
	}, nil
}

func (mockFieldStore) AddToProject(u models.User, p models.Project, f *models.Field, t ...models.TicketType) error {
	return nil
}

func (mockFieldStore) New(f *models.Field) error {
	f.ID = 1
	return nil
}

func (mockFieldStore) Create(u models.User, f *models.Field) error {
	f.ID = 1
	return nil
}

func (mockFieldStore) Save(u models.User, f models.Field) error {
	return nil
}

func (mockFieldStore) Remove(u models.User, f models.Field) error {
	return nil
}

// //A mock TicketStore struct
type mockTicketStore struct{}

func (mockTicketStore) Get(u models.User, t *models.Ticket) error {
	t.ID = 1

	t.CreatedDate = time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc)
	t.UpdatedDate = time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc)

	t.Key = "TEST-1"

	t.Summary = "A mock issue"
	t.Description = "This issue is a fake."

	t.Transitions = []models.Transition{
		{
			ID:   2,
			Name: "In Progress",
			ToStatus: models.Status{
				ID:   2,
				Name: "In Progress",
			},
		},
		{
			ID:   3,
			Name: "Done",
			ToStatus: models.Status{
				ID:   3,
				Name: "Done",
			},
		},
	}

	t.Fields = []models.FieldValue{
		{
			ID:       1,
			Name:     "String Field",
			DataType: "STRING",
			Value:    "This is a string",
		},
		{
			ID:       2,
			Name:     "Int Field",
			DataType: "INT",
			Value:    3,
		},
	}

	t.Labels = []models.Label{
		{
			ID:   1,
			Name: "mock",
		},
	}

	t.Type = models.TicketType{1, "Bug"}

	t.Reporter = models.User{
		1,
		"foouser",
		"foopass",
		"foo@foo.com",
		"Foo McFooserson",
		"",
		false,
		true,
		&settings,
	}

	t.Assignee = models.User{
		2,
		"baruser",
		"barpass",
		"bar@bar.com",
		"Bar McBarserson",
		"",
		true,
		true,
		&settings,
	}

	t.Status = models.Status{
		ID:   1,
		Name: "Backlog",
	}

	return nil
}

func (ms mockTicketStore) GetAll(u models.User) ([]models.Ticket, error) {
	return []models.Ticket{
		{
			ID:          1,
			CreatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			UpdatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),

			Key: "TEST-1",

			Summary:     "A mock issue",
			Description: "This issue is a fake.",

			Fields: []models.FieldValue{
				{
					ID:       1,
					Name:     "String Field",
					DataType: "STRING",
					Value:    "This is a string",
				},
				{
					ID:       2,
					Name:     "Int Field",
					DataType: "INT",
					Value:    3,
				},
			},

			Labels: []models.Label{
				{
					ID:   1,
					Name: "mock",
				},
			},

			Type: models.TicketType{1, "Bug"},

			Reporter: models.User{
				1,
				"foouser",
				"foopass",
				"foo@foo.com",
				"Foo McFooserson",
				"",
				false,
				true,
				&settings,
			},

			Assignee: models.User{
				2,
				"baruser",
				"barpass",
				"bar@bar.com",
				"Bar McBarserson",
				"",
				true,
				true,
				&settings,
			},

			Status: models.Status{
				ID:   1,
				Name: "In Progress",
			},
		},

		{
			ID:          2,
			CreatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			UpdatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),

			Key: "TEST-2",

			Summary:     "A mock issue",
			Description: "This issue is a fake.",

			Fields: []models.FieldValue{
				{
					ID:       1,
					Name:     "String Field",
					DataType: "STRING",
					Value:    "This is a string",
				},
				{
					ID:       2,
					Name:     "Int Field",
					DataType: "INT",
					Value:    3,
				},
			},

			Labels: []models.Label{
				{
					ID:   1,
					Name: "mock",
				},
			},

			Type: models.TicketType{1, "Bug"},

			Reporter: models.User{
				1,
				"foouser",
				"foopass",
				"foo@foo.com",
				"Foo McFooserson",
				"",
				false,
				true,
				&settings,
			},

			Assignee: models.User{
				2,
				"baruser",
				"barpass",
				"bar@bar.com",
				"Bar McBarserson",
				"",
				true,
				true,
				&settings,
			},

			Status: models.Status{
				ID:   1,
				Name: "In Progress",
			},
		},
	}, nil
}

func (ms mockTicketStore) ExecuteTransition(u models.User, p models.Project, t *models.Ticket, tr models.Transition) error {
	t.Status = tr.ToStatus
	return nil
}

func (ms mockTicketStore) GetAllByProject(u models.User, p models.Project) ([]models.Ticket, error) {
	return []models.Ticket{
		{
			ID:          1,
			CreatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			UpdatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),

			Key: "TEST-1",

			Summary:     "A mock issue",
			Description: "This issue is a fake.",

			Fields: []models.FieldValue{
				{
					ID:       1,
					Name:     "String Field",
					DataType: "STRING",
					Value:    "This is a string",
				},
				{
					ID:       2,
					Name:     "Int Field",
					DataType: "INT",
					Value:    3,
				},
			},

			Labels: []models.Label{
				{
					ID:   1,
					Name: "mock",
				},
			},

			Type: models.TicketType{1, "Bug"},

			Reporter: models.User{
				1,
				"foouser",
				"foopass",
				"foo@foo.com",
				"Foo McFooserson",
				"",
				false,
				true,
				&settings,
			},

			Assignee: models.User{
				2,
				"baruser",
				"barpass",
				"bar@bar.com",
				"Bar McBarserson",
				"",
				true,
				true,
				&settings,
			},

			Status: models.Status{
				ID:   1,
				Name: "In Progress",
			},
		},

		{
			ID:          2,
			CreatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			UpdatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),

			Key: "TEST-2",

			Summary:     "A mock issue",
			Description: "This issue is a fake.",

			Fields: []models.FieldValue{
				{
					ID:       1,
					Name:     "String Field",
					DataType: "STRING",
					Value:    "This is a string",
				},
				{
					ID:       2,
					Name:     "Int Field",
					DataType: "INT",
					Value:    3,
				},
			},

			Labels: []models.Label{
				{
					ID:   1,
					Name: "mock",
				},
			},

			Type: models.TicketType{1, "Bug"},

			Reporter: models.User{
				1,
				"foouser",
				"foopass",
				"foo@foo.com",
				"Foo McFooserson",
				"",
				false,
				true,
				&settings,
			},

			Assignee: models.User{
				2,
				"baruser",
				"barpass",
				"bar@bar.com",
				"Bar McBarserson",
				"",
				true,
				true,
				&settings,
			},

			Status: models.Status{
				ID:   1,
				Name: "In Progress",
			},
		},
	}, nil
}

func (ms mockTicketStore) GetComment(u models.User, cm *models.Comment) error {
	cm.ID = 1
	return nil
}

func (ms mockTicketStore) GetComments(u models.User, p models.Project, t models.Ticket) ([]models.Comment, error) {
	return []models.Comment{
		{
			1,
			time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			"This is a fake comment",
			t.Key,
			models.User{
				2,
				"baruser",
				"barpass",
				"bar@bar.com",
				"Bar McBarserson",
				"",
				true,
				true,
				&settings,
			},
		},
	}, nil
}

func (ms mockTicketStore) CreateComment(u models.User, p models.Project, t models.Ticket, c *models.Comment) error {
	c.ID = 1
	return nil
}

func (ms mockTicketStore) NewComment(t models.Ticket, c *models.Comment) error {
	c.ID = 1
	return nil
}

func (ms mockTicketStore) SaveComment(u models.User, p models.Project, c models.Comment) error {
	return nil
}

func (ms mockTicketStore) RemoveComment(u models.User, p models.Project, c models.Comment) error {
	return nil
}

func (ms mockTicketStore) NextTicketKey(p models.Project) string {
	return "TEST-2"
}

func (ms mockTicketStore) New(p models.Project, t *models.Ticket) error {
	t.ID = 1
	return nil
}

func (ms mockTicketStore) Create(u models.User, p models.Project, t *models.Ticket) error {
	t.ID = 1
	return nil
}

func (ms mockTicketStore) Save(u models.User, p models.Project, t models.Ticket) error {
	return nil
}

func (ms mockTicketStore) Remove(u models.User, p models.Project, t models.Ticket) error {
	return nil
}

// A mock TypeStore struct
type mockTypeStore struct{}

func (ms mockTypeStore) Get(t *models.TicketType) error {
	t.ID = 1
	t.Name = "mock type"
	return nil
}

func (ms mockTypeStore) GetAll() ([]models.TicketType, error) {
	return []models.TicketType{
		{
			ID:   1,
			Name: "mock type",
		},
		{
			ID:   2,
			Name: "fake type",
		},
	}, nil
}

func (ms mockTypeStore) New(t *models.TicketType) error {
	t.ID = 1
	return nil
}

func (ms mockTypeStore) Save(t models.TicketType) error {
	return nil
}

func (ms mockTypeStore) Remove(t models.TicketType) error {
	return nil
}

// A mock ProjectStore struct
type mockProjectStore struct{}

func (ms mockProjectStore) Get(u models.User, p *models.Project) error {
	p.ID = 1
	p.Name = "Test Project"
	p.Key = "TEST"
	p.CreatedDate = time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc)
	p.Lead = models.User{
		2,
		"baruser",
		"barpass",
		"bar@bar.com",
		"Bar McBarserson",
		"",
		true,
		true,
		&settings,
	}
	return nil
}

func (ms mockProjectStore) GetAll(u models.User) ([]models.Project, error) {
	return []models.Project{
		{
			ID:          1,
			CreatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			Name:        "Test Project",
			Key:         "TEST",
			Lead: models.User{
				2,
				"baruser",
				"barpass",
				"bar@bar.com",
				"Bar McBarserson",
				"",
				true,
				true,
				&settings,
			},
		},
		{
			ID:          2,
			Name:        "mock Project",
			Key:         "MOCK",
			CreatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			Lead: models.User{
				1,
				"foouser",
				"foopass",
				"foo@foo.com",
				"Foo McFooserson",
				"",
				false,
				true,
				&settings,
			},
		},
	}, nil
}

func (ms mockProjectStore) New(p *models.Project) error {
	p.ID = 1
	return nil
}

func (ms mockProjectStore) Create(u models.User, p *models.Project) error {
	p.ID = 1
	return nil
}

func (ms mockProjectStore) Save(u models.User, p models.Project) error {
	return nil
}

func (ms mockProjectStore) Remove(u models.User, p models.Project) error {
	return nil
}

// A mock StatusStore struct
type mockStatusStore struct{}

func (ms mockStatusStore) Get(s *models.Status) error {
	s.ID = 1
	s.Name = "mock Status"
	return nil
}

func (ms mockStatusStore) GetAll() ([]models.Status, error) {
	return []models.Status{
		{
			1,
			"mock Status",
		},
		{
			2,
			"Fake Status",
		},
	}, nil
}

func (ms mockStatusStore) New(s *models.Status) error {
	s.ID = 1
	return nil
}

func (ms mockStatusStore) Save(p models.Status) error {
	return nil
}

func (ms mockStatusStore) Remove(p models.Status) error {
	return nil
}

// A mock Workflow Store
type mockWorkflowStore struct{}

func (ms mockWorkflowStore) GetForTicket(t models.Ticket) (models.Workflow, error) {
	return models.Workflow{
		ID:   1,
		Name: "Simple Workflow",
		Transitions: map[string][]models.Transition{
			"Backlog": {
				{
					Name:     "In Progress",
					ToStatus: models.Status{ID: 2},
					Hooks:    []models.Hook{},
				},
			},
			"In Progress": {
				{
					Name:     "Done",
					ToStatus: models.Status{ID: 3},
					Hooks:    []models.Hook{},
				},
				{
					Name:     "Backlog",
					ToStatus: models.Status{ID: 1},
					Hooks:    []models.Hook{},
				},
			},
			"Done": {
				{
					Name:     "ReOpen",
					ToStatus: models.Status{ID: 1},
					Hooks:    []models.Hook{},
				},
			},
		},
	}, nil
}

func (ms mockWorkflowStore) Get(w *models.Workflow) error {
	w.Name = "Simple Workflow"
	w.Transitions = map[string][]models.Transition{
		"Backlog": {
			{
				Name:     "In Progress",
				ToStatus: models.Status{ID: 2},
				Hooks:    []models.Hook{},
			},
		},
		"In Progress": {
			{
				Name:     "Done",
				ToStatus: models.Status{ID: 3},
				Hooks:    []models.Hook{},
			},
			{
				Name:     "Backlog",
				ToStatus: models.Status{ID: 1},
				Hooks:    []models.Hook{},
			},
		},
		"Done": {
			{
				Name:     "ReOpen",
				ToStatus: models.Status{ID: 1},
				Hooks:    []models.Hook{},
			},
		},
	}

	return nil
}

func (ms mockWorkflowStore) GetByProject(p models.Project) ([]models.Workflow, error) {
	return []models.Workflow{
		{
			ID:   1,
			Name: "Simple Workflow",
			Transitions: map[string][]models.Transition{
				"Backlog": {
					{
						Name:     "In Progress",
						ToStatus: models.Status{ID: 2},
						Hooks:    []models.Hook{},
					},
				},
				"In Progress": {
					{
						Name:     "Done",
						ToStatus: models.Status{ID: 3},
						Hooks:    []models.Hook{},
					},
					{
						Name:     "Backlog",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
				"Done": {
					{
						Name:     "ReOpen",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
			},
		},

		{
			ID:   2,
			Name: "Another Simple Workflow",
			Transitions: map[string][]models.Transition{
				"Backlog": {
					{
						Name:     "In Progress",
						ToStatus: models.Status{ID: 2},
						Hooks:    []models.Hook{},
					},
				},
				"In Progress": {
					{
						Name:     "Done",
						ToStatus: models.Status{ID: 3},
						Hooks:    []models.Hook{},
					},
					{
						Name:     "Backlog",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
				"Done": {
					{
						Name:     "ReOpen",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
			},
		},
	}, nil
}

func (ms mockWorkflowStore) GetAll() ([]models.Workflow, error) {
	return []models.Workflow{
		{
			ID:   1,
			Name: "Simple Workflow",
			Transitions: map[string][]models.Transition{
				"Backlog": {
					{
						Name:     "In Progress",
						ToStatus: models.Status{ID: 2},
						Hooks:    []models.Hook{},
					},
				},
				"In Progress": {
					{
						Name:     "Done",
						ToStatus: models.Status{ID: 3},
						Hooks:    []models.Hook{},
					},
					{
						Name:     "Backlog",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
				"Done": {
					{
						Name:     "ReOpen",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
			},
		},

		{
			ID:   2,
			Name: "Another Simple Workflow",
			Transitions: map[string][]models.Transition{
				"Backlog": {
					{
						Name:     "In Progress",
						ToStatus: models.Status{ID: 2},
						Hooks:    []models.Hook{},
					},
				},
				"In Progress": {
					{
						Name:     "Done",
						ToStatus: models.Status{ID: 3},
						Hooks:    []models.Hook{},
					},
					{
						Name:     "Backlog",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
				"Done": {
					{
						Name:     "ReOpen",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
			},
		},
	}, nil
}

func (ms mockWorkflowStore) New(p models.Project, w *models.Workflow) error {
	w.ID = 1
	return nil
}

func (ms mockWorkflowStore) Save(p models.Workflow) error {
	return nil
}

func (ms mockWorkflowStore) Remove(p models.Workflow) error {
	return nil
}

type mockSessionStore struct {
	store map[string]*models.User
}

func (m mockSessionStore) Remove(id string) error { return nil }

func (m mockSessionStore) Get(id string) (models.Session, error) {
	u := m.store[id]
	if u == nil {
		return models.Session{}, errors.New("no session")
	}

	return models.Session{
		Expires: time.Now().Add(time.Hour),
		User:    *u,
	}, nil
}

func (m mockSessionStore) Set(id string, u models.Session) error {
	m.store[id] = &u.User
	return nil
}

func (m mockSessionStore) GetRaw(id string) ([]byte, error) { return nil, nil }
func (m mockSessionStore) SetRaw(id string, b []byte) error { return nil }

// A mock PermissionStore struct
type mockPermissionStore struct{}

func (ms mockPermissionStore) Get(u models.User, l *models.PermissionScheme) error {
	l.ID = 1
	l.Name = "mock"
	return nil
}

func (ms mockPermissionStore) GetAll(u models.User) ([]models.PermissionScheme, error) {
	return []models.PermissionScheme{
		{
			ID:   1,
			Name: "mock",
		},
		{
			ID:   2,
			Name: "fake",
		},
	}, nil
}

func (ms mockPermissionStore) Create(u models.User, l *models.PermissionScheme) error {
	return ms.New(l)
}

func (ms mockPermissionStore) New(l *models.PermissionScheme) Error {
	l.ID = 1
	return nil
}

func (ms mockPermissionStore) Save(u models.User, l models.PermissionScheme) error {
	return nil
}

func (ms mockPermissionStore) Remove(u models.User, l models.PermissionScheme) error {
	return nil
}

func (ms mockPermissionStore) CheckPermission(permName permission.Permission, p models.Project, u models.User) bool {
	return true
}

func (ms mockPermissionStore) IsAdmin(u models.User) bool {
	return true
}

// A mock RoleStore struct
type mockRoleStore struct{}

func (ms mockRoleStore) Get(l *models.Role) error {
	l.ID = 1
	l.Name = "mock"
	return nil
}

func (ms mockRoleStore) GetAll() ([]models.Role, error) {
	return []models.Role{
		{
			ID:   1,
			Name: "mock",
		},
		{
			ID:   2,
			Name: "fake",
		},
	}, nil
}

func (ms mockRoleStore) GetForUser(u models.User) ([]models.Role, error) {
	return []models.Role{
		{
			ID:   1,
			Name: "mock",
		},
		{
			ID:   2,
			Name: "fake",
		},
	}, nil
}

func (ms mockRoleStore) GetForProject(u models.User, p models.Project) ([]models.Role, error) {
	return []models.Role{
		{
			ID:   1,
			Name: "mock",
		},
		{
			ID:   2,
			Name: "fake",
		},
	}, nil
}

func (ms mockRoleStore) Create(u models.User, l *models.Role) error {
	return ms.New(l)
}

func (ms mockRoleStore) New(l *models.Role) error {
	l.ID = 1
	return nil
}

func (ms mockRoleStore) Save(u models.User, l models.Role) error {
	return nil
}

func (ms mockRoleStore) Remove(u models.User, l models.Role) error {
	return nil
}

func (ms mockRoleStore) AddUserToRole(u models.User,
	u2 models.User, p models.Project, r models.Role) error {
	return nil
}
