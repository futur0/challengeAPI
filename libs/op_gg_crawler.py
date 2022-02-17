import requests
from urllib.parse import quote
import json
import datetime
from scrapy.selector import Selector

class OpGGCrawler:
    def __str__(self):
        return 'OpGGCrawler'

    def __init__(self, username, region, RETRY_TIMES=5, minutes=12 * 60):
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
            # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept' : 'application/json',
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
        # changed 10/dec/2021 : input data as tuple for multiprocessing
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
                    # self.payload = f"summonerId={str(random.randint(33092139-1000,33092139+1000))}"
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

                # if (response.status_code == 200 or response.status_code == 418) and 'error has occurred' not in response.text:
                if (response.status_code == 200 or response.status_code == 418):
                    text_data = response.text
                    break

                self.RETRY_TIMES -= 1

            except Exception as e:
                print(e)
                self.RETRY_TIMES -= 1
        return text_data



    def find_id_and_data(self, url, headers):

        r = requests.get(url , headers=headers)
        
        # soup = BeautifulSoup(r.text)

        response = Selector(text=r.text)

        # script_list = soup.find_all('script')
        # script_header = {'id': '__NEXT_DATA__', 'type': 'application/json'}
        # idx = [idx for idx, element in enumerate(script_list) if script_list[idx].attrs == script_header][0]
        # script = script_list[idx].text.strip()

        # update 17/2/22
        # json location changes, so loop over all of the available json to get the correct one
        all_json_path = response.xpath('//script//text()')

        for element in all_json_path:
            try:
                json_str = element.root
            except:
                continue
        
        id = json.loads(json_str)['props']['pageProps']['data']['id']
        
        champions = json.loads(json_str)['props']['pageProps']['data']['championsById']

        all_matches = json.loads(json_str)['props']['pageProps']['games']['data']

        now = datetime.datetime.now()
        all_data = []
        try:
            for match in all_matches:

                name = self.username
                timestamp_str = match['created_at']
                date_format = datetime.datetime.fromisoformat(timestamp_str)
                timestamp_game = datetime.datetime.timestamp(date_format)
                delta = datetime.datetime.timestamp(now) - timestamp_game

                result = match['myData']['stats']['result']
                result = 'Victory' if result=='WIN' else 'Defeat'

                # kda = (kills+assists)/deaths
                kills = match['myData']['stats']['kill']
                deaths = match['myData']['stats']['death']
                assists = match['myData']['stats']['assist']

                if deaths > 0:
                    kda = (kills + assists) / deaths
                    kda = str(round(kda , 2))

                if deaths == 0:
                    kda = '20'

                champion_id = match['myData']['champion_id']
                champion = champions[str(champion_id)]['name']

                game_type = match['queue_info']['queue_translate']
                
                game_length_sec = match['game_length_second']
                game_length = str(game_length_sec // 60) + 'm ' + str(game_length_sec % 60) + 's'

                for skip_game in self.BAD_GAME_TYPE:
                    if skip_game.lower() in game_type.lower():
                        continue
                
                data = {
                            "name": name,
                            "timestamp": int(timestamp_game),
                            "result": result,
                            "KDA": kda,
                            "champion": champion,
                            'GameType': game_type,
                            'GameLength': game_length
                        }

                if delta <= self.allowed_seconds:
                    all_data.append(data)


        except Exception as e:
                print(e)

        return id , all_data



    def get_data(self):

        # url for posting
        base_url = self.get_url()

        # new way of finding id
        user = self.username
        region = self.region.lower()
        site_url = 'https://na.op.gg/summoners/' + region + '/' + user

        # get id and player data
        self.summoner_id , all_data = self.find_id_and_data(site_url , self.HEADERS)

        text = self.load_url(base_url, 'POST')

        return all_data
