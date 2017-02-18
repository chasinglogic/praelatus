package api

import (
	"net/http"
	"time"

	"github.com/praelatus/praelatus/models"
	"github.com/praelatus/praelatus/store"
)

var loc, _ = time.LoadLocation("")

var router http.Handler

func init() {
	m := make(map[string]*models.User, 0)
	router = New(mockStore{}, mockSessionStore{m})
}

type mockStore struct{}

func (ms mockStore) Users() store.UserStore {
	return mockUsersStore{}
}

func (ms mockStore) Teams() store.TeamStore {
	return mockTeamStore{}
}

func (ms mockStore) Labels() store.LabelStore {
	return mockLabelStore{}
}

func (ms mockStore) Fields() store.FieldStore {
	return mockFieldStore{}
}

func (ms mockStore) Tickets() store.TicketStore {
	return mockTicketStore{}
}

func (ms mockStore) Projects() store.ProjectStore {
	return mockProjectStore{}
}

func (ms mockStore) Types() store.TypeStore {
	return mockTypeStore{}
}

func (ms mockStore) Statuses() store.StatusStore {
	return mockStatusStore{}
}

func (ms mockStore) Workflows() store.WorkflowStore {
	return mockWorkflowStore{}
}

type mockUsersStore struct{}

func (ms mockUsersStore) Get(u *models.User) error {
	u.ID = 1
	u.Username = "foouser"
	u.Password = "foopass"
	u.Email = "foo@foo.com"
	u.FullName = "Foo McFooserson"
	u.IsActive = true
	return nil
}

// because you can't use a pointer in a struct initializer
var settings = models.Settings{}

