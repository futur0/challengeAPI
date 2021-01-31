# To be run every few minutes
import os
from datetime import datetime
from time import sleep

from app import app, db
from configs.models import JackPotIndex, Settings
from configs.env import config

from libs.utils import load_instance, check_time
from libs.emailer import Emailer

APP_ENV = os.environ.get('APP_ENV', 'PRD')

DOMAIN = config[APP_ENV]['DOMAIN']

MESAGE_TEMPLATE = '''Hi {name}, <br>
                    
                                The Jackpot {instance_name} has been completed.. <br>
                                
                                Please add a new one. {url}
                                Book Of Relics <br>
                                NetBet 
                            '''


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

            if result == 'Closed':
                active_instance.is_closed = True
                db.session.add(active_instance)
                db.session.commit()
                # send email
                setting = Settings.query.first()
                emails = setting.emails.split(',')
                print('Turning off  Status for {} and notitying'.format(instance_id))
                print('Threshold touched for {}. Sending Email'.format(instance_name))
                for email in emails:
                    username = email.split('@')[0]
                    subject = '{instance_name} | Book Of Relics | NetBet'.format(instance_name=instance_name)
                    message = MESAGE_TEMPLATE.format(
                        name=username,
                        instance_name=instance_name,
                        url=DOMAIN + '/add_jackpot',
                    )
                    print(message)
                    emailer = Emailer(email=email, message=message, subject=subject)
                    emailer.send_email()
                continue
            elif result != 0:

                if result > data or data == None:
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
