package migrations

const workflows = `
CREATE TABLE IF NOT EXISTS statuses (
    id   SERIAL PRIMARY KEY,
    name varchar(250) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS workflows (
    id   SERIAL PRIMARY KEY,
    name varchar(250) UNIQUE NOT NULL,

    project_id integer REFERENCES projects (id)
);

CREATE TABLE IF NOT EXISTS workflow_statuses (
    workflow_id integer REFERENCES workflows (id),
    status_id   integer REFERENCES statuses (id)
);

CREATE TABLE IF NOT EXISTS transitions (
    id   SERIAL PRIMARY KEY,
    name varchar(250) NOT NULL,

    workflow_id integer REFERENCES workflows (id),
    from_status integer REFERENCES statuses (id),
    to_status   integer REFERENCES statuses (id)
);

CREATE TABLE IF NOT EXISTS hooks (
    id       SERIAL PRIMARY KEY,
    endpoint varchar(250) NOT NULL,
    method   varchar(10) NOT NULL,
    body     text DEFAULT '',

    transition_id integer REFERENCES transitions (id)
);
`

var v5schema = schema{5, workflows, "create workflow tables"}
