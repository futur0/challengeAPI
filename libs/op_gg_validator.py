import random

import requests
from scrapy.selector import Selector
import time
from urllib.parse import quote
from multiprocessing import Pool
from multiprocessing import Process



class OpGGValidator:
    def __str__(self):
        return 'OpGGValidator'

    def __init__(self, username, region, RETRY_TIMES=5):
        self.username = username
        self.region = region
        self.RETRY_TIMES = RETRY_TIMES

        self.BAD_GAME_TYPE = [
            'ARAM',
            'Bot'
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

    def get_url(self):
        """
        CREATES THE CORRECT region
        :return:
        """
        return self.REGIONS.get(self.region).format(quote(self.username))

    def get_data(self, tuple):
        # changed 10/dec/2021 : input data as tuple for multiprocessing
        """
        Loads the url and returns the text
        :param url:
        :return:
        """
        url, req_type = tuple
        URL_LOADED = False
        text_data = ''
        # self.payload =f"summonerId={str(random.randint(33092139-1000,33092139+1000))}" #changed summonerId (doesnot seem to matter what id we use)
        # changed summonerId appraoch 25 OCt, 2021
        while not URL_LOADED and self.RETRY_TIMES >= 0:
            try:
                print('{} -----> {}'.format(self.RETRY_TIMES, url))
                
                response = requests.get(url=url, headers=self.HEADERS,
                                            # proxies=self.PROXY_DICT
                                            )

                if (response.status_code == 200 or response.status_code == 418) and 'error has occurred' not in response.text:
                    text_data = response.text
                    break

                self.RETRY_TIMES -= 1

            except Exception as e:
                print(e)
                self.RETRY_TIMES -= 1

        return text_data

    def find_summoner_id(self, text_data):

        id = Selector(text=text_data).xpath('//*[@class="MostChampionContent"]/@data-summoner-id').get('')
        id2 = Selector(text=text_data).xpath('//*[@class="GameListContainer"]/@data-summoner-id').get('')

        if id != '': return id
        elif id2!= '': return id2
        else : return ''

    def run(self):

        base_url = self.get_url()
        # Get summnor ID
        text_data = self.get_data((base_url, 'GET'))
        id = self.find_summoner_id(text_data)

        if id != '':

            return 1
        
        return 0
