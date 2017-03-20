package models

import "time"

// Comment is a comment on an issue / ticket.
type Comment struct {
	ID          int64     `json:"id"`
	UpdatedDate time.Time `json:"updated_date"`
	CreatedDate time.Time `json:"created_date"`
	TicketKey   string    `json:"ticket_key"`
	Body        string    `json:"body"`
	Author      User      `json:"author"`
}

func (c *Comment) String() string {
	return jsonString(c)
}
