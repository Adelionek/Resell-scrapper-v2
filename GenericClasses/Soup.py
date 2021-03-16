import time
import requests
from bs4 import BeautifulSoup
import random
from selenium import webdriver
import os
from cookies import RefreshCookies


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
        rand = random.randint(0, ua_len - 1)
        new_ua = self.user_agents[rand].rstrip()
        self.request_headers['user-agent'] = new_ua
        return new_ua

    def make_soup(self, link):
        payload = {}
        headers = self.request_headers
        while True:
            try:
                rand = random.randint(2, 100)
                self.switch_ua()
                # print('sleeping for {0} sec...'.format(rand))
                # time.sleep(rand)
                link_req = requests.request("GET", link, headers=headers, data=payload)
                link_content = link_req.text

                if link_req.status_code == 200:
                    # print('passed')
                    soup = BeautifulSoup(link_content, 'html.parser')
                    return soup
                else:
                    while True:
                        print("not passed")
                        self.switch_ua()

                        if 'allegro' in link:

                            new_cookie = RefreshCookies.start_process()
                            self.request_headers['cookie'] = new_cookie
                            print('new cookie applied')

                            new_link = "http://api.scraperapi.com?api_key=64f35214a3ab1ce53b4d73f88b4f750c"\
                            "&url={0}&session_number={1}".format(link, rand)
                            link_req = requests.request("GET", new_link, headers=self.request_headers, data=payload)
                            if link_req.status_code == 200:
                                soup = BeautifulSoup(link_content, 'html.parser')
                                return soup
                            else:
                                print("Didnt get 200 while invoking scraperapi, retrying")
                                pass
                        else:
                            time.sleep(60)
                            link_req = requests.request("GET", link, headers=self.request_headers, data=payload)
                            link_content = link_req.text
                            if link_req.status_code == 200:
                                soup = BeautifulSoup(link_content, 'html.parser')
                                print('passed after fail')
                                return soup
                            else:
                                pass



            except Exception as e:
                print("Exception while making soup: {0}".format(e))
                return None


    # def create_soup_from_content
