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
            'cookie': '__cfduid=d33aca2c178cf77c7dc82df8c1d4efc371608985205; stockx_homepage=sneakers; language_code=en; stockx_market_country=PL; is_gdpr=true; stockx_ip_region=PL; stockx_session=eae1730b-247a-4b21-ae62-e4ea296020c7; _gcl_au=1.1.492563348.1608985207; below_retail_type=; bid_ask_button_type=; brand_tiles_version=v1; browse_page_tile_size_update_web=true; bulk_shipping_enabled=true; default_apple_pay=false; intl_payments=true; multi_edit_option=beatLowestAskBy; product_page_affirm_callout_enabled_web=false; related_products_length=v2; riskified_recover_updated_verbiage=false; show_all_as_number=false; show_bid_education=v2; show_bid_education_times=1; show_how_it_works=true; show_watch_modal=true; pdp_refactor_web=undefined; recently_viewed_web_home=false; ops_delay_messaging_pre_checkout_ask=false; ops_delay_messaging_post_checkout_ask=false; ops_delay_messaging_selling=false; ops_delay_messaging_buying=false; ops_delay_messaging_ask_status=false; ops_delay_messaging_bid_status=false; ops_delay_messaging_pre_checkout_buy=false; ops_delay_messaging_post_checkout_buy=false; salesforce_chatbot_prod=true; web_low_inv_checkout=v0; _pk_ses.421.1a3e=*; IR_gbd=stockx.com; IR_9060=1608985207525%7C0%7C1608985207525%7C%7C; IR_PI=b0f9794f-4774-11eb-a8cd-42010a246625%7C1609071607525; _px3=14243d0248a0ce51d11929fd73d6fd2d225bc4dfb585a9b0266407e1ecf9e548:gquI5vDjnh6He8M1cb9YcE7HmKThfKkPIvXyylNwNiirQ8KE6fw3TGRMhvol2NQ3+BQJTAuBTyPkcNCa1TWsjg==:1000:RZhfO5sod++1Tg8EZsHLBun+74hjbW5qa9aRZMaxERPsZkQwoeV52uaiiruvfN8cm4d82fUvelJ9v+twyh71HaBq/YAM2iM3hfSL6F/9LKAZJH+ANkwznyy4A+nxeYMQV+0lRacsSEJjss+WKQwrqBYrrGNrBh+TdSg7kGrOQ90=; _scid=0fb54553-0561-47ca-8964-b81a225d5ddb; rskxRunCookie=0; rCookie=w96dlokp7mtm5dw9ji5hrokj1jznya; QuantumMetricUserID=99c87bd3d278bbc43d3056f315bdfafe; QuantumMetricSessionID=781f8db0fe2a27d4cf361e11cf21e686; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2020-12-26T12%3A20%3A08.796Z; stockx_dismiss_modal_expiration=2021-01-02T12%3A20%3A08.796Z; _pxvid=b42ae1e5-4774-11eb-87d7-0242ac12000c; _dd_s=rum=0&expire=1608986128443; _pk_id.421.1a3e=fc1c3dc2f0f11d7e.1608985207.1.1608985228.1608985207.; lastRskxRun=1608985228639; __cfduid=d1ad1006b53683ef23e2202f8885708301606496220'
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
            'cookie': '_pk_ses.421.1a3e=*; rskxRunCookie=0; _scid=d90a6d91-93b2-429f-bc83-4bd3c577c06c; IR_gbd=stockx.com; rCookie=w96dlokp7mtm5dw9ji5hrokj1jznya; _pxvid=703c7075-4775-11eb-ab27-0242ac12000d; QuantumMetricUserID=c0a422cfde80243b514873ee598ae910; QuantumMetricSessionID=93907da6ad0cc7b9839741d307dab455; _dd_s=rum=0&expire=1608986434933; _pk_id.421.1a3e=66abd08559be727a.1608985527.1.1608985536.1608985527.; lastRskxRun=1608985535712; IR_9060=1608985527733%7C0%7C1608985228828%7C%7C; IR_PI=b0f9794f-4774-11eb-a8cd-42010a246625%7C1609071927733; stockx_session=38bb618f-2ed5-430f-a048-6d5576db4067; __cfduid=d1ad1006b53683ef23e2202f8885708301606496220',
            'if-none-match': 'W/"33cea-ZwyFbWBgXEOP/q/pb8cc9RAsE2s"'
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
            'referer': 'https://stockx.com/search/sneakers?s=nike',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': '_pk_ses.421.1a3e=*; rskxRunCookie=0; _scid=5b02445e-54cf-4231-8e19-caab8077c615; IR_gbd=stockx.com; rCookie=w96dlokp7mtm5dw9ji5hrokj1jznya; _pxvid=9323b48c-4775-11eb-94a3-0242ac120005; QuantumMetricUserID=f8371a05b898cc035342bff5cac3179a; QuantumMetricSessionID=98f984f54468e010a0935937f0856259; _dd_s=rum=0&expire=1608986492285; _pk_id.421.1a3e=6f677cb48415bd9c.1608985586.1.1608985593.1608985586.; stockx_homepage=sneakers; lastRskxRun=1608985593075; IR_9060=1608985586290%7C0%7C1608985535886%7C%7C; IR_PI=b0f9794f-4774-11eb-a8cd-42010a246625%7C1609071986290; stockx_session=3c4243e9-9383-4f52-883d-8c1cf23e7a3b'
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
        if not self.is_pid_available(pid):
            # print('Skipping pid bc its not on stockX {}'.format(pid))
            return None
        url = self.product_info_uri.replace('PID', pid.replace(' ', '%20'))

        json_response = self.make_request(url, self.payload, self.request_headers)
        stockx_product = None
        if not json_response:
            return None
        if json_response['Pagination']['total'] == 0:
            file_pid = pid + '\n'
            if file_pid not in self.pids_not_available:
                self.file.write(file_pid)
            return None
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
                self.header_num = (self.header_num + 1) % 4
                self.request_headers = self.request_headers_list[self.header_num]
                # self.refresh_stockx_cookies()
                # print('calling api from scraperapi')
                # new_link = "http://api.scraperapi.com?api_key=64f35214a3ab1ce53b4d73f88b4f750c&url={}".format(link)
                new_resp = requests.request("GET", link, headers=headers, data=payload)
                if new_resp.status_code != 200:
                    return None
                else:
                    return new_resp.json()
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
