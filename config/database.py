from cryptography.fernet import Fernet
from os import getenv
import pymongo
from utils.funtions import validate_token
from werkzeug.exceptions import HTTPException
import certifi

ca = certifi.where()


class connect_to_database:
    @staticmethod
    def connect_to_mongo(headers: str):
        f = Fernet(getenv("SECRET"))
        tokens = validate_token(headers, output=True)
        data_to_connect_to_mongoDB = {
            "username": f.decrypt(tokens['x_token'].encode('utf-8')).decode('utf-8'),
            "password": f.decrypt(tokens['x_api_key'].encode('utf-8')).decode('utf-8'),
            "cluster": f.decrypt(tokens['x_secret_id'].encode('utf-8')).decode('utf-8'),
        }
        mongo_url = "mongodb+srv://{username}:{password}@{cluster}/retryWrites=true&w=majority".format(
            **data_to_connect_to_mongoDB)
        client = pymongo.MongoClient(mongo_url, tlsCAFile=ca)
        db = client['halek']
        try:
            db.command("ping")
            return db
        except Exception:
            raise HTTPException("Error connecting to MongoDB.")
