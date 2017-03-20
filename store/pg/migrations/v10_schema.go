package migrations

const addWorkflowID = `
ALTER TABLE tickets ADD COLUMN workflow_id 
	integer REFERENCES workflows (id);
UPDATE tickets SET workflow_id = 1 WHERE workflow_id = null;
`

var v10schema = schema{10, addWorkflowID, "add workflow_id to tickets table"}
