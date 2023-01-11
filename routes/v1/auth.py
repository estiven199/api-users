import jwt
import flask
from os import getenv
import json
from datetime import datetime, timedelta
from werkzeug.exceptions import HTTPException
from flask import request
from flask_restful import Api, Resource
from schemas.auth import AuthToken
from models.auth import keys

auth_v1 = flask.Blueprint('auth_v1', __name__)

api = Api(auth_v1)

class Authentication(Resource):

    def expire_date(self, days: int):
        return datetime.now() + timedelta(days)

    def write_token(self, data: keys):
        return jwt.encode(payload={**data, "exp": self.expire_date(10)}, key=getenv("SECRET"), algorithm="HS256")

    def post(self):
        headers = json.loads(json.dumps({k.replace("-", "_").lower(): request.headers[k] for k in request.headers.keys()}))
        if "x_token" not in headers or "x_api_key" not in headers or "x_secret_id" not in headers:
            raise HTTPException("You are not authorized to perform this operation")
        return AuthToken(self.write_token({
            "x_token": headers['x_token'],
            "x_api_key": headers['x_api_key'],
            "x_secret_id": headers['x_secret_id']
        }
        ))

        

api.add_resource(Authentication, '/api/oauth/v1/token', endpoint='')
