from monitor.selenium_chrome import get_chromedriver
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class NetBetJackPotMonitor:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.proxy = 'oliver3487:9W3LEmStvb3VLZdC_country-UnitedKingdom@proxy.packetstream.io:31112'
        self.relic_url = 'https://casino.netbet.co.uk/play/book-of-relics-mega-drop'

    def login(self, driver):
        """
        logins to netbet.com
        """
        print('Logging in')
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[placeholder="E-mail/Username"]')))
        except Exception as e:
            print(str(e))

        driver.find_element_by_css_selector('[placeholder="E-mail/Username"]').send_keys(self.username)
        sleep(1)
        driver.find_element_by_css_selector('[placeholder="Password"]').send_keys(self.password)
        #
        sleep(1)
        driver.find_element_by_xpath('//button[contains(text(),"Log in and play")]').click()
        sleep(1)
        # Wait for the balance pop up
        #
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//h4[contains(.,"Your current balance is")]')))
        except Exception as e:
            print(str(e))

        # CLOSE POPUP
        try:
            driver.find_element_by_css_selector('.close_btn_holder').click()
            print('Closed the balance popup')
        except Exception as e:
            print('No popup detected')

        # wait untill  the Loading Game message dissapears
        wait_for_instances = True

        print('Logged in')

    def check_new_instance(self):
        """

        :return:  returns 3 tokens and their jackpot value. To be run every 1 hour.
        """

    def load_book_of_relics(self):
        """
        Load and open the game completely
        :return:
        """
        pass

    def get_jackpot_tokens(self):
        """
        Use it after the login and book of relics is loaded completely
        :return:
        """
        driver = get_chromedriver(proxy=self.proxy)
        driver.get(self.relic_url)
        # # import ipdb
        self.login(driver)

        return {
            "TOKEN": {
                'EPIC': '9df7b3b2-dec3-4a08-8991-e38e956a0aea',
                'MAJOR': 'f857f635-df85-44a6-b19b-692a52ca74c6',
                'MINOR': '6f4a2200-8b9f-4482-82ee-8651078ab84f',
            },
            "DROP_AMOUNT": {
                'EPIC': '13542.50',
                'MAJOR': '4514.10',
                'MINOR': '1354.23',
            }

        }

        # return 'https://jackpot-query-mt.nyxop.net/v3/jackpots?instance=9df7b3b2-dec3-4a08-8991-e38e956a0aea&instance=f857f635-df85-44a6-b19b-692a52ca74c6&instance=6f4a2200-8b9f-4482-82ee-8651078ab84f&currency=GBP'
        # ipdb.set_trace()

        #
        #
        #
        #
        # try:
        #     driver.find_element_by_xpath('//*[@class="close_btn_holder"]').click()
        # except:
        #     pass
        #
        #
        #
        # try:
        #     driver.find_element_by_css_selector('[ng-click="popupService.closeCurrentPopup(\'canceled\')"]').click()
        #
        # except:
        #     pass
        # # driver.find_element_by_xpath('//*[@id="game-container"]').click()
        # # wait for getting logged in
        #
        # driver.find_element_by_xpath('//html').click()
        # import ipdb
        #
        # ipdb.set_trace()

        # driver = get_chromedriver(proxy=proxy)
        return 'https://jackpot-query-mt.nyxop.net/v3/jackpots?instance=9df7b3b2-dec3-4a08-8991-e38e956a0aea&instance=f857f635-df85-44a6-b19b-692a52ca74c6&instance=6f4a2200-8b9f-4482-82ee-8651078ab84f&currency=GBP'


#

# driver.find_element_by_css_selector('[placeholder="E-mail/Username"]').send_keys('Olivertabz')
# driver.find_element_by_css_selector('[placeholder="Password"]').send_keys('Macau915')

object = NetBetJackPotMonitor(username='Olivertabz', password='Macau915')
object.get_jackpot_tokens()
