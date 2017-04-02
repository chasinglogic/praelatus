package migrations

const setupRoleBasedPermissions = `
DROP TABLE permissions;

CREATE TABLE roles(
       id SERIAL PRIMARY KEY,
       name varchar(100) NOT NULL
);

CREATE TABLE user_roles(
       user_id    integer REFERENCES users(id),
       project_id integer REFERENCES projects(id),
       role_id    integer REFERENCES roles(id)
);

INSERT INTO roles (name) VALUES ('Admin');
INSERT INTO roles (name) VALUES ('Contributor');
INSERT INTO roles (name) VALUES ('User');
INSERT INTO roles (name) VALUES ('Anonymous');

CREATE TABLE permissions (
       id SERIAL PRIMARY KEY,
       name varchar(100)
);

INSERT INTO permissions (name) VALUES ('VIEW_PROJECT');
INSERT INTO permissions (name) VALUES ('CREATE_TICKET');
INSERT INTO permissions (name) VALUES ('COMMENT_TICKET');
INSERT INTO permissions (name) VALUES ('REMOVE_COMMENT');
INSERT INTO permissions (name) VALUES ('REMOVE_OWN_COMMENT');
INSERT INTO permissions (name) VALUES ('EDIT_OWN_COMMENT');
INSERT INTO permissions (name) VALUES ('EDIT_COMMENT');
INSERT INTO permissions (name) VALUES ('TRANSITION_TICKET');
INSERT INTO permissions (name) VALUES ('EDIT_TICKET');
INSERT INTO permissions (name) VALUES ('DELETE_TICKET');

CREATE TABLE permission_schemes(
       id SERIAL PRIMARY KEY,
       name varchar(100),
       description varchar(250)
);

CREATE TABLE permission_scheme_permissions(
       role_id integer REFERENCES roles(id),
       scheme_id integer REFERENCES permission_schemes(id),
       perm_id integer REFERENCES permissions(id)
);

CREATE TABLE project_permission_schemes(
       permission_scheme_id integer REFERENCES permission_schemes(id),
       project_id           integer REFERENCES projects(id)
);
`

var v12schema = schema{12, setupRoleBasedPermissions, "setup role based permissions"}
