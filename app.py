import os

from flask import (Flask, jsonify, request)
from flask_cors import CORS
from configs.env import config
import time

APP_ENV = os.environ.get('APP_ENV', 'DEV')
PROJECT_PATH = config[APP_ENV]['PROJECT_PATH']
DB_HOST = config[APP_ENV]['DB_HOST']
DB_NAME = config[APP_ENV]['DB_NAME']
DB_USER = config[APP_ENV]['DB_USER']
DB_PASSWORD = config[APP_ENV]['DB_PASSWORD']

print(PROJECT_PATH) 
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = '38c12fd78e53488da82c1e27003c2030'
CORS(app)
# TO create the database
# with app.app_context():db.create_all()

from libs import OpGGCrawler

RESPONSE = {
    'status': False,
    'message': '',
    'data': {
        'count': 0,
        'results': []
    }
}

RESP_VALID = {
    'message': '',
    'status': '',
}


@app.route('/')
def home():
    RESPONSE['status'] = True
    RESPONSE['message'] = 'Nothing here, use the guide to use API'
    return jsonify(RESPONSE)


@app.route('/load_username')
def load_username():
    """
    Reads username and region and returns the json formatted data
    :return:
    """
    t1 = time.time()

    username = request.args.get('username')
    region = request.args.get('region', 'KR').upper()
    minutes = int(request.args.get('minutes', 12*60))


    if not username:
        RESPONSE['status'] = False
        RESPONSE['message'] = 'Username is required'
        RESPONSE['data'] = {}
        return jsonify(RESPONSE)

    crawler = OpGGCrawler(username=username, region=region, minutes=minutes)
    
    data = crawler.get_data()
    
    RESPONSE['status'] = True
    RESPONSE['message'] = 'Data Loaded Succesfully'
    RESPONSE['data']['results'] = data
    RESPONSE['data']['count'] = len(data)

    t2 = time.time()
    print(t2-t1 ,'seconds')

    return jsonify(RESPONSE)



#
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,threaded = True)
