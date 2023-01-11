import os
from services import create_app
from flask_cors import CORS
from dotenv import load_dotenv

app = create_app()
CORS(app)
FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
load_dotenv()

if __name__ == '__main__':
    if FLASK_DEBUG == 'prod':
        app.run(ssl_context="adhoc", host='0.0.0.0', port=80)
    app.run(debug=True, port=5000)
