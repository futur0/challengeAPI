import os

from flask import (Flask, jsonify, request)

from configs.env import config

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


@app.route('/')
def home():
    RESPONSE['status'] = True
    RESPONSE['message'] = 'Nothing here, use hte guide to use API'
    return jsonify(RESPONSE)


@app.route('/load_username')
def load_username():
    """
    Reads username and region and returns the json formatted data
    :return:
    """
    username = request.args.get('username')
    region = request.args.get('region', 'KR').upper()
    hours = int(request.args.get('hours', 12))

    if not username:
        RESPONSE['status'] = False
        RESPONSE['message'] = 'Username is required'
        RESPONSE['data'] = {}
        return jsonify(RESPONSE)

    crawler = OpGGCrawler(username=username, region=region, hours=hours)
    data = crawler.get_data()
    RESPONSE['status'] = True
    RESPONSE['message'] = 'Data Loaded Succesfully'
    RESPONSE['data']['results'] = data
    RESPONSE['data']['count'] = len(data)
    return jsonify(RESPONSE)


#
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
