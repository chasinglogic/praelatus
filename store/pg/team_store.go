package pg

import (
	"database/sql"
	"encoding/json"

	"github.com/praelatus/praelatus/models"
)

// TeamStore contains methods for storing and retrieving Teams from a Postgres
// DB
type TeamStore struct {
	db *sql.DB
}

func intoTeam(db *sql.DB, row rowScanner, t *models.Team) error {
	var u models.User
	var ujson json.RawMessage

	err := row.Scan(&t.ID, &t.Name, &ujson)
	if err != nil {
		return err
	}

	err = json.Unmarshal(ujson, &u)
	if err != nil {
		return err
	}

	t.Lead = u

	rows, err := db.Query(`
SELECT u.id, u.username, u.email, 
       u.full_name, u.profile_picture, u.is_admin
FROM teams_users AS tu 
JOIN users AS u ON tu.user_id = u.id
JOIN teams AS t ON tu.team_id = t.id
WHERE tu.team_id = $1;
`,
		t.ID)
	if err != nil {
		return handlePqErr(err)
	}

	defer rows.Close()

	for rows.Next() {
		var u models.User

		err = rows.Scan(&u.ID, &u.Username, &u.Email, &u.FullName,
			&u.ProfilePic, &u.IsAdmin)
		if err != nil {
			return err
		}

		t.Members = append(t.Members, u)
	}

	return nil
}

// Get retrieves a team from the database based on ID
func (ts *TeamStore) Get(t *models.Team) error {
	row := ts.db.QueryRow(`
SELECT t.id, t.name, 
       json_build_object('id', lead.id, 
                         'username', lead.username, 
                         'email', lead.email, 
                         'full_name', lead.full_name, 
                         'profile_picture', lead.profile_picture) AS lead 
FROM teams AS t
JOIN users AS lead ON lead.id = t.lead_id
WHERE t.id = $1
OR t.name = $2;
`,
		t.ID, t.Name)
	err := intoTeam(ts.db, row, t)
	return handlePqErr(err)
}

// GetMembers will get the members for the given team.
func (ts *TeamStore) GetMembers(t *models.Team) error {
	rows, err := ts.db.Query(`
SELECT u.id, username, email, full_name, 
       profile_picture, is_admin
FROM teams_users AS tu
JOIN users AS u ON tu.user_id = u.id
WHERE tu.team_id = $1
`,
		t.ID)
	if err != nil {
		return handlePqErr(err)
	}

	defer rows.Close()

	for rows.Next() {
		var u *models.User

		err = rows.Scan(&u.ID, &u.Username, &u.Email, &u.FullName,
			&u.ProfilePic, &u.IsAdmin)
		if err != nil {
			return handlePqErr(err)
		}

		t.Members = append(t.Members, *u)
	}

	return nil
}

// GetAll retrieves all the teams from the db
func (ts *TeamStore) GetAll() ([]models.Team, error) {
	var teams []models.Team

	rows, err := ts.db.Query(`
SELECT t.id, t.name, 
       json_build_object('id', lead.id, 
                         'username', lead.username, 
                         'email', lead.email, 
                         'full_name', lead.full_name, 
                         'profile_picture', lead.profile_picture) AS lead
FROM teams AS t
JOIN users AS lead ON lead.id = t.lead_id
`)
	if err != nil {
		return teams, handlePqErr(err)
	}

	defer rows.Close()

	for rows.Next() {
		t := &models.Team{}

		err := intoTeam(ts.db, rows, t)
		if err != nil {
			return teams, handlePqErr(err)
		}

		teams = append(teams, *t)
	}

	return teams, handlePqErr(err)
}

// GetForUser will get the given users associated teams
func (ts *TeamStore) GetForUser(u models.User) ([]models.Team, error) {
	var teams []models.Team

	rows, err := ts.db.Query(`
SELECT t.id, t.name, row_to_json(lead.*)
FROM teams_users
JOIN teams AS t ON t.id = teams_users.team_id
JOIN users as u ON u.id = teams_users.user_id
JOIN users as lead ON lead.id = t.lead_id
WHERE u.id = $1
`,
		u.ID)
	if err != nil {
		return teams, err
	}

	defer rows.Close()

	for rows.Next() {
		t := &models.Team{}

		err = intoTeam(ts.db, rows, t)
		if err != nil {
			return teams, err
		}

		teams = append(teams, *t)
	}

	return teams, nil
}

// AddMembers will add users to the given team
func (ts *TeamStore) AddMembers(t models.Team, users ...models.User) error {
	if users == nil {
		return nil
	}

	for _, u := range users {
		_, err := ts.db.Exec(`
INSERT INTO teams_users (team_id, user_id)
VALUES ($1, $2)`, t.ID, u.ID)
		if err != nil {
			return handlePqErr(err)
		}
	}

	return nil
}

// New adds a new team to the database.
func (ts *TeamStore) New(t *models.Team) error {
	err := ts.db.QueryRow(`
INSERT INTO teams (name, lead_id) 
VALUES ($1, $2)
RETURNING id;`,
		t.Name, t.Lead.ID).
		Scan(&t.ID)
	if err != nil {
		return handlePqErr(err)
	}

	for _, mem := range t.Members {
		_, err = ts.db.Exec(`
INSERT INTO teams_users (team_id, user_id) 
VALUES ($1, $2)`, t.ID, mem.ID)
	}

	return handlePqErr(err)
}

// Save updates a t to the database.
func (ts *TeamStore) Save(t models.Team) error {
	_, err := ts.db.Exec(`
UPDATE teams 
SET (name, lead_id) = ($1, $2)
WHERE id = $3;
`,
		t.Name, t.Lead.ID, t.ID)
	return handlePqErr(err)
}

// Remove updates a t to the database.
func (ts *TeamStore) Remove(t models.Team) error {
	tx, err := ts.db.Begin()
	if err != nil {
		return handlePqErr(err)
	}

	_, err = tx.Exec(`DELETE FROM teams_users WHERE team_id = $1;`, t.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	_, err = tx.Exec(`DELETE FROM teams WHERE id = $1;`, t.ID)
	if err != nil {
		tx.Rollback()
		return handlePqErr(err)
	}

	return handlePqErr(tx.Commit())
}
