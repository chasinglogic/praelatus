+++
date = "2017-01-20T13:11:31-05:00"
title = "REST API Reference"
tags  = [ "rest" ]

+++

# Schema

All access is over `http/https` depending on your setup, if you're using our
hosted version then the access is `https`.

All routes are of the form `/api/<version number>/<plural of model name>`

Blank fields are omitted from the response

All timestamps are returned in ISO 8601 format:

`YYYY-MM-DDTHH:MM:SSZ`

All responses are consistent meaning that besides missing fields a Ticket json
response will be the same no matter how it was requested (i.e. individually by
key, as part of an all tickets request, or as part of a all tickets for project
request.)

All relationships are preloaded and expanded to the full object in keeping with
the above rule. The only exception is comments on a ticket, these are **only**
preloaded when a specific ticket is requested by key with the url param
`?preload=comments`

All errors will return an appropriate http status code and json of the form:

```
{
    "message": "error message"
}
```

When creating a new object that has relationships on the "related" objects only
the id is ever required. For example when creating a team:

```json
{
    "name": "Example Team",
    "lead": {
        "id": 1
    }
    "members": [
        {
            "id": 2
        }
    ]
}
```

Each of the objects in members and lead are user objects, but since we are
creating we only need the id's the returned completed team will have the fully
expanded users in their place

## HTTP Verbs

Praelatus assigns meaning to certain HTTP verbs and only uses a subset of the
available verbs.

|Verb|Description|
|------|------|
|GET|Used for retrieving resources.|
|POST|Used for creating resources.|
|PUT|Used for updating resources. Praelatus always expects the full representation of the object and will reject partial representations.|
|DELETE|Used for deleting resources.|

## Authentication

Praelatus only accepts authentication via a JWT token which can be requested
using the sessions endpoints which will be detailed below.

Once you have the token you can provide it on your requests using either of the
below forms:

```
Authorization: Token jwt_token
```

```
Authorization: Bearer jwt_token
```

# API Resources


## Users

### List Users

You must be a system administrator for this call

`GET /users`

**Example Response:**

```json
[
    {
        "id": 1,
        "username": "foouser",
        "email": "foo@foo.com",
        "full_name": "Foo McFooserson",
        "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
        "is_active": true,
    },
    {
        "id": 2,
        "username": "foouser",
        "email": "foo@foo.com",
        "full_name": "Foo McFooserson",
        "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
        "is_active": true,
    }
]
```

### Get a User

`GET /users/:username`

**Example Response:**

```json
{
    "id": 1,
    "username": "foouser",
    "email": "foo@foo.com",
    "full_name": "Foo McFooserson",
    "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
    "is_active": true,
}
```

### Update a User

`PUT /users/:username`

**Example Request:**

```json
{
    "id": 1,
    "username": "foouser",
    "email": "foo@foo.com",
    "full_name": "My New Full Name",
    "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
    "is_active": true,
}
```

**Example Response:**

```json
Status: 200 OK
```

### Delete a User

`DELETE /users/:username`

**Example Response:**

```json
Status: 200 OK
```

### Create a User

`POST /users`

**Example Request:**

```json
{
    "password": "foopass",
    "username": "foouser",
    "email": "foo@foo.com",
    "full_name": "Foo D. Isgood",
}
```

**Example Response:**

```json
{
    "id": 1,
    "username": "foouser",
    "email": "foo@foo.com",
    "full_name": "Foo D. Isgood",
    "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
    "is_active": true,
}
```

## Sessions

### Create a Session

`POST /sessions`

**Example Request:**

```json
{
    "username": "foouser",
    "password": "foopass"
}
```

**Example Response:**

```json
{
    "token": "jwt_token_here",
    "user": {
        "id": 1,
        "username": "foouser",
        "email": "foo@foo.com",
        "full_name": "Foo D. Isgood",
        "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
        "is_active": true
    } 
}
```

### Refresh a Session

`GET /sessions`

**Example Response:**

```json
3717483f26171b61a4e2154fb37ffbd1
```

## Teams

### Create a Team

`POST /teams`

