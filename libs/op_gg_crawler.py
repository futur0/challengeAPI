#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

# ------------------------------------------------------------
import datetime
import os
import logging
from bs4 import BeautifulSoup
import requests

from forceRefreshQueue import forceUpdate


def loggerInit(logFileName):
    try:
        os.makedirs("logs")
    except:
        pass
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
    file_handler = logging.FileHandler(f'logs/{logFileName}')
    # file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    # stream_handler.setLevel(logging.ERROR)
    logger.addHandler(stream_handler)
    return logger


logger = loggerInit(logFileName="op_gg.log")


def fetchSummonerID(region, username):
    headers = {
        'authority': 'www.op.gg',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    }

    # response = requests.get('https://www.op.gg/summoners/kr/elsilver%20net', headers=headers)
    response = requests.get(f'https://www.op.gg/summoners/{region}/{username}', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    jsonData = json.loads(soup.find("script", id='__NEXT_DATA__').text)

    championsDictRAW = jsonData['props']['pageProps']['data']['championsById']
    championsDict = {x:championsDictRAW[x]['key'] for x in championsDictRAW}
    summonerID = jsonData['props']['pageProps']['data']['summoner_id']
    return summonerID, championsDict



def loadUserProfile(region, username, observedTimeRange):
    headers = {
        'authority': 'www.op.gg',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'ext_name=ojplmecpdpgccookcobabopnaifgidhf; __hist=%5B%7B%22region%22%3A%22kr%22%2C%22summonerName%22%3A%22elsilver%20net%22%7D%2C%7B%22region%22%3A%22kr%22%2C%22summonerName%22%3A%22%EC%9A%A9%EC%82%B0%EC%A0%84%EC%9E%90%EC%83%81%EA%B0%80%20%EB%B8%94%EB%9E%99%EB%A6%AC%EC%8A%A4%ED%8A%B8%20%EC%A0%95%EC%83%81%EC%88%98%22%7D%5D',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://www.op.gg/summoners/kr/elsilver%20net',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    }
    params = {
        'hl': 'en_US',
        'game_type': 'TOTAL',
    }
    summonerID, championsDict = fetchSummonerID(region, username)

    entriesInQueue = json.loads(open("/home/ubuntu/op_gg_scraper_api/refreshQueue.json", "r").read())
    entriesInQueue[username] = (summonerID, region)

    # forceUpdate(summonerID,region)

    open("/home/ubuntu/op_gg_scraper_api/refreshQueue.json", "w").write(json.dumps(entriesInQueue, ensure_ascii=False))

    response = requests.get(f'https://www.op.gg/api/games/{region}/summoners/{summonerID}', params=params,
                            headers=headers)
    outData = response.json()
    # observedTimeRange = 5000

    results = []
    deadlineTime = datetime.datetime.timestamp(datetime.datetime.now()) - (observedTimeRange * 60)
    for x in outData['data']:
        entry = {}
        gameLength = str(datetime.timedelta(seconds=x['game_length_second'])).split(":")
        gameLengthStr = f'{gameLength[1]}m {gameLength[2]}s'
        entry["GameLength"] = gameLengthStr
        entry["GameType"] = x['queue_info']['game_type'].title()
        try: entry["KDA"] = round((x['myData']['stats']["kill"] + x['myData']['stats']["assist"]) / x['myData']['stats']["death"],2)
        except: entry["KDA"] = "Perfect KDA"
        entry["champion"] = championsDict[str(x['myData']['champion_id'])]
        entry["name"] = x['myData']['summoner']['name']
        if x['myData']['stats']['result'] == 'WIN':
            entry["result"] = 'Victory'
        elif x['myData']['stats']['result'] == 'LOSE':
            entry["result"] = 'Defeat'
        else:
            entry["result"] = x['myData']['stats']['result']
        entry["timestamp"] = str(datetime.datetime.timestamp(datetime.datetime.fromisoformat(x['created_at']))).split(".")[0]

        if datetime.datetime.timestamp(datetime.datetime.fromisoformat(x['created_at'])) < deadlineTime:
            break
        results.append(entry)

    lastFetchedTime = datetime.datetime.timestamp(datetime.datetime.fromisoformat(outData['meta']['last_game_created_at']))

    while lastFetchedTime > deadlineTime:
        params = {
            'hl': 'en_US',
            'game_type': 'TOTAL',
            'ended_at': str(outData['meta']['last_game_created_at']),
        }
        response = requests.get(f'https://www.op.gg/api/games/{region}/summoners/{summonerID}', params=params,
                                headers=headers)
        outData = response.json()
        for x in outData['data']:
            entry = {}
            gameLength = str(datetime.timedelta(seconds=x['game_length_second'])).split(":")
            gameLengthStr = f'{gameLength[1]}m {gameLength[2]}s'

            entry["GameLength"] = gameLengthStr
            entry["GameType"] = x['queue_info']['game_type'].title()
            try:entry["KDA"] = round((x['myData']['stats']["kill"] + x['myData']['stats']["assist"]) / x['myData']['stats']["death"],2)
            except: entry["KDA"] = "Perfect KDA"
            entry["champion"] = championsDict[str(x['myData']['champion_id'])]
            entry["name"] = x['myData']['summoner']['name']
            if x['myData']['stats']['result'] == 'WIN':
                entry["result"] = 'Victory'
            elif x['myData']['stats']['result'] == 'LOSE':
                entry["result"] = 'Defeat'
            else:
                entry["result"] = x['myData']['stats']['result']
            entry["timestamp"] = str(datetime.datetime.timestamp(datetime.datetime.fromisoformat(x['created_at']))).split(".")[0]

            if datetime.datetime.timestamp(datetime.datetime.fromisoformat(x['created_at'])) < deadlineTime:
                break
            results.append(entry)

        lastFetchedTime = datetime.datetime.timestamp(datetime.datetime.fromisoformat(outData['meta']['last_game_created_at']))

    entries = {}
    entries['data'] = {}
    entries['data']['count'] = len(results)
    entries['data']['results'] = results
    return results


if __name__ == '__main__':
    region, username = 'kr','elsilver%20net'
    observedTimeRange = 50000
    endDate = ''
    sample = loadUserProfile(region, username, observedTimeRange)
