
import requests
from urllib.parse import quote
import requests
import json
from bs4 import BeautifulSoup


class OpGGValidator:
    def __str__(self):
        return 'OpGGValidator'

    def __init__(self, username, region, RETRY_TIMES=5):
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

    def get_url(self):
        """
        CREATES THE CORRECT region
        :return:
        """
        return self.REGIONS.get(self.region).format(quote(self.username))


    def find_id_using_bs4(self, url, headers):

        r = requests.get(url , headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        script_list = soup.find_all('script')

        #find the json file correct index (it changes !)
        json_header = {'id': '__NEXT_DATA__', 'type': 'application/json'}
        idx = [idx for idx, element in enumerate(script_list) if script_list[idx].attrs == json_header][0]
        script = script_list[idx].text.strip()

        try:
            id = json.loads(script)['props']['pageProps']['data']['id']
        except:
            id = ''
            print('user not found')

        return id


    def run(self):

        user = self.username
        region = self.region.lower()

        base_url = 'https://na.op.gg/summoners/' + region + '/' + user
        id = self.find_id_using_bs4(base_url , self.HEADERS)

        if id != '':

            return 1
        
        else:
            
            return 0