When creating a team only the id of the users is required, if you do not have
the id for a user you can get it by requesting the object for that user via
[get a user](#users) above.

**Example Request:**

```json
{
    "name": "The A Team",
    "lead": {
        "id": 1,
        "username": "hannibal",
        "full_name": "John Smith"
    },
    "members": [
        {
            "id": 2,
            "username": "faceman",
            "full_name": "Templeton Peck",
        },
        {
            "id": 3,
            "username": "howling_mad",
            "full_name": "H.M. Murdock"
        },
        {
            "id": 4,
            "username": "Mr. T",
            "full_name": "T"
        }
    ]
}
```

**Example Response:**

```json
{
    "id": 1,
    "name": "The A Team",
    "lead": {
        "id": 1,
        "username": "hannibal",
        "full_name": "John Smith"
        "email": "leader@theateam.com",
        "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
        "is_active": true,
    },
    "members": [
        {
            "id": 2,
            "username": "faceman",
            "full_name": "Templeton Peck",
            "email": "face@theateam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        },
        {
            "id": 3,
            "username": "howling_mad",
            "full_name": "H.M. Murdock"
            "email": "mad@theateam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        },
        {
            "id": 4,
            "username": "Mr. T",
            "full_name": "T"
            "email": "mrt@theateam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        }
    ]
}
```

### Get a Team

`GET /teams/:team_name`

**Example Response:**

```json
{
    "id": 1,
    "name": "The A Team",
    "lead": {
        "id": 1,
        "username": "hannibal",
        "full_name": "John Smith"
        "email": "leader@theateam.com",
        "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
        "is_active": true,
    },
    "members": [
        {
            "id": 2,
            "username": "faceman",
            "full_name": "Templeton Peck",
            "email": "face@theateam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        },
        {
            "id": 3,
            "username": "howling_mad",
            "full_name": "H.M. Murdock"
            "email": "mad@theateam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        },
        {
            "id": 4,
            "username": "Mr. T",
            "full_name": "T"
            "email": "mrt@theateam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        }
    ]
}
```

### Get all Teams

`GET /teams`

**Example Response:**

```json
[
    {
        "id": 1,
        "name": "The A Team",
        "lead": {
            "id": 1,
            "username": "hannibal",
            "full_name": "John Smith"
            "email": "leader@theateam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        },
        "members": [
            {
                "id": 2,
                "username": "faceman",
                "full_name": "Templeton Peck",
                "email": "face@theateam.com",
                "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
                "is_active": true,
            },
            {
                "id": 3,
                "username": "howling_mad",
                "full_name": "H.M. Murdock"
                "email": "mad@theateam.com",
                "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
                "is_active": true,
            },
            {
                "id": 4,
                "username": "Mr. T",
                "full_name": "T"
                "email": "mrt@theateam.com",
                "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
                "is_active": true,
            }
        ]
    },
    {
        "id": 2,
        "name": "The B Team",
        "lead": {
            "id": 1,
            "username": "shmanibal",
            "full_name": "Smith John"
            "email": "leader@thebteam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        },
        "members": [
            {
                "id": 2,
                "username": "twoface",
                "full_name": "Peck Templeton",
                "email": "noface@thebteam.com",
                "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
                "is_active": true,
            },
            {
                "id": 3,
                "username": "screaming_sane",
                "full_name": "S.S. Nurdock"
                "email": "sane@thebteam.com",
                "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
                "is_active": true,
            },
            {
                "id": 4,
                "username": "Mr. T",
                "full_name": "T"
                "email": "mrt@thebteam.com",
                "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
                "is_active": true,
            }
        ]
    }
]
```

### Update a Team

`PUT /teams/:name`

**Example Request**:

```json
{
    "id": 1,
    "name": "Not The A Team",
    "lead": {
        "id": 1,
        "username": "hannibal",
        "full_name": "John Smith"
        "email": "leader@theateam.com",
        "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
        "is_active": true,
    },
    "members": [
        {
            "id": 2,
            "username": "faceman",
            "full_name": "Templeton Peck",
            "email": "face@theateam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        },
        {
            "id": 3,
            "username": "howling_mad",
            "full_name": "H.M. Murdock"
            "email": "mad@theateam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        },
        {
            "id": 4,
            "username": "Mr. T",
            "full_name": "T"
            "email": "mrt@theateam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        }
    ]
}
```

**Example Response**:

```json
{
    "id": 1,
    "name": "Not The A Team",
    "lead": {
        "id": 1,
        "username": "hannibal",
        "full_name": "John Smith"
        "email": "leader@theateam.com",
        "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
        "is_active": true,
    },
    "members": [
        {
            "id": 2,
            "username": "faceman",
            "full_name": "Templeton Peck",
            "email": "face@theateam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        },
        {
            "id": 3,
            "username": "howling_mad",
            "full_name": "H.M. Murdock"
            "email": "mad@theateam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        },
        {
            "id": 4,
            "username": "Mr. T",
            "full_name": "T"
            "email": "mrt@theateam.com",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        }
    ]
}
```

### Delete a Team

`DELETE /teams/:name`

**Example Response:**

```json
Status: 200 OK
```

## Projects

### Create a Project

`POST /projects`

**Example Request:**

```json
{
    "key": "EXPL",
    "name": "Example",
    "lead": {
        "id": 1
    }
}
```

**Example Response:**

```json
{
    "id": 1,
    "key": "EXPL",
    "name": "Example",
    "lead": {
        "id": 1
        "username": "foouser",
        "email": "foo@foo.com",
        "full_name": "Foo McFooserson",
        "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
        "is_active": true,
    }
}
```

### Get a Project

`GET /projects/:key`

**Example Response:**

```json
{
    "id": 1,
    "key": "EXPL",
    "name": "Example",
    "lead": {
        "id": 1,
        "username": "foouser",
        "email": "foo@foo.com",
        "full_name": "Foo McFooserson",
        "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
        "is_active": true,
    },
    "homepage": "http://example.com",
    "repo": "https://github.com/example/example",
    "icon_url": "/images/EXPL/icon.png",
}
```

### Get all Projects

`GET /projects/:key`

```json
[
    {
        "id": 1,
        "key": "EXPL",
        "name": "Example",
        "lead": {
            "id": 1,
            "username": "foouser",
            "email": "foo@foo.com",
            "full_name": "Foo McFooserson",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        },
        "homepage": "http://example.com",
        "repo": "https://github.com/example/example",
        "icon_url": "/images/EXPL/icon.png",
    },
    {
        "id": 2,
        "key": "AEXPL",
        "name": "Another Example",
        "lead": {
            "id": 1,
            "username": "foouser",
            "email": "foo@foo.com",
            "full_name": "Foo McFooserson",
            "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
            "is_active": true,
        },
        "homepage": "http://example.com",
        "repo": "https://github.com/example/example",
        "icon_url": "/images/EXPL/icon.png",
    }
]
```

### Update a Project

`PUT /projects/:key`

**Example Request:**

```json
{
    "id": 1,
    "key": "EXPL",
    "name": "Example",
    "lead": {
        "id": 1,
        "username": "foouser",
        "email": "foo@foo.com",
        "full_name": "Foo McFooserson",
        "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
        "is_active": true,
    },
    "homepage": "http://example.com",
    "repo": "https://github.com/example/example",
    "icon_url": "/images/EXPL/icon.png",
}
```

**Example Response:**

```json
{
    "id": 1,
    "key": "EXPL",
    "name": "Example",
    "lead": {
        "id": 1,
        "username": "foouser",
        "email": "foo@foo.com",
        "full_name": "Foo McFooserson",
        "profile_picture": "https://gravatar.com/avatar/51f08d950c617d3d93013d4b9cd998a4",
        "is_active": true,
    },
    "homepage": "http://example.com",
    "repo": "https://github.com/example/example",
    "icon_url": "/images/EXPL/icon.png",
}
```

### Delete a Project

`DELETE /projects/:key`

**Example Response:**

```json
Status: 200 OK
```

## Fields

### Create a Field

`POST /fields`

**Example Request:**

```json
{
    "name": "Example Field",
	"data_type": "OPT", // can be any of INT, STRING, FLOAT, DATE, OPT
	"options": { // Optional, if field is not OPT type do not include
		"options": [ "option one", "option two", "option three" ]
	}
}
```

**Example Response:**

```json
{
	"id": 1,
    "name": "Example Field",
	"data_type":
	"options": {
		"options": [ "option one", "option two", "option three" ]
	}
}
```

### Get a Field

`GET /fields/:id`

**Example Response:**

```json
{
	"id": 1,
    "name": "Example Field",
	"data_type": "OPT",
	"options": {
		"options": [ "option one", "option two", "option three" ]
	}
}
```

### Get all Fields

`GET /fields`

**Example Response:**

```json
[
   {
      "id":1,
      "name":"Story Points",
      "data_type":"INT"
   },
   {
      "id":3,
      "name":"TestField3",
      "data_type":"INT"
   },
   {
      "id":4,
      "name":"TestField4",
      "data_type":"DATE"
   },
   {
      "id":5,
      "name":"Priority",
      "data_type":"OPT",
      "options":{
         "options":[
            "HIGH",
            "MEDIUM",
            "LOW"
         ]
      }
   },
   {
      "id":2,
      "name":"Field Save Test",
      "data_type":"INT"
   }
]
```

### Update a Field

`PUT /fields/:id`

**Example Request:**

```json
{
    "name": "Updated Field",
	"data_type": "INT",
}
```

**Example Response:**

```json
Status: 200 OK
```

### Delete a Field

`DELETE /fields/:id`

**Example Response:**

```json
Status: 200 OK
```

## Tickets

### Create a Ticket

`POST /tickets/:pkey`

**Example Request:**

```json
{
   "summary":"This is a test ticket. #0",
   "description":"No really, this is just a test",
   "fields":[
      {
         "id":1,
         "name":"Story Points",
         "data_type":"INT",
         "value":81
      },
      {
         "id":2,
         "name":"Priority",
         "data_type":"OPT",
         "value":{
            "selected":"HIGH",
            "options":[
               "HIGH",
               "MEDIUM",
               "LOW"
            ]
         }
      }
   ],
   "labels":[
      {
         "id":1,
         "name":"test"
      }
   ],
   "ticket_type":{
      "id":1,
      "name":"Bug"
   },
   "reporter":{
      "id":1,
      "username":"testuser",
      "email":"test@example.com",
      "full_name":"Test Testerson",
      "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
   },
   "assignee":{
      "id":1,
      "username":"testuser",
      "email":"test@example.com",
      "full_name":"Test Testerson",
      "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
   },
   "status":{
      "id":1,
      "name":"Backlog"
   }
}
```

**Example Response:**

```json
{
   "id":1,
   "created_date":"2017-01-05T11:46:20.525186Z",
   "updated_date":"2017-01-10T14:42:25.557443Z",
   "key":"TEST-1",
   "summary":"This is a test ticket. #0",
   "description":"No really, this is just a test",
   "fields":[
      {
         "id":1,
         "name":"Story Points",
         "data_type":"INT",
         "value":81
      },
      {
         "id":2,
         "name":"Priority",
         "data_type":"OPT",
         "value":{
            "selected":"HIGH",
            "options":[
               "HIGH",
               "MEDIUM",
               "LOW"
            ]
         }
      }
   ],
   "labels":[
      {
         "id":1,
         "name":"test"
      }
   ],
   "ticket_type":{
      "id":1,
      "name":"Bug"
   },
   "reporter":{
      "id":1,
      "username":"testuser",
      "email":"test@example.com",
      "full_name":"Test Testerson",
      "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
   },
   "assignee":{
      "id":1,
      "username":"testuser",
      "email":"test@example.com",
      "full_name":"Test Testerson",
      "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
   },
   "status":{
      "id":1,
      "name":"Backlog"
   }
}
```

### Get a Ticket

`GET /tickets/:pkey/:ticket_key`

**Example Response:**

```json
{
   "id":1,
   "created_date":"2017-01-05T11:46:20.525186Z",
   "updated_date":"2017-01-10T14:42:25.557443Z",
   "key":"TEST-1",
   "summary":"This is a test ticket. #0",
   "description":"No really, this is just a test",
   "fields":[
      {
         "id":1,
         "name":"Story Points",
         "data_type":"INT",
         "value":81
      },
      {
         "id":2,
         "name":"Priority",
         "data_type":"OPT",
         "value":{
            "selected":"HIGH",
            "options":[
               "HIGH",
               "MEDIUM",
               "LOW"
            ]
         }
      }
   ],
   "labels":[
      {
         "id":1,
         "name":"test"
      }
   ],
   "ticket_type":{
      "id":1,
      "name":"Bug"
   },
   "reporter":{
      "id":1,
      "username":"testuser",
      "email":"test@example.com",
      "full_name":"Test Testerson",
      "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
   },
   "assignee":{
      "id":1,
      "username":"testuser",
      "email":"test@example.com",
      "full_name":"Test Testerson",
      "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
   },
   "status":{
      "id":1,
      "name":"Backlog"
   }
}
```

### Get all Tickets

`GET /tickets`

**Example Response:**

```json
[
   {
      "id":1202,
      "created_date":"2017-01-10T14:24:02.8079Z",
      "updated_date":"2017-01-10T14:42:01.368603Z",
      "key":"TEST-1202",
      "summary":"This is a test ticket. #1",
      "description":"No really, this is just a test",
      "fields":[
         {
            "id":2403,
            "name":"Story Points",
            "data_type":"INT",
            "value":47
         },
         {
            "id":2404,
            "name":"Priority",
            "data_type":"OPT",
            "value":{
               "options":[
                  "HIGH",
                  "MEDIUM",
                  "LOW"
               ]
            }
         }
      ],
      "labels":[
         {
            "id":1,
            "name":"test"
         }
      ],
      "ticket_type":{
         "id":1,
         "name":"Bug"
      },
      "reporter":{
         "id":1,
         "username":"testuser",
         "email":"test@example.com",
         "full_name":"Test Testerson",
         "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
      },
      "assignee":{
         "id":1,
         "username":"testuser",
         "email":"test@example.com",
         "full_name":"Test Testerson",
         "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
      },
      "status":{
         "id":1,
         "name":"Backlog"
      }
   },
   {
      "id":1203,
      "created_date":"2017-01-10T14:24:02.819095Z",
      "updated_date":"2017-01-10T14:42:01.387784Z",
      "key":"TEST-1203",
      "summary":"This is a test ticket. #2",
      "description":"No really, this is just a test",
      "fields":[
         {
            "id":2405,
            "name":"Story Points",
            "data_type":"INT",
            "value":59
         },
         {
            "id":2406,
            "name":"Priority",
            "data_type":"OPT",
            "value":{
               "options":[
                  "HIGH",
                  "MEDIUM",
                  "LOW"
               ]
            }
         }
      ],
      "labels":[
         {
            "id":1,
            "name":"test"
         }
      ],
      "ticket_type":{
         "id":1,
         "name":"Bug"
      },
      "reporter":{
         "id":1,
         "username":"testuser",
         "email":"test@example.com",
         "full_name":"Test Testerson",
         "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
      },
      "assignee":{
         "id":1,
         "username":"testuser",
         "email":"test@example.com",
         "full_name":"Test Testerson",
         "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
      },
      "status":{
         "id":1,
         "name":"Backlog"
      }
   }
]
```

### Get all Tickets by project

`GET /tickets/:pkey`

**Example Response:**

```json
[
   {
      "id":1202,
      "created_date":"2017-01-10T14:24:02.8079Z",
      "updated_date":"2017-01-10T14:42:01.368603Z",
      "key":"TEST-1202",
      "summary":"This is a test ticket. #1",
      "description":"No really, this is just a test",
      "fields":[
         {
            "id":2403,
            "name":"Story Points",
            "data_type":"INT",
            "value":47
         },
         {
            "id":2404,
            "name":"Priority",
            "data_type":"OPT",
            "value":{
               "options":[
                  "HIGH",
                  "MEDIUM",
                  "LOW"
               ]
            }
         }
      ],
      "labels":[
         {
            "id":1,
            "name":"test"
         }
      ],
      "ticket_type":{
         "id":1,
         "name":"Bug"
      },
      "reporter":{
         "id":1,
         "username":"testuser",
         "email":"test@example.com",
         "full_name":"Test Testerson",
         "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
      },
      "assignee":{
         "id":1,
         "username":"testuser",
         "email":"test@example.com",
         "full_name":"Test Testerson",
         "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
      },
      "status":{
         "id":1,
         "name":"Backlog"
      }
   },
   {
      "id":1203,
      "created_date":"2017-01-10T14:24:02.819095Z",
      "updated_date":"2017-01-10T14:42:01.387784Z",
      "key":"TEST-1203",
      "summary":"This is a test ticket. #2",
      "description":"No really, this is just a test",
      "fields":[
         {
            "id":2405,
            "name":"Story Points",
            "data_type":"INT",
            "value":59
         },
         {
            "id":2406,
            "name":"Priority",
            "data_type":"OPT",
            "value":{
               "options":[
                  "HIGH",
                  "MEDIUM",
                  "LOW"
               ]
            }
         }
      ],
      "labels":[
         {
            "id":1,
            "name":"test"
         }
      ],
      "ticket_type":{
         "id":1,
         "name":"Bug"
      },
      "reporter":{
         "id":1,
         "username":"testuser",
         "email":"test@example.com",
         "full_name":"Test Testerson",
         "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
      },
      "assignee":{
         "id":1,
         "username":"testuser",
         "email":"test@example.com",
         "full_name":"Test Testerson",
         "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
      },
      "status":{
         "id":1,
         "name":"Backlog"
      }
   }
]
```

### Update a Ticket

`PUT /tickets/:pkey/:ticket_key`

**Example Request:**

```json
{
   "id":1,
   "created_date":"2017-01-05T11:46:20.525186Z",
   "updated_date":"2017-01-10T14:42:25.557443Z",
   "key":"TEST-1",
   "summary":"This is a test ticket. #0",
   "description":"No really, this is just a test",
   "fields":[
      {
         "id":1,
         "name":"Story Points",
         "data_type":"INT",
         "value":81
      },
      {
         "id":2,
         "name":"Priority",
         "data_type":"OPT",
         "value":{
            "selected":"HIGH",
            "options":[
               "HIGH",
               "MEDIUM",
               "LOW"
            ]
         }
      }
   ],
   "labels":[
      {
         "id":1,
         "name":"test"
      }
   ],
   "ticket_type":{
      "id":1,
      "name":"Bug"
   },
   "reporter":{
      "id":1,
      "username":"testuser",
      "email":"test@example.com",
      "full_name":"Test Testerson",
      "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
   },
   "assignee":{
      "id":1,
      "username":"testuser",
      "email":"test@example.com",
      "full_name":"Test Testerson",
      "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
   },
   "status":{
      "id":1,
      "name":"Backlog"
   }
}
```

**Example Response:**

```json
Status: 200 OK
```

### Delete a Ticket

`DELETE /tickets/:key`

**Example Response:**

```json
Status: 200 OK
```

## Comments

### Create a Comment

`POST /tickets/:pkey/:ticket_key/comments`

**Example Request:**

```json
{
   "body":"This is the 0 th comment\n\t\t\t\t# Yo Dawg\n\t\t\t\t**I** *heard* you\n\t\t\t\t> like markdown\n\t\t\t\tso I put markdown in your comments",
   "author":{
      "id":1,
      "username":"testuser",
      "email":"test@example.com",
      "full_name":"Test Testerson",
      "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0",
    }
}
```

**Example Response:**

```json
{
   "id":1226,
   "updated_date":"2017-01-05T11:46:21.654079Z",
   "created_date":"2017-01-05T11:46:21.654079Z",
   "body":"This is the 0 th comment\n\t\t\t\t# Yo Dawg\n\t\t\t\t**I** *heard* you\n\t\t\t\t> like markdown\n\t\t\t\tso I put markdown in your comments",
   "author":{
      "id":1,
      "username":"testuser",
      "email":"test@example.com",
      "full_name":"Test Testerson",
      "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0",
    }
}
```

### Update a Comment

`PUT /comments/:id`

**Example Request:**

```json
{
   "id":1226,
   "updated_date":"2017-01-05T11:46:21.654079Z",
   "created_date":"2017-01-05T11:46:21.654079Z",
   "body":"This is the 0 th comment\n\t\t\t\t# Yo Dawg\n\t\t\t\t**I** *heard* you\n\t\t\t\t> like markdown\n\t\t\t\tso I put markdown in your comments",
   "author":{
      "id":1,
      "username":"testuser",
      "email":"test@example.com",
      "full_name":"Test Testerson",
      "profile_picture":"https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0",
    }
}
```

**Example Response:**

```json
Status: 200 OK
```

### Delete a Comment

`DELETE /comments/:id`

**Example Response:**

```json
Status: 200 OK
```

## Labels

### Create a Label

`POST /labels`

**Example Request:**

```json
{
	"name": "example"
}
```

**Example Response:**

```json
{
	"id": 1,
	"name": "example"
}
```

### Get a Label

`GET /labels/:id`

**Example Response:**

```json
{
	"id": 1,
	"name": "example"
}
```

### Get all Labels

`GET /labels`

**Example Response:**

```json
[
   {
      "id":1,
      "name":"test"
   },
   {
      "id":2,
      "name":"SAVE_TEST_LABEL"
   },
   {
      "id":32,
      "name":"duplicate"
   },
   {
      "id":33,
      "name":"wontfix"
   }
]
```

### Update a Label

`PUT /labels/:id`

```json
{
	"id": 1,
	"name": "new_example",
}
```

**Example Response:**

```json
Status: 200 OK
```

### Delete a Label

`DELETE /labels/:id`

**Example Response:**

```json
Status: 200 OK
```

## Statuses

### Create a Status

`POST /statuses`

**Example Request:**

```json
{
	"name": "example"
}
```

**Example Response:**

```json
{
	"id": 1,
	"name": "example"
}
```

### Get a Status

`GET /statuses/:id`

**Example Response:**

```json
{
	"id": 1,
	"name": "example"
}
```

### Get all Statuss

`GET /statuses`

**Example Response:**

```json
[
   {
      "id":1,
      "name":"test"
   },
   {
      "id":2,
      "name":"SAVE_TEST_STATUS"
   }
]
```

### Update a Status

`PUT /statuses/:id`

```json
{
	"id": 1,
	"name": "new_example",
}
```

**Example Response:**

```json
Status: 200 OK
```

### Delete a Status

`DELETE /statuses/:id`

**Example Response:**

```json
Status: 200 OK
```

## Ticket Types


### Create a Ticket Type

`POST /types`

**Example Request:**

```json
{
	"name": "example"
}
```

**Example Response:**

```json
{
	"id": 1,
	"name": "example"
}
```

### Get a Ticket Type

`GET /types/:id`

**Example Response:**

```json
{
	"id": 1,
	"name": "example"
}
```

### Get all Ticket Types

`GET /types`

**Example Response:**

```json
[
   {
      "id":1,
      "name":"test"
   },
   {
      "id":2,
      "name":"SAVE TEST TYPE"
   },
   {
      "id":32,
      "name":"duplicate"
   },
   {
      "id":33,
      "name":"wontfix"
   }
]
```

### Update a Ticket Type

`PUT /types/:id`

```json
{
	"id": 1,
	"name": "not a bug",
}
```

**Example Response:**

```json
Status: 200 OK
```

### Delete a Ticket Type

`DELETE /types/:id`

**Example Response:**

```json
Status: 200 OK
```

## Workflows

Workflows are the most complicated model we have and are made up of
three parts, we manage those all inside one object from a REST 
perspective to get a better idea of what's happening here view our 
[Workflows Explanation]("/workflows")

### Create a Workflow

`POST /workflows/:pkey`


**Example Request:**

```json
{
  "name": "Simple Workflow",
  "transitions": {
    "Backlog": [
      {
        "name": "In Progress",
        "to_status": {
          "name": "In Progress"
        },
        "hooks": null
      }
    ],
    "Done": [
      {
        "name": "ReOpen",
        "to_status": {
          "name": "Backlog"
        },
        "hooks": null
      }
    ],
    "In Progress": [
      {
        "name": "Done",
        "to_status": {
          "name": "Done"
        },
        "hooks": null
      },
      {
        
        "name": "Backlog",
        "to_status": {
          "name": "Backlog"
        },
        "hooks": null
      }
    ]
  }
}
```

**Example Response:**

```json
{
  "id": 1,
  "name": "Simple Workflow",
  "transitions": {
    "Backlog": [
      {
        "id": 4,
        "name": "In Progress",
        "to_status": {
          "id": 2,
          "name": "In Progress"
        },
        "hooks": null
      }
    ],
    "Done": [
      {
        "id": 3,
        "name": "ReOpen",
        "to_status": {
          "id": 1,
          "name": "Backlog"
        },
        "hooks": null
      }
    ],
    "In Progress": [
      {
        "id": 1,
        "name": "Done",
        "to_status": {
          "id": 3,
          "name": "Done"
        },
        "hooks": null
      },
      {
        "id": 2,
        "name": "Backlog",
        "to_status": {
          "id": 1,
          "name": "Backlog"
        },
        "hooks": null
      }
    ]
  }
}
```


### Get a Workflow

`GET /workflows/:id`

```json
**Example Reponse:**

```json
{
  "id": 1,
  "name": "Simple Workflow",
  "transitions": {
    "Backlog": [
      {
        "id": 4,
        "name": "In Progress",
        "to_status": {
          "id": 2,
          "name": "In Progress"
        },
        "hooks": null
      }
    ],
    "Done": [
      {
        "id": 3,
        "name": "ReOpen",
        "to_status": {
          "id": 1,
          "name": "Backlog"
        },
        "hooks": null
      }
    ],
    "In Progress": [
      {
        "id": 1,
        "name": "Done",
        "to_status": {
          "id": 3,
          "name": "Done"
        },
        "hooks": null
      },
      {
        "id": 2,
        "name": "Backlog",
        "to_status": {
          "id": 1,
          "name": "Backlog"
        },
        "hooks": null
      }
    ]
  }
}
```

### Get all Workflows

`GET /workflows`

**Example Response:**

```json
[
  {
    "id": 1,
    "name": "Simple Workflow",
    "transitions": {
      "Backlog": [
        {
          "id": 4,
          "name": "In Progress",
          "to_status": {
            "id": 2,
            "name": "In Progress"
          },
          "hooks": null
        }
      ],
      "Done": [
        {
          "id": 3,
          "name": "ReOpen",
          "to_status": {
            "id": 1,
            "name": "Backlog"
          },
          "hooks": null
        }
      ],
      "In Progress": [
        {
          "id": 1,
          "name": "Done",
          "to_status": {
            "id": 3,
            "name": "Done"
          },
          "hooks": null
        },
        {
          "id": 2,
          "name": "Backlog",
          "to_status": {
            "id": 1,
            "name": "Backlog"
          },
          "hooks": null
        }
      ]
    }
  },
  {
    "id": 2,
    "name": "Simple Workflow-TEST",
    "transitions": {
      "Backlog": [
        {
          "id": 8,
          "name": "In Progress",
          "to_status": {
            "id": 2,
            "name": "In Progress"
          },
          "hooks": null
        }
      ],
      "Done": [
        {
          "id": 7,
          "name": "ReOpen",
          "to_status": {
            "id": 1,
            "name": "Backlog"
          },
          "hooks": null
        }
      ],
      "In Progress": [
        {
          "id": 5,
          "name": "Done",
          "to_status": {
            "id": 3,
            "name": "Done"
          },
          "hooks": null
        },
        {
          "id": 6,
          "name": "Backlog",
          "to_status": {
            "id": 1,
            "name": "Backlog"
          },
          "hooks": null
        }
      ]
    }
  },
  {
    "id": 3,
    "name": "Simple Workflow-TEST-TEST1",
    "transitions": {
      "Backlog": [
        {
          "id": 9,
          "name": "In Progress",
          "to_status": {
            "id": 2,
            "name": "In Progress"
          },
          "hooks": null
        }
      ],
      "Done": [
        {
          "id": 12,
          "name": "ReOpen",
          "to_status": {
            "id": 1,
            "name": "Backlog"
          },
          "hooks": null
        }
      ],
      "In Progress": [
        {
          "id": 10,
          "name": "Done",
          "to_status": {
            "id": 3,
            "name": "Done"
          },
          "hooks": null
        },
        {
          "id": 11,
          "name": "Backlog",
          "to_status": {
            "id": 1,
            "name": "Backlog"
          },
          "hooks": null
        }
      ]
    }
  },
  {
    "id": 4,
    "name": "Simple Workflow-TEST-TEST1-TEST2",
    "transitions": {
      "Backlog": [
        {
          "id": 14,
          "name": "In Progress",
          "to_status": {
            "id": 2,
            "name": "In Progress"
          },
          "hooks": null
        }
      ],
      "Done": [
        {
          "id": 13,
          "name": "ReOpen",
          "to_status": {
            "id": 1,
            "name": "Backlog"
          },
          "hooks": null
        }
      ],
      "In Progress": [
        {
          "id": 15,
          "name": "Done",
          "to_status": {
            "id": 3,
            "name": "Done"
          },
          "hooks": null
        },
        {
          "id": 16,
          "name": "Backlog",
          "to_status": {
            "id": 1,
            "name": "Backlog"
          },
          "hooks": null
        }
      ]
    }
  }
]
```

### Update a Workflow

**This endpoint is not stabilized in any way shape or form.**

### Delete a Workflow

`DELETE /workflows/:id`

**Example Response:**

```json
Status: 200 OK
```
