
import requests
from urllib.parse import quote
import requests


class Validator:

    def __str__(self):
        return 'Validator'

    def __init__(self, username, region, RETRY_TIMES=5):
        self.username = username
        self.region = region
        self.RETRY_TIMES = RETRY_TIMES

        

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
                    resp = 'exist'
                    break

                if response.status_code == 400:
                    # bad url
                    resp = 'not existing'

                self.RETRY_TIMES -= 1

            except Exception as e:
                print(e)
                self.RETRY_TIMES -= 1
        return resp

    def run(self):

        # get url depending on region and user
        base_url = self.get_url()
        # get json data from url
        resp = self.load_url(base_url)
        

        if resp == 'exist':

            return 1
        
        else:
            
            return 0