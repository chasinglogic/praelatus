package migrations

const setupRoleBasedPermissions = `
DROP TABLE permissions;

CREATE TABLE roles(
    id SERIAL PRIMARY KEY,
    name varchar(100) UNIQUE NOT NULL
);

CREATE TABLE user_roles(
    user_id    integer REFERENCES users(id),
    project_id integer REFERENCES projects(id),
    role_id    integer REFERENCES roles(id),
    PRIMARY KEY(user_id, project_id, role_id)
);

INSERT INTO roles (name) VALUES ('Administrator');
INSERT INTO roles (name) VALUES ('Contributor');
INSERT INTO roles (name) VALUES ('User');
INSERT INTO roles (name) VALUES ('Anonymous');

CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name varchar(100)
);

INSERT INTO permissions (name) VALUES ('VIEW_PROJECT');
INSERT INTO permissions (name) VALUES ('ADMIN_PROJECT');
INSERT INTO permissions (name) VALUES ('CREATE_TICKET');
INSERT INTO permissions (name) VALUES ('COMMENT_TICKET');
INSERT INTO permissions (name) VALUES ('REMOVE_COMMENT');
INSERT INTO permissions (name) VALUES ('REMOVE_OWN_COMMENT');
INSERT INTO permissions (name) VALUES ('EDIT_OWN_COMMENT');
INSERT INTO permissions (name) VALUES ('EDIT_COMMENT');
INSERT INTO permissions (name) VALUES ('TRANSITION_TICKET');
INSERT INTO permissions (name) VALUES ('EDIT_TICKET');
INSERT INTO permissions (name) VALUES ('REMOVE_TICKET');

CREATE TABLE permission_schemes(
    id       SERIAL PRIMARY KEY,
    name     varchar(100) UNIQUE NOT NULL,
    description varchar(250) DEFAULT ''
);

CREATE TABLE permission_scheme_permissions(
    role_id   integer REFERENCES roles(id),
    scheme_id integer REFERENCES permission_schemes(id),
    perm_id   integer REFERENCES permissions(id),
    PRIMARY KEY(scheme_id, perm_id, role_id)
);

CREATE TABLE project_permission_schemes(
    permission_scheme_id  integer REFERENCES permission_schemes(id),
    project_id            integer REFERENCES projects(id),
    PRIMARY KEY(permission_scheme_id, project_id)
);
`

var v12schema = schema{12, setupRoleBasedPermissions, "setup role based permissions"}
