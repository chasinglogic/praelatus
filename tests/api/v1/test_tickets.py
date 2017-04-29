import falcon
from praelatus.api.schemas import TicketSchema
from praelatus.api.schemas import CommentSchema


def test_crud_ticket_endpoints(client, auth_headers):
    new_ticket = {
        'summary': 'This is a test ticket',
        'description': 'This is a test',
        'workflow_id': 1,
        'reporter': {'id': 2},
        'status': {'id': 1},
        'project': {'id': 1, 'key': 'TEST'},
        'labels': ['test', 'lbl'],
        'fields': [
            {
                'name': 'Story Points',
                'value': 20
            }
        ],
        'ticket_type': {
            'id': 1,
        }
    }

    resp = client.post('/api/v1/tickets', new_ticket, headers=auth_headers)
    assert resp.status == falcon.HTTP_200
    assert resp.json is not None
    assert resp.json['summary'] == new_ticket['summary']

    jsn = resp.json

    jsn['fields'][0]['value'] = 10
    jsn['labels'].append('updated')

    resp = client.put('/api/v1/tickets/' + jsn['key'], jsn,
                      headers=auth_headers)
    assert resp.status == falcon.HTTP_200
    assert resp.json is not None
    assert resp.json['message'] == 'Successfully updated ticket.'

    resp = client.get('/api/v1/tickets/' + jsn['key'], headers=auth_headers)
    assert resp.status == falcon.HTTP_200
    assert resp.json is not None
    assert resp.json['fields'][0]['value'] == 10
    assert 'updated' in resp.json['labels']

    resp = client.delete('/api/v1/tickets/' + jsn['key'], headers=auth_headers)
    assert resp.status == falcon.HTTP_200
    assert resp.json is not None
    assert resp.json['message'] == 'Successfully deleted ticket.'

    resp = client.get('/api/v1/tickets/' + jsn['key'], headers=auth_headers)
    assert resp.status == falcon.HTTP_404


def test_crud_comments(client, auth_headers):
    new = 'updated-api'
    url = '/api/v1/tickets/TEST-5/comments'
    resp = client.post(url, headers=auth_headers,
                       body={
                           'author': {'id': 2},
                           'body': 'test-crud-api'
                       })
    CommentSchema.validate(resp.json)
    jsn = resp.json
    jsn['body'] = new
    resp = client.put(url + '/' + str(jsn['id']),
                      headers=auth_headers,
                      body=jsn)
    assert resp.status == falcon.HTTP_200
    resp = client.get(url, headers=auth_headers)
    cmt = {}
    for c in resp.json:
        if c['id'] == jsn['id']:
            cmt = c
            break
    assert cmt['body'] == new
