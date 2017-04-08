package migrations

const tickets = `
CREATE TABLE IF NOT EXISTS fields (
    id   SERIAL PRIMARY KEY,
    name varchar(250) UNIQUE NOT NULL,

    data_type varchar(6) NOT NULL
);

CREATE TABLE IF NOT EXISTS ticket_types (
    id        SERIAL PRIMARY KEY,
    name      varchar(250) UNIQUE NOT NULL,
    icon_path varchar(250) DEFAULT ''
);

CREATE TABLE IF NOT EXISTS tickets (
    id           SERIAL PRIMARY KEY,
    updated_date timestamp DEFAULT current_timestamp,
    created_date timestamp DEFAULT current_timestamp,
    key          varchar(250) UNIQUE NOT NULL CHECK (key <> ''),
    summary      varchar(250) NOT NULL CHECK (summary <> ''),
    description  text DEFAULT '',

    project_id     integer REFERENCES projects (id) NOT NULL,
    assignee_id    integer REFERENCES users (id),
    reporter_id    integer REFERENCES users (id) NOT NULL,
    ticket_type_id integer REFERENCES ticket_types (id) NOT NULL,
    status_id      integer REFERENCES statuses (id) NOT NULL
);

CREATE TABLE IF NOT EXISTS field_values (
    id        SERIAL PRIMARY KEY,
    name      varchar(250) NOT NULL,
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
    option varchar(100) NOT NULL,

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
