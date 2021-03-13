import time
import requests
from bs4 import BeautifulSoup
import random
from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options

def open_ua_file():
    file_path = os.path.join(os.getcwd(), 'txt', 'userAgents.txt')
    file = open(file_path, 'r')
    return file


class Soup:
    def __init__(self, request_headers):
        self.request_headers = request_headers
        self.proxies = [{'http': 'http://18.196.102.225:3128'},
                        {'http': 'http://88.198.24.108:8080'}]
        self.user_agents = open_ua_file().readlines()

    def switch_ua(self):
        ua_len = len(self.user_agents)
        rand = random.randint(0, ua_len-1)
        self.request_headers['user-agent'] = self.user_agents[rand].rstrip()

    def make_soup(self, link):
        payload = {}
        headers = self.request_headers
        retry_times = 0
        while True:
            try:
                rand = random.randint(1, 1)
                self.switch_ua()
                # link_req = requests.request("GET", link, headers=headers, data=payload, proxies=self.proxies[rand])
                link_req = requests.request("GET", link, headers=headers, data=payload)
                print('sleeping for {0} sec...'.format(rand))
                time.sleep(rand)
                link_content = link_req.text
                if link_req.status_code == 200:
                    print('passed')
                    soup = BeautifulSoup(link_content, 'html.parser')
                    return soup
                else:
                    print("not passed")

                    while True:
                        # new_link = "http://api.scraperapi.com?api_key=64f35214a3ab1ce53b4d73f88b4f750c&url={}".format(link)
                        self.switch_ua()
                        link_req = requests.request("GET", link, headers=headers, data=payload)
                        link_content = link_req.text
                        soup = BeautifulSoup(link_content, 'html.parser')
                        if link_req.status_code == 200:
                            # print('passed')
                            return soup
                        else:
                            pass

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
