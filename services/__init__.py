from flask import Flask,jsonify
from flask_restful import Api
from routes.v1.auth import auth_v1
from routes.v1.users import users_v1
class AppErrorBaseClass(Exception):
    pass


class ObjectNotFound(AppErrorBaseClass):
    pass

def create_app():
    app = Flask(__name__)
    Api(app, catch_all_404s=True)
    app.register_blueprint(auth_v1)
    app.register_blueprint(users_v1)
    register_error_handlers(app)
    return app

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        print(e)
        return jsonify({'message': f'Internal server error {e}'}), 500

    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'message': 'Method not allowed'}), 405

    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'message': 'Forbidden error'}), 403

    @app.errorhandler(404)
    def handle_404_error(e):
        print(e)
        return jsonify({'message': 'Not Found error'}), 404

    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return jsonify({'message': str(e)}), 500

    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        print(e)
        return jsonify({'message': str(e)}), 404