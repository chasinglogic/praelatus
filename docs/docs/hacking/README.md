# Introduction

This document will help you get ready to make your first contribution
to Praelatus. It assumes that you have no prior knowledge and are on a
unix-like operating system using Bash or another equivalent shell. If
you are not please modify the commands accordingly for your platform /
preferences.

If you experience any problems with this document please report
them [here](https://github.com/praelatus/docs/issues)

# What You'll Need

- [The Python Interpreter](https://python.org) Version 3.5 or greater.
- A SQL Database, we
  recommend [Postgres](https://postgresql.org/download)
- [Redis](https://redis.io/downoad)
- [Rabbitmq](https://www.rabbitmq.com/)
- [Git](https://git-scm.com)
- A text editor,
  [Atom](https://atom.io),
  [Emacs](https://www.gnu.org/software/emacs/),
  and [Vim](https://www.vim.org) are all good choices.

# Clone the repo

**NOTE:** We provide all the git commands you'll need to get started
but for a better tutorial on git itself you can
go [here](https://try.github.io/levels/1/challenges/1)

If you don't have a "workspace" we recommend setting one up, you can
create a workspace using the following commands:

```bash
mkdir -P ~/code/
cd ~/code/
```

Now if you haven't forked the project yet you can do so by clicking this
[link](https://github.com/praelatus/praelatus#fork-destination-box)

Once you've got your fork you can get the code by cloning your fork, the url
will be `https://github.com/{yourusername}/praelatus`. For example my github
username is chasinglogic so if I were to clone my fork the command would be

```bash
git clone https://github.com/chasinglogic/praelatus
```

You should then have a folder at `~/code/praelatus` let's go ahead and
move into that directory:

```
cd ~/code/praelatus
```

# Setting up the Virtualenv

In Python development we use virtualenv's to contain our dependencies
and lock in versions of the python interpreter, you can find a great
guide on understanding virtualenvs
[here](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/) but
the commands you need to get started with praelatus are simply:

```bash
# Assuming your OS puts python v3 as python3 (most do)
python3 -m venv venv
source venv/bin/activate
```

Now we can install praelatus and it's dependencies using the following
command:

```bash
python setup.py install
```

Now to install development dependencies we use:

```bash
pip install -r test_requirements.txt
```

# Setting up the Database

Now that we've got the code the first thing to do is configure our
database and our environment. I'm going to go over the minimal
configuration needed to get hacking here but if you're curious about
how to customize / configure this setup you
can [read the source, Luke](https://github.com/praelatus/praelatus)
or [read the deployment guides](/Deployments/Linux) which cover how to
configure the app.

I'm assuming that you've installed Postgres and gotten it running, I won't
cover how to do so here as it's different for every platform / Linux
distro and outside the scope of this document, however
the documentation and downloads can be found
[here](https://postgresql.org/download)

Following whichever guide you did connect to the database as the admin account.
For me that's the user postgres, you should be looking at a prompt similiar to
this:

```
psql (9.5.6)
Type "help" for help.

postgres=#
```

First let's create the database that Praelatus will use by default:

```
postgres=# CREATE DATABASE prae_dev;
CREATE DATABASE
postgres=#
```

Next let's set a password for the postgres account:

**NOTE:** If your database is on the public internet (i.e. not on your laptop
and listening on localhost only) DO NOT USE THIS PASSWORD and read the
appropriate [deployment guide](/Deployments) to
configure postgres.

```
postgres=# ALTER ROLE postgres PASSWORD 'postgres';
ALTER ROLE
postgres=#
```

**NOTE:** If you don't have a user called postgres because your installation
guide didn't set one up, you can create one by running `CREATE ROLE postgres;`
in the postgres command shell. Then re-run the above command.

Finally, let's give the postgres account full control to our new database, this
step may not be necessary for some readers:

```
postgres=# GRANT ALL PRIVILEGES ON DATABASE prae_dev TO postgres;
GRANT
postgres=#
```

Now that's all in place we can quit the shell using `\q` and move on to
actually executing some code!

If you're not there already go to the directory we created earlier:

```
cd ~/code/praelatus
source venv/bin/activate
```

First let's make sure we can connect to the database:

```
praelatus testdb
```

You should get a message indicating either a success or an error message,
address any issues you see.

As an aside if you're curious about all of the things praelatus can do run it
with the help command:

```
praelatus --help
```

Once that's working let's go ahead and migrate then seed the database:

```
praelatus migrate
praelatus seeddb
```

This seeds ("loads") the database with a bunch of test data.

# Testing, Building, and Running the Backend

Now that all the prerequisites are met we can actually run the api:

```
cd src/
gunicorn --reload praelatus:api
```

You should see some output like this:

```
[2017-04-29 11:43:41 -0400] [5586] [INFO] Starting gunicorn 19.7.1
[2017-04-29 11:43:41 -0400] [5586] [INFO] Listening at: http://127.0.0.1:8000 (5586)
[2017-04-29 11:43:41 -0400] [5586] [INFO] Using worker: sync
[2017-04-29 11:43:41 -0400] [5589] [INFO] Booting worker with pid: 5589
```

At that point the API is listening on localhost:8000 to verify you can navigate
in your browser to http://localhost:8000/api/v1/tickets/TEST-1 and you should
see a JSON representation of a ticket.

You should also be able to test the backend including integration tests using
the following command:

```
cd ~/code/praelatus
tox -e all_tests
```

# Creating a branch for your patch

Before you change any code you should go ahead and make a branch, if working on
a feature name your branch for your feature some-cool-feature, if for a bug fix
name it fix-short-description-of-bug. The command you need to run either way is:

```
git checkout develop
git checkout -b name-of-your-branch
```

Now you can make all of the changes to implement your feature or fix the bug
you're targetting then simply submit a pull request from your fork / branch to
the main repo's develop branch. If you're not familiar with submitting a pull
request github has some excellent documentation on that
[here](https://help.github.com/articles/creating-a-pull-request/)
