# Introduction

This document will help you get ready to make your first contribution to
Praelatus. It assumes that you have no prior knowledge and are on a unix-like
operating system using Bash or another equivalent shell. If you are not
please modify the commands accordingly for your platform / preferences. If
you have experience developing Django apps on Windows we would love to have
you [Write a guide](https://github.com/praelatus/praelatus/issues/173) for
us!

If you experience any problems with this document please report them
[here](https://github.com/praelatus/docs/issues)

# What You'll Need

- [Docker](https://docs.docker.com/install/) 
- [Docker Compose](https://docs.docker.com/compose/) 
- [Git](https://git-scm.com) 
- A text editor

<span id="checking-out-the-repo"></span>
# Checking out the Repo

First read the Praelatus [Git workflow docs](https://github.com/praelatus/praelatus/blob/master/docs/contributing/git_workflow.md) 
to understand how we manage the project from a VCS perspective before submitting
a PR but if you follow the steps below you will be on the right track.

If you plan on making changes [fork](https://help.github.com/articles/fork-a-repo/) the 
[main repo](https://github.com/praelatus/praelatus). 

You will need to clone the main repo with:

```bash
git clone https://github.com/praelatus/praelatus
```

Then add your fork as a remote with:

```bash
git remote add fork <your-fork-git-url>
```

Now you can make all of the changes to implement your feature or fix the bug
you're targetting then simply submit a pull request from your fork / branch
to the main repo's master branch. If you're not familiar with submitting a
pull request github has some excellent documentation on that
[here](https://help.github.com/articles/creating-a-pull-request-from-a-fork/).

<span id="running-praelatus"></span>
# Running Praelatus

Praelatus is a large web app with many external dependencies. To ease
development and deployment we make use of docker and docker-compose. This
allows us to run a full production simulation environment using one command.
It does slightly complicate some infrequent operations required during
development however, so we provide extensive documentation on how to perform
various tasks using this docker based system. 

Once you have docker and docker-compose installed you can get a fully
operational dev environment running with the following command from the root
of the repository:

```bash 
docker-compose up 
```

Praelatus will now be listening at `localhost:8000`. To access it, simply
navigate to that address in your web browser. As you make changes to
Praelatus will automatically reload them. If you make any changes to models
you will have to generate migrations and apply them separately however. The
section [Migrating Model Changes](#migrating-model-changes) documents
this process. 

<span id="description-of-containers"></span>
# Description of Containers

Praelatus development runs using 7 containers. A `docker container list`
shows the following after starting the app with compose:

```
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                                NAMES
ac1922fa9b69        nginx                  "nginx -g 'daemon of…"   3 days ago          Up 7 seconds        0.0.0.0:8000->80/tcp                 praelatus_nginx_1
4eb59f35443c        praelatus-celery:dev   "celery -A praelatus…"   3 days ago          Up 8 seconds                                             praelatus_celery_1
a2ea50bb0218        praelatus:dev          "/bin/bash /opt/prae…"   3 days ago          Up 8 seconds                                             praelatus_app_1
f7373480d601        rabbitmq               "docker-entrypoint.s…"   3 days ago          Up 9 seconds        4369/tcp, 5671-5672/tcp, 25672/tcp   praelatus_rabbitmq_1
177fa0f04340        postgres               "docker-entrypoint.s…"   3 days ago          Up 9 seconds        5432/tcp                             praelatus_db_1
972851538db9        praelatus_frontend     "/bin/sh -c 'npm run…"   3 days ago          Up 9 seconds                                             praelatus_frontend_1
5b36e1fce544        redis                  "docker-entrypoint.s…"   3 days ago          Up 9 seconds        6379/tcp                             praelatus_redis_1
```

## praelatus_nginx_1

NGINX is used to proxy requests to the gunicorn server as well as serve
static content. Since static assets for Praelatus are built using webpack
these changes get reloaded without using the manage.py runserver command.

## praelatus_celery_1

Praelatus uses celery to run async tasks like sending notifications, emails,
and web hooks. This container is running our celery worker.

## praelatus_app_1

This is the container used to run the actual django application. This container will be needed later if you want to run any manage.py commands. Such as for generating / running database migrations.

## praelatus_db_1

The postgres database used for our development environment.

## praelatus_frontend_1

A node.js container which is running webpack --watch to rebuild static assets like CSS and JavaScript.

## praelatus_redis_1

Redis in memory cache / database used for session storage.

<span id="accessing-shells"></span>
# Accessing Shells Inside of Containers

Docker allows you to "exec" commands in a running container. You can specify
the container by it's name. The container names and purposes are all listed
above. As an example let's say we wanted to generate migrations after changing a
model. First we connect to the running app container:

```bash
docker exec -it praelatus_app_1 /bin/bash
```

> Note: the -it means "interactive" and "pseudo-tty". These flags are
> required to "attach" the bash shell to your current terminal session.

This will give you a root bash prompt from /opt/praelatus from inside the
container:

```bash
python/praelatus master Δ docker exec -it praelatus_app_1 /bin/bash
root@83309a6b5d55:/opt/praelatus#
```

From here you can run any manage.py commands you wish. The default system
python is used (no need for virtualenvs inside a container) and at the time
of this writing is Python 3.6.4 but will update to the latest Python 3
version as they are released. For example to generate migrations and to 
migrate the database you can:

```bash
root@83309a6b5d55:/opt/praelatus# python manage.py makemigrations
No changes detected
root@83309a6b5d55:/opt/praelatus# python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, fields, guardian, labels, notifications, profiles, projects, queries, schemes, sessions, tickets, workflows
Running migrations:
  No migrations to apply.
root@83309a6b5d55:/opt/praelatus#
```

> **Note:** Praelatus automatically migrates and seeds the database (as part
> of docker-compose.sh) when it starts, but not after the container is running.

Interactive django enabled shells also work, this can be very useful for
debugging:

```bash
root@83309a6b5d55:/opt/praelatus# python manage.py shell
Python 3.6.4 (default, Feb 17 2018, 09:32:33)
[GCC 4.9.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from tickets.models import Ticket
>>> Ticket.objects.first()
<Ticket: Ticket object (1)>
>>>
```

Because of how environment variables are passed to the container any
manage.py commands you run will automatically have the correct config in
settings.py, no changes required.

# Accessing a Postgres SQL Prompt

Sometimes it is necessary to have access to the actual postgres shell. This can be accomplished with the following command:

```bash
docker exec -it praelatus_db_1 psql -U postgres -d praelatus
```

# Running Tests

Praelatus uses the Django standard test command for running tests. Connect to
the app container as described in 
[Accessing Shells in Containers](#accessing-shells) and run:

```bash 
python manage.py test
```

Additionally, our CI system runs pylint to make sure that code meets our style
requirements. You can preemptively test this by running pylint from inside the
same container:

```bash
pylint -j 4 apps/* praelatus
```

# Next Steps

Praelatus makes heavy use of [Bootstrap v4](https://v4-alpha.getbootstrap.com/getting-started/introduction/) and the
[Django Web Framework](https://docs.djangoproject.com/en/1.11/) so be sure to
read up on those. If you're looking for something to work on there is always
our [issue tracker](https://github.com/praelatus/praelatus/issues) so pick an
unassigned issue and start cracking!

If you need additional help or have questions of any kind you can reach out
to Mathew Robinson, the project lead, via email: chasinglogic@gmail.com or 
on our Discord server: https://discord.gg/juMkygx

<iframe src="https://discordapp.com/widget?id=422495225286623233&theme=dark"
  width="350" height="500" allowtransparency="true" frameborder="0"></iframe>