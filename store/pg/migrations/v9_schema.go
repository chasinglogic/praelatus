package migrations

const permissions = `
CREATE TABLE IF NOT EXISTS permissions (
	id			 SERIAL PRIMARY KEY,
	updated_date timestamp,
	created_date timestamp DEFAULT current_timestamp,
	level		 varchar(50),

	project_id	 integer REFERENCES projects (id),
	team_id		 integer REFERENCES teams(id),
	user_id		 integer REFERENCES users (id) NOT NULL
);
`

var v9schema = schema{9, permissions, "add permission tables"}
