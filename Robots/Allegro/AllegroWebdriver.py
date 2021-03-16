from bs4 import BeautifulSoup
from selenium import webdriver
import os

from selenium.common.exceptions import NoSuchElementException

from Robots import AllegroRobot
import time


class AllegroWebdriver:

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'webDrivers', 'chromedriver.exe'))

    def get_offers_urls(self, url):
        soup = self.make_soup_from_url(url)
        while True:
            try:
                offers_elements = soup.find_all("div", class_='msts_9u mp7g_oh mse2_k4 m7er_k4 _9c44d_2Narh')
                offer_urls = [offer.contents[0].attrs['href'] for offer in offers_elements if 'emission'
                              not in offer.contents[0].attrs['href']]
                return offer_urls
            except NoSuchElementException as exception:
                print(exception)
                print('Offers links not located on page. Sleeping...')
                time.sleep(15)
                pass

    def make_soup_from_url(self, url):
        self.driver.get(url)
        time.sleep(3)
        while True:
            try:
                mainwraper = self.driver.find_element_by_class_name('main-wrapper')
                html = mainwraper.parent.page_source
                soup = BeautifulSoup(html, 'html.parser')
                return soup
            except NoSuchElementException as exception:
                print(exception)
                print('html.parser elementnot located on page. Sleeping...')
                time.sleep(15)
