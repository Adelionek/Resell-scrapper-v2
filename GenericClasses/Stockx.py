import requests
from requests.exceptions import HTTPError
from Products.StockxProduct import StockxProduct
from Const.Currency import *
from selenium.webdriver.chrome.options import Options
import time
import random


class Stockx:
    def __init__(self):
        self.request_headers_list = [
            {
                'authority': 'stockx.com',
                'appos': 'web',
                'dnt': '1',
                'x-requested-with': 'XMLHttpRequest',
                'authorization': '',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                'appversion': '0.1',
                'accept': '*/*',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://stockx.com/search?s=yeezy',
                'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': 'lastRskxRun=1611909286117; QuantumMetricUserID=3648103c5ab96c15b8375727bf88a956; QuantumMetricSessionID=49d26c714ccc2c025270e930a312ad02; rCookie=ow8cfwna6x2vrmjxmpqi2kkfdnh4h; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2021-01-29T08%3A34%3A48.757Z; stockx_dismiss_modal_expiration=2021-02-05T08%3A34%3A48.756Z; __cfduid=db91da5fa6cfb40a8cb0c3bc7ed14f6a41611909290; stockx_homepage=sneakers; language_code=en; stockx_market_country=PL; _pxvid=db0d117b-620c-11eb-bfb3-0242ac12000e; is_gdpr=true; stockx_ip_region=PL; _gcl_au=1.1.1771123155.1611909293; IR_gbd=stockx.com; IR_9060=1611909294176%7C0%7C1611909294176%7C%7C; below_retail_type=; brand_tiles_version=v1; bulk_shipping_enabled=true; default_apple_pay=false; related_products_length=v2; riskified_recover_updated_verbiage=false; product_page_affirm_callout_enabled_web=false; multi_edit_option=beatLowestAskBy; intl_payments=true; show_all_as_number=false; show_how_it_works=true; show_watch_modal=true; pdp_refactor_web=undefined; recently_viewed_web_home=false; salesforce_chatbot_prod=true; web_low_inv_checkout=v1; home_vertical_rows_web=false; ops_banner_id=blteaa2251163e21ba6; IR_PI=dc468200-620c-11eb-9a1b-42010a246625%7C1611995694176; _scid=1d7b551a-5d10-4c0e-b687-6059411764e1; _px_f394gi7Fvmc43dfg_user_id=ZGQyZmQwODAtNjIwYy0xMWViLWI1MDctNmRjYTA5ODcyMDk3; _px3=08a98fa4d077f31dc5657e6fa16789a6ec85175f13b74563604deceb6824fe8b:dceAbN5aXlprVMxHr9yalSKqUP9myuRN8yv+Mqig7LjxaoZV6l2yg6H8B0yr7UM3HkVmoUMILi07DJIwpRpcsw==:1000:KSVVXM3x1lo/wdniUxcvlhy7TkeApB4NE0gyFfv4gJ68x65UoPD3f/dzySF+ZgedJmBk6wwKm2B3+cnPgUKivjkh90e7EXnomZkk1xU1A9HTr0kzUqHf9QJpFJkWTNjjfTO57KvyQhT58rKza0ZjBC7rCGiWHKu3vgBOIXnE0BA=; _px_7125205957_cs=eyJpZCI6IjlkOTg2NjAwLTYyMjMtMTFlYi1iNTA3LTZkY2EwOTg3MjA5NyIsInN0b3JhZ2UiOnt9LCJleHBpcmF0aW9uIjoxNjExOTIwODk0NzEzfQ==; _dd_s=rum=0&expire=1611919998243; _pk_id.421.1a3e=145bd360b973e476.1611909294.2.1611919098.1611909294.; _pk_ses.421.1a3e=1; stockx_session=5fb5d480-ac46-4c0d-be5a-9aadef1554aa',
                'if-none-match': 'W/"34228-PH0ickGOGQ9hJTfjXhHZo7WGJ9w"'
            },
            {
                'authority': 'stockx.com',
                'appos': 'web',
                'dnt': '1',
                'x-requested-with': 'XMLHttpRequest',
                'authorization': '',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                'appversion': '0.1',
                'accept': '*/*',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://stockx.com/search?s=yeezy2',
                'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': '__cfduid=d9939df0946dbe380cfa43a1f429bd6911611919138; stockx_homepage=sneakers; language_code=en; stockx_market_country=PL; _pxvid=c89a90aa-6223-11eb-b098-0242ac120003; is_gdpr=true; stockx_ip_region=PL; stockx_session=c2a056b7-45c5-4041-97cd-52ef1fdedb5e; _px3=a04bf22c13949fa652349e0af104524a932842efe347ff36be3ff0b64bfe1bed:UgI7nunIWucbUuCgc2PRHF36HiInxTHPChtmyub4KnNmFRjHiIMbx4ajyfS175eFX8hB54rZKdYkZVAJYviiQg==:1000:/U40eMi2Yla/6F/NTrcxPlHpoUzyqfrmVUox24kL5ixyhxUgxmhRpKYzL38jM+3UcrYX8ucqNfWK+JxnNA80a+ilRb928CH/CKBbX/6yVnnHuyiorxEhASL1OUOBWz9G+rEOd5p6gUjLvtNQ65kNy7dPeW4vXsAGOoiCa3sPfL8=; _gcl_au=1.1.1954284711.1611919142; below_retail_type=; brand_tiles_version=v1; bulk_shipping_enabled=true; default_apple_pay=false; intl_payments=true; multi_edit_option=beatLowestAskBy; product_page_affirm_callout_enabled_web=false; related_products_length=v2; riskified_recover_updated_verbiage=false; show_all_as_number=false; show_how_it_works=true; show_watch_modal=true; pdp_refactor_web=undefined; recently_viewed_web_home=false; salesforce_chatbot_prod=true; web_low_inv_checkout=v1; home_vertical_rows_web=false; ops_banner_id=blteaa2251163e21ba6; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2021-01-29T11%3A19%3A02.742Z; stockx_dismiss_modal_expiration=2021-02-05T11%3A19%3A02.741Z; IR_gbd=stockx.com; IR_9060=1611919143815%7C0%7C1611919143815%7C%7C; _pk_ses.421.1a3e=1; IR_PI=dc468200-620c-11eb-9a1b-42010a246625%7C1612005543815; _scid=908bbca6-b554-45f5-ac1c-673c6fcd74e1; _px_f394gi7Fvmc43dfg_user_id=Y2JhYjk4NTAtNjIyMy0xMWViLTllYzctNjU1YjQzMmJlMGU3; QuantumMetricUserID=3648103c5ab96c15b8375727bf88a956; QuantumMetricSessionID=49d26c714ccc2c025270e930a312ad02; rskxRunCookie=0; rCookie=ow8cfwna6x2vrmjxmpqi2kkfdnh4h; _px_7125205957_cs=eyJpZCI6ImM3YTVjNzgwLTYyMjMtMTFlYi1iNTA3LTZkY2EwOTg3MjA5NyIsInN0b3JhZ2UiOnt9LCJleHBpcmF0aW9uIjoxNjExOTIwOTU3NzA0fQ==; _dd_s=rum=0&expire=1611920059492; _pk_id.421.1a3e=23dc6c88b56acaf6.1611919144.1.1611919159.1611919144.; lastRskxRun=1611919159662'
            },
            {
                'authority': 'stockx.com',
                'appos': 'web',
                'dnt': '1',
                'x-requested-with': 'XMLHttpRequest',
                'authorization': '',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                'appversion': '0.1',
                'accept': '*/*',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://stockx.com/search?s=nike',
                'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': '__cfduid=dd5b61fd3ea7e7064d7b1c6e55662c7e91611919191; _pk_ses.421.1a3e=1; stockx_homepage=sneakers; rskxRunCookie=0; _scid=f1e4d575-63f8-4f18-9639-4f4710b74e99; IR_gbd=stockx.com; rCookie=ow8cfwna6x2vrmjxmpqi2kkfdnh4h; stockx_session=08fbfb83-0cb6-41c4-bfbf-c61673768b3a; QuantumMetricUserID=3648103c5ab96c15b8375727bf88a956; QuantumMetricSessionID=49d26c714ccc2c025270e930a312ad02; _px_7125205957_cs=eyJpZCI6ImU2NmVjYTkwLTYyMjMtMTFlYi05ZWM3LTY1NWI0MzJiZTBlNyIsInN0b3JhZ2UiOnt9LCJleHBpcmF0aW9uIjoxNjExOTIxMDAzMTUwfQ==; _dd_s=rum=0&expire=1611920106215; _pk_id.421.1a3e=7b62419f2dedae11.1611919192.1.1611919206.1611919192.; lastRskxRun=1611919206397; IR_9060=1611919193680%7C0%7C1611919159905%7C%7C; IR_PI=dc468200-620c-11eb-9a1b-42010a246625%7C1612005593680',
                'if-none-match': 'W/"34ef7-RGYNgbpM1jKLP9KmjL3GjqIjcK0"'
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
                    time.sleep(120)
                    for i in range(4):
                        self.header_num = (self.header_num + i) % 3
                        self.request_headers = self.request_headers_list[self.header_num]
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
