package migrations

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
