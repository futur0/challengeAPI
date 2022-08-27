from flask import (Flask, jsonify, request)
from flask_cors import CORS
from libs import loadUserProfile
from libs import OpGGValidator

app = Flask(__name__)
app.config['SECRET_KEY'] = '38c12fd78e53488da82c1e27003c2030'
CORS(app)


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
    username = request.args.get('username')
    region = request.args.get('region', 'KR').upper()
    minutes = int(request.args.get('minutes', 12 * 60))

    if not username:
        RESPONSE['status'] = False
        RESPONSE['message'] = 'Username is required'
        RESPONSE['data'] = {}
        return jsonify(RESPONSE)

    data = loadUserProfile(region, username, minutes)
    RESPONSE['status'] = True
    RESPONSE['message'] = 'Data Loaded Succesfully'
    RESPONSE['data']['results'] = data
    RESPONSE['data']['count'] = len(data)

    return jsonify(RESPONSE)


@app.route('/valid')
def validate_username():
    """
    Reads username and region and check whether the combination exists
    """
    username = request.args.get('username')
    region = request.args.get('region', 'KR').upper()

    if not username:
        RESP_VALID['status'] = False
        RESP_VALID['message'] = 'Username is required'
        return jsonify(RESP_VALID)

    crawler = OpGGValidator(username=username, region=region)

    data = crawler.run()

    if data:
        RESP_VALID['message'] = 'search done'
        RESP_VALID['status'] = True

    if not data:
        RESP_VALID['message'] = 'search done'
        RESP_VALID['status'] = False

    return jsonify(RESP_VALID)


if __name__ == "__main__":
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
    app.run(host='0.0.0.0', port=5000)
