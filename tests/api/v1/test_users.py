import falcon
from praelatus.api.schemas import UserSchema


def test_signup(client, headers):
    new_user = {
        "username": "some_new_user",
        "password": "supersecure",
        "full_name": "New User",
        "email": "new@praelatus.io"
    }

    resp = client.post('/api/v1/users', new_user, headers=headers)
    print(resp.body)
    assert resp.status == falcon.HTTP_200
    assert resp.json['token'] is not None
    UserSchema.validate(resp.json['user'])
