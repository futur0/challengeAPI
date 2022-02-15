import requests
from urllib.parse import quote
import json
import datetime

class Crawler:
    def __str__(self):
        return 'Crawler'

    def __init__(self, username, region, RETRY_TIMES=5, minutes=12 * 60):

        self.username = username
        self.region = region
        self.RETRY_TIMES = RETRY_TIMES

        self.BAD_GAME_TYPE = [
            'ARAM',
            'Bot'
        ]  # ADDED NOV6, 2021

        self.URL = {
            'KR': 'https://api.tracker.gg/api/v2/lol/standard/matches/riot/{}?region=KR&type=',
            'JP': 'https://api.tracker.gg/api/v2/lol/standard/matches/riot/{}?region=JP&type=',
            'NA': 'https://api.tracker.gg/api/v2/lol/standard/matches/riot/{}?region=NA&type=',
            'EUW': 'https://api.tracker.gg/api/v2/lol/standard/matches/riot/{}?region=EUW&type=',
            'EUNE': 'https://api.tracker.gg/api/v2/lol/standard/matches/riot/{}?region=EUNE&type=',
            'OCE': 'https://api.tracker.gg/api/v2/lol/standard/matches/riot/{}?region=OCE&type=',
            'BR': 'https://api.tracker.gg/api/v2/lol/standard/matches/riot/{}?region=BR&type=',
            'LAS': 'https://api.tracker.gg/api/v2/lol/standard/matches/riot/{}?region=LAS&type=',
            'LAN': 'https://api.tracker.gg/api/v2/lol/standard/matches/riot/{}?region=LAN&type=',
            'RU': 'https://api.tracker.gg/api/v2/lol/standard/matches/riot/{}?region=RU&type=',
            'TR': 'https://api.tracker.gg/api/v2/lol/standard/matches/riot/{}?region=TR&type=',

        }
        self.PROXY = 'exito0:69VxUEcbiQrubdy9@proxy.packetstream.io:31112'
        self.PROXY = 'amitupreti:RefzyvyXp1QVZRfx@proxy.packetstream.io:31112'
        self.PROXY_DICT = {"http": f"http://quote{self.PROXY}",
                           "https": f"http://{self.PROXY}"
                           }

        self.TRACKERS_HEADERS = {
            'authority': 'www.api.tracker.gg',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.130 Safari/537.36',
            'accept': 'application/json',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://api.tracker.gg/',
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
        return self.URL.get(self.region).format(quote(self.username))

    def load_url(self, url):
        """
        Loads the url and returns the text
        :param url:
        :return:
        """
        
        URL_LOADED = False
        text_data = ''
        
        while not URL_LOADED and self.RETRY_TIMES >= 0:
            try:
                print('{} -----> {}'.format(self.RETRY_TIMES, url))
                response = requests.get(url=url, headers=self.TRACKERS_HEADERS)

                if response.status_code == 200:
                    text_data = response.text
                    break

                self.RETRY_TIMES -= 1

            except Exception as e:
                print(e)
                self.RETRY_TIMES -= 1
        return text_data

    def parse_json(self , string):

        # getting current time in timestamp
        now = datetime.datetime.now()

        # getting all matches data 
        all_matches_data = json.loads(string)['data']['matches']

        all_data = []

        try:
            for match in all_matches_data:

                # game type (starting with it to omit other ops when bad game type)
                gameType = match['metadata']['queueName']

                for skip_game in self.BAD_GAME_TYPE:
                    if skip_game.lower() in gameType.lower():
                        continue

                # timestamp
                timestamp_str = match['metadata']['timestamp']
                date_format = datetime.datetime.fromisoformat(timestamp_str)
                timestamp_game = datetime.datetime.timestamp(date_format)
                delta = datetime.datetime.timestamp(now) - timestamp_game

                # game length
                gameLength = match['metadata']['duration']['displayValue']

            
                # champion name
                championName = match['segments'][0]['metadata']['championName']

                # result
                result = match['segments'][0]['stats']['win']['value']
                result = 'Victory' if result else 'Defeat'

                # KDA calculation
                kills = int(match['segments'][0]['stats']['kills']['displayValue'])
                deaths = int(match['segments'][0]['stats']['deaths']['displayValue'])
                assists = int(match['segments'][0]['stats']['assists']['displayValue'])

                if deaths > 0:
                    KDA = (kills + assists)/deaths
                    KDA = str(round(KDA, 2))

                elif deaths == 0:
                    # perfect
                    KDA = '20'


                # put data in dictionnary
                data = {
                        "name": self.username,
                        "timestamp": timestamp_game,
                        "result": result,
                        "KDA": KDA,
                        "champion": championName,
                        'GameType': gameType,
                        'GameLength': gameLength
                        }

                # add only most recent match acording to allowed minutes in request
                if delta <= self.allowed_seconds:
                    all_data.append(data)

        except Exception as e:
            print('Exception : ', e)

        return all_data



    def get_data(self):

        # get url depending on region and user
        base_url = self.get_url()
        # get json data from url
        json_string = self.load_url(base_url)
        # parse json text into list of dictionnaries
        all_data = self.parse_json(json_string)

        return all_data
