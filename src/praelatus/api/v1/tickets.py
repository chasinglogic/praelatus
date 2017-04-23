"""Contains resources for interacting with tickets."""

import json
import falcon

from praelatus.lib import session
import praelatus.lib.tickets as tickets


class TicketsResource():
    """Handlers for /api/v1/tickets."""

    def on_post(self, req, resp):
        """
        Create a ticket and return the new ticket object.

        Accepts JSON of the form:

        ```json
        {
            "summary": "praelatus is broke",
            "description": "it doesn't work at all",
            "ticket_type": {
                "id": 1,
                "name": "Bug"
            },
            "project": {
                "id": 1,
                "key": "TEST"
            },


            // optional fields

            // If unset it is assumed to be the user who is making
            // the request.
            "reporter": {
                "id": 2
            },

            "assignee": {
                "id": 2
            },

            "labels": ["internal", "duplicate"],

            "fields": [
                {
                    "name": "Story Points",
                    "data_type": "INT",
                    "value": 10000000
                },
                {
                    "name": "Priority",
                    "data_type": "OPT",
                    "value": "HIGH",
                    "options": [
                        "HIGH",
                        "MEDIUM",
                        "LOW"
                    ]
                }
            ]
        }
        ```

        **Notes:**
        - Inside Fields the name field MUST correspond to an existing
          field for this instance otherwise you will recieve an error.
        - Labels are not required to exist if they do not exist the API
          will create them.
        - The fields shown on the nested objects above are the minimum
          fields required to not recieve a HTTP 400 error. You can
          include the full objects in those fields and you will not
          receive an error.

        The API will return a ticket object as defined by
        schema.ticket:

        ```json
        ```
        """
        user = req.context.get('user', None)
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        if jsn.get('reporter') is None:
            jsn['reporter'] = user
        with session() as db:
            db_res = tickets.new(db, actioning_user=user, **jsn)
        resp.body = db_res.to_json()

    def on_get(self, req, resp):
        """
        Return all tickets the current user has access to.

        Accepts the query parameter filter which searches through
        tickets on the instance. This will eventually be replaced with
        a query language but for now supports simple text searching.

        Returns an array of ticket objects as defined by schemas.ticket

        ```json
        [
          {
            "id": 1,
            "created_date": "2017-04-22 09:52:28.252461",
            "updated_date": "2017-04-22 09:52:28.252504",
            "key": "TEST-1",
            "summary": "This is ticket #1",
            "description": "This is a test",
            "reporter": {
              "id": 1,
              "full_name": "Anonymous User",
              "username": "anonymous",
              "email": "anonymous",
              "profile_pic": "https://gravatar.com/avatar/294de3557d9d00b3d2d8a1e6aab028cf",
              "is_admin": false,
              "is_active": false
            },
            "ticket_type": {
              "id": 1,
              "name": "Bug"
            },
            "status": {
              "id": 1,
              "name": "Backlog"
            },
            "project": {
              "id": 1,
              "created_date": "2017-04-22 09:52:28.233556",
              "name": "TEST Project",
              "key": "TEST",
              "homepage": null,
              "icon_url": null,
              "repo": null,
              "lead": {
                "id": 3,
                "full_name": "Test Testerson II",
                "username": "testuser",
                "email": "test@example.com",
                "profile_pic": "https://gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0",
                "is_admin": false,
                "is_active": true
              }
            },
            "fields": [
              {
                "id": 1,
                "name": "Story Points",
                "data_type": "INT",
                "value": 24
              },
              {
                "id": 2,
                "name": "Priority",
                "data_type": "OPT",
                "value": "LOW",
                "options": [
                  "HIGH",
                  "MEDIUM",
                  "LOW"
                ]
              }
            ],
            "labels": [],
            "workflow_id": 1,
            "transitions": [],
            "assignee": {
              "id": 3,
              "full_name": "Test Testerson II",
              "username": "testuser",
              "email": "test@example.com",
              "profile_pic": "https://gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0",
              "is_admin": false,
              "is_active": true
            }
          },
          {
            "id": 10,
            "created_date": "2017-04-22 09:52:28.252461",
            "updated_date": "2017-04-22 09:52:28.252504",
            "key": "TEST-10",
            "summary": "This is ticket #10",
            "description": "This is a test",
            "reporter": {
              "id": 1,
              "full_name": "Anonymous User",
              "username": "anonymous",
              "email": "anonymous",
              "profile_pic": "https://gravatar.com/avatar/294de3557d9d00b3d2d8a1e6aab028cf",
              "is_admin": false,
              "is_active": false
            },
            "ticket_type": {
              "id": 1,
              "name": "Bug"
            },
            "status": {
              "id": 1,
              "name": "Backlog"
            },
            "project": {
              "id": 1,
              "created_date": "2017-04-22 09:52:28.233556",
              "name": "TEST Project",
              "key": "TEST",
              "homepage": null,
              "icon_url": null,
              "repo": null,
              "lead": {
                "id": 3,
                "full_name": "Test Testerson II",
                "username": "testuser",
                "email": "test@example.com",
                "profile_pic": "https://gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0",
                "is_admin": false,
                "is_active": true
              }
            },
            "fields": [
              {
                "id": 19,
                "name": "Story Points",
                "data_type": "INT",
                "value": 13
              },
              {
                "id": 20,
                "name": "Priority",
                "data_type": "OPT",
                "value": "MEDIUM",
                "options": [
                  "HIGH",
                  "MEDIUM",
                  "LOW"
                ]
              }
            ],
            "labels": [],
            "workflow_id": 1,
            "transitions": []
          }
        ]
        ```

        This endpoint never 404's it will return an empty `[]` instead.
        """
        user = req.context['user']
        query = req.params.get('filter', '*')

        with session() as db:
            db_res = tickets.get(db, actioning_user=user, filter=query)

        ticks = []
        for t in db_res:
            ticks.append(t.clean_dict())

        resp.body = json.dumps(ticks)
