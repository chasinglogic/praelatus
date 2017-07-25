In this guide anywhere the commands would differ based on Linux distro
we will provide seperate commands for all supported Linux distros,
otherwise only the required command will be provided.

# Installing Postgres

If you already have Postgres set up skip ahead
to [Installing Redis](#installing-redis). 

First install postgres using your package manager:

**Ubuntu**

```bash
# apt-get install postgresql
```

**Fedora**

```bash
# dnf install postgresql postgresql-server
```

**CentOS / Redhat**

```bash
# yum install postgresql postgresql-server
```

Then enable and start the postgres server using systemd:

```bash
# systemctl enable postgresql
# systemctl start postgresql
```

Then we need to setup password based authentication switch to the
postgres user then connect to the database:

```bash
# su - postgres
$ psql
```

You should then be greeted with a postgres shell that looks something
like this:

```bash
psql (9.5.6)
Type "help" for help.

postgres=#
```

Let's create the database for praelatus:

```bash
postgres=# CREATE DATABASE praelatus;
CREATE DATABASE
postgres=#
```

Now create an account and give it privileges on the database, **MAKE
SURE TO CHANGE THE PASSWORD IN THIS QUERY**:

```bash
postgres=# CREATE ROLE praelatus WITH PASSWORD 'changeme';
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE praelatus TO praelatus;
GRANT
postgres=#
```

Feel free to change the database name, account name, and password to
taste as we will be configuring what praelatus uses later.

You can then quit out of the postgres prompt by running `\q` you're
now reading to move on to [Installing Redis](#installing-redis).

# Installing Redis

Per the [Redis quick start guide](https://redis.io/topics/quickstart) 
it is recommended to install Redis from source. To do this simply run the 
following commands:

```bash
# Download the source tarball
$ curl -O http://download.redis.io/redis-stable.tar.gz

# Extract the contents
$ tar xvzf redis-stable.tar.gz

# Compile Redis
$ cd redis-stable
$ make
```

**Note:** If you're missing make or gcc you'll need to install gcc and make via 
your package manager.


You'll need to be root to finish installing Redis simply run:

```bash
# make install
```

This will copy the Redis binaries to /usr/local/bin so it is in your `$PATH`.
Next we will "productionalize" and secure Redis. Let's start by creating
directories for the configuration and data of Redis.

```bash
# mkdir /etc/redis
# mkdir /var/redis
```

**Note:** The following commands assume you're still in the directory that you 
compiled Redis in.

```bash
# cp redis.conf /etc/redis/main.conf
# mkdir /var/redis/main
```

Make the following changes to `/etc/redis/main.conf`:

- Change supervised to yes
- Change dir to `/var/redis/main`
- Change logfile to `/var/log/redis.log`
- Change pidfile to `/var/run/redis_main.pid`

Next create a file at `/etc/systemd/system/redis.service` and write the following
to it

```
[Unit]
Description=Redis Datastore Server
After=network.target

[Service]
Type=forking
PIDFile=/var/run/redis/redis_main.pid
ExecStartPre=/bin/mkdir -p /var/run/redis
ExecStartPre=/bin/chown redis:redis /var/run/redis

ExecStart=/sbin/start-stop-daemon --start --chuid redis:redis --pidfile /var/run/redis/redis.pid --umask 007 --exec /usr/bin/redis-server -- /etc/redis/redis.conf
ExecReload=/bin/kill -USR2 $MAINPID

[Install]
WantedBy=multi-user.target
```

Now create the user to run Redis:

```bash
# useradd redis
# chown -R /var/redis
```

Finally enable and start the Redis service:

```bash
# systemctl enable redis
# systemctl start redis
```

**Note:** Most modern Linux distributions use SystemD now. If you're using a 
distribution on SysV Init or some other init system the Redis quick start guide
has [pretty good docs](https://redis.io/topics/quickstart#installing-redis-more-properly) 
on how to set that up.

You're almost there! You can set up Rabbitmq for async messaging in Praelatus
but if you would rather not [install rabbitmq](#installing-rabbitmq) you can
move on to [installing Praelatus](#installing-praelatus). Celery can use Redis
as a messaging backend however it is not recommended (and not supported).


**Note:** This guide leaves Redis configured without a password. Praelatus does
support authenticated instances of Redis but configuring it is outside the
scope of this document. Redis with this configuration however is NOT exposed
to the internet. If you feel the need to add a password to Redis please consult
[Redis' documentation](https://redis.io)

# Installing Rabbitmq

Luckily rabbitmq is in most major distro's repositories so installing is simply
a matter of the appropriate command:

**Ubuntu**

```bash
# apt-get install rabbitmq
```

**Fedora**

```bash
# dnf install rabbitmq-server
```

**CentOS / Redhat**

```bash
# yum install rabbitmq-server
```

**Note:** If you're on Fedora / RHEL / CentOS you can download an RPM with newer
versions of RabbitMQ from 
[their website](https://admin.fedoraproject.org/updates/rabbitmq-server)

Once installed just enable and start the service:

```bash
# systemctl enable rabbitmq-server
# systemctl start rabbitmq-server
```

That's all that's required to get RabbitMQ up and running.

**Note:** Configuring RabbitMQ for remote access is oustide the scope of this 
document. As it stands RabbitMQ will be bound to localhost with a user and 
password of guest. If you would like to further steps in configuring 
RabbitMQ [please consult their website](https://rabbitmq.com)


# Installing Praelatus

For security reasons it's highly recommended that you create a service
account for running the application and configure a reverse proxy to
serve the application. You can create an account to do this with the
following command:

```bash
# useradd --create-home --home-dir /opt/praelatus/ --comment "service account for praelatus" praelatus
```

## Downloading Praelatus

Before downloading switch to the service account. Then choose a download method
below.

```bash
# su - praelatus
```

### Downloading using curl

The curl command below will get the latest tarball from our github releases 
page. You will then need to extract the contents from that tarball. Make sure
to change the version number accordingly.

```bash
$ curl -s https://api.github.com/repos/praelatus/praelatus/releases/latest | grep browser_download_url | grep -i 'linux' | cut -d '"' -f 4
$ tar xzvf praelatus-<version number>-linux.tar.gz
```

### Downloading using git 

Alternatively you can "download" Praelatus using git if you'd like to do 
something fancy. Our tip of master is always our latest release and develop
tends to stay fairly stable if you'd like to be on the bleeding edge. Otherwise
skip this step:

```bash
$ git clone https://github.com/praelatus/praelatus .
```

```bash
$ tar xzf praelatus-v0.0.2-linux-amd64.tar.gz
```

## Setting up Python

At this point you should have a praelatus installation located at 
`/opt/praelatus` (if there is not a python script at 
`/opt/praelatus/manage.py` then something has gone awry). The first step is to
set up a virtualenv. Virtualenv's are a way that Python programmers keep app
dependencies isolated from the system to prevent nastiness. You can read more
about them [here](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/)
though it is not necessary as we will document everything you need to know to
get Praelatus up and running here.

First install python3 if not already installed:

**Ubuntu**

```bash
# apt-get install python3 python3-dev
```

**Fedora**

```bash
# dnf install python3 python3-devel
```

**CentOS / Redhat**

```bash
# yum install yum-utils
# yum install https://centos7.iuscommunity.org/ius-release.rpm
# yum install python36u
```

**Note:** If you're on CentOS / Redhat replace python3 with python3.6 wherever
you see it below.

Now create the virtualenv and activate it:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

If everything goes right you should see a little `(venv)` added to your git 
prompt. For example here was my prompt before and after:

```bash
chasinglogic@ubuntu-test:/opt/praelatus$ source venv/bin/activate
(venv) chasinglogic@ubuntu-test:/opt/praelatus$
```

Now install the dependencies required by Praelatus with pip:

```bash
$ pip install -r requirements.txt
```

# Configuring Praelatus

Praelatus supports configuration through environment variables as well as a
config.json file which should be located in the same directory as the praelatus
binary. If a config.json file is present it will override all environment
variable based configuration.

The easiest way to get a config.json is using the `config gen` subcommand:

```bash
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
		"ConbashPath": "",
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

This is the conbash path that will be prepended to all of Praelatus' routes,
by default it is unset.

# Running Praelatus

Once you have set your configuration appropriately you can now run praelatus.
First make sure the database connection is working using the testdb subcommand:

```bash
$ praelatus testdb
```

TODO UPDATE ALL OF THIS

If this comes back with `connection successful!` then we can run the API server
by just running the binary:

```bash
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

```bash
# systemctl enable praelatus
# systemctl start praelatus
```

Finally you'll need an http server to use as a reverse proxy and
serving the client, this is MUCH faster than Praelatus serving it
directly you can view the guides for:

- [NGINX](/deployment/advanced/Configuring NGINX as a reverse proxy)
- [Apache](/deployment/advanced/Configuring Apache as a reverse proxy)
