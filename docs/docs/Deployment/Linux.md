In this guide anywhere the commands would differ based on Linux distro
we will provide seperate commands for all supported Linux distros,
otherwise only the required command will be provided.

## Installing Postgres

If you already have Postgres set up skip ahead
to [Installing Praelatus](#installing-praelatus)
or [Installing Redis (Optional)](#installing-redis-optional) if you
plan on using Redis

First install postgres using your package manager:

**Ubuntu**

```text
# apt-get install postgresql
```

**Fedora**

```text
# dnf install postgresql postgresql-server
```

**CentOS / Redhat**

```text
# yum install postgresql postgresql-server
```

Then enable and start the postgres server using systemd:

```text
# systemctl enable postgresql
# systemctl start postgresql
```

Then we need to setup password based authentication switch to the
postgres user then connect to the database:

```text
# su - postgres
$ psql
```

You should then be greeted with a postgres shell that looks something
like this:

```text
psql (9.5.6)
Type "help" for help.

postgres=#
```

Let's create the database for praelatus:

```text
postgres=# CREATE DATABASE praelatus;
CREATE DATABASE
postgres=#
```

Now create an account and give it privileges on the database, **MAKE
SURE TO CHANGE THE PASSWORD IN THIS QUERY**:

```text
postgres=# CREATE ROLE praelatus WITH PASSWORD 'changeme';
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE praelatus TO praelatus;
GRANT
postgres=#
```

Feel free to change the database name, account name, and password to
taste as we will be configuring what praelatus uses later.

You can then quit out of the postgres prompt by running `\q` you're
now reading to move on
to [Installing Praelatus](#installing-praelatus)
or [Installing Redis (Optional)](#installing-redis-optional) as
appropriate.

## Installing Redis

TODO

## Installing Rabbitmq

TODO

## Running Celery

TODO

## Installing Praelatus

For security reasons it's highly recommended that you create a service
account for running the application and configure a reverse proxy to
serve the application. You can create an account to do this with the
following command:

```text
# useradd --create-home --home-dir /opt/praelatus/ --comment "service account for praelatus" praelatus
```

Download the latest Praelatus release
from [here](https://github.com/praelatus/praelatus/releases) then you
extract the tarball and place the files in an appropriate folder, we
recommend using `/opt/praelatus/` and if you created the user as above
you can install it by simply changing to that user:

```text
# su - praelatus
```
Once you have the download link from the release page you can curl it down to
your server, here I'm downloading v0.0.2:

```text
$ curl -sSOL https://github.com/praelatus/praelatus/releases/download/v0.0.2/praelatus-v0.0.2-linux-amd64.tar.gz
```

Then simply extract the tar ball:

```text
$ tar xzf praelatus-v0.0.2-linux-amd64.tar.gz
```

TODO FINISH THE INSTALLATION

You should now have the praelatus REST API and client folder inside of
`/opt/praelatus` at this point you're ready to move on
to [Configuring Praelatus](#configuring-praelatus)

## Configuring Praelatus

Praelatus supports configuration through environment variables as well as a
config.json file which should be located in the same directory as the praelatus
binary. If a config.json file is present it will override all environment
variable based configuration.

The easiest way to get a config.json is using the `config gen` subcommand:

```text
$ praelatus config gen
```

TODO UPDATE CONFIG

Here are all of the possible variables and default values:

| Environment Variable    | Default Value                                                        |
|-------------------------|----------------------------------------------------------------------|
| $PRAELATUS_DB           | postgres://postgres:postgres@localhost:5432/prae_dev?sslmode=disable |
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

This is the url / connection string that praelatus will use for
connecting to the database, `postgres:postgres` is the username /
password to be used when connecting. See
the
[envfile.example](https://raw.githubusercontent.com/praelatus/praelatus/develop/envfile.example) for
alternative ways of setting this and further paramterization.

**PRAELATUS_PORT**

The port that Praelatus will listen for incoming connections on. This can
optionally include an ip to specify which interface to listen on, if just a
port is given we listen on all devices.

For example to listen only on localhost:

`127.0.0.1:8080`

**PRAELATUS_CONTEXT_PATH**

This is the context path that will be prepended to all of Praelatus' routes,
by default it is unset.

## Running Praelatus

Once you have set your configuration appropriately you can now run praelatus.
First make sure the database connection is working using the testdb subcommand:

```text
$ praelatus testdb
```

TODO UPDATE ALL OF THIS

If this comes back with `connection successful!` then we can run the API server
by just running the binary:

```text
$ praelatus serve
```

You will see some logging about migrating the database and will see a
message stating `Ready to Serve Requests!` once you see that you'll be
able to start hitting the API, and the client should be served at
`<your server ip>:8080`

Alternatively you can configure it to run as a systemd service. Here
is an example configuration file:

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

Save that to `/etc/systemd/system/multi-user.target.wants` with the
name `praelatus.service` and you can then enable and start praelatus
using systemd:

```text
# systemctl enable praelatus
# systemctl start praelatus
```

Finally you'll need an http server to use as a reverse proxy and
serving the client, this is MUCH faster than Praelatus serving it
directly you can view the guides for:

- [NGINX](/deployment/advanced/Configuring NGINX as a reverse proxy)
- [Apache](/deployment/advanced/Configuring Apache as a reverse proxy)
