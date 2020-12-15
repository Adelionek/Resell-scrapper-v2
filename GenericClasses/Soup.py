import time
import requests
from bs4 import BeautifulSoup


class Soup:
    def __init__(self, request_headers):
        self.request_headers = request_headers

    def make_soup(self, link):
        payload = {}
        headers = self.request_headers
        retry_times = 0
        while True:
            try:
                link_req = requests.request("GET", link, headers=headers, data=payload)
                link_content = link_req.text
                soup = BeautifulSoup(link_content, 'html.parser')
                if link_req.status_code == 200:
                    return soup
                else:
                    print("Error occurred while creating soup. StatusCode={} URL={}".format(link_req.status_code, link))
                    if retry_times < 4:
                        time.sleep(60)
                        retry_times += 1
                    else:
                        print("Exceeded retry times while creating soup")
                        return None
            except Exception as e:
                print("Exception while making soup: {0}".format(e))
                return None
