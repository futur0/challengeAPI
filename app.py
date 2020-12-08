from flask import (Flask, jsonify, request, render_template, flash, redirect)

from datetime import datetime
import humanize
import datetime as dt

from configs.models import db
from configs.models import JackPotIndex, JackPotData
from libs.utils import humanize_date_difference

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/amitupreti/jackpot-tracker/database.db'

app.config['SECRET_KEY'] = '38c12fd78e53488da82c1e27003c2030'

db.init_app(app)


# TO create the database
# with app.app_context():
#     db.create_all()


@app.route('/')
def home():
    """Main Automation tracker and starter for all account and websites"""
    jackpot_data = []
    jackpots = JackPotIndex.query.all()
    for jackpot in jackpots:
        instance_minor = jackpot.instance_minor
        instance_major = jackpot.instance_major
        instance_epic = jackpot.instance_epic
        status = jackpot.status
        drop_amount_major = jackpot.drop_amount_major
        drop_amount_minor = jackpot.drop_amount_minor
        drop_amount_epic = jackpot.drop_amount_epic
        tracking_started_at = jackpot.indexed_date
        last_updated_at = jackpot.last_updated_at

        jackpot_id = jackpot.id
        jackpot_data_object_count = JackPotData.query.filter_by(index_id=jackpot_id).count()
        jackpot_data_object = JackPotData.query.filter_by(index_id=jackpot_id).order_by(JackPotData.updated_date.desc()).first()
        jackpot_data_object_id = jackpot_data_object.id
        epic_data = jackpot_data_object.epic_data
        major_data = jackpot_data_object.major_data
        minor_data = jackpot_data_object.minor_data
        updated_date = jackpot_data_object.updated_date

        jackpot_data.append({
            'instance_minor': instance_minor,
            'instance_major': instance_major,
            'instance_epic': instance_epic,

            'tracking_started_at': tracking_started_at,
            'tracking_started_at_natural': humanize.naturaltime(tracking_started_at),

            'last_updated_at': last_updated_at,
            'last_updated_at_natural': humanize.naturaltime(last_updated_at),
            #

            'jackpot_id': jackpot_id,

            'jackpot_data_object_count': jackpot_data_object_count,
            'jackpot_data_object_id': jackpot_data_object_id,

            'epic_data': epic_data,
            'major_data': major_data,
            'minor_data': minor_data,

            'drop_amount_major': drop_amount_major,
            'drop_amount_minor': drop_amount_minor,
            'drop_amount_epic': drop_amount_epic,

            'updated_date': updated_date,
            'updated_date_natural': humanize.naturaltime(updated_date),
            #
            'status': status,

        })


    return render_template('home.html', jackpot_data=jackpot_data)

    return jsonify(jackpot_data)


@app.route('/get_history')
def get_history():
    """Main Automation tracker and starter for all account and websites"""

    return render_template('history.html')

    return jsonify(jackpot_data)


@app.route('/get_all_jackpots_json')
def get_all_jackpots_json():
    """Main Automation tracker and starter for all account and websites"""

    jackpot_data = []
    jackpots = JackPotIndex.query.all()
    for jackpot in jackpots:
        instance_minor = jackpot.instance_minor
        instance_major = jackpot.instance_major
        instance_epic = jackpot.instance_epic
        status = jackpot.status
        drop_amount_major = jackpot.drop_amount_major
        drop_amount_minor = jackpot.drop_amount_minor
        drop_amount_epic = jackpot.drop_amount_epic
        tracking_started_at = jackpot.indexed_date

        jackpot_id = jackpot.id
        jackpot_data_object_count = JackPotData.query.filter_by(index_id=jackpot_id).count()
        jackpot_data_object = JackPotData.query.filter_by(index_id=jackpot_id).order_by(JackPotData.updated_date.desc()).first()
        jackpot_data_object_id = jackpot_data_object.id
        epic_data = jackpot_data_object.epic_data
        major_data = jackpot_data_object.major_data
        minor_data = jackpot_data_object.minor_data
        updated_date = jackpot_data_object.updated_date
        jackpot_data.append({
            'instance_minor': instance_minor,
            'instance_major': instance_major,
            'instance_epic': instance_epic,

            'tracking_started_at': tracking_started_at,

            'jackpot_id': jackpot_id,

            'jackpot_data_object_count': jackpot_data_object_count,
            'jackpot_data_object_id': jackpot_data_object_id,

            'epic_data': epic_data,
            'major_data': major_data,
            'minor_data': minor_data,

            'drop_amount_major': drop_amount_major,
            'drop_amount_minor': drop_amount_minor,
            'drop_amount_epic': drop_amount_epic,

            'updated_date': updated_date,

        })

    return jsonify(jackpot_data)


# https://jackpot-query-mt.nyxop.net/v3/jackpots?instance=9df7b3b2-dec3-4a08-8991-e38e956a0aea&instance=f857f635-df85-44a6-b19b-692a52ca74c6&instance=6f4a2200-8b9f-4482-82ee-8651078ab84f&currency=GBP
@app.route('/add_jackpot_instance')
def add_jackpot_instance():
    # s
    instance_epic = request.args['instance_epic']
    instance_major = request.args['instance_major']
    instance_minor = request.args['instance_minor']
    drop_amount_epic = request.args['drop_amount_epic']
    drop_amount_major = request.args['drop_amount_major']
    drop_amount_minor = request.args['drop_amount_minor']

    jackpot = JackPotIndex(
        instance_epic=instance_epic,
        instance_major=instance_major,
        instance_minor=instance_minor,
        drop_amount_epic=drop_amount_epic,
        drop_amount_major=drop_amount_major,
        drop_amount_minor=drop_amount_minor
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


@app.route('/add_jackpot_data')
def add_jackpot_data():
    # http://0.0.0.0:8000/add_jackpot_data?epic_data=9606.97726592&major_data=4276.03998086&minor_data=850.72016905&index_id=1
    epic_data = request.args['epic_data']
    major_data = request.args['major_data']
    minor_data = request.args['minor_data']
    index_id = request.args['index_id']
    # Check if the item exist if not update the data

    # existing_provider = Provider.query.get(1)  # or whatever
    # # update the rssfeed column
    # existing_provider.rssfeed = form.rssfeed.data
    # db.session.commit()

    jackpot = JackPotData.query.filter_by(index_id=index_id).first()
    if jackpot:
        jackpot.epic_data = epic_data
        jackpot.major_data = major_data
        jackpot.minor_data = minor_data
        jackpot.updated_date = datetime.now()

    else:
        jackpot = JackPotData(
            epic_data=epic_data,
            major_data=major_data,
            minor_data=minor_data,
            index_id=index_id,
            updated_date=datetime.now()

        )
    db.session.add(jackpot)
    db.session.commit()

    try:
        db.session.add(jackpot)
        db.session.commit()
        message = '{} Jackpot id'.format(jackpot.id)
    except Exception as e:
        message = e
    response = {
        'status': True,
        'message': message,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
