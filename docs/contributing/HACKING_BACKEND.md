+++

date = "2017-02-17T23:00:36-05:00"
title = "Hacking on the Backend"
tags = ["contributing"]

+++
# Hacking on the Backend

## What You'll Need

#### Required Dependencies

- [The go compiler](https://golang.org/downloads)
- [The glide package manager](https://github.com/Masterminds/glide)
- [Postgres](https://postgresql.org/download)

#### Optional Dependencies

- [Redis if you are using it (BoltDB is used by default as it requires no external dependencies)](https://redis.io/downoad)

## Getting Started

First you'll need to setup your `$GOPATH` and `git` if you need more 
information on `git` or `$GOPATH` you can click 
[here for git](https://try.github.io/levels/1/challenges/1) and 
[here for go](https://golang.org/doc/install) we will continue assuming you're
using the default `$GOPATH` which comes with recent versions of go.

## Clone the repo

Before you clone the repo you need ro create the proper location in your 
`$GOPATH`. Make the prerequisite directories with this command:

```
mkdir -p $GOPATH/src/github.com/praelatus
```

This is where you'll be doing all of your work, even if your hacking on a fork.
Otherwise the go compiler will not be able to properly import and build the
project. So don't be concerned if you're used to working on go projects in a
folder with your username.

Next let's cd into the directory we just created:

```
cd $GOPATH/src/github.com/praelatus
```

If you haven't forked the project yet you can do so by clicking this 
[link](https://github.com/praelatus/praelatus#fork-destination-box)

Once you've got your fork you can get the code by cloning your fork, the url
will be `https://github.com/{yourusername}/praelatus`. For example my github
username is chasinglogic so if I were to clone my fork the command would be

```
git clone https://github.com/chasinglogic/praelatus
```

You should then have a folder at `$GOPATH/src/github.com/praelatus/praelatus`
let's go ahead and move into that directory:

```
cd $GOPATH/src/github.com/praelatus/praelatus
```

## Setting up the Database

Now that we've got the code the first thing to do is configure our database and
our environment. I'm going to go over the minimal configuration needed to get
hacking here but if you're curious about how to customize / configure this
setup you can [read the source, Luke](https://raw.githubusercontent.com/praelatus/praelatus/develop/config/config.go)
or [read the deployment guides](/deployments/linux)
which cover how to configure the app.

I'm assuming that you've installed Postgres and gotten it running, I won't
cover how to do so here as it's different for every platform / Linux distro but
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
appropriate [deployment guide](/deployments) to 
configure postgres.

**NOTE:** If you don't have a user called postgres because your installation
guide didn't set one up, you can create one by running `CREATE ROLE postgres;` 
in the postgres command shell.

```
postgres=# ALTER ROLE postgres PASSWORD 'postgres';
ALTER ROLE
postgres=# 
```

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
cd $GOPATH/src/github.com/praelatus/praelatus
```

First let's make sure the db is running, if you have praelatus installed you
can run these commands using the installed binary but since we're in the source
tree anyway let's use:

```
go run praelatus.go testdb
```

You should get a message indicating either a success or an error message,
address any issues you see. 

As an aside if you're curious about all of the things praelatus can do run it 
with the help command:

```
go run praelatus.go help
```

Once that's working let's go ahead and seed the database:

```
go run praelatus.go seeddb
```

If required this command will migrate then seed the database with a bunch of
test data. 


## Testing, Building, and Running the Backend

Now that all the prerequisites are met we can actually run the api:

```
go run praelatus.go
```

You should see some output like this:

```
2017/02/19 14:15:03 Starting Praelatus...
2017/02/19 14:15:03 Initializing database...
2017/02/19 14:15:03 Migrating database...
2017/02/19 14:15:03 Prepping API
2017/02/19 14:15:03 Ready to serve requests!
```

At that point the API is listening on localhost:8080 to verify you can navigate
in your browser to http://localhost:8080/api/v1/tickets/TEST-1 and you should 
see a JSON representation of a ticket.

You should also be able to test the backend including integration tests using
the following command:

```
go test $(glide novendor)
```

If you would like to just build a praelatus executable you can simple run:

```
go build
```

This will create an executable named praelatus in the root of the repo.

## Creating a branch for your patch

Before you change any code you should go ahead and make a branch, if working on
a feature name your branch for your feature some-cool-feature, if for a bug fix 
name it fix-description-of-bug. The command you need to run either way is:

```
git checkout -b name-of-your-branch
```

Now you can make all of the changes to implement your feature or fix the bug
you're targetting then simply submit a pull request from your fork / branch to
the main repo's develop branch. If you're not familiar with submitting a pull
request github has some excellent documentation on that
[here](https://help.github.com/articles/creating-a-pull-request/)

