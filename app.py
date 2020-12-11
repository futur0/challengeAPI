import os

import humanize
from flask import (Flask, jsonify, request, render_template, redirect)

from configs.env import config
from configs.models import JackPotIndex, Settings
from configs.models import db

APP_ENV = os.environ.get('APP_ENV', 'PRD')
PROJECT_PATH = config[APP_ENV]['PROJECT_PATH']
print(PROJECT_PATH)
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PROJECT_PATH}/database.db'

app.config['SECRET_KEY'] = '38c12fd78e53488da82c1e27003c2030'

db.init_app(app)

if not os.path.exists(f'{PROJECT_PATH}/database.db'):
    print('No Data Base file found')
    # TO create the database
    with app.app_context():
        db.create_all()


#

@app.route('/')
def home():
    """Main Automation tracker and starter for all account and websites"""
    jackpot_data = []
    jackpots = JackPotIndex.query.filter_by(is_closed=False).all()
    for jackpot in jackpots:
        instance_id = jackpot.instance_id
        instance_name = jackpot.instance_name
        drop_amount = jackpot.drop_amount
        data = jackpot.data
        is_closed = jackpot.is_closed
        last_updated_at = jackpot.last_updated_at
        tracking_started_at = jackpot.indexed_date
        notified = jackpot.notified

        jackpot_data.append({
            'instance_id': instance_id,
            'instance_name': instance_name,
            'drop_amount': drop_amount,
            'data': data,
            'tracking_started_at': tracking_started_at,
            'tracking_started_at_natural': humanize.naturaltime(tracking_started_at),
            'status': is_closed,
            'notified': notified,
            'last_updated_at': last_updated_at,
            'last_updated_at_natural': humanize.naturaltime(last_updated_at),

        })

    return render_template('home.html', jackpot_data=jackpot_data)

    return jsonify(jackpot_data)


@app.route('/get_all_jackpots_json')
def get_all_jackpots_json():
    """Main Automation tracker and starter for all account and websites"""
    jackpot_data = []
    jackpots = JackPotIndex.query.filter_by(is_closed=False).all()
    for jackpot in jackpots:
        instance_id = jackpot.instance_id
        instance_name = jackpot.instance_name
        drop_amount = jackpot.drop_amount
        data = jackpot.data
        is_closed = jackpot.is_closed
        last_updated_at = jackpot.last_updated_at
        tracking_started_at = jackpot.indexed_date
        notified = jackpot.notified

        jackpot_data.append({
            'instance_id': instance_id,
            'instance_name': instance_name,
            'drop_amount': drop_amount,
            'data': data,
            'tracking_started_at': tracking_started_at,
            'tracking_started_at_natural': humanize.naturaltime(tracking_started_at),
            'status': is_closed,
            'notified': notified,
            'last_updated_at': last_updated_at,
            'last_updated_at_natural': humanize.naturaltime(last_updated_at),

        })

    return jsonify(jackpot_data)


# https://jackpot-query-mt.nyxop.net/v3/jackpots?instance=9df7b3b2-dec3-4a08-8991-e38e956a0aea&instance=f857f635-df85-44a6-b19b-692a52ca74c6&instance=6f4a2200-8b9f-4482-82ee-8651078ab84f&currency=GBP
@app.route('/add_jackpot_instance')
def add_jackpot_instance():
    # &instance_major=
    # &instance_minor=9df7b3b2-dec3-4a08-8991-e38e956a0aea
    # &drop_amount_major=
    # &drop_amount_minor=

    # http://0.0.0.0:8000/add_jackpot_instance?instance_id=6f4a2200-8b9f-4482-82ee-8651078ab84f&instance_name=EPIC&drop_amount=13665.00
    # http://0.0.0.0:8000/add_jackpot_instance?instance_id=bcdbc277-a35d-465a-97b4-4ea2476ab874&instance_name=MAJOR&drop_amount=4555.00

    # http://0.0.0.0:8000/add_jackpot_instance?instance_id=9df7b3b2-dec3-4a08-8991-e38e956a0aea&instance_name=MINOR&drop_amount=1366.50

    instance_id = request.args['instance_id']

    instance_name = request.args['instance_name'].upper()
    drop_amount = request.args['drop_amount']

    jackpot = JackPotIndex(
        instance_id=instance_id,
        instance_name=instance_name,
        drop_amount=drop_amount,
    )
    try:
        db.session.add(jackpot)
        db.session.commit()
        message = '{} Jackpot id'.format(jackpot.id)
    except Exception as e:
        message = str(e)
    response = {
        'status': True,
        'message': message,
    }
    return jsonify(response)


