import requests
from requests.exceptions import HTTPError
from Products.StockxProduct import StockxProduct
from Const.Currency import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random


class Stockx:
    def __init__(self):
        self.request_headers_list = [{
            'authority': 'stockx.com',
            'accept': 'application/json',
            'dnt': '1',
            'x-requested-with': 'XMLHttpRequest',
            'appos': 'web',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'appversion': '0.1',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://stockx.com/search/sneakers?s=adidas2',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': '_pk_ses.421.1a3e=*; stockx_session=b0a886bc-f000-4735-b474-0f5d22959af6; __cfduid=dc84a6ce884ae4c5bbbe7ecc01f50f4781607857489; stockx_homepage=sneakers; rskxRunCookie=0; _scid=69794e68-daaa-4689-a08a-653f2c2dbe07; IR_gbd=stockx.com; rCookie=2xu1o2c58lne31knzc5sbkim2rr2c; language_code=en; stockx_market_country=PL; _pxvid=087dda0f-3d33-11eb-b2af-0242ac12000e; _gcl_au=1.1.447518067.1607857498; stockx_product_visits=3; below_retail_type=; bid_ask_button_type=; brand_tiles_version=v1; browse_page_tile_size_update_web=true; bulk_shipping_enabled=true; default_apple_pay=false; intl_payments=true; multi_edit_option=beatLowestAskBy; product_page_affirm_callout_enabled_web=false; related_products_length=v2; riskified_recover_updated_verbiage=true; show_all_as_number=false; show_bid_education=v2; show_bid_education_times=1; show_how_it_works=true; show_watch_modal=true; pdp_refactor_web=undefined; recently_viewed_web_home=false; ops_delay_messaging_pre_checkout_ask=false; ops_delay_messaging_post_checkout_ask=false; ops_delay_messaging_selling=false; ops_delay_messaging_buying=false; ops_delay_messaging_ask_status=false; ops_delay_messaging_bid_status=false; ops_delay_messaging_pre_checkout_buy=false; ops_delay_messaging_post_checkout_buy=false; salesforce_chatbot_prod=true; web_low_inv_checkout=v0; QuantumMetricUserID=ac60b5525eda46fbacf6bad55f21e75d; QuantumMetricSessionID=319525b7894c1e882401922758634c30; is_gdpr=true; stockx_ip_region=PL; _px3=e25d45b8342ba31c6935d7664720001a234bc55f5f870982cedadc40265ea4d3:SqR2naJF0SUyk/0KmNcs2Z+zaReVGF0U/7TK8/cxxz3VdhHMuDxn53uVwbcFDEBtvDmEGGTt3ifNNsWwBUUmtQ==:1000:ejGI9pEg3jz6YgsUEPziAzK+V4xwTMdUoh2lcTgWmdsfRcEBJ/6rpAP0vE5FLPvmGkmQ2eZHbVuJtYtfwDV4HTSWVUb25nu7GFvnM/OHM6dzgLT9yemGN04VF2VY7dZOGHHjlEbyoe+17R76O33Fe6/sJ4q+qMcxnZikaLlVxVI=; IR_9060=1607858369541%7C0%7C1607857478671%7C%7C; IR_PI=56cb718c-3d30-11eb-a8cd-42010a246625%7C1607944769541; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2020-12-13T11%3A19%3A29.665Z; stockx_dismiss_modal_expiration=2020-12-20T11%3A19%3A29.662Z; _dd_s=rum=0&expire=1607859275688; _pk_id.421.1a3e=7ddbd94845b1f656.1607857490.1.1607858376.1607857490.; lastRskxRun=1607858376498; __cfduid=d1ad1006b53683ef23e2202f8885708301606496220'
        }, {
  'authority': 'stockx.com',
  'appos': 'web',
  'dnt': '1',
  'x-requested-with': 'XMLHttpRequest',
  'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5USkNNVVEyUmpBd1JUQXdORFk0TURRelF6SkZRelV4TWpneU5qSTNNRFJGTkRZME0wSTNSQSJ9.eyJodHRwczovL3N0b2NreC5jb20vY3VzdG9tZXJfdXVpZCI6ImRiYmE3NjYwLTVjZGEtMTFlOC1hZmVkLTEyZjkyNmEyYzZjNiIsImh0dHBzOi8vc3RvY2t4LmNvbS9nYV9ldmVudCI6IkxvZ2dlZCBJbiIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuc3RvY2t4LmNvbS8iLCJzdWIiOiJhdXRoMHxkYmJhNzY2MC01Y2RhLTExZTgtYWZlZC0xMmY5MjZhMmM2YzYiLCJhdWQiOiJnYXRld2F5LnN0b2NreC5jb20iLCJpYXQiOjE2MDc5MzQwMzQsImV4cCI6MTYwNzk3NzIzNCwiYXpwIjoiT1Z4cnQ0VkpxVHg3TElVS2Q2NjFXMER1Vk1wY0ZCeUQiLCJzY29wZSI6Im9mZmxpbmVfYWNjZXNzIn0.P9AXu_MRCDsKLLqRI8nSwRzHLEe0NGmf-ox8Nf45aEGSBq0TnvEwIKImP-lS4ZF84wPXcEADkoIFdvALwQ1J3KHjGPH6VnsBgWpep24ZRHwOSoJm2_TMtCqDlcIGeKAHa0Pi8ASYcypYJLtzSHqNqKe-Sjkzri1FSdDiF3fiyFz3kkDOVt-8LOArxkO8ivlx_dc04sw7ZpLW4gZ_8mSDRQ9bk4PTh14QKGIalju5vt_IKgQRVdNod8S_s8xB0yG0bybqhSigYpIpJ2Y-rQHREVh4SYJMGUREmGLhruhcHSZcDidz-FT__IZthluqfK6XOj7hJr6-tqUoMGRutvUaAg',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
  'appversion': '0.1',
  'accept': '*/*',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://stockx.com/search?s=nike',
  'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
  'cookie': '__cfduid=dc84a6ce884ae4c5bbbe7ecc01f50f4781607857489; rskxRunCookie=0; _scid=69794e68-daaa-4689-a08a-653f2c2dbe07; IR_gbd=stockx.com; rCookie=2xu1o2c58lne31knzc5sbkim2rr2c; language_code=en; stockx_market_country=PL; _pxvid=087dda0f-3d33-11eb-b2af-0242ac12000e; _gcl_au=1.1.447518067.1607857498; QuantumMetricUserID=ac60b5525eda46fbacf6bad55f21e75d; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2020-12-13T11%3A19%3A29.665Z; stockx_dismiss_modal_expiration=2020-12-20T11%3A19%3A29.662Z; stockx_seen_ask_new_info=true; stockx_user_shipping_region=PL; _ga=GA1.2.896455818.1607871259; _gid=GA1.2.596938581.1607871259; tracker_device=af9b767b-f5c7-4c9b-82b7-4b4f88cd97a8; ajs_user_id=%22dbba7660-5cda-11e8-afed-12f926a2c6c6%22; ajs_anonymous_id=%22d994a95e-d527-4946-a271-583f164498d0%22; mfaLogin=err; token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5USkNNVVEyUmpBd1JUQXdORFk0TURRelF6SkZRelV4TWpneU5qSTNNRFJGTkRZME0wSTNSQSJ9.eyJodHRwczovL3N0b2NreC5jb20vY3VzdG9tZXJfdXVpZCI6ImRiYmE3NjYwLTVjZGEtMTFlOC1hZmVkLTEyZjkyNmEyYzZjNiIsImh0dHBzOi8vc3RvY2t4LmNvbS9nYV9ldmVudCI6IkxvZ2dlZCBJbiIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuc3RvY2t4LmNvbS8iLCJzdWIiOiJhdXRoMHxkYmJhNzY2MC01Y2RhLTExZTgtYWZlZC0xMmY5MjZhMmM2YzYiLCJhdWQiOiJnYXRld2F5LnN0b2NreC5jb20iLCJpYXQiOjE2MDc5MzQwMzQsImV4cCI6MTYwNzk3NzIzNCwiYXpwIjoiT1Z4cnQ0VkpxVHg3TElVS2Q2NjFXMER1Vk1wY0ZCeUQiLCJzY29wZSI6Im9mZmxpbmVfYWNjZXNzIn0.P9AXu_MRCDsKLLqRI8nSwRzHLEe0NGmf-ox8Nf45aEGSBq0TnvEwIKImP-lS4ZF84wPXcEADkoIFdvALwQ1J3KHjGPH6VnsBgWpep24ZRHwOSoJm2_TMtCqDlcIGeKAHa0Pi8ASYcypYJLtzSHqNqKe-Sjkzri1FSdDiF3fiyFz3kkDOVt-8LOArxkO8ivlx_dc04sw7ZpLW4gZ_8mSDRQ9bk4PTh14QKGIalju5vt_IKgQRVdNod8S_s8xB0yG0bybqhSigYpIpJ2Y-rQHREVh4SYJMGUREmGLhruhcHSZcDidz-FT__IZthluqfK6XOj7hJr6-tqUoMGRutvUaAg; below_retail_type=; _pk_ses.421.1a3e=*; QuantumMetricSessionID=576a264c50692c69aa44dede262b9d5a; bid_ask_button_type=; stockx_selected_currency=EUR; is_gdpr=true; cookie_policy_accepted=true; stockx_ip_region=PL; stockx_session=8025b7dd-d250-4a5c-ae74-7af2fb84c295; brand_tiles_version=v1; browse_page_tile_size_update_web=true; bulk_shipping_enabled=true; default_apple_pay=false; intl_payments=true; multi_edit_option=beatLowestAskBy; product_page_affirm_callout_enabled_web=false; related_products_length=v2; riskified_recover_updated_verbiage=true; show_all_as_number=false; show_bid_education=v2; show_bid_education_times=1; show_how_it_works=true; show_watch_modal=false; pdp_refactor_web=undefined; recently_viewed_web_home=false; ops_delay_messaging_pre_checkout_ask=false; ops_delay_messaging_post_checkout_ask=false; ops_delay_messaging_selling=false; ops_delay_messaging_buying=false; ops_delay_messaging_ask_status=false; ops_delay_messaging_bid_status=false; ops_delay_messaging_pre_checkout_buy=false; ops_delay_messaging_post_checkout_buy=false; salesforce_chatbot_prod=true; web_low_inv_checkout=v1; stockx_product_visits=19; stockx_default_sneakers_size=All; stockx_homepage=sneakers; _px3=be977b7ff995be17f3c8d73f3346f67df6b6ddbaa1892ba8043ecedbf04a826d:YlW/DLwkXcScF5fBiI2duWai5Ls0wEv5JPEnX0Yf5IHrNud7rQU63QX3i/B8Nhzouv4CbM0ANzGrKUHcnTVO1Q==:1000:t9cwCFceCxwrAzDiUlJShsFBxZa4uIeDfE4mk+yd6Skamji9Nefuj8+fw6lUxJMyfCIYy7h77NPIZUUy9AGq1FO5tClIq4p99tYX8kBAx/iKoJMPvaOCy8dv5rmtyoQdQirJh0cG2Bc9nagEabFvoTUcfao38lzavYQmzVyHmho=; _dd_s=rum=0&expire=1607941706755; _pk_id.421.1a3e=7ddbd94845b1f656.1607857490.8.1607940807.1607939244.; _gat=1; lastRskxRun=1607940807370; IR_9060=1607940794993%7C0%7C1607939244579%7C%7C; IR_PI=56cb718c-3d30-11eb-a8cd-42010a246625%7C1608027194993; __cfduid=d1ad1006b53683ef23e2202f8885708301606496220'
}, {
  'authority': 'stockx.com',
  'appos': 'web',
  'dnt': '1',
  'x-requested-with': 'XMLHttpRequest',
  'authorization': '',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
  'appversion': '0.1',
  'accept': '*/*',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://stockx.com/search/sneakers?s=new%20balance',
  'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
  'cookie': '__cfduid=db752f586b5f762d7696980c5a09840471607940902; stockx_homepage=sneakers; language_code=en; stockx_market_country=PL; _pxvid=3b30e5b8-3df5-11eb-9fc2-0242ac120018; is_gdpr=true; stockx_ip_region=PL; stockx_session=2b14769e-6293-435a-9bdb-d2317a6c29ee; below_retail_type=; bid_ask_button_type=; brand_tiles_version=v1; browse_page_tile_size_update_web=true; bulk_shipping_enabled=true; default_apple_pay=false; intl_payments=true; multi_edit_option=beatLowestAskBy; product_page_affirm_callout_enabled_web=false; related_products_length=v2; riskified_recover_updated_verbiage=false; show_all_as_number=false; show_bid_education=v2; show_bid_education_times=1; show_how_it_works=true; show_watch_modal=true; pdp_refactor_web=undefined; recently_viewed_web_home=false; ops_delay_messaging_pre_checkout_ask=false; ops_delay_messaging_post_checkout_ask=false; ops_delay_messaging_selling=false; ops_delay_messaging_buying=false; ops_delay_messaging_ask_status=false; ops_delay_messaging_bid_status=false; ops_delay_messaging_pre_checkout_buy=false; ops_delay_messaging_post_checkout_buy=false; salesforce_chatbot_prod=true; web_low_inv_checkout=v0; _gcl_au=1.1.551579300.1607940905; _px3=7618a017f9e1c3eb28e2cb86f1e9fa8a50511f8019693c0d728e247fd4bce9f4:CEwjk900x8qq5NBtEfsYn0xpcBVgbm5MwwT0ZGIOQWnAYEhb0MIFJEeFaYNk7BxWCkdOrvluCvMfBPQBMhtfqA==:1000:sBZVlcAXQugpNBvwihYrNckT8p31ctOwNgypNirnuOPLrOgC8pcATLKc6xpU6l5pULJttldfRXqyvTzYedHrc3KQac1rx52SyiTDA1rf7+jd0ZOMwd/3cjRmED4cVhT9Y9wytzEIu+uBGHXcpVXroJyJWZz9uRrQvJcxkZESQzY=; _pk_ses.421.1a3e=*; IR_gbd=stockx.com; IR_9060=1607940905589%7C0%7C1607940905589%7C%7C; IR_PI=3ca4899e-3df5-11eb-a8cd-42010a246625%7C1608027305589; _scid=5676874d-3f0c-475d-b14c-5a260507f216; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2020-12-14T10%3A15%3A05.908Z; stockx_dismiss_modal_expiration=2020-12-21T10%3A15%3A05.907Z; QuantumMetricUserID=86bacc1978f378b8fe82d45c854c2fa5; QuantumMetricSessionID=f4bb0cb9315caa3a03a447fb78dab190; rskxRunCookie=0; rCookie=2xu1o2c58lne31knzc5sbkim2rr2c; _dd_s=rum=0&expire=1607941813418; _pk_id.421.1a3e=100ce670607d7a43.1607940906.1.1607940914.1607940906.; lastRskxRun=1607940914216; __cfduid=d1ad1006b53683ef23e2202f8885708301606496220',
  'if-none-match': 'W/"2f6ec-3qA5NZj4ZVMKVfxcevP21HlgMNw"'
}, {
  'authority': 'stockx.com',
  'appos': 'web',
  'dnt': '1',
  'x-requested-with': 'XMLHttpRequest',
  'authorization': '',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
  'appversion': '0.1',
  'accept': '*/*',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://stockx.com/search?s=yeezy',
  'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
  'cookie': '__cfduid=d133b014e376c63f8ac61346267df45e31607943701; stockx_homepage=sneakers; language_code=en; stockx_market_country=PL; _pxvid=bff6c9f2-3dfb-11eb-8e7c-0242ac12000e; stockx_session=7675c383-f625-4efb-9789-034f4736002f; _gcl_au=1.1.637044575.1607943704; below_retail_type=; bid_ask_button_type=; brand_tiles_version=v1; browse_page_tile_size_update_web=true; bulk_shipping_enabled=true; default_apple_pay=false; intl_payments=true; multi_edit_option=beatLowestAskBy; product_page_affirm_callout_enabled_web=false; related_products_length=v2; riskified_recover_updated_verbiage=false; show_all_as_number=false; show_bid_education=v2; show_bid_education_times=1; show_how_it_works=true; show_watch_modal=true; pdp_refactor_web=undefined; recently_viewed_web_home=false; ops_delay_messaging_pre_checkout_ask=false; ops_delay_messaging_post_checkout_ask=false; ops_delay_messaging_selling=false; ops_delay_messaging_buying=false; ops_delay_messaging_ask_status=false; ops_delay_messaging_bid_status=false; ops_delay_messaging_pre_checkout_buy=false; ops_delay_messaging_post_checkout_buy=false; salesforce_chatbot_prod=true; web_low_inv_checkout=v0; IR_gbd=stockx.com; _pk_ses.421.1a3e=*; _scid=b8207a25-2fe3-42fa-a1c1-2949a03bd147; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2020-12-14T11%3A01%3A45.893Z; stockx_dismiss_modal_expiration=2020-12-21T11%3A01%3A45.892Z; rskxRunCookie=0; rCookie=2xu1o2c58lne31knzc5sbkim2rr2c; QuantumMetricUserID=d1b57f90c8868ae9f8fd39eecd6dda51; QuantumMetricSessionID=5bed916dd1af498daaa501a02d3a44ed; is_gdpr=true; stockx_ip_region=PL; _px3=e210fc51c33ae2f017dc8c7180955cc0a366bf39138c01191a4583d35853f611:3g7eH4G8pr5D8IKEdHWJ21igfgAr6LkUenm3kVSfhidVYQm6PUwsQXXCBdbg+B+eHL+2Gl5Vl0gNotWloNnD6g==:1000:TR5pkraRdHF30Aii/4jU4zXAsj4YLcEA8cP/ncw2SpTt1YMl00Sa8kbC07dzYNkyqGRv44xKRO/hJLjdyWlNG/wmWQI4xxkBgUbw+wY7UDBmCf8tkIj7W43WzN8KNZK59ztl+51JJ9CNpbKHwjrHfkdbxo0ffDoJqJtXOHSL4Y8=; _dd_s=rum=0&expire=1607945191992; _pk_id.421.1a3e=1d76a011dbbbd062.1607943705.1.1607944292.1607943705.; lastRskxRun=1607944292165; IR_9060=1607943718833%7C0%7C1607943704738%7C%7C; IR_PI=c113add8-3dfb-11eb-a8cd-42010a246625%7C1608030118833; __cfduid=d1ad1006b53683ef23e2202f8885708301606496220'
}]
        self.request_headers = self.request_headers_list[0]
        self.product_info_uri = 'https://stockx.com/api/browse?&_search=PID&dataType=product&country=PL'
        self.product_bids_uri = "https://stockx.com/api/products/PRODUCT/activity?state=300&currency=EUR&limit=1000" \
                                "&page=PAGE&sort=amount&order=DESC&country=PL"
        self.payload = {}
        self.pids_not_available = self.open_files()
        # TODO remove hardcoded path
        self.file = None

    header_num = 0

    def open_files(self):
        dict = None
        try:
            dict = {
                'adidas': open('D:\\Projects\\Python\\ResellScraperv2\\txt\\adidas_PID_not_available.txt',
                               'r').readlines(),
                'nike': open('D:\\Projects\\Python\\ResellScraperv2\\txt\\nike_PID_not_available.txt', 'r').readlines()
            }
        except IOError as E:
            print('Problem with opening file')
            print(E)

        return dict

    def is_pid_available(self, pid):
        pids_a = self.pids_not_available['adidas']
        pids_n = self.pids_not_available['nike']
        if pid in pids_a or pid in pids_n:
            return False
        else:
            return True

    def get_stockx_product_info(self, pid):
        if not self.is_pid_available(pid):
            print('Skipping pid bc its not on stockX {}'.format(pid))
            return None
        url = self.product_info_uri.replace('PID', pid.replace(' ', '%20'))

        json_response = self.make_request(url, self.payload, self.request_headers)
        stockx_product = None
        if not json_response:
            return None
        if json_response['Pagination']['total'] == 0:
            # self.file.write(pid + '\n')
            return None
        for product in json_response['Products']:
            try:
                # TODO NoneType' object has no attribute 'replace'
                if product['styleId'].replace('-', '').replace(' ', '') == pid.replace('-', '').replace(' ', ''):
                    retail = product['retailPrice']
                    retail_pl = retail * EUR_PLN if retail else None
                    stockx_link = "https://stockx.com/%s" % (product['urlKey'])
                    stockx_pid = product['id']
                    stockx_product = StockxProduct(product['styleId'], product['title'], product['brand'],
                                                   retail_pl, stockx_link, stockx_pid)
                    return stockx_product
            except AttributeError as e:
                print(e)
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

    def make_request(self, link, payload, headers):
        try:
            # time.sleep(5)
            url_resp = requests.request("GET", link, headers=headers, data=payload)
            url_resp.raise_for_status()
            jsonResponse = url_resp.json()
            return jsonResponse
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            if url_resp.status_code in [403, 502]:
                self.header_num = (self.header_num + 1) % 4
                self.request_headers = self.request_headers_list[self.header_num]
                # self.refresh_stockx_cookies()
                print('calling api from scraperapi')
                new_link = "http://api.scraperapi.com?api_key=64f35214a3ab1ce53b4d73f88b4f750c&url={}".format(link)
                new_resp = self.make_request(new_link, payload, headers)
                return new_resp
            return None
        except requests.exceptions.RequestException as e:
            print("Request error: {}\nURL: {}".format(e, link))
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None

    def refresh_stockx_cookies(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        cookie = self.request_headers[0]['cookie']
        splitted = cookie.split(';')
        splitted.sort()
        old_cookies = splitted
        splitted1_keys = [s.split('=')[0].strip() for s in splitted]
        stockx_cookies_dictionary = {}
        for cookie in splitted:
            cookie.strip()
            c = cookie.split('=')
            stockx_cookies_dictionary[c[0].strip()] = c[1]

        driver = webdriver.Chrome(executable_path='D:\Projects\Python\ResellScraperv2\webDrivers\chromedriver.exe',
                                  chrome_options=chrome_options)
        driver.get('https://stockx.com/search?s=yeezy')
        time.sleep(5)
        driver.refresh()
        time.sleep(5)
        driver_cookies = driver.get_cookies()
        splitted2 = []
        for d in driver_cookies:
            splitted2.append('{0}={1}'.format(d['name'], d['value']))

        splitted2.sort()
        splitted2_keys = [s.split('=')[0].strip() for s in splitted2]
        driver_cookies_dictionary = {}
        for cookie in splitted2:
            cookie.strip()
            c = cookie.split('=')
            driver_cookies_dictionary[c[0].strip()] = c[1]

        new_cookie = []
        unique_cookie_names = []

        for sp1 in splitted1_keys:
            if sp1.strip() not in splitted2_keys:
                unique_cookie_names.append(sp1)

        for ucn in unique_cookie_names:
            new_cookie.append("{0}={1}".format(ucn, stockx_cookies_dictionary[ucn]))

        for dcd in driver_cookies_dictionary:
            new_cookie.append("{0}={1}".format(dcd, driver_cookies_dictionary[dcd]))

        str_new_cookie = '; '.join(new_cookie)
        self.request_headers['cookie'] = str_new_cookie
        print('cookies refreshed')
        print('Old cookies: ', sorted(old_cookies))
        print('New cookies: ', sorted(new_cookie))
