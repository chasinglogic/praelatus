package migrations

const comments = `
CREATE TABLE IF NOT EXISTS comments (
	id SERIAL PRIMARY KEY,
	updated_date timestamp DEFAULT current_timestamp,
	created_date timestamp DEFAULT current_timestamp,
	body text NOT NULL,
	author_id integer REFERENCES users (id) NOT NULL,
	ticket_id integer REFERENCES tickets (id) NOT NULL
);`

var v7schema = schema{7, comments, "add comments table"}
