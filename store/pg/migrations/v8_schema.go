package migrations

const labels = `
CREATE TABLE IF NOT EXISTS labels (
	id SERIAL PRIMARY KEY,
	name varchar(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets_labels (
	label_id integer REFERENCES labels (id),
	ticket_id integer REFERENCES tickets (id),
	PRIMARY KEY(label_id, ticket_id)
);`

var v8schema = schema{8, labels, "add labels tables"}
