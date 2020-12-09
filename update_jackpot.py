# To be run every few minutes
from datetime import datetime
from time import sleep

from app import app, db
from configs.models import JackPotData, JackPotIndex, JackPotDataHistory
from libs.utils import load_instance, check_time


def refresh_current_instance():
    with app.app_context():
        active_instances = JackPotIndex.query.filter_by(status=True)

        for active_instance in active_instances:
            instance_minor = active_instance.instance_minor
            instance_major = active_instance.instance_major
            instance_epic = active_instance.instance_epic
            status = active_instance.status
            drop_amount_major = active_instance.drop_amount_major
            drop_amount_minor = active_instance.drop_amount_minor
            drop_amount_epic = active_instance.drop_amount_epic
            tracking_started_at = active_instance.indexed_date
            active_instance.last_updated_at = datetime.now()

            db.session.add(active_instance)
            db.session.commit()
            jackpot_id = active_instance.id
            print('Checking for {}'.format(jackpot_id))
            jackpot_data_object_count = JackPotData.query.filter_by(index_id=jackpot_id).count()
            if jackpot_data_object_count != 0:
                jackpot_data_object = JackPotData.query.filter_by(index_id=jackpot_id).order_by(JackPotData.updated_date.desc()).first()
                jackpot_data_object_id = jackpot_data_object.id
                epic_data = jackpot_data_object.epic_data
                major_data = jackpot_data_object.major_data
                minor_data = jackpot_data_object.minor_data
                updated_date = jackpot_data_object.updated_date

                # TODO
                #  if last update was 1 hour ago. Change status to off
                has_been_1_hour = check_time(updated_date)
                # if has_been_1_hour:
                #     active_instance.status = False
                #     db.session.add(active_instance)
                #     db.session.commit()
                #     print('Turning off  Status for {}'.format(jackpot_id))
                #     continue

                # get the data for instances and compare to the old data here
                check_data = {
                    'epic': instance_epic,
                    'minor': instance_minor,
                    'major': instance_major,
                }
                result = load_instance(check_data)

                if result['epic'] == None and result['minor'] == None and result['major'] == None:
                    active_instance.status = False
                    db.session.add(active_instance)
                    db.session.commit()
                    print('Turning off  Status for {}'.format(jackpot_id))
                    continue
                else:
                    # import ipdb
                    # ipdb.set_trace()
                    if epic_data != result['epic'] or major_data != result['major'] or minor_data != result['minor']:
                        jackpot_history = JackPotDataHistory(
                            epic_data=result['epic'],
                            major_data=result['major'],
                            minor_data=result['minor'],
                            jack_pot_data=jackpot_data_object_id,
                            updated_date=datetime.now()
                        )
                        db.session.add(jackpot_history)
                        db.session.commit()
                        print('History Updated')

                if epic_data != result['epic'] and result['epic']:
                    jackpot_data_object.epic_data = result['epic']
                    print('Epic Old Data: {} New Data: {}'.format(epic_data, result['epic']))
                    print('Epic updated at {}'.format(datetime.now()))
                    jackpot_data_object.updated_date = datetime.now()

                if minor_data != result['minor'] and result['minor']:
                    jackpot_data_object.minor_data = result['minor']
                    print('Minor Old Data: {} New Data: {}'.format(minor_data, result['minor']))
                    jackpot_data_object.updated_date = datetime.now()
                    print('Minor updated at {}'.format(datetime.now()))

                if major_data != result['major'] and result['major']:
                    jackpot_data_object.major_data = result['major']
                    print('Major Old Data: {} New Data: {}'.format(major_data, result['major']))
                    jackpot_data_object.updated_date = datetime.now()
                    print('Major updated at {}'.format(datetime.now()))

                db.session.add(jackpot_data_object)
                db.session.commit()

            else:
                check_data = {
                    'epic': instance_epic,
                    'minor': instance_minor,
                    'major': instance_major,
                }
                result = load_instance(check_data)

                jackpot = JackPotData(
                    epic_data=result['epic_data'],
                    major_data=result['epic_data'],
                    minor_data=result['epic_data'],
                    index_id=jackpot_id,
                    updated_date=datetime.now()

                )
                db.session.add(jackpot)
                db.session.commit()


if __name__ == '__main__':
    refresh_current_instance()
    sleep(10)
    refresh_current_instance()
    sleep(10)
    refresh_current_instance()
    sleep(7)
    refresh_current_instance()
    sleep(5)
    refresh_current_instance()
