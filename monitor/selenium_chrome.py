

import os
import zipfile
import  os
# from fake_useragent import UserAgent
# from selenium import webdriver
from seleniumwire import  webdriver
from configs.env import config

APP_ENV = os.environ.get('APP_ENV', 'DEV')
PROJECT_PATH = config[APP_ENV]['PROJECT_PATH']

def get_chromedriver(proxy):
    PROXY_HOST = proxy.split('@')[1].split(':')[0]
    PROXY_PORT = proxy.split('@')[1].split(':')[1]
    PROXY_USER = proxy.split('@')[0].split(':')[0]
    PROXY_PASS = proxy.split('@')[0].split(':')[1]

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    # ua = UserAgent()
    # userAgent = ua.data_browsers['firefox'][0]
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
    # userAgent = 'Mozilla/5.0 (Linux; Android 9; SM-G950F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36'
    print('User agent setup', userAgent)

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_GB'})
    chrome_options.add_argument('--lang=es')

    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument(f'user-agent={userAgent}')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument(
        '--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    prefs = {"credentials_enable_service", False}
    prefs = {"profile.password_manager_enabled": False}
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile': {
            'password_manager_enabled': False
        }
    })
    #
    if proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    
    CHROME_DRIVER_PATH = os.path.join(PROJECT_PATH,'monitor/chromedriver')
    print(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=chrome_options) #/home/amitupreti/betting-automation/scraping/chromedriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                           "userAgent": userAgent})

    driver.set_window_position(0, 0)
    driver.set_window_size(1920,1080)
    return driver
