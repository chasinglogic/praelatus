package models

import "time"

// TicketType represents the type of ticket.
type TicketType struct {
	ID   int64  `json:"id"`
	Name string `json:"name"`
}

// Ticket represents a ticket
type Ticket struct {
	ID          int64        `json:"id"`
	CreatedDate time.Time    `json:"created_date"`
	UpdatedDate time.Time    `json:"updated_date"`
	Key         string       `json:"key"`
	Summary     string       `json:"summary"`
	Description string       `json:"description"`
	Fields      []FieldValue `json:"fields"`
	Labels      []Label      `json:"labels"`
	Type        TicketType   `json:"ticket_type"`
	Reporter    User         `json:"reporter"`
	Assignee    User         `json:"assignee"`
	Status      Status       `json:"status"`

	WorkflowID int64 `json:"workflow_id"`

	Transitions []Transition `json:"transitions"`
	Comments    []Comment    `json:"comments,omitempty"`

	Project Project `json:"project"`
}

func (t *Ticket) String() string {
	return jsonString(t)
}

// Transition searches through the available transitions for the ticket
// returning a boolean indicating success or failure and the transition
func (t *Ticket) Transition(name string) (Transition, bool) {
	for _, transition := range t.Transitions {
		if transition.Name == name {
			return transition, true
		}
	}

	return Transition{}, false
}

// Status represents a ticket's current status.
type Status struct {
	ID   int64  `json:"id"`
	Name string `json:"name"`
}

func (s *Status) String() string {
	return jsonString(s)
}

// Label is a label used on tickets
type Label struct {
	ID   int64  `json:"id"`
	Name string `json:"name"`
}

func (l *Label) String() string {
	return jsonString(l)
}
