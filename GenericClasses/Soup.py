import time
import requests
from bs4 import BeautifulSoup
import random


class Soup:
    def __init__(self, request_headers):
        self.request_headers = request_headers
        self.proxies = [{'http': 'http://18.196.102.225:3128'},
                        {'http': 'http://88.198.24.108:8080'}]

    def make_soup(self, link):
        payload = {}
        headers = self.request_headers
        retry_times = 0
        while True:
            try:
                rand = random.randint(0, 1)
                link_req = requests.request("GET", link, headers=headers, data=payload, proxies=self.proxies[rand])
                link_content = link_req.text
                soup = BeautifulSoup(link_content, 'html.parser')
                if link_req.status_code == 200:
                    return soup
                else:
                    # print('Calling scraperAPI')
                    new_link = "http://api.scraperapi.com?api_key=64f35214a3ab1ce53b4d73f88b4f750c&url={}".format(link)
                    link_req = requests.request("GET", new_link, headers=headers, data=payload,
                                                proxies=self.proxies[rand])
                    link_content = link_req.text
                    soup = BeautifulSoup(link_content, 'html.parser')
                    return soup

                    # print("Error occurred while creating soup. StatusCode={} URL={}".format(link_req.status_code, link))
                    # if retry_times < 1:
                    #     # time.sleep(60)
                    #     retry_times += 1
                    # else:
                    #     print("Exceeded retry times while creating soup")
                    #     return None

            except Exception as e:
                print("Exception while making soup: {0}".format(e))
                return None
