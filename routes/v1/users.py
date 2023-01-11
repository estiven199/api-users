import flask
import json
from flask import request
from flask_restful import Api, Resource
from dataclasses import dataclass
from config.database import connect_to_database as cdb
from models.users import UsersModel
from pydantic import ValidationError
from bson import ObjectId

users_v1 = flask.Blueprint('users_v1', __name__)
api = Api(users_v1)


class BSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


@dataclass
class UserResource(Resource):

    def __post_init__(self):
        self.headers = json.loads(json.dumps(
            {k.replace("-", "_").lower(): request.headers[k] for k in request.headers.keys()}))
        self.db = cdb.connect_to_mongo(self.headers)
        self.data = request.get_json(
        ) if request.method == 'POST' or request.method == 'PUT' else {}

    def post(self):
        try:
            UsersModel(**self.data)
            id = self.db.users.insert_one(self.data).inserted_id
            user = self.db.users.find_one({"_id": ObjectId(id)})
            user['user_id'] = str(user['_id'])
            del user['_id']
            return {
                "code": 0,
                "message": "The User has been created",
                "data": user
            }
        except ValidationError as e:
            errors = e.errors()
            return {
                "code": 400,
                "message": errors,
                "data": []
            }

    def put(self, user_id):
        self.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": self.data})
        user = self.db.users.find_one({"_id": ObjectId(user_id)})
        user['user_id'] = str(user['_id'])
        del user['_id']
        return {
            "code": 0,
            "message": "User has been updated successfully",
            "data": user
        }

    def get(self, user_id=None):
        users = [user for user in self.db.users.find({})] if not user_id else self.db.users.find_one({"_id": ObjectId(user_id)})
        json_users = json.dumps(users, cls=BSONEncoder)
        return {
            "code": 0,
            "message": "success",
            "data": json_users
        } if json_users != "null" else {
            "code": 404,
            "message": "User does not exist.",
            "data": []
        }
 
    def delete(self, user_id):
        self.db.users.delete_one({"_id":ObjectId(user_id)})
        return { 
            "code": 0,
            "message": "User Deleted Successfully.",
            "data": []}


api.add_resource(UserResource, '/api/v1/users','/api/v1/users/<user_id>', endpoint='')

