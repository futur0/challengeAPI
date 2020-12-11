# To be run every few minutes
from datetime import datetime
from time import sleep

from app import app, db
from configs.models import JackPotIndex
from libs.utils import load_instance, check_time


def refresh_current_instance():
    with app.app_context():
        active_instances = JackPotIndex.query.filter_by(is_closed=False)

        for active_instance in active_instances:
            instance_id = active_instance.instance_id
            instance_name = active_instance.instance_name
            drop_amount = active_instance.drop_amount
            data = active_instance.data
            is_closed = active_instance.is_closed
            last_updated_at = active_instance.last_updated_at
            tracking_started_at = active_instance.indexed_date
            notified = active_instance.notified

            active_instance.last_updated_at = datetime.now()

            db.session.add(active_instance)
            db.session.commit()
            print('Checking for {}'.format(instance_id))

            result = load_instance(instance_id)

            if result == None:
                active_instance.is_closed = True
                db.session.add(active_instance)
                db.session.commit()
                print('Turning off  Status for {}'.format(instance_id))
                continue
            else:

                if data != result:
                    active_instance.data = result
                    active_instance.last_updated_at = datetime.now()
                    db.session.add(active_instance)
                    db.session.commit()
                    print('History Updated')


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
