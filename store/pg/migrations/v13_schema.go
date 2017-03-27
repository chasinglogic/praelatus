package migrations

const shareableWorkflows = `
CREATE TABLE workflows_projects(
    workflow_id integer REFERENCES workflows(id),
    project_id  integer REFERENCES projects(id)
);

INSERT INTO workflows_projects (workflow_id, project_id)
SELECT id, project_id
FROM workflows;

ALTER TABLE workflows DROP COLUMN project_id;
`

var v13schema = schema{13, shareableWorkflows, "setup shareable workflows"}
