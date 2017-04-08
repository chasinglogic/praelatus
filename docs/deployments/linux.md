+++
date = "2017-01-23T15:23:37-05:00"
title = "Deploy on Linux"
tags = ["deployment"]

+++
# Deploy On Linux

In this guide anywhere the commands would differ based on Linux distro we will
provide seperate commands for all supported Linux distros, otherwise only the
required command will be provided.

## Installing Postgres

If you already have Postgres set up skip ahead to [Installing 
Praelatus](#installing-praelatus) or [Installing Redis 
(Optional)](#installing-redis-optional) if you plan on using Redis

First install postgres using your package manager:

**Ubuntu**
```
# apt-get install postgresql
```
**Fedora**
```
# dnf install postgresql postgresql-server
```
**CentOS / Redhat**
```
# yum install postgresql postgresql-server
```

Then enable and start the postgres server using systemd:

```
# systemctl enable postgresql
# systemctl start postgresql
```

Then we need to setup password based authentication switch to the postgres
user then connect to the database:

```
# su - postgres
$ psql
```

You should then be greeted with a postgres shell that looks something like
this:

```
psql (9.5.6)
Type "help" for help.

postgres=# 
```

Let's create the database for praelatus:

```
postgres=# CREATE DATABASE praelatus;
CREATE DATABASE
postgres=# 
```

Now create an account and give it privileges on the database, **MAKE SURE TO
CHANGE THE PASSWORD IN THIS QUERY**:

```
postgres=# CREATE ROLE praelatus WITH PASSWORD 'changeme';
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE praelatus TO praelatus;
GRANT
postgres=#
```

Feel free to change the database name, account name, and password to taste as
we will be configuring what praelatus uses later.

You can then quit out of the postgres prompt by running `\q` you're now reading
to move on to [Installing Praelatus](#installing-praelatus) or [Installing
Redis (Optional)](#installing-redis-optional) as appropriate.

## Installing Redis (Optional)

If you already have Redis set up or you plan on using the built-in BoltDB which
requires no setup then skip ahead to [Installing Praelatus](#installing-praelatus) 

TODO

## Installing Praelatus

For security reasons it's highly recommended that you create a service account
for running the application and configure a reverse proxy to serve the
application. You can create an account to do this with the following command:

```
# useradd --create-home --home-dir /opt/praelatus/ --comment "service account for praelatus" praelatus
```

As Praelatus is a static binary installation all that is required is that you
extract the tarball and place the files in an appropriate folder, we recommend
using `/opt/praelatus/` and if you created the user as above you can install to
here by simply changing to that user:

```
# su - praelatus
```

You can get the latest release of praelatus for Linux from our 
[releases page](https://github.com/praelatus/praelatus/releases)

Once you have the download link from the release page you can curl it down to
your server, here I'm downloading v0.0.2:

```
$ curl -sSOL https://github.com/praelatus/praelatus/releases/download/v0.0.2/praelatus-v0.0.2-linux-amd64.tar.gz
```

Then simply extract the tar ball:

```
$ tar xzf praelatus-v0.0.2-linux-amd64.tar.gz
```

You should now have the praelatus binary and client folder inside of
`/opt/praelatus` at this point you're ready to move on to [Configuring 
Praelatus](#configuring-praelatus)

## Configuring Praelatus

Praelatus supports configuration through environment variables as well as a
config.json file which should be located in the same directory as the praelatus
binary. If a config.json file is present it will override all environment
variable based configuration. 

The easiest way to get a config.json is using the `config gen` subcommand:

```
$ ./praelatus config gen
```

Here are all of the possible variables and default values:

| Environment Variable    | Default Value                                                        |
|-------------------------|----------------------------------------------------------------------|
| $PRAELATUS_DB           | postgres://postgres:postgres@localhost:5432/prae_dev?sslmode=disable |
| $PRAELATUS_SESSION      | bolt                                                                 |
| $PRAELATUS_SESSION_URL  | sessions.db                                                          |
| $PRAELATUS_PORT         | :8080                                                                |
| $PRAELATUS_CONTEXT_PATH |                                                                      |
| $PRAELATUS_LOGLOCATIONS | stdout                                                               |

The default config.json that is generated from this looks like:

```json
{
        "DBURL": "postgres://postgres:postgres@localhost:5432/prae_dev?sslmode=disable",
        "SessionStore": "bolt"
        "SessionURL": "sessions.db",
        "Port": ":8080",
        "ContextPath": "",
        "LogLocations": [
                "stdout"
        ],
}
```

Here is more in depth explanation of each variable:

**PRAELATUS_DB**

This is the url / connection string that praelatus will use for connecting to 
the database, `postgres:postgres` is the username / password to be used when 
connecting. See the 
[envfile.example](https://raw.githubusercontent.com/praelatus/praelatus/develop/envfile.example) 
for alternative ways of setting this and further paramterization.

**PRAELATUS_SESSION**

This is sets which session store to use, the possible values are:

- bolt
- redis

**PRAELATUS_SESSION_URL**

This is the url / file to be used for storing session data, defaults to a file 
name as boltdb is used by default, if using redis this will need to be a 
connection string for redis.

**PRAELATUS_PORT**

The port that Praelatus will listen for incoming connections on. This can
optionally include an ip to specify which interface to listen on, if just a
port is given we listen on all devices.

For example to listen only on localhost:

`127.0.0.1:8080`

**PRAELATUS_CONTEXT_PATH**

This is the context path that will be prepended to all of Praelatus' routes, 
by default it is unset.

**PRAELATUS_LOGLOCATIONS**

This is a semicolon separated list of locations which to log to, this can be
absolute paths to files where to log or the keywords `stdout` and `syslog`.

Any or all of the options can be used and praelatus will log to all locations
provided

## Running Praelatus

Once you have set your configuration appropriately you can now run praelatus.
First make sure the database connection is working using the testdb subcommand:

```
$ ./praelatus testdb
```

If this comes back with `connection successful!` then we can run the API server 
by just running the binary:

```
$ ./praelatus
```

You will see some logging about migrating the database and will see a message
stating `Ready to Serve Requests!` once you see that you'll be able to start
hitting the API, and the client should be served at `<your server ip>:8080`

You can run praelatus in the background by forking it with `&`:

```
$ ./praelatus &
```

Alternatively you can configure it to run as a systemd service. Here is an
example configuration file:

```toml
[Unit]
Description=Praelatus, an Open Source Ticketing / Bug Tracking System
Requires=postgresql.service
After=network-online.target

[Service]
ExecStart=/opt/praelatus/praelatus
User=praelatus

[Install]
WantedBy=multi-user.target
```

Save that to `/etc/systemd/system/multi-user.target.wants` with the name
`praelatus.service` and you can then enable and start praelatus using systemd:

```
# systemctl enable praelatus
# systemctl start praelatus
```

Finally we recommend using a http server as a reverse proxy, we have guides
for:

- [NGINX](/advanced/nginx)
- [Apache](/advanced/nginx)
