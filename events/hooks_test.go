package events

import (
	"math/rand"
	"testing"

	"github.com/praelatus/praelatus/models"
)

func TestHookListener(t *testing.T) {
	evm := New()
	evm.RegisterListener(hookEventChan)

	go handleHookEvent(evm.Result)

	tk := models.Ticket{
		Key:         "TEST-1",
		Summary:     "This is a test ticket. #1",
		Description: "No really, this is just a test",
		Reporter:    models.User{ID: 1},
		Assignee:    models.User{ID: 1},
		Status:      models.Status{ID: 1},
		Labels: []models.Label{
			{
				ID:   1,
				Name: "test",
			},
		},
		Fields: []models.FieldValue{
			{
				Name:  "Story Points",
				Value: rand.Intn(100),
			},
			{
				Name:  "Priority",
				Value: []string{"HIGH"},
			},
		},
		Type: models.TicketType{ID: 1},
	}

	e := models.Event{
		Ticket: tk,
		Data: models.Transition{
			Name:     "In Progress",
			ToStatus: models.Status{ID: 2},
			Hooks: []models.Hook{
				{
					Method:   "GET",
					Endpoint: "https://praelatus.io/",
					Body:     "{{ . }}",
				},
			},
		},
	}

	hookEventChan <- e

	res := <-evm.Result
	if !res.Success {
		t.Errorf("%s: %s\n", res.Reporter, res.Error.Error())
	}
}
