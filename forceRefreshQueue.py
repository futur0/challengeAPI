import json
import time

import requests


def forceUpdate(summonerID, region):
    headers = {
        'authority': 'www.op.gg',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        # 'content-length': '0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'ext_name=ojplmecpdpgccookcobabopnaifgidhf; __hist=%5B%7B%22region%22%3A%22kr%22%2C%22summonerName%22%3A%22%EC%9A%A9%EC%82%B0%EC%A0%84%EC%9E%90%EC%83%81%EA%B0%80%20%EB%B8%94%EB%9E%99%EB%A6%AC%EC%8A%A4%ED%8A%B8%20%EC%A0%95%EC%83%81%EC%88%98%22%7D%2C%7B%22region%22%3A%22kr%22%2C%22summonerName%22%3A%22elsilver%20net%22%7D%5D',
        'dnt': '1',
        'origin': 'https://www.op.gg',
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

    response = requests.post(f'https://www.op.gg/api/summoners/{region}/{summonerID}/renewal', headers=headers)
    refreshStatus = response.json()
    print(f"Refresh triggered for {summonerID}")
    time.sleep(10)
    return refreshStatus

if __name__ == '__main__':
    # while True:
    queueData = json.loads(open("refreshQueue.json","r").read())
    for x in queueData:
        print(f"{x} renewal")
        summonerID, region = queueData[x]
        print(forceUpdate(summonerID, region))

    open("refreshQueue.json", "w").write(json.dumps({}))
    time.sleep(10)