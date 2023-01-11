
import jwt
from os import getenv
from jwt import exceptions
from werkzeug.exceptions import HTTPException


def validate_token(headers, output=False):
    token = validate_headers(headers)
    try:
        if output:
            return jwt.decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        jwt.decode(token, key=getenv("SECRET"), algorithms=["HS256"])
    except exceptions.DecodeError:
        raise HTTPException("Invalid token.")
    except exceptions.ExpiredSignatureError:
        raise HTTPException("You are not authorized to perform this operation")


def validate_headers(headers):
    if "authorization" not in headers:
        raise HTTPException("You are not authorized to perform this operation")
    return headers['authorization']
