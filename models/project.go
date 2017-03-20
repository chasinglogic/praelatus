package models

import "time"

// Project is the model used to represent a project in the database.
type Project struct {
	ID              int64     `json:"id"`
	CreatedDate     time.Time `json:"created_date"`
	Name            string    `json:"name"`
	Key             string    `json:"key"`
	Lead            User      `json:"lead"`
	Homepage        string    `json:"homepage,omitempty"`
	IconURL         string    `json:"icon_url,omitempty"`
	Repo            string    `json:"repo,omitempty"`
	AnonymousAccess bool      `json:"anonymous_access,omitempty"`
}

func (p *Project) String() string {
	return jsonString(p)
}
