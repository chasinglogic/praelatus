import json
import binascii
import base64
from itsdangerous import TimestampSigner


def get(signed_token):
    """Desearialize token into a user object."""
    print("Unsigning Token")
    token = serializer.unsign(signed_token, max_age=28800)
    return json.loads(token)


def gen_session_id(user):
    """Generate a secure token."""
    jsn = json.dumps(user)
    return serializer.sign(jsn)


serializer = TimestampSigner('test')
