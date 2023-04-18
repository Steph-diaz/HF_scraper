from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from food_spider.settings import USER_AGENT, CHROMEDRIVER_PATH, CHROMEPROFILE_PATH   # for helloFresh_spider.py
# from settings import USER_AGENT, CHROMEDRIVER_PATH, CHROMEPROFILE_PATH  # for helloFresh_scrape.py
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import undetected_chromedriver as uc
# from seleniumwire.undetected_chromedriver.v2 import Chrome
# This is used to access a single instance of Selenium to control a Chrome profile
class CDriver(object):
    __instance = None

    def __new__(cls):
        if CDriver.__instance is None:
            CDriver.__instance = object.__new__(cls)
            caps = DesiredCapabilities().CHROME
            caps["pageLoadStrategy"] = "none"
            caps["applicationCacheEnabled"] = "true"

            options = webdriver.ChromeOptions()

            options.add_argument("user-data-dir=" + CHROMEPROFILE_PATH)
            options.add_argument("user-agent=" + USER_AGENT)
            options.add_argument("--start-maximized")

            # prevent Selenium detection
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            CDriver.__instance.driver = webdriver.Chrome(desired_capabilities=caps, executable_path=CHROMEDRIVER_PATH, options=options)

            CDriver.__instance.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            CDriver.__instance.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": USER_AGENT})
        return CDriver.__instance
