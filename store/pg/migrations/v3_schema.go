package migrations

const teams = `
CREATE TABLE IF NOT EXISTS teams (
    id           SERIAL PRIMARY KEY,
    name         varchar(40) UNIQUE NOT NULL,

    lead_id integer REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS teams_users (
	id SERIAL PRIMARY KEY,

	team_id integer REFERENCES teams (id) NOT NULL,
	user_id integer REFERENCES users (id) NOT NULL
);`

var v3schema = schema{3, teams, "create team tables"}
