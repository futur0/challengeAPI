import requests
from scrapy.selector import Selector
import time


class OpGGCrawler:
    def __str__(self):
        return 'OpGGCrawler'

    def __init__(self, username, region, RETRY_TIMES=5, minutes=12 * 60):
        self.username = username
        self.region = region
        self.RETRY_TIMES = RETRY_TIMES
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

        self.post_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'x-datadog-origin': 'rum',
            'x-datadog-sampled': '1',
            'x-datadog-sampling-priority': '1',
            'Origin': 'https://www.op.gg',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://www.op.gg/summoner/userName=wopazz',
            'TE': 'Trailers'
        }
        self.allowed_seconds = minutes * 60

    def get_url(self):
        """
        CREATES THE CORRECT region
        :return:
        """
        return self.REGIONS.get(self.region).format(self.username)

    def load_url(self, url, req_type='POST'):
        """
        Loads the url and returns the text
        :param url:
        :return:
        """
        URL_LOADED = False
        text_data = ''
        payload = "summonerId=86372608"
        while not URL_LOADED and self.RETRY_TIMES >= 0:
            try:
                print('{} -----> {}'.format(self.RETRY_TIMES, url))
                if req_type != 'POST':
                    response = requests.get(url=url, headers=self.HEADERS)
                else:
                    self.post_headers['Referer'] = url
                    response = requests.request("POST", url, headers=self.post_headers, data=payload)

                if response.status_code == 200:
                    text_data = response.text
                    URL_LOADED = True

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
        self.load_url(url=base_url,req_type='POST')
        time.sleep(1)
        text_data = self.load_url(base_url)
        all_data = self.parse_data(text=text_data)
        return all_data
