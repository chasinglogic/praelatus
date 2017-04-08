package migrations

const fixPermissionsTable = `
ALTER TABLE permissions DROP COLUMN level;
ALTER TABLE permissions ADD COLUMN level integer DEFAULT 0;
`

var v11schema = schema{11, fixPermissionsTable, "fix permission table"}
