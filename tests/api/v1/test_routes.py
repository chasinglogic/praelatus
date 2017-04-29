import falcon
from praelatus.api.schemas import *


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
        }
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
            'url': '/api/v1/statuses/',
            'new': 'updated-api',
            'schema': StatusSchema
        }
    ]

    for t in tests:
        print('Testing update', t['url'])
        resp = client.post(t['create']['url'],
                           headers=auth_headers,
                           body=t['create']['body'])
        jsn = resp.json
        jsn['name'] = t['new']
        resp = client.put(t['url'] + str(jsn['id']),
                          headers=auth_headers,
                          body=jsn)
        assert resp.status == falcon.HTTP_200
        resp = client.get(t['url'] + str(jsn['id']),
                          headers=auth_headers)
        assert resp.json['name'] == t['new']


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
        }
    ]

    for t in tests:
        print('Testing delete', t['url'])
        resp = client.post(t['create']['url'],
                           headers=auth_headers,
                           body=t['create']['body'])
        jsn = resp.json
        resp = client.delete(t['url'] + str(jsn['id']),
                             headers=auth_headers)
        assert resp.status == falcon.HTTP_200
        resp = client.get(t['url'] + str(jsn['id']),
                          headers=auth_headers)
        assert resp.status == falcon.HTTP_404
