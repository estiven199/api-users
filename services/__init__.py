from flask import Flask
from flask_restful import Api
from routes.v1.auth import auth_v1
from routes.v1.users import users_v1

def create_app():
    app = Flask(__name__)
    Api(app, catch_all_404s=True)
    app.register_blueprint(auth_v1)
    app.register_blueprint(users_v1)
    return app