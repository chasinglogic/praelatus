package migrations

const dbInfo = `
CREATE TABLE IF NOT EXISTS database_information (
	id SERIAL PRIMARY KEY,
	schema_version integer
);
INSERT INTO database_information (schema_version) VALUES (1);
`

var v1schema = schema{1, dbInfo, "add db info"}

const users = `
CREATE TABLE IF NOT EXISTS users (
    id              SERIAL PRIMARY KEY,
    username        varchar(40) UNIQUE NOT NULL,
    password        varchar(250) NOT NULL,
    email           varchar(250) NOT NULL,
    full_name       varchar(250) NOT NULL,
    is_admin        boolean DEFAULT false,
    is_active       boolean DEFAULT true,
    profile_picture varchar(250) NOT NULL
);`

var v2schema = schema{2, users, "create user tables"}

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

const projects = `
CREATE TABLE IF NOT EXISTS projects (
    id              SERIAL PRIMARY KEY,
	created_date    timestamp DEFAULT current_timestamp,
    name            varchar(250) NOT NULL,
    key				varchar(40)  NOT NULL UNIQUE,
    repo			varchar(250),
    homepage        varchar(250),
    icon_url        varchar(250),

    lead_id			integer REFERENCES users (id) NOT NULL
);`

var v4schema = schema{4, projects, "create project tables"}

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
    id          SERIAL PRIMARY KEY,
	name		varchar(250) NOT NULL,

    workflow_id integer REFERENCES workflows (id),
	from_status integer REFERENCES statuses (id),
    to_status integer REFERENCES statuses (id)
);

CREATE TABLE IF NOT EXISTS hooks (
    id            SERIAL PRIMARY KEY,
	endpoint      varchar(250) NOT NULL,
	method        varchar(10) NOT NULL,
	body          text,

    transition_id integer REFERENCES transitions (id)
);
`

var v5schema = schema{5, workflows, "create workflow tables"}

const tickets = `
CREATE TABLE IF NOT EXISTS fields (
    id        SERIAL PRIMARY KEY,
    name      varchar(250) UNIQUE NOT NULL,

    data_type varchar(6)
);

CREATE TABLE IF NOT EXISTS ticket_types (
    id        SERIAL PRIMARY KEY,
    name      varchar(250) UNIQUE NOT NULL,
    icon_path varchar(250)
);

CREATE TABLE IF NOT EXISTS tickets (
    id           SERIAL PRIMARY KEY,
	updated_date timestamp DEFAULT current_timestamp,
	created_date timestamp DEFAULT current_timestamp,
    key          varchar(250) UNIQUE NOT NULL CHECK (key <> ''),
    summary      varchar(250) NOT NULL CHECK (summary <> ''),
    description  text NOT NULL,

    project_id     integer REFERENCES projects (id) NOT NULL,
    assignee_id    integer REFERENCES users (id),
    reporter_id    integer REFERENCES users (id) NOT NULL,
    ticket_type_id integer REFERENCES ticket_types (id) NOT NULL,
    status_id      integer REFERENCES statuses (id) NOT NULL
);

CREATE TABLE IF NOT EXISTS field_values (
    id		  SERIAL PRIMARY KEY,
	name	  varchar(250) NOT NULL,
	data_type varchar(6) NOT NULL,

    int_value integer,
	flt_value decimal,
	str_value varchar(250),
	dte_value timestamp,
	opt_value varchar(100),

    ticket_id integer REFERENCES tickets (id),
	field_id  integer REFERENCES fields (id)
);

CREATE TABLE IF NOT EXISTS field_options (
	id SERIAL PRIMARY KEY,
	option varchar(100),

	field_id integer REFERENCES fields (id)
);

CREATE TABLE IF NOT EXISTS field_tickettype_project (
    id             SERIAL PRIMARY KEY,

    field_id       integer REFERENCES fields (id),
    ticket_type_id integer REFERENCES ticket_types (id),
    project_id     integer REFERENCES projects (id)
);
`

var v6schema = schema{6, tickets, "create ticket tables"}

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

const addWorkflowID = `
ALTER TABLE tickets ADD COLUMN workflow_id 
	integer REFERENCES workflows (id);
UPDATE tickets SET (workflow_id) = 1;
`

var v10schema = schema{10, addWorkflowID, "add workflow_id to tickets table"}
