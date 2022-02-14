import requests
import time
from urllib.parse import quote
import json
from bs4 import BeautifulSoup
import datetime

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

    def string_to_delta(self, string_delta):

        # check if day, month or year
        value, unit, _ = string_delta.split()

        if unit == 'hour':
            value = 1        # bcz value = 'an'
            unit = 'hours'
        
        if unit == 'day':
            value = 1        # bcz value = 'a'
            unit = 'days'
        if unit == 'month':
            value = 1 * 30   # bcz value = 'a'
            unit = 'days'   
        if unit == 'months':
            value = int(value) * 30
            unit = 'days'
        if unit == 'year':
            value = 1 * 365
            unit = 'days'
        if unit == 'years':
            value = int(value) * 365
            unit = 'days'
            
        return int(datetime.timedelta(**{unit: float(value)}).total_seconds())


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
        soup = BeautifulSoup(r.text , features="lxml" )

        script_list = soup.find_all('script')
        li_list = soup.find_all('li')

        #find the json file correct index (it changes !)
        script_header = {'id': '__NEXT_DATA__', 'type': 'application/json'}
        idx = [idx for idx, element in enumerate(script_list) if script_list[idx].attrs == script_header][0]
        script = script_list[idx].text.strip()
    
        try:
            id = json.loads(script)['props']['pageProps']['data']['id']
        except:
            id = ''
            print('user not found')

        li_header = {'class': ['css-ja2wlz', 'e1iiyghw3']}
        idx = [idx for idx, element in enumerate(li_list) if li_list[idx].attrs == li_header]

        curr_time = int(time.time())
        all_data = []
        try:
            for i in idx:
                block = li_list[i].find_all('div')

                name = self.username
                timestamp = block[4].contents[0]
                result = block[6].contents[0]
                kda = block[23].contents[0].text.split(':')[0]
                champion = block[20].contents[0] 
                game_type = block[2].contents[0]
                try:
                    GameLength = block[7].contents[0].split(':')[0] + 'm'  + ' ' + block[7].contents[0].split(':')[1] + 's'
                except:
                    GameLength = ' '
                    
                time_delta = curr_time - self.string_to_delta(timestamp)
                
                for skip_game in self.BAD_GAME_TYPE:
                    if skip_game.lower() in game_type.lower():
                        continue
                
                data = {
                            "name": name,
                            "timestamp": time_delta,
                            "result": result,
                            "KDA": kda,
                            "champion": champion,
                            'GameType': game_type,
                            'GameLength': GameLength
                        }

                if (curr_time - time_delta) <= self.allowed_seconds:
                    all_data.append(data)


        except Exception as e:
                print(e)

        return id, all_data



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
