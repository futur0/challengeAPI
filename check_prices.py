# To be run every few minutes
from datetime import datetime
from time import sleep

from app import app, db
from configs.models import JackPotIndex, Settings
from libs.utils import load_instance, check_time

from libs.emailer import Emailer


def check_for_price_change():
    with app.app_context():

        active_instances = JackPotIndex.query.filter_by(notified=False)
        if active_instances.count() == 0:
            print('All Instances have been notified')
            return

        setting = Settings.query.first()
        emails = setting.emails.split(',')
        epic_threshold = setting.epic_threshold
        major_threshold = setting.major_threshold
        minor_threshold = setting.minor_threshold
        data = {
            'emails': emails,
            'epic_threshold': epic_threshold,
            'major_threshold': major_threshold,
            'minor_threshold': minor_threshold,
        }

        messages_objects = []
        message_template = '''Hi {name}, <br>
                    
                                The bet amount for {instance_name} is £ {data}  which is higher than or equal to {threshold}. <br>
                                
                                It is {higher} more than the threshold. <br>
                                Book Of Relics <br>
                                NetBet 
                            '''

        for active_instance in active_instances:
            instance_id = active_instance.instance_id
            instance_name = active_instance.instance_name
            drop_amount = active_instance.drop_amount
            data = active_instance.data
            is_closed = active_instance.is_closed
            last_updated_at = active_instance.last_updated_at
            tracking_started_at = active_instance.indexed_date
            notified = active_instance.notified

            if instance_name.upper() == 'MAJOR':
                threshold = major_threshold
            elif instance_name.upper() == 'EPIC':
                threshold = epic_threshold
            else:
                threshold = minor_threshold

            if data >= threshold:
                if threshold == 0:
                    continue
                increased_data = data - threshold
                print('Threshold touched for {}. Sending Email'.format(instance_name))
                for email in emails:
                    username = email.split('@')[0]
                    subject = '{instance_name} | Book Of Relics | NetBet'.format(instance_name=instance_name)
                    message = message_template.format(
                        name=username,
                        instance_name=instance_name,
                        data=data,
                        threshold=threshold,
                        higher=increased_data

                    )
                    print(message_template)
                    emailer = Emailer(email=email, message=message, subject=subject)
                    emailer.send_email()
                    active_instance.notified = True
                    db.session.add(active_instance)
                    db.session.commit()
                    print('Notified and turned off in ')


if __name__ == '__main__':
    check_for_price_change()

# Run every minute
