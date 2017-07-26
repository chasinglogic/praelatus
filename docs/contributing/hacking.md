# Introduction

This document will help you get ready to make your first contribution
to Praelatus. It assumes that you have no prior knowledge and are on a
unix-like operating system using Bash or another equivalent shell. If
you are not please modify the commands accordingly for your platform /
preferences. If you have experience developing Django apps on Windows we would
love to have you
[Write a guide](https://github.com/praelatus/praelatus/issues/173) for us!

If you experience any problems with this document please report
them [here](https://github.com/praelatus/docs/issues)

# What You'll Need

- [A Python Interpreter](https://python.org) Version 3.5 or greater.
- [Redis](https://redis.io/downoad)
- [Git](https://git-scm.com)
- A text editor. [Atom](https://atom.io),
  [Emacs](https://www.gnu.org/software/emacs/), and
  [Neovim](https://www.neovim.io) are all good choices.

# Installing Prerequisites

Here we will document a "quick start" way to set up the prerequisites for
running Praleatus on your laptop in development mode. It's worth noting if
you're looking for more comprehensive docs on these two tools then you should
visit their websites linked above.

## Installing Python

**Ubuntu**

```bash
sudo apt install python3 python3-dev python3-pip python3-wheel
```

**Fedora**

```bash
sudo dnf install python3 python3-devel
```

**Mac OSX**

This assumes you have homebrew installed. If not you can install it
[here](https://brew.sh/)

```bash
brew install python3
```

**Windows**

Get the latest release download from
[here](https://www.python.org/downloads/windows/) click the "Latest Python 3
Release" at the top of the page. Scroll to the bottom of that page and there
will be a table titled "Files". Click the link for "Windows x86-64 executable
installer", this will download an `exe` installer which you can use to set up
python.

## Installing Redis

**Ubuntu**

```bash
sudo apt install redis-server
sudo systemctl start redis-server
```

**Fedora**

```bash
sudo dnf install redis
sudo systemctl start redis
```

**Mac OSX**

Again this assumes you have homebrew installed. If not you can install it
[here](https://brew.sh/)

```bash
brew install redis
# Run in this terminal with
redis-server
# Or if you have brew services installed
brew services start redis
```

**Windows**

Getting Redis on windows is a bit more complicated and you have a couple of
options:

- You can get Redis as a Vagrant VM
[here](https://github.com/ServiceStack/redis-windows)
- You can try one of the various "Redis for Windows" binaries out there but we
  don't feel comfortable recommending any of them as it's a changing and poorly
  documented landscape.
- Finally, you can simply use a different caching mechanism for Praelatus via
  modifying the settings.py as described
  [here](https://docs.djangoproject.com/en/1.11/topics/cache/#local-memory-caching)

  **Note:** Please do not submit PR's with this change to settings.py to
  Praelatus you can simply not stage the settings.py or you can stage it in
  hunks with git.

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

```bash
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

Now we can install praelatus' dependencies using the following
command:

```bash
pip install -r requirements.txt
```

And for running tests we'll need an additional tool called tox:

```bash
pip install tox
```

# Setting up the Database

Now that we've got the code the first thing to do is configure our database and
our environment. I'm going to go over the minimal configuration needed to get
hacking here but if you're curious about how to customize / configure this
setup you can [read the source,
Luke](https://github.com/praelatus/praelatus/blob/master/praelatus/settings.py)
or [read the deployment guides](/deployment/) which cover how to
configure the app.

First we need to generate a config file. You can do so using the management
command genconfig:

```bash
./manage.py genconfig
```

This will create a directory called `data/` inside you will see two files
`.secret_key` which you can leave alone and `config.yaml` which you need to
open in a text editor and make the some edits.

First remove these lines:

```yaml
allowed_hosts:
- localhost
```

Then change this line from false to true:

```yaml
debug: false
```

to

```yaml
debug: true
```

Change the email backend from `django.core.mail.backends.smtp.EmailBackend` to:

```yaml
email:
  ...
  backend: django.core.mail.backends.console.EmailBackend
  ...
```

Change `mq_server` to:

```yaml
mq_server: redis://127.0.0.1:6379/0
```

Finally change the database settings to this (Note: just remove everything
under "default" and replace it with this):

```yaml
database:
    default:
        ENGINE: django.db.backends.sqlite3
        NAME: db.sqlite3
```

Now we can "migrate" the database. When dealing with SQL databases you have to
make tables and adjust columns to match your data model. Migrations apply these
schema changes in order so the Database is in an expected state. For more info
here are the [Django
docs](https://docs.djangoproject.com/en/1.11/topics/migrations/) on the
subject. To perform the migration run the following command:

```bash
./manage.py migrate
```

Now we have added a command to management that allows us to "seed" the database
with a bunch of test data which is really useful for playing with features. To
fill the database run this command:

```bash
./manage.py seeddb
```

This will create workflow, a couple custom fields, a test project, about 100
tickets with some comments, and two users "testadmin" (A system administrator)
and "testuser" (A regular user). The password for both accounts is "test" so
you can test features that require permissions. Now your development
environment is all set up you can move on to writing some code!

# Testing, Building, and Running Praelatus

To run praelatus in development mode you use the standard Django `runserver`:

```bash
./manage.py runserver
```

Praelatus will now be listening at `localhost:8000` to access it simply
navigate to that address in your web browser. As you make changes to Praelatus
runserver will automatically reload them. If you make any changes to models you
will have to generate migrations and apply them separately however. To do so
you can use the following commands:

```bash
./manage.py makemigrations
./manage.py migrate
```

Praelatus uses `tox` to run tests on our CI system. If `tox` reports a failure
we won't merge the PR so to run it locally (which is much faster than waiting
on Travis) you just have to run:

```bash
tox
```

This will lint your code and run the tests, if any failures are reported it
will show you output that tells you where to look. Address issues as necessary.

# Creating a branch for your work

First read the Praelatus [Git workflow docs](contributing/git_workflow) to
understand how we manage the project from a VCS perspective before submitting a
PR but if you follow the steps below you will be on the right track.

Before you change any code you should go ahead and make a branch, if working on
a feature name your branch for your feature some-cool-feature, if for a bug fix
name it fix-short-description-of-bug. The command you need to run either way is:

```bash
git checkout master
git checkout -b name-of-your-branch
```

Now you can make all of the changes to implement your feature or fix the bug
you're targetting then simply submit a pull request from your fork / branch to
the main repo's master branch. If you're not familiar with submitting a pull
request github has some excellent documentation on that
[here](https://help.github.com/articles/creating-a-pull-request/)


# Next Steps

Praelatus makes heavy use of
[Bootstrap v4](https://v4-alpha.getbootstrap.com/getting-started/introduction/)
and the [Django Web Framework](https://docs.djangoproject.com/en/1.11/) so be
sure to read up on those. If you're looking for something to work on there is
always our [issue tracker](https://github.com/praelatus/praelatus/issues) so
pick an unassigned issue and start cracking!

If you need additional help or have questions of any kind you can reach out to
us via email [team@praelatus.io](mailto:team@praelatus.io) or on our [mailing
lists](http://mail.praelatus.io)
