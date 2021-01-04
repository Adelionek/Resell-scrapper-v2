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
  'cookie': '__cfduid=dea078ea4978b641ec04a5d67dd6a590c1609163239; cf_clearance=04f91b7ddba96e9d76a8ab5014b0fe47073cab5e-1609710490-0-250; ajs_user_id=%22d146558e-7e5e-11ea-b5c9-124738b50e12%22; ajs_anonymous_id=%225275da7b-9a4b-40e2-94b2-8be38f057935%22; _scid=d2c9f3fd-b945-4ea0-8925-788746169130; QuantumMetricUserID=da2a9aec94e13ecb63fa5080edfc89d4; _pxvid=0cb31dd7-4e16-11eb-a9aa-0242ac120017; _gcl_au=1.1.319618014.1609714229; rskxRunCookie=0; rCookie=53iay4clxv6ii9izj3yunkjhqanpx; stockx_homepage=sneakers; language_code=en; stockx_market_country=PL; is_gdpr=true; stockx_ip_region=PL; stockx_session=be5290bc-9da3-46d7-a254-cdf8a1115118; below_retail_type=; bid_ask_button_type=; brand_tiles_version=v1; browse_page_tile_size_update_web=true; bulk_shipping_enabled=true; default_apple_pay=false; intl_payments=true; multi_edit_option=beatLowestAskBy; product_page_affirm_callout_enabled_web=false; related_products_length=v2; riskified_recover_updated_verbiage=true; show_all_as_number=false; show_bid_education=v2; show_bid_education_times=1; show_how_it_works=true; show_watch_modal=true; pdp_refactor_web=undefined; recently_viewed_web_home=false; ops_delay_messaging_pre_checkout_ask=false; ops_delay_messaging_post_checkout_ask=false; ops_delay_messaging_selling=false; ops_delay_messaging_buying=false; ops_delay_messaging_ask_status=false; ops_delay_messaging_bid_status=false; ops_delay_messaging_pre_checkout_buy=false; ops_delay_messaging_post_checkout_buy=false; salesforce_chatbot_prod=true; web_low_inv_checkout=v0; _px3=886467362b0d37a4b15e0c9be5e90636a56c3f508183fe7d817141a820395700:V3FQ76ZxksbCJ9dmcHXXYA+SQl/x1sgroOHWlrgswbSGdfxunwuwoJouAb09hWWG3QvLZRQpu/fud+9xm1La5A==:1000:C/OFoQJ7pv6o1K/RGJOd/wNOiHznFfxZ8oaEnf1JaVdZV5z/RnkvbAifkYGHCD8En5tBTvyEW4Xj6fYdMAxJrgVImf03xlDDMAGlyOgLnZJWbO9G89GO2KnCpRONonEAyPweCYUE8WD19k9S8hl6brqcBC2Ygb519bOKjPfLoac=; IR_gbd=stockx.com; IR_9060=1609762686717%7C0%7C1609762686717%7C%7C; IR_PI=3572472e-4913-11eb-a8cd-42010a246625%7C1609849086717; _pk_ses.421.1a3e=*; QuantumMetricSessionID=bae142b49883a25b379ad7efdd81d514; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2021-01-04T12%3A18%3A14.758Z; stockx_dismiss_modal_expiration=2021-01-11T12%3A18%3A14.755Z; _dd_s=rum=0&expire=1609763611208; _pk_id.421.1a3e=e52f58f246d1e66b.1609163243.17.1609762711.1609762687.; lastRskxRun=1609762711641; __cfduid=d7f59d621ac9b56bb0492f438fd4c5da81609098328'
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
  'cookie': '__cfduid=d3c87e36efe0e1ae9159ffba984db7da91609762840; stockx_homepage=sneakers; stockx_market_country=PL; _pxvid=43140dac-4e87-11eb-a268-0242ac12000d; stockx_session=b20926f8-45f6-4ab7-811c-cc28b53f8c9b; below_retail_type=; bid_ask_button_type=; brand_tiles_version=v1; browse_page_tile_size_update_web=true; bulk_shipping_enabled=true; default_apple_pay=false; intl_payments=true; multi_edit_option=beatLowestAskBy; product_page_affirm_callout_enabled_web=false; related_products_length=v2; riskified_recover_updated_verbiage=true; show_all_as_number=false; show_bid_education=v2; show_bid_education_times=1; show_how_it_works=true; show_watch_modal=true; pdp_refactor_web=undefined; recently_viewed_web_home=false; ops_delay_messaging_pre_checkout_ask=false; ops_delay_messaging_post_checkout_ask=false; ops_delay_messaging_selling=false; ops_delay_messaging_buying=false; ops_delay_messaging_ask_status=false; ops_delay_messaging_bid_status=false; ops_delay_messaging_pre_checkout_buy=false; ops_delay_messaging_post_checkout_buy=false; salesforce_chatbot_prod=true; web_low_inv_checkout=v0; _gcl_au=1.1.1492549214.1609762846; stockx_selected_currency=EUR; language_code=en; stockx_selected_locale=en; stockx_selected_region=PL; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2021-01-04T12%3A20%3A46.531Z; stockx_dismiss_modal_expiration=2022-01-04T12%3A20%3A46.529Z; IR_9060=1609762847269%7C0%7C1609762847269%7C%7C; IR_gbd=stockx.com; _pk_id.421.1a3e=4268a045481cd7ef.1609762847.1.1609762847.1609762847.; _pk_ses.421.1a3e=*; IR_PI=45ff693c-4e87-11eb-a8cd-42010a246625%7C1609849247269; _scid=deaece4f-7346-46c5-987e-2b4dcae734d0; QuantumMetricSessionID=9a5e770cca9495331067539854e02e7b; QuantumMetricUserID=3e93681e4e3aa1bfa79e06a8d1c6bdca; _dd_s=rum=0&expire=1609763749817; is_gdpr=true; stockx_ip_region=PL; _px3=a394340fda6f03b0bbaf13173d7d0e193605b58629bf52645496d4a97e8b5d20:RR4aZ4G/UZp/+ec0s9PN1s7+Cttn67clZMjC9hDsUBCsijevWk92i6zljAAqLOoertNGb5OCOySVAL1+cqGbQg==:1000:vaq9KzxH1glfTdiePGeykiygNujgpxAXtZdk9kTPWL8wyYycHbXcefn2yj6dtepJfr6iaf62D1QEGrJWS+yfmqLcLz8Kzc/nhjRs9BxUzmYIW7D1v2W04XQ+Cym5tSfuv86kYDSmQGltSEU45379dKFKpX80TqD4+UZvr42FDvE=; __cfduid=d7f59d621ac9b56bb0492f438fd4c5da81609098328',
  'if-none-match': 'W/"342da-GwbNDhq/Sx71+rstkRUOwU22nXU"'
},
            {
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
                'referer': 'https://stockx.com/search?s=yeezy1',
                'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': '__cfduid=d1c9f3a262a6302c462c786e4bcd566bf1609770609; stockx_homepage=sneakers; stockx_market_country=PL; _pxvid=59d391b4-4e99-11eb-8947-0242ac120003; stockx_session=4144714b-e350-4045-bc36-4369e89d112f; _gcl_au=1.1.1417446819.1609770612; below_retail_type=; bid_ask_button_type=; brand_tiles_version=v1; browse_page_tile_size_update_web=true; bulk_shipping_enabled=true; default_apple_pay=false; multi_edit_option=beatLowestAskBy; intl_payments=true; product_page_affirm_callout_enabled_web=false; related_products_length=v2; riskified_recover_updated_verbiage=true; show_all_as_number=false; show_bid_education=v2; show_bid_education_times=1; show_how_it_works=true; show_watch_modal=false; pdp_refactor_web=undefined; recently_viewed_web_home=false; ops_delay_messaging_pre_checkout_ask=false; ops_delay_messaging_post_checkout_ask=false; ops_delay_messaging_selling=false; ops_delay_messaging_buying=false; ops_delay_messaging_ask_status=false; ops_delay_messaging_pre_checkout_buy=false; ops_delay_messaging_bid_status=false; ops_delay_messaging_post_checkout_buy=false; salesforce_chatbot_prod=true; web_low_inv_checkout=v0; IR_gbd=stockx.com; _pk_ses.421.1a3e=*; _scid=aed02e45-1045-47e4-b2f8-39829b236763; QuantumMetricSessionID=d28be2aa370e28158a59a22b94cab246; QuantumMetricUserID=b836313567d8f2acc8836a42078b9d67; rskxRunCookie=0; rCookie=53iay4clxv6ii9izj3yunkjhqanpx; stockx_selected_currency=EUR; language_code=en; stockx_selected_locale=en; stockx_selected_region=PL; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2021-01-04T14%3A30%3A19.717Z; stockx_dismiss_modal_expiration=2022-01-04T14%3A30%3A19.717Z; is_gdpr=true; stockx_ip_region=PL; stockx_product_visits=2; IR_9060=1609770623536%7C0%7C1609770613601%7C%7C; IR_PI=5b1d6dda-4e99-11eb-a8cd-42010a246625%7C1609857023536; _dd_s=rum=0&expire=1609771536524; _pk_id.421.1a3e=2febdcc4f266d763.1609770614.1.1609770637.1609770614.; lastRskxRun=1609770636727'
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
                self.header_num = (self.header_num + 1) % 3
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
