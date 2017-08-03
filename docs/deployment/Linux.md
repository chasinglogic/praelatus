# Deploying Praelatus on Linux

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
postgres=# ALTER ROLE "praelatus" WITH LOGIN;
```

Feel free to change the database name, account name, and password to
taste as we will be configuring what praelatus uses later.

You can then quit out of the postgres prompt by running `\q` you're
now reading to move on to [Installing Redis](#installing-redis).

# Installing Redis

Per the [Redis quick start guide](https://redis.io/topics/quickstart) it is
recommended to install Redis from source. To do this you have to switch back to
the root account:

if still the postgres account

```bash
$ exit
```

or

```bash
$ su - root
```

Then download and compile Redis:

```bash
# mkdir /opt/redis
# cd /opt/redis
# curl -O http://download.redis.io/redis-stable.tar.gz
# tar xvzf redis-stable.tar.gz
# cd redis-stable
# make
```

**Note:** If you're missing make or gcc you'll need to install gcc and
make via your package manager.

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

- Change supervised to sytemd or v init based on your startup manager
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

ExecStart=/sbin/start-stop-daemon --start --chuid redis:redis --pidfile /var/run/redis/redis.pid --umask 007 --exec /usr/local/bin/redis-server -- /etc/redis/redis.conf
ExecReload=/bin/kill -USR2 $MAINPID

[Install]
WantedBy=multi-user.target
```

Now create the user to run Redis:

```bash
# useradd redis
# chown -R redis:redis /var/redis
```
Now we create the log file:

```bash
# touch /var/log/redis.log
# chown redis:redis /var/log/redis.log
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
# apt-get install rabbitmq-server
```

**Fedora**

```bash
# dnf install rabbitmq-server
```

**CentOS / Redhat**

```bash
# yum install rabbitmq-server
```

