import json
import binascii
from itsdangerous import TimestampSigner


def get(token):
    """Desearialize token into a user object."""
    print("Unsigning Token")
    signed = serializer.unsign(token, max_age=28800)
    print('signed', signed)
    jsn = json.loads(signed, return_header=True)
    print(jsn)
    return jsn


serializer = TimestampSigner(signer)


def gen_session_id(user):
    """Generate a secure token."""
    jsn = json.dumps(user)
    convertii = binascii.a2b_qp(jsn)
    print('convertii', convertii)
    maketoken = serializer.sign(convertii)
    print('maketoken', maketoken)
    return str(maketoken)
