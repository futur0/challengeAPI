"""
Helper file to interact with database. Small wrapper to save few lines of code
"""
from datetime import datetime

import pytz

from sqlalchemy import extract

from configs.db_connect import loadSession, BookieBashingAccounts, Logs, GlobalSettings, BetAccounts,BetWesites, ReportLogs


def get_betaccount_settings(bet_account_obj: object):
    """
    Reads and returns settings for bet accounts
    :param bet_account_obj:  bet account sqlalchemy object
    :return: dictionary
    """
    # Get EB setttings
    bb_settings = get_bookie_bashing_settings()

    bet_account_data = {
        'username': bet_account_obj.user_name,
        'password': bet_account_obj.password,

        
        'max_allowed_bet_amount_solo': float(bet_account_obj. max_allowed_bet_amount_solo),
        'max_allowed_bet_amount_combo': float(bet_account_obj. max_allowed_bet_amount_combo),
        'max_allowed_bet_amount_double': float(bet_account_obj. max_allowed_bet_amount_double),


        'bid_win_amount_solo': float(bet_account_obj.bid_win_amount_solo),
        'bid_win_amount_combo': float(bet_account_obj.bid_win_amount_combo),
        'bid_win_amount_double': float(bet_account_obj.bid_win_amount_double),

        'max_allowed_odds_combo': float(bet_account_obj.max_allowed_odds_combo),
        'max_allowed_odds_double': float(bet_account_obj.max_allowed_odds_double),

        'max_allowed_bets_single_per_day': bet_account_obj.max_allowed_bets_single_per_day,
        'max_allowed_bets_double_per_day': bet_account_obj.max_allowed_bets_double_per_day,
        'max_allowed_bets_combo_per_day': bet_account_obj.max_allowed_bets_combo_per_day,

        'max_bets_per_horse_double_per_day': bet_account_obj.max_bets_per_horse_double_per_day,
        'max_bets_per_horse_combo_per_day': bet_account_obj.max_bets_per_horse_combo_per_day,

        'bet_account_pk': bet_account_obj.id,
        'bet_website_pk': bet_account_obj.account_type_id,

        'balance_threshold': bet_account_obj.balance_threshold,
        'email_to_notify': bet_account_obj.email_to_notify,
        'last_email_notified': bet_account_obj.last_email_notified,

        'combo': bet_account_obj.combo,
        'double': bet_account_obj.double,
        'single': bet_account_obj.single,

        'ev_threshold_single': bb_settings['ev_threshold_single'],
        'ev_threshold_combo': bb_settings['ev_threshold_combo'],
        'ev_threshold_double': bb_settings['ev_threshold_double'],
    }
    return bet_account_data


def get_bookie_bashing_settings():
    """Returns BB settings"""
    session = loadSession()
    bookie_obj = session.query(BookieBashingAccounts).all()[0]
    session.close()
    return {
        'bookie_username': bookie_obj.user_name,
        'bookie_password': bookie_obj.password,
        'ev_threshold_single': bookie_obj.ev_threshold_single,
        'ev_threshold_combo': bookie_obj.ev_threshold_combo,
        'ev_threshold_double': bookie_obj.ev_threshold_double,
    }



def get_betting_accounts():
    session = loadSession()
    bet_accounts = session.query(BetAccounts).all()
    return bet_accounts

def get_betting_website():
    session = loadSession()
    bet_accounts = session.query(BetWesites).all()
    return bet_accounts



def get_global_settings():
    """Returns BB settings"""
    session = loadSession()
    global_settings = session.query(GlobalSettings).all()[0]
    session.close()
    return global_settings


def get_placed_bets(account_id: int, website_id: int, bet_type: str):
    """

    Returns list of placed bet for the current date.
    :param account_id:
    :param website_id:
    :return:
    """

    tz = pytz.timezone('Europe/London')
    berlin_now = datetime.now(tz)

    session = loadSession()
    logs_object = session.query(Logs)

    all_bets = logs_object.filter_by(bet_type=bet_type).filter(
        extract('year', Logs.transaction_time) == berlin_now.year).filter(
        extract('month', Logs.transaction_time) == berlin_now.month).filter(
        extract('day', Logs.transaction_time) == berlin_now.day).filter_by(website_type_id=website_id).filter_by(
        account_id=account_id).filter_by(status=True).all()
    session.close()
    return all_bets


def check_bet_status(account_id: int, website_id: int, bet_type: str, race_horse_info):
    """
    Returns true if bet is already placed.
    :param account_id:
    :param website_id:
    :return:
    """
    # Limitation can only be used for
    is_bet_placed = False
    tz = pytz.timezone('Europe/London')
    berlin_now = datetime.now(tz)

    session = loadSession()
    logs_object = session.query(Logs)
    logs_object = logs_object.filter_by(bet_type=bet_type).filter(
        extract('year', Logs.transaction_time) == berlin_now.year).filter(
        extract('month', Logs.transaction_time) == berlin_now.month).filter(
        extract('day', Logs.transaction_time) == berlin_now.day).filter_by(website_type_id=website_id).filter_by(
        account_id=account_id).filter_by(status=True)
    if bet_type == 'single':
        all_bets = logs_object.filter_by(race_horse_info=race_horse_info).all()
        if len(all_bets) != 0:
            is_bet_placed = True
    else:
        # Double and combinations. We will have to loop through all the todays bets and compare the race horse info.
        race_horse_info_local_data = race_horse_info.split('\n')
        for item in logs_object.all(): #leave this check as it is. Because sometimes the combination can be in any order. So it is necessary to compare the set of items
            race_horse_db_data = item.race_horse_info
            race_horse_db_data = race_horse_db_data.split('\n')

            if set(race_horse_db_data) == set(race_horse_info_local_data):
                is_bet_placed = True
                break
            else:
                pass
    session.close()
    return is_bet_placed



def get_all_logs_today():
    tz = pytz.timezone('Europe/London')
    berlin_now = datetime.now(tz)

    session = loadSession()
    all_logs = session.query(Logs)
        # .filter(
        # extract('year', Logs.transaction_time) == berlin_now.year).filter(
        # extract('month', Logs.transaction_time) == berlin_now.month).filter(
        # extract('day', Logs.transaction_time) == berlin_now.day)
    return all_logs



def update_logs(log_data):
    session = loadSession()
    newLog = Logs(**log_data)
    session.add((newLog))
    session.commit()
    session.close()


def update_report_logs(log_data):
    session = loadSession()
    tz = pytz.timezone('Europe/London')
    berlin_now = datetime.now(tz)
    log_data['created_at'] = berlin_now
    newLog = ReportLogs(**log_data)

    session.add((newLog))
    session.commit()
    session.close()


