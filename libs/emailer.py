
from datetime import datetime
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Emailer:
    """This class will help sending emails. It will have 2 major responsibilites.
    1. logging email locally which has not been sent.
    2. Sending emails from the Local Saved data. Ideally this would be invoked by an script is the shell script at
    the end of program. or would be invoked automatically every x hours via cron jobs. Anyway there will be another
    script that will utilize a method here to send emails if they are scheduled to be sent.

    References:
            https://realpython.com/python-send-email/
            https://docs.python.org/3/library/configparser.html
    """

    def __init__(self, email, messaage, subject=''):
        # these credentials will be used to send email

        # Summary will be send to the client email
        self.client_email = email

        self.html_content = messaage

        if subject:
            self.subject = subject
        else:
            crawler_ended_utc = datetime.utcnow().strftime('%a %b %d,%Y %I:%M:%S %p')
            self.subject = f'Low Balance Alert | {crawler_ended_utc}'

        # excel sheet to email

        # logger

    def send_email(self):
        """
        sends an email to client id after every run to update the progress of the crawl.
        The email may include an excel file which contains all the crawled data and any new following/unfollowing.

        :param crawler_started_utc: (str) Timestamp of crawl
        :param data: (dict) crawled data
        :param report_path: (str) filepath of the excel sheet
        :param send_report: (bool) if true the excel sheet is also emailed
        :param error_messages: (list) All the errors messages from all the modules of the crawler
        :return:
        """


        message = Mail(
            from_email='info@scrapingmesh.com',
            to_emails=self.client_email,
            subject= self.subject,
            html_content=self.html_content)

        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

        print(f'Email sent successfully')