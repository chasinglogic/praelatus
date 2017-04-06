package migrations

const projects = `
CREATE TABLE IF NOT EXISTS projects (
    id              SERIAL PRIMARY KEY,
    created_date    timestamp DEFAULT current_timestamp,
    name            varchar(250) NOT NULL,
    key		    varchar(40)  NOT NULL UNIQUE,
    repo            varchar(250) DEFAULT '',
    homepage        varchar(250) DEFAULT '',
    icon_url        varchar(250) DEFAULT '',

    lead_id         integer REFERENCES users (id) NOT NULL
);`

var v4schema = schema{4, projects, "create project tables"}
