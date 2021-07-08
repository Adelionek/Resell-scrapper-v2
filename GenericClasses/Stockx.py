import requests
from requests.exceptions import HTTPError
from Products.StockxProduct import StockxProduct
from Const.Currency import *
from selenium.webdriver.chrome.options import Options
import time
import pyautogui
import os
import random
from selenium import webdriver


class Stockx:
    def __init__(self):
        self.request_headers_list = [
            {
                'authority': "stockx.com",
                'appos': "web",
                'x-requested-with': "XMLHttpRequest",
                'sec-ch-ua-mobile': "?0",
                'authorization': "",
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                'appversion': "0.1",
                'accept': "*/*",
                'sec-fetch-site': "same-origin",
                'sec-fetch-mode': "cors",
                'sec-fetch-dest': "empty",
                'referer': "https://stockx.com/search?s=yeezy",
                'accept-language': "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
                'cookie': "_pxvid=2638991c-87bc-11eb-8d51-0242ac120010; _scid=bb278f4f-9d07-4a11-8e6b-cd2101264d21; _fbp=fb.1.1616052775468.1512743026; _px_f394gi7Fvmc43dfg_user_id=MjdjZDlkMDAtODdiYy0xMWViLTlmMmMtNzNhZDk0ZThiY2Y1; QuantumMetricUserID=956ee6dcda1bac7b622d71231759ba9b; rskxRunCookie=0; rCookie=iyvmzr2igdaz3bbyyp2uikmek3imk; _ga=GA1.2.522846141.1616052827; tracker_device=658e0c03-2df0-44f1-948e-4dcd83135bbe; stockx_seen_ask_new_info=true; ajs_anonymous_id=%22493b7ba2-13ad-4605-9d29-bfe7a25d8e45%22; ajs_user_id=%22d146558e-7e5e-11ea-b5c9-124738b50e12%22; stockx_experiments_id=web-61766968-43a2-4a9b-af32-d4daef82d74a; _rdt_uuid=1621339681588.06ff227e-26aa-4a64-bc53-9fdb0e68a852; ajs_group_id=%22ab_buy_now_rage_click_android.false%2Cab_conversion_module_location_ios.neither%2Cab_cross_sell_pdp_ios.neither%2Cab_ios_seller_profile_redesign.novariant%2Cab_multiask_redesign_android_v2.false%2Cab_product_page_refactor_ios_v3.false%2Cab_seller_profile_redesign_android.false%2Cab_test_most_popular_by_region_web.true%2Cab_test_product_page_refactor_web.false%2Cab_web_platform_targeting_test.false%22; _pk_id.421.1a3e=95f97e33a775061f.1616052775.157.1621957734.1621955632.; stockx_homepage=sneakers; language_code=en; stockx_market_country=PL; pxcts=df2bc880-dcd7-11eb-8f5e-ff71bbdf6131; stockx_session=3c8cec77-8e52-46f3-912b-b08e75aa9d07; _gcl_au=1.1.279748316.1625410568; _px3=4e872d45276a42b36aac51024248d3c095fc7098cf2fb5274e409b8d6924a1d0:8B20J7Qk9IfFRgwdx0PBJYYTD2mZM6d+EAEA2caErVfWWzXNYFiXagMNwZ8+1287ZKZIzYuHJrTph3FXhAAepQ==:1000:aKsRX0MGjmUvO+3YU+ifTM093L9KvzXNikNLBgQcIV8rnL13nJa7B34KHQoL+423fB4AKpFpYEmYpcITZ7WV8vSwGQIKtbXXvcqNc8m8rfrzOGxUUoNywMQj9Ra0OgJq2Nq5zSCRpqYVZ5bAgv0RgV64f87lLhNX/9C7Goy+KYy5sejFJ/0Aihgt4KbRkN4ceCctFtZMXHCkdJcy4XUyjw==; _uetsid=f6be37a0dcd711eba8745d7a524a90f3; _uetvid=d0aa8e40bd6b11ebb1cb851c7536a1f2; IR_gbd=stockx.com; IR_9060=1625410568092%7C0%7C1625410568092%7C%7C; __pdst=e3b9be5cd9a1470a84d86dd0f9ff113a; IR_PI=27180943-87bc-11eb-a4a8-42010a24662e%7C1625496968092; below_retail_type=; product_page_affirm_callout_enabled_web=false; riskified_recover_updated_verbiage=true; recently_viewed_web_home=false; home_vertical_rows_web=true; ops_banner_id=blteaa2251163e21ba6; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2021-07-04T14%3A56%3A10.009Z; stockx_dismiss_modal_expiration=2021-07-11T14%3A56%3A10.009Z; QuantumMetricSessionID=d5ad50f91c8348329abb4f5eec2882d2; _px_7125205957_cs=eyJpZCI6ImY3ODU5YmUwLWRjZDctMTFlYi05MGYzLTIzMDVhZTJmYWUzOSIsInN0b3JhZ2UiOnt9LCJleHBpcmF0aW9uIjoxNjI1NDEyMzc0MDQ1fQ==; _dd_s=rum=0&expire=1625411475660; lastRskxRun=1625410576271",
                'cache-control': "no-cache"
            }
        ]
        self.request_headers = self.request_headers_list[0]
        self.product_info_uri = 'https://stockx.com/api/browse?&_search=PID&dataType=product&country=PL'
        self.product_bids_uri = "https://stockx.com/api/products/PRODUCT/activity?state=300&currency=EUR&limit=1000" \
                                "&page=PAGE&sort=amount&order=DESC&country=PL"
        self.payload = {}
        self.pids_not_available = None
        self.file = None
        # TODO remove hardcoded path

    header_num = 0

    def is_pid_available(self, pid):
        pid = pid + '\n'
        if pid in self.pids_not_available:
            return False
        else:
            return True

    def get_stockx_product_info(self, pid):
        # if not self.is_pid_available(pid):
        #     # print('Skipping pid bc its not on stockX {}'.format(pid))
        #     return None

        url = self.product_info_uri.replace('PID', pid.replace(' ', '%20'))
        json_response = self.make_request(url, self.payload, self.request_headers)
        stockx_product = None
        if not json_response:
            return None
        # if json_response['Pagination']['total'] == 0:
        #     file_pid = pid + '\n'
        #     if file_pid not in self.pids_not_available:
        #         self.file.write(file_pid)
        #     return None
        for product in json_response['Products']:
            try:
                # TODO NoneType' object has no attribute 'replace'
                if product['brand'].lower() not in ['reebok', 'nike', 'puma', 'adidas', 'new balance']:
                    continue
                if product['styleId'].replace('-', '').replace(' ', '') == pid.replace('-', '').replace(' ', ''):
                    retail = product['retailPrice']
                    retail_pl = retail * EUR_PLN if retail else None
                    stockx_link = "https://stockx.com/%s" % (product['urlKey'])
                    stockx_pid = product['id']
                    stockx_product = StockxProduct(product['styleId'], product['title'], product['brand'],
                                                   retail_pl, stockx_link, stockx_pid)
                    stockx_product.gender = product['gender']
                    return stockx_product
            except AttributeError as e:
                print("Get stockx product info error: {}".format(e))
                pass

        return stockx_product

    def get_stockx_product_bids(self, stockx_product):
        stockx_product_bids = []
        page = 1
        next_page = 'page'
        while next_page:
            url = "https://stockx.com/api/products/{}/activity?state=300&currency=EUR&limit=1000&page=" \
                  "{}&sort=amount&order=DESC&country=PL".format(stockx_product.stockx_pid.replace(' ', '%20'), page)
            url_resp = self.make_request(url, self.payload, self.request_headers)

            if not url_resp:
                return None

            json_response = url_resp
            if json_response.get('ProductActivity'):
                stockx_product_bids += (json_response['ProductActivity'])
            next_page = json_response['Pagination']['nextPage']
            page += 1
        return stockx_product_bids

    def calculate_payout(self, bid_price):
        pass

    def get_last_sales(self, stockx_product):
        pass

    # TODO switch user agents
    def make_request(self, link, payload, headers):
        try:
            # time.sleep(1)
            url_resp = requests.request("GET", link, headers=headers, data=payload)
            url_resp.raise_for_status()
            jsonResponse = url_resp.json()
            return jsonResponse
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            if url_resp.status_code in [403, 502]:
                while True:
                    print("While loop, sleeping")
                    self.hold_W(4, link)
                    time.sleep(10)
                    for i in range(4):
                        self.header_num = (self.header_num + i) % 3
                        self.request_headers = self.request_headers_list[0]
                        # print('calling api from scraperapi')
                        # new_link = "http://api.scraperapi.com?api_key=64f35214a3ab1ce53b4d73f88b4f750c&url={}".format(link)
                        new_resp = requests.request("GET", link, headers=self.request_headers, data=payload)
                        if new_resp.status_code == 200:
                            print("response 200 after 403")
                            return new_resp.json()
            return None
        except requests.exceptions.RequestException as e:
            print("Request error: {}\nURL: {}".format(e, link))
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None

    def hold_W(self, hold_time, link):
        driver2 = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'webDrivers', 'chromedriver.exe'))
        driver2.get(link)
        time.sleep(5)
        pyautogui.moveTo(250, 431)
        start = time.time()
        while time.time() - start < hold_time:
            pyautogui.mouseDown()
        pyautogui.mouseUp()
        pyautogui.moveTo(601, 390, 1, pyautogui.easeInQuad)
        pyautogui.moveTo(301, 190, 2, pyautogui.easeInQuad)
        driver2.close()
