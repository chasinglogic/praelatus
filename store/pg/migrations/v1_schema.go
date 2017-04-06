package migrations

const dbInfo = `
CREATE TABLE IF NOT EXISTS database_information (
	id SERIAL PRIMARY KEY,
	schema_version integer
);

INSERT INTO database_information (schema_version) VALUES (1);
`

var v1schema = schema{1, dbInfo, "add db info"}
