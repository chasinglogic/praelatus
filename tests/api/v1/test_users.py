import falcon
from praelatus.api.schemas import UserSchema


def test_crud_user_endpoints(client, headers):
    # Sign up a new user
    new_user = {
        'username': 'some_new_user',
        'password': 'supersecure',
        'full_name': 'New User',
        'email': 'new@praelatus.io'
    }

    resp = client.post('/api/v1/users', new_user, headers=headers)
    assert resp.status == falcon.HTTP_200
    assert resp.json['token'] is not None
    UserSchema.validate(resp.json['user'])
    new_user = resp.json['user']

    # Try to log in to our new user
    login = {
        'username': 'some_new_user',
        'password': 'supersecure'
    }

    resp = client.post('/api/v1/tokens', login, headers=headers)
    assert resp.status == falcon.HTTP_200
    assert resp.json['token'] is not None
    token = resp.json['token']
    UserSchema.validate(resp.json['user'])

    # Get the new user
    resp = client.get('/api/v1/users/some_new_user', headers=headers)
    assert resp.status == falcon.HTTP_200
    UserSchema.validate(resp.json)

    auth_headers = headers
    auth_headers['Authorization'] = 'Token ' + token

    # Update the new user
    new_user['username'] = 'delete_me'
    resp = client.put('/api/v1/users/some_new_user', new_user,
                      headers=auth_headers)
    assert resp.json['message'] == 'Successfully updated user.'

    # Delete the new user
    resp = client.delete('/api/v1/users/delete_me', headers=auth_headers)
    assert resp.json['message'] == 'Successfully deleted user.'


def test_get_all_users(client, headers):
    resp = client.get('/api/v1/users', headers=headers)
    assert resp.status == falcon.HTTP_200
    assert len(resp.json) > 0


def test_get_filter(client, headers):
    resp = client.get('/api/v1/users?filter=testadmin', headers=headers)
    assert resp.status == falcon.HTTP_200
    assert len(resp.json) == 1


def test_404(client, headers):
    resp = client.get('/api/v1/users/marypoppins', headers=headers)
    assert resp.status == falcon.HTTP_404

    login = {'username': 'marypoppins', 'password': 'spoonful'}
    resp = client.post('/api/v1/tokens', login, headers=headers)
    assert resp.status == falcon.HTTP_404


def test_failed_login(client, headers):
    login = {'username': 'testuser', 'password': 'wrong'}
    resp = client.post('/api/v1/tokens', login, headers=headers)
    assert resp.status == falcon.HTTP_401
    assert resp.json['message'] == 'invalid password'