@app.route('/get_jackpot_history')
def get_jackpot_history():
    # http://0.0.0.0:8000/add_jackpot_instance?instance_epic=6f4a2200-8b9f-4482-82ee-8651078ab84f&instance_major=f857f635-df85-44a6-b19b-692a52ca74c6&instance_minor=9df7b3b2-dec3-4a08-8991-e38e956a0aea&drop_amount_epic=13542.50&drop_amount_major=4514.10&drop_amount_minor=1354.23
    instance_name = request.args['instance_name']

    jackpots = JackPotIndex.query.filter_by(instance_name=instance_name).order_by(JackPotIndex.last_updated_at.desc()).all()

    jackpot_data = []

    for jackpot in jackpots:
        instance_id = jackpot.instance_id
        instance_name = jackpot.instance_name
        drop_amount = jackpot.drop_amount
        data = jackpot.data
        is_closed = jackpot.is_closed
        last_updated_at = jackpot.last_updated_at
        tracking_started_at = jackpot.indexed_date
        notified = jackpot.notified

        jackpot_data.append({
            'instance_id': instance_id,
            'instance_name': instance_name,
            'drop_amount': drop_amount,
            'data': data,
            'tracking_started_at': str(tracking_started_at).split('.')[0],
            'tracking_started_at_natural': humanize.naturaltime(tracking_started_at),
            'status': is_closed,
            'notified': notified,
            'last_updated_at': str(last_updated_at).split('.')[0],
            'last_updated_at_natural': humanize.naturaltime(last_updated_at),

        })

    return render_template('history.html', jackpot_data=jackpot_data, instance_name=instance_name)


@app.route('/toggle_notification')
def toggle_notification():
    # http://0.0.0.0:8000/add_jackpot_instance?instance_epic=6f4a2200-8b9f-4482-82ee-8651078ab84f&instance_major=f857f635-df85-44a6-b19b-692a52ca74c6&instance_minor=9df7b3b2-dec3-4a08-8991-e38e956a0aea&drop_amount_epic=13542.50&drop_amount_major=4514.10&drop_amount_minor=1354.23
    instance_id = request.args['instance_id']

    jackpot = JackPotIndex.query.filter_by(instance_id=instance_id).first()
    jackpot.notified = not jackpot.notified
    db.session.add(jackpot)
    db.session.commit()
    return redirect('/')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    count = Settings.query.count()
    if count == 0:
        setting = Settings(
            emails='',
            epic_threshold=0,
            major_threshold=0,
            minor_threshold=0,
        )

        db.session.add(setting)
        db.session.commit()

    if request.method == 'POST':
        setting = Settings.query.first()
        emails = request.values.get('email', '')
        try:
            epic_threshold = float(request.values.get('epic', ''))
        except:
            epic_threshold = 0

        try:
            major_threshold = float(request.values.get('major', ''))
        except:
            major_threshold = 0

        try:
            minor_threshold = float(request.values.get('minor', ''))
        except:
            minor_threshold = 0
        setting.emails = emails
        setting.epic_threshold = epic_threshold
        setting.major_threshold = major_threshold
        setting.minor_threshold = minor_threshold
        db.session.add(setting)
        db.session.commit()

    setting = Settings.query.first()

    emails = setting.emails
    epic_threshold = setting.epic_threshold
    major_threshold = setting.major_threshold
    minor_threshold = setting.minor_threshold
    data = {
        'emails': emails,
        'epic_threshold': epic_threshold,
        'major_threshold': major_threshold,
        'minor_threshold': minor_threshold,
    }
    return render_template('settings.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
