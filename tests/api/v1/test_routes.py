import falcon
from praelatus.app.api.schemas import *


def test_create_and_read_endpoints(client, auth_headers):
    tests = [
        {
            'url': '/api/v1/labels',
            'method': 'GET',
            'validator': lambda x: len(x.json) > 1 and x.json[0]['name'] is not None
        },
        {
            'url': '/api/v1/labels/1',
            'method': 'GET',
            'schema': LabelSchema
        },
        {
            'url': '/api/v1/labels',
            'method': 'POST',
            'body': {'name': 'test-api', 'data_type': 'STRING'},
            'schema': LabelSchema
        },
        {
            'url': '/api/v1/fields',
            'method': 'GET',
            'validator': lambda x: len(x.json) > 1 and x.json[0]['name'] is not None
        },
        {
            'url': '/api/v1/fields/1',
            'method': 'GET',
            'schema': FieldSchema
        },
        {
            'url': '/api/v1/fields',
            'method': 'POST',
            'body': {'name': 'test-api', 'data_type': 'STRING'},
            'schema': FieldSchema
        },
        {
            'url': '/api/v1/ticketTypes',
            'method': 'GET',
            'validator': lambda x: len(x.json) > 1 and x.json[0]['name'] is not None
        },
        {
            'url': '/api/v1/ticketTypes/1',
            'method': 'GET',
            'schema': TicketTypeSchema
        },
        {
            'url': '/api/v1/ticketTypes',
            'method': 'POST',
            'body': {'name': 'TestAPI'},
            'schema': TicketTypeSchema
        },
        {
            'url': '/api/v1/statuses',
            'method': 'GET',
            'validator': lambda x: len(x.json) > 1 and x.json[0]['name'] is not None
        },
        {
            'url': '/api/v1/statuses/1',
            'method': 'GET',
            'schema': StatusSchema
        },
        {
            'url': '/api/v1/statuses',
            'method': 'POST',
            'body': {'name': 'TestAPI'},
            'schema': StatusSchema
        },
        {
            'url': '/api/v1/workflows',
            'method': 'GET',
            'validator': lambda x: len(x.json) > 0 and x.json[0]['name'] is not None
        },
        {
            'url': '/api/v1/workflows/1',
            'method': 'GET',
            'schema': WorkflowSchema
        },
        {
            'url': '/api/v1/workflows',
            'method': 'POST',
            'body': {'name': 'TestAPI'},
            'schema': WorkflowSchema
        },
        {
            'url': '/api/v1/tickets/TEST-5/comments',
            'method': 'GET',
            'validator': lambda x: (len(x.json) > 0 and
                                    x.json[0]['author'] is not None and
                                    x.json[0]['body'] is not None)
        },
        {
            'url': '/api/v1/tickets/TEST-5/comments',
            'method': 'POST',
            'body': {
                'author': {'id': 2},
                'body': 'TestAPI'
            },
            'schema': CommentSchema
        },
        {
            'url': '/api/v1/projects',
            'method': 'GET',
            'validator': lambda x: len(x.json) > 0 and x.json[0]['name'] is not None
        },
        {
            'url': '/api/v1/projects/TEST',
            'method': 'GET',
            'schema': ProjectSchema
        },
        {
            'url': '/api/v1/projects',
            'method': 'POST',
            'body': {
                'lead': {
                    'id': 2,
                    'username': 'testadmin',
                    'email': 'test@example.com',
                    'full_name': 'Test Testerson',
                },
                'key': 'TESTAPI',
                'name': 'TestAPI'
            },
            'schema': ProjectSchema
        },
    ]

    for t in tests:
        print('Testing', t['method'], t['url'])
        resp = client.fake_request(t['url'], method=t['method'],
                                   headers=auth_headers, body=t.get('body'))
        print(resp.status_code)
        print(resp.json)
        print(resp.body)
        schema = t.get('schema')
        if schema:
            schema.validate(resp.json)

        validator = t.get('validator')
        if validator:
            valid = validator(resp)
            assert valid


