import datetime
import json

import requests


# from configs.env import config
#
# APP_ENV = os.environ.get('APP_ENV', 'DEV')
# PROJECT_PATH = config[APP_ENV]['PROJECT_PATH']
# BB_DOMAIN = config[APP_ENV]['BB_DOMAIN']


def humanize_date_difference(otherdate=None, offset=None):
    now = datetime.datetime.now()
    if otherdate:
        dt = now - otherdate
        # dt = now - otherdate

        offset = dt.seconds + (dt.days * 60 * 60 * 24)
    if offset:
        delta_s = offset % 60
        offset /= 60
        delta_m = offset % 60
        offset /= 60
        delta_h = offset % 24
        offset /= 24
        delta_d = offset
    else:
        raise ValueError("Must supply otherdate or offset (from now)")

    if delta_d > 1:
        if delta_d > 6:
            date = now + datetime.timedelta(days=-delta_d, hours=-delta_h, minutes=-delta_m)
            return date.strftime('%A, %Y %B %m, %H:%I')
        else:
            wday = now + datetime.timedelta(days=-delta_d)
            return wday.strftime('%A')
    if delta_d == 1:
        return "Yesterday"
    if delta_h > 0:
        return "%dh%dm ago" % (delta_h, delta_m)
    if delta_m > 0:
        return "%dm%ds ago" % (delta_m, delta_s)
    else:
        return "%ds ago" % delta_s


def load_instance(instance_id):
    headers = {
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    output = {'epic': '', 'minor': '', 'major': ''}
    result = 0
    try:
        params = (
            ('instance', instance_id),
            ('currency', 'GBP'),
        )
        # print('Loading Minor')
        response = requests.get('https://jackpot-query-mt.nyxop.net/v3/jackpots', headers=headers, params=params)
        if 'instance is inactive' in response.text:
            return 'Closed'
        print('Ok Loaded')

        data = json.loads(response.text)['jackpots'][0]
        result = data['balanceAmountInRequestedCurrency']
        print(result)
    except Exception as e:
        print(e)

    return result


def check_time(start_time):
    ALLOWED_SECONDS = 60 * 60 * 24
    seconds_passed = (datetime.datetime.now() - start_time).seconds
    print('Time passed {} minutes'.format(seconds_passed / 60))
    if seconds_passed >= ALLOWED_SECONDS:
        return True
    return False