func (ms mockUsersStore) GetAll() ([]models.User, error) {
	return []models.User{
		models.User{
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
		models.User{
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
		models.User{
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
		models.User{
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
		models.User{
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
		models.User{
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
			models.Team{
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
					models.User{
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
					models.User{
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
			models.Team{
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
					models.User{
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
					models.User{
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
		models.Team{
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
				models.User{
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
				models.User{
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
		models.Team{
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
				models.User{
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
				models.User{
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
		models.Label{
			ID:   1,
			Name: "mock",
		},
		models.Label{
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
		models.Label{
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
		models.Field{
			ID:       1,
			Name:     "String Field",
			DataType: "STRING",
		},
		models.Field{
			ID:       2,
			Name:     "Int Field",
			DataType: "INT",
		},
	}, nil
}

func (mockFieldStore) GetByProject(p models.Project) ([]models.Field, error) {
	return []models.Field{
		models.Field{
			ID:       1,
			Name:     "String Field",
			DataType: "STRING",
		},
		models.Field{
			ID:       2,
			Name:     "Int Field",
			DataType: "INT",
		},
	}, nil
}

func (mockFieldStore) AddToProject(p models.Project, f *models.Field, t ...models.TicketType) error {
	return nil
}

func (mockFieldStore) New(f *models.Field) error {
	f.ID = 1
	return nil
}

func (mockFieldStore) Save(f models.Field) error {
	return nil
}

func (mockFieldStore) Remove(f models.Field) error {
	return nil
}

// //A mock TicketStore struct
type mockTicketStore struct{}

func (mockTicketStore) Get(t *models.Ticket) error {
	t.ID = 1

	t.CreatedDate = time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc)
	t.UpdatedDate = time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc)

	t.Key = "TEST-1"

	t.Summary = "A mock issue"
	t.Description = "This issue is a fake."

	t.Fields = []models.FieldValue{
		models.FieldValue{
			ID:       1,
			Name:     "String Field",
			DataType: "STRING",
			Value:    "This is a string",
		},
		models.FieldValue{
			ID:       2,
			Name:     "Int Field",
			DataType: "INT",
			Value:    3,
		},
	}

	t.Labels = []models.Label{
		models.Label{
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
		Name: "In Progress",
	}

	return nil
}

func (ms mockTicketStore) GetAll() ([]models.Ticket, error) {
	return []models.Ticket{
		models.Ticket{
			ID:          1,
			CreatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			UpdatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),

			Key: "TEST-1",

			Summary:     "A mock issue",
			Description: "This issue is a fake.",

			Fields: []models.FieldValue{
				models.FieldValue{
					ID:       1,
					Name:     "String Field",
					DataType: "STRING",
					Value:    "This is a string",
				},
				models.FieldValue{
					ID:       2,
					Name:     "Int Field",
					DataType: "INT",
					Value:    3,
				},
			},

			Labels: []models.Label{
				models.Label{
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

		models.Ticket{
			ID:          2,
			CreatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			UpdatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),

			Key: "TEST-2",

			Summary:     "A mock issue",
			Description: "This issue is a fake.",

			Fields: []models.FieldValue{
				models.FieldValue{
					ID:       1,
					Name:     "String Field",
					DataType: "STRING",
					Value:    "This is a string",
				},
				models.FieldValue{
					ID:       2,
					Name:     "Int Field",
					DataType: "INT",
					Value:    3,
				},
			},

			Labels: []models.Label{
				models.Label{
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
func (ms mockTicketStore) GetAllByProject(p models.Project) ([]models.Ticket, error) {
	return []models.Ticket{
		models.Ticket{
			ID:          1,
			CreatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			UpdatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),

			Key: "TEST-1",

			Summary:     "A mock issue",
			Description: "This issue is a fake.",

			Fields: []models.FieldValue{
				models.FieldValue{
					ID:       1,
					Name:     "String Field",
					DataType: "STRING",
					Value:    "This is a string",
				},
				models.FieldValue{
					ID:       2,
					Name:     "Int Field",
					DataType: "INT",
					Value:    3,
				},
			},

			Labels: []models.Label{
				models.Label{
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

		models.Ticket{
			ID:          2,
			CreatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			UpdatedDate: time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),

			Key: "TEST-2",

			Summary:     "A mock issue",
			Description: "This issue is a fake.",

			Fields: []models.FieldValue{
				models.FieldValue{
					ID:       1,
					Name:     "String Field",
					DataType: "STRING",
					Value:    "This is a string",
				},
				models.FieldValue{
					ID:       2,
					Name:     "Int Field",
					DataType: "INT",
					Value:    3,
				},
			},

			Labels: []models.Label{
				models.Label{
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

func (ms mockTicketStore) GetComments(t models.Ticket) ([]models.Comment, error) {
	return []models.Comment{
		models.Comment{
			1,
			time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			time.Date(2016, time.Month(12), 25, 0, 0, 0, 0, loc),
			"This is a fake comment",
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

func (ms mockTicketStore) NewComment(t models.Ticket, c *models.Comment) error {
	c.ID = 1
	return nil
}

func (ms mockTicketStore) SaveComment(c models.Comment) error {
	return nil
}

func (ms mockTicketStore) RemoveComment(c models.Comment) error {
	return nil
}

func (ms mockTicketStore) NextTicketKey(p models.Project) string {
	return "TEST-2"
}

func (ms mockTicketStore) New(p models.Project, t *models.Ticket) error {
	t.ID = 1
	return nil
}

func (ms mockTicketStore) Save(t models.Ticket) error {
	return nil
}

func (ms mockTicketStore) Remove(t models.Ticket) error {
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
		models.TicketType{
			ID:   1,
			Name: "mock type",
		},
		models.TicketType{
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

func (ms mockProjectStore) Get(p *models.Project) error {
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

func (ms mockProjectStore) GetAll() ([]models.Project, error) {
	return []models.Project{
		models.Project{
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
		models.Project{
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

func (ms mockProjectStore) Save(p models.Project) error {
	return nil
}

func (ms mockProjectStore) Remove(p models.Project) error {
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
		models.Status{
			1,
			"mock Status",
		},
		models.Status{
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

func (ms mockWorkflowStore) Get(w *models.Workflow) error {
	w = &models.Workflow{
		Name: "Simple Workflow",
		Transitions: map[string][]models.Transition{
			"Backlog": []models.Transition{
				models.Transition{
					Name:     "In Progress",
					ToStatus: models.Status{ID: 2},
					Hooks:    []models.Hook{},
				},
			},
			"In Progress": []models.Transition{
				models.Transition{
					Name:     "Done",
					ToStatus: models.Status{ID: 3},
					Hooks:    []models.Hook{},
				},
				models.Transition{
					Name:     "Backlog",
					ToStatus: models.Status{ID: 1},
					Hooks:    []models.Hook{},
				},
			},
			"Done": []models.Transition{
				models.Transition{
					Name:     "ReOpen",
					ToStatus: models.Status{ID: 1},
					Hooks:    []models.Hook{},
				},
			},
		},
	}

	return nil
}

func (ms mockWorkflowStore) GetByProject(p models.Project) ([]models.Workflow, error) {
	return []models.Workflow{
		models.Workflow{
			ID:   1,
			Name: "Simple Workflow",
			Transitions: map[string][]models.Transition{
				"Backlog": []models.Transition{
					models.Transition{
						Name:     "In Progress",
						ToStatus: models.Status{ID: 2},
						Hooks:    []models.Hook{},
					},
				},
				"In Progress": []models.Transition{
					models.Transition{
						Name:     "Done",
						ToStatus: models.Status{ID: 3},
						Hooks:    []models.Hook{},
					},
					models.Transition{
						Name:     "Backlog",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
				"Done": []models.Transition{
					models.Transition{
						Name:     "ReOpen",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
			},
		},

		models.Workflow{
			ID:   2,
			Name: "Another Simple Workflow",
			Transitions: map[string][]models.Transition{
				"Backlog": []models.Transition{
					models.Transition{
						Name:     "In Progress",
						ToStatus: models.Status{ID: 2},
						Hooks:    []models.Hook{},
					},
				},
				"In Progress": []models.Transition{
					models.Transition{
						Name:     "Done",
						ToStatus: models.Status{ID: 3},
						Hooks:    []models.Hook{},
					},
					models.Transition{
						Name:     "Backlog",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
				"Done": []models.Transition{
					models.Transition{
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
		models.Workflow{
			ID:   1,
			Name: "Simple Workflow",
			Transitions: map[string][]models.Transition{
				"Backlog": []models.Transition{
					models.Transition{
						Name:     "In Progress",
						ToStatus: models.Status{ID: 2},
						Hooks:    []models.Hook{},
					},
				},
				"In Progress": []models.Transition{
					models.Transition{
						Name:     "Done",
						ToStatus: models.Status{ID: 3},
						Hooks:    []models.Hook{},
					},
					models.Transition{
						Name:     "Backlog",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
				"Done": []models.Transition{
					models.Transition{
						Name:     "ReOpen",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
			},
		},

		models.Workflow{
			ID:   2,
			Name: "Another Simple Workflow",
			Transitions: map[string][]models.Transition{
				"Backlog": []models.Transition{
					models.Transition{
						Name:     "In Progress",
						ToStatus: models.Status{ID: 2},
						Hooks:    []models.Hook{},
					},
				},
				"In Progress": []models.Transition{
					models.Transition{
						Name:     "Done",
						ToStatus: models.Status{ID: 3},
						Hooks:    []models.Hook{},
					},
					models.Transition{
						Name:     "Backlog",
						ToStatus: models.Status{ID: 1},
						Hooks:    []models.Hook{},
					},
				},
				"Done": []models.Transition{
					models.Transition{
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

func testLogin(r *http.Request) {
	u := models.User{
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

	err := SetUserSession(u, r)
	if err != nil {
		panic(err)
	}
}

func testAdminLogin(r *http.Request) {
	u := models.User{
		1,
		"foouser",
		"foopass",
		"foo@foo.com",
		"Foo McFooserson",
		"",
		true,
		true,
		&settings,
	}

	err := SetUserSession(u, r)
	if err != nil {
		panic(err)
	}
}

type mockSessionStore struct {
	store map[string]*models.User
}

func (m mockSessionStore) Get(id string) (models.User, error) {
	u := m.store[id]
	if u == nil {
		return models.User{
			1,
			"foouser",
			"foopass",
			"foo@foo.com",
			"Foo McFooserson",
			"",
			false,
			true,
			&settings,
		}, nil
	}

	return *u, nil
}

func (m mockSessionStore) Set(id string, u models.User) error {
	m.store[id] = &u
	return nil
}