def test_update_endpoints(client, auth_headers):
    tests = [
        {
            'create': {
                'url': '/api/v1/fields',
                'body': {
                    'name': 'test-update-api',
                    'data_type': 'STRING'
                }
            },
            'field': 'name',
            'url': '/api/v1/fields/',
            'new': 'updated-api',
            'schema': FieldSchema
        },
        {
            'create': {
                'url': '/api/v1/labels',
                'body': {
                    'name': 'test-update-api'
                }
            },
            'field': 'name',
            'url': '/api/v1/labels/',
            'new': 'updated-api',
            'schema': LabelSchema
        },
        {
            'create': {
                'url': '/api/v1/workflows',
                'body': {
                    'name': 'test-update-api'
                }
            },
            'field': 'name',
            'url': '/api/v1/workflows/',
            'new': 'updated-api',
            'schema': WorkflowSchema
        },
        {
            'create': {
                'url': '/api/v1/ticketTypes',
                'body': {
                    'name': 'test-update-api'
                }
            },
            'field': 'name',
            'url': '/api/v1/ticketTypes/',
            'new': 'updated-api',
            'schema': TicketTypeSchema
        },
        {
            'create': {
                'url': '/api/v1/statuses',
                'body': {
                    'name': 'test-update-api'
                }
            },
            'field': 'name',
            'url': '/api/v1/statuses/',
            'new': 'updated-api',
            'schema': StatusSchema
        },
        {
            'create': {
                'url': '/api/v1/projects',
                'body': {
                    'key': 'UPDATEAPI',
                    'name': 'test update api',
                    'lead': {
                        'id': 2,
                        'username': 'testadmin',
                        'email': 'test@example.com',
                        'full_name': 'Test Testerson',
                    }
                }
            },
            'field': 'name',
            'select': 'key',
            'new': 'updated api',
            'url': '/api/v1/projects/',
            'schema': ProjectSchema
        }
    ]

    for t in tests:
        print('Testing update', t['url'])
        resp = client.post(t['create']['url'],
                           headers=auth_headers,
                           body=t['create']['body'])
        jsn = resp.json
        jsn[t['field']] = t['new']
        resp = client.put(t['url'] + str(jsn[t.get('select', 'id')]),
                          headers=auth_headers,
                          body=jsn)
        assert resp.status == falcon.HTTP_200
        resp = client.get(t['url'] + str(jsn[t.get('select', 'id')]),
                          headers=auth_headers)
        assert resp.json[t['field']] == t['new']


def test_delete_endpoints(client, auth_headers):
    tests = [
        {
            'create': {
                'url': '/api/v1/fields',
                'body': {
                    'name': 'test-delete-api',
                    'data_type': 'STRING'
                }
            },
            'url': '/api/v1/fields/',
        },
        {
            'create': {
                'url': '/api/v1/labels',
                'body': {
                    'name': 'test-delete-api'
                }
            },
            'url': '/api/v1/labels/',
        },
        {
            'create': {
                'url': '/api/v1/workflows',
                'body': {
                    'name': 'test-delete-api'
                }
            },
            'url': '/api/v1/workflows/',
        },
        {
            'create': {
                'url': '/api/v1/ticketTypes',
                'body': {
                    'name': 'test-delete-api'
                }
            },
            'url': '/api/v1/ticketTypes/',
        },
        {
            'create': {
                'url': '/api/v1/statuses',
                'body': {
                    'name': 'test-delete-api'
                }
            },
            'url': '/api/v1/statuses/',
        },
        {
            'create': {
                'url': '/api/v1/projects',
                'body': {
                    'key': 'DELETEAPI',
                    'lead': {
                        'id': 2,
                        'username': 'testadmin',
                        'email': 'test@example.com',
                        'full_name': 'Test Testerson',
                    },
                    'name': 'test delete api'
                }
            },
            'field': 'key',
            'url': '/api/v1/projects/',
        }
    ]

    for t in tests:
        print('Testing delete', t['url'])
        resp = client.post(t['create']['url'],
                           headers=auth_headers,
                           body=t['create']['body'])
        jsn = resp.json
        resp = client.delete(t['url'] + str(jsn[t.get('field', 'id')]),
                             headers=auth_headers)
        assert resp.status == falcon.HTTP_200
        resp = client.get(t['url'] + str(jsn[t.get('field', 'id')]),
                          headers=auth_headers)
        assert resp.status == falcon.HTTP_404
