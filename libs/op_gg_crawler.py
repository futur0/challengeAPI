import random

import requests
from scrapy.selector import Selector
import time
from urllib.parse import quote


class OpGGCrawler:
    def __str__(self):
        return 'OpGGCrawler'

    def __init__(self, username, region, RETRY_TIMES=5, minutes=12 * 60):
        self.username = username
        self.region = region
        self.RETRY_TIMES = RETRY_TIMES

        self.BAD_GAME_TYPE = [
            'ARAM',
            'BOT'
        ]  # ADDED NOV6, 2021

        self.REGIONS = {
            'KR': 'https://www.op.gg/summoner/userName={}',
            'JP': 'https://jp.op.gg/summoner/userName={}',
            'NA': 'https://na.op.gg/summoner/userName={}',
            'EUW': 'https://euw.op.gg/summoner/userName={}',
            'EUNE': 'https://eune.op.gg/summoner/userName={}',
            'OCE': 'https://oce.op.gg/summoner/userName={}',
            'BR': 'https://br.op.gg/summoner/userName={}',
            'LAS': 'https://las.op.gg/summoner/userName={}',
            'LAN': 'https://lan.op.gg/summoner/userName={}',
            'RU': 'https://ru.op.gg/summoner/userName={}',
            'TR': 'https://tr.op.gg/summoner/userName={}',

        }
        self.PROXY = 'exito0:69VxUEcbiQrubdy9@proxy.packetstream.io:31112'
        self.PROXY = 'amitupreti:RefzyvyXp1QVZRfx@proxy.packetstream.io:31112'
        self.PROXY_DICT = {"http": f"http://{self.PROXY}",
                           "https": f"http://{self.PROXY}"
                           }

        self.HEADERS = {
            'authority': 'www.op.gg',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.130 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://jp.op.gg/',
            'accept-language': 'en-US,en;q=0.9',
            'sec-gpc': '1',
        }
        self.cookies = {
            '_hist': quote(self.username),  # added cookies 25 oct , 2021 Without cookies, the website was rejecting update request and sending us in a loop

        }

        self.post_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.op.gg',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://www.op.gg/summoner/userName=%EC%9D%B4%EC%BF%A0%EC%97%90%EC%BF%A0%EB%8F%99%EC%BF%A0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
        }
        self.allowed_seconds = minutes * 60

    def get_url(self):
        """
        CREATES THE CORRECT region
        :return:
        """
        return self.REGIONS.get(self.region).format(quote(self.username))

    def load_url(self, url, req_type):
        """
        Loads the url and returns the text
        :param url:
        :return:
        """
        URL_LOADED = False
        text_data = ''
        # self.payload =f"summonerId={str(random.randint(33092139-1000,33092139+1000))}" #changed summonerId (doesnot seem to matter what id we use)
        # changed summonerId appraoch 25 OCt, 2021
        while not URL_LOADED and self.RETRY_TIMES >= 0:
            try:
                print('{} -----> {}'.format(self.RETRY_TIMES, url))
                if req_type != 'POST':

                    response = requests.get(url=url, headers=self.HEADERS,
                                            # proxies=self.PROXY_DICT
                                            )
                else:
                    self.payload = f"summonerId={self.summoner_id}"
                    self.post_headers['Referer'] = url
                    url = url.split('userName')[0] + 'ajax/renew.json/'
                    headers = self.post_headers.copy()
                    headers['Referer'] = self.get_url()  # To accomodate all region, Seems like we have to set the referrer and origin correctly
                    headers['Origin'] = self.get_url().split('/summoner')[0]
                    headers['Cookie'] = f'_hist={quote(self.username)}'

                    #
                    response = requests.request("POST", url, headers=headers, data=self.payload,
                                                # proxies=self.PROXY_DICT
                                                )  # Updated 25 oct 2021, Added cookies and quoted url to reduce the errors

                if (response.status_code == 200 or response.status_code == 418) and 'error has occurred' not in response.text:
                    text_data = response.text
                    break

                self.RETRY_TIMES -= 1

            except Exception as e:
                print(e)
                self.RETRY_TIMES -= 1
        return text_data

    def parse_data(self, text):
        """
        parses the text and then returns the json data
        :param text:
        :return:
        """
        response = Selector(text=text)
        boxes = response.css('[class="GameItemWrap"]')
        curr_time = int(time.time())
        all_data = []
        for box in boxes:
            try:
                champion = box.xpath('.//*[@class="ChampionName"]/a/text()').get('')
                result = box.xpath('.//*[@class="GameResult"]/text()').get('').strip()
                kda = ''.join(box.css('.KDARatio').xpath('./text()').getall()).strip().replace('KDA', '').strip().split(':')[0]
                name = self.username
                timestamp = int(box.css('._timeago').xpath('./@data-datetime').get(''))
                game_type = box.xpath('.//*[@class="GameType"]/text()').get('').strip()
                GameLength = box.xpath('.//*[@class="GameLength"]/text()').get('').strip()
                # GameLength

                skip_bool = False
                for skip_game in self.BAD_GAME_TYPE:
                    print(skip_game.lower(),game_type.lower())
                    if skip_game.lower() in game_type.lower():
                        skip_bool = True
                        break


                if skip_bool:
                    continue
                data = {
                    "name": name,
                    "timestamp": timestamp,
                    "result": result,
                    "KDA": kda,
                    "champion": champion,
                    'GameType': game_type,
                    'GameLength': GameLength,
                }
                if (curr_time - timestamp) <= self.allowed_seconds:
                    all_data.append(data)
            except Exception as e:
                print(e)
        return all_data

    def get_data(self):
        base_url = self.get_url()
        # Get summnor ID
        text_data = self.load_url(base_url, 'GET')
        self.summoner_id = Selector(text=text_data).xpath('//*[@class="MostChampionContent"]/@data-summoner-id').get('')
        text = self.load_url(url=base_url, req_type='POST')  # request to update the data
        time.sleep(random.randint(1, 3) * 0.5)  # Wait for 2-3 seconds randomly(Added more to be on the safe side)
        text_data = self.load_url(base_url, 'GET')
        all_data = self.parse_data(text=text_data)
        return all_data