**Note:** If you're on Fedora / RHEL / CentOS you can download an RPM
with newer versions of RabbitMQ
from
[their website](https://admin.fedoraproject.org/updates/rabbitmq-server)

Once installed just enable and start the service:

```bash
# systemctl enable rabbitmq-server
# systemctl start rabbitmq-server
```

That's all that's required to get RabbitMQ up and running.

**Note:** Configuring RabbitMQ for remote access is oustide the scope
of this document. As it stands RabbitMQ will be bound to localhost
with a user and password of guest. If you would like to further steps
in configuring
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

Before downloading switch to the service account. Then choose a
download method below.

```bash
# su - praelatus
```

### Downloading using curl

The curl command below will get the latest tarball from our github
releases page. You will then need to extract the contents from that
tarball. Make sure to change the version number accordingly.

```bash
$ curl -s https://api.github.com/repos/praelatus/praelatus/releases/latest | grep browser_download_url | grep -i 'linux' | cut -d '"' -f 4
$ tar xzvf praelatus-<version number>-linux.tar.gz
```

### Downloading using git

Alternatively you can "download" Praelatus using git if you'd like to
do something fancy. Our tip of master is always our latest release and
develop tends to stay fairly stable if you'd like to be on the
bleeding edge. Otherwise skip this step:

```bash
$ git clone https://github.com/praelatus/praelatus .
```

## Setting up Python

At this point you should have a praelatus installation located at
`/opt/praelatus` (if there is not a python script at
`/opt/praelatus/manage.py` then something has gone awry). The first
step is to set up a virtualenv. Virtualenv's are a way that Python
programmers keep app dependencies isolated from the system to prevent
nastiness. You can read more about
them
[here](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/) though
it is not necessary as we will document everything you need to know to
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

**Note:** If you're on CentOS / Redhat replace python3 with python3.6
wherever you see it below.

Now create the virtualenv and activate it:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

If everything goes right you should see a little `(venv)` added to
your git prompt. For example here was my prompt before and after:

```bash
chasinglogic@ubuntu-test:/opt/praelatus$ source venv/bin/activate
(venv) chasinglogic@ubuntu-test:/opt/praelatus$
```

Now install the dependencies required by Praelatus with pip:

```bash
$ pip install -r requirements.txt
```

# Configuring Praelatus

Praelatus supports configuration through environment variables as well
as a config.yaml file in the data directory. Here we will be using the
config.yaml file but if you would like to set up Praelatus in a 12
factor or some other more complex environment you can view the
advanced configuration
docs [here](deployment/advanced/configuration). In this doc we will
only cover the necessary and "most common" configuration done to have
a successfully running Praelatus instance.

Praelatus ships with a management command for generating a config
file. It will use environment variables if set to fill in the
generated config file otherwise it will load the defaults. To generate
this file run the following:

```bash
$ ./manage.py genconfig
```

This will create a file at `$PRAELATUS_DATA_DIR/config.yaml` (The
default will generate a folder `data` in the same directory as the
manage.py script.). For the rest of this section we will be editing
this file so open it with `$ vi data/config.yaml` or `$ nano
data/config.yaml` as appropriate.

## Allowed Hosts

Django by default will only accept requests from domain names in the
"allowed_hosts" section. When the config file is generated it
automatically adds the $HOST of the current machine to this list. For
example mine looks like:

```yaml
allowed_hosts:
- ubuntu-test
```

We need to change this to a list of domains that our instance will be
receiving requests from. If we were running this at
http://test.praelatus.io then we would need to change it to:

```yaml
allowed_hosts:
- test.praelatus.io
```

## Cache and Database

If you used the instructions above to set up Redis, then you don't
need to change the cache settings at all. If you customized the Redis
install at all then you'll have to update the keys accordingly. For
the database settings we primarily care about the username and
password. Set them accordingly (using the password you setup earlier):

```yaml
database:
	default:
		...
		USER: praelatus
		PASS: changeme
		...
```

You can now set up Email notifications below or skip
to [Running Praelatus](#running-praelatus) if you do not want to send
email notifications.

## Email (Optional)

If you would like to enable email notifications in Praelatus you will need
to connect it to an SMTP server. First set up the "sending address"
that Praelatus will use when sending email notifications. This is
whatever your SMTP server requires:

```yaml
email:
	address: praelatus@ubuntu-test
	...
```

Next choose the appropriate backend. For 90% of use cases the default
`django.core.amil.backends.smtp.EmailBackend` is what you will
need. For other use cases please reference
the
[Django Documentation](https://docs.djangoproject.com/en/1.11/topics/email/#email-backends) on
the subject for additional options.

```yaml
email:
	...
	backend: django.core.mail.backends.smtp.EmailBackend
	...
```

Now set the host and port for your SMTP server:

```yaml
email:
	...
	host: localhost
	port: 25
	...
```

If required you can set a username and password:

```yaml
email:
	...
	user: somerusername
	pass: somepassword
	...
```

And finally you can set use_tls if the server users STARTTLS or
use_ssl if the server uses SSL for encryption:

```yalm
email:
	...
	# either
	use_ssl: true
	# or
	use_tls: true
	# but probably not both
	...
```

That's all the configuration required to get Praelatus up and
going. You can leave everything else as the default assuming you
followed this guide!

# Running Praelatus

Before actually running Praelatus we first have to "migrate" the
database to the latest schema. To do this simply run:

```bash
$ ./manage.py migrate
```

Now we need to collect all the static files into a directory from
which we can serve them. This is done with:

```bash
$ ./manage.py collectstatic
```

## Daemonizing Praelatus

Praelatus runs using gunicorn, we have provided a script with the
distribution which automatically configures gunicorn to the
recommended settings based on your server. It is located in
`bin/start-praelatus.sh`, however we recommend setting up a SystemD
service to run Praelatus for you. Our configuration is below:

```toml
[Unit]
Description=Praelatus, an Open Source Ticketing / Bug Tracking System
Requires=postgresql.service
After=network-online.target

[Service]
WorkingDir=/opt/praelatus
Requires=postgresql.service redis.service
After=network-online.target
ExecStart=/opt/praelatus/bin/start-praelatus.sh
User=praelatus

[Install]
WantedBy=multi-user.target
```

Save that to `/etc/systemd/system/praelatus.service`. You can then
enable and start praelatus using systemd:

```bash
# systemctl enable praelatus
# systemctl start praelatus
```

Praelatus will now be running at: localhost:8000

Finally you'll need an http server to use as a reverse proxy and
serving the client, this is MUCH faster than Praelatus serving it
directly. You can view our guides for:

- [NGINX](/deployment/advanced/nginx)
- [Apache](/deployment/advanced/apache)
