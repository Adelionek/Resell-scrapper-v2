from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.common.exceptions import NoSuchElementException
import time
from . import DatadomeBypass as DP


def create_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'webDrivers', 'chromedriver.exe'),
                              chrome_options=chrome_options)
    driver.get('https://allegro.pl/')
    return driver


class AllegroWebdriver:

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'webDrivers', 'chromedriver.exe'))

    def get_offers_urls(self, url):
        soup = self.make_soup_from_url(url)
        skip_val = ['emission', 'lokalnie', 'klapki']
        while True:
            try:
                offers_elements = soup.find_all("div", class_='msts_9u mp7g_oh mse2_k4 m7er_k4 _9c44d_2Narh')
                offer_urls = [offer.contents[0].attrs['href'] for offer in offers_elements if
                              not any(w in offer.contents[0].attrs['href'] for w in skip_val)]
                new_urls = []
                for url in offer_urls:
                    s = url.split('-')
                    s = "-".join(s[:-1])
                    new_urls.append(s)

                deduplicated = list(dict.fromkeys(new_urls))

                for i, ded in enumerate(deduplicated):
                    for big in offer_urls:
                        if ded in big:
                            deduplicated[i] = big
                            break

                print("Original: {0}, Urls: {1}, Deduplicated: {2}".format(len(offers_elements), len(offers_elements),
                                                                           len(deduplicated)))
                return deduplicated
            except NoSuchElementException as exception:
                print(exception)
                print('Offers links not located on page. Sleeping...')
                time.sleep(15)
                pass

    def make_soup_from_url(self, url):
        self.driver.get(url)
        time.sleep(1)
        while True:
            try:
                mainwraper = self.driver.find_element_by_class_name('main-wrapper')
                html = mainwraper.parent.page_source
                soup = BeautifulSoup(html, 'html.parser')
                return soup
            except NoSuchElementException as exception:
                print('Datadome protection. Sleeping...')
                DP.start_process(self.driver)
                time.sleep(1)
