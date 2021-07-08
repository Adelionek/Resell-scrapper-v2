import time

from Robots.SiteRobot import SiteRobot
from Products.SourceProduct import SourceProduct
from Products.OutputProduct import OutputProduct
from GenericFunctions.Functions import *
from Const.Currency import *
import re
import json
from .Allegro import AllegroConst, AllegroWebdriver as awd
import datetime


class AllegroRobotClass(SiteRobot):
    def __init__(self):
        super().__init__(request_headers={
            'authority': 'allegro.pl',
            'dpr': '2',
            'viewport-width': '750',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS i686 1660.57.0) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.46 Safari/535.19',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'referer': 'https://allegro.pl/oferta/fiskars-zestaw-5-nozy-noz-blok-857197-legendarny-7582593446?reco_id=36805f06-7b4e-11eb-8ac9-0c42a10e6d08&sid=e87b00735b7a626d8cf4ab04068da77c41db6208f84b5c14d8d681dddc612d88&bi_m=mpage&',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': '_ga=GA1.2.499925289.1615639123; _gat_UA-2827377-1=1; cartUserId=ba3gh4rr-ajuu-5bhd-cuc3-f48d7js56bjm; _gcl_au=1.1.1268673892.1615639122; datadome=MZf0jOwdebRRGEpdfhgXyLPbphnhEt2roJ~7eYu9_1tLk_nSaeyaX5AY~fixjrBnPbYeBVv0g4APovElWtOTH4Bj2zo8nnmHxW-1zo6vBO; _ga_2FTJ836HTM=GS1.1.1615639122.1.0.1615639122.60; _gid=GA1.2.696275626.1615639123; __gfp_64b=zFN7fJwNZnUtvyp5w4rSjWSRqNV0KM0hgP5iLe4jWRL.x7|1615639121; _cmuid=ba3gh4rr-ajuu-5bhd-cuc3-f48d7js56bjm;'
        })
        self.site_configuration = {
            "title_class": ['h1', '_1s2v1 _1djie _4lbi0'],
            "nick_class": ['a', '_w7z6o _15mod _9a071_3tKtu'],
            "price": ['div', '_1svub _lf05o _9a071_3SxcJ'],
            "ship_country": ['div', '_15mod _1vryf _34279_13Rv4'],
            "offer_title": ['h2', 'mgn2_14 m9qz_yp mqu1_16 mp4t_0 m3h2_0 mryx_0 munh_0'],
            "sizes_tile": ['div', '_1nfka _9a071_2llTZ'],
            "current_size": ['div', '_17qy1 _1vryf _f8818_1X1F-']
        }
        self.allegro_driver = awd.AllegroWebdriver()

    def get_available_sizes(self, soup):
        available_sizes = []
        tiles = soup.find_all(self.site_configuration['sizes_tile'][0], self.site_configuration['sizes_tile'][1])

        if not tiles:
            col = soup.find_all(self.site_configuration['current_size'][0], self.site_configuration['current_size'][1])
            for t in col:
                if t.text == 'Rozmiar:':
                    size = t.next_sibling.text
                    if size != 'inny':
                        available_sizes.append(size)
                        return available_sizes

        for size in tiles:
            try:
                found_size = re.search(SIZE_PATTERN, size.text).group(0)
                if found_size:
                    available_sizes.append(found_size)
            except Exception as e:
                pass

        return available_sizes

    def get_auction_seller_and_title(self, soup):
        self.site_configuration['nick_class'] = ['a', '_w7z6o _15mod _9a071_3tKtu']
        self.site_configuration['title_class'] = ['h1', '_1s2v1 _1djie _4lbi0']

        try:
            seller_name = soup.find_all('a', '_w7z6o _15mod _9a071_3tKtu')[0].text.split(' ')[0].strip()
            auction_title = soup.find_all('h1', '_1s2v1 _1djie _4lbi0')[0].text
        except IndexError as ie:
            seller_name = soup.find_all('div', '_1s2v1 _1djie')[0].text.split(' ')[1]
            auction_title = soup.find_all('h4', '_18vat _9a071_U7GFO _1s2v1 _dsf2b')[0].text
            print('switched config')

    def validate_offer(self, soup, offer_link):
        try:
            seller_name = soup.find_all(self.site_configuration['nick_class'][0],
                                        self.site_configuration['nick_class'][1])[0].text.split(' ')[0].strip()
            auction_title = soup.find_all(self.site_configuration['title_class'][0],
                                          self.site_configuration['title_class'][1])[0].text
        except Exception as e:
            print('Uunhandled seller name and action title exception: ', e)
            return False

        if seller_name in AllegroConst.FAKE_SELLERS:
            return False
        for washed in AllegroConst.WASHED_TITLES:
            if washed in auction_title.lower():
                return False

        if 'lokalnie' in offer_link:
            print('Local offer, skipping')
            return False
        if any(elem.text in ['Chiny', 'Holandia'] for elem in soup.find_all(
                self.site_configuration['ship_country'][0], self.site_configuration['ship_country'][1])):
            return False
        return True

    def validate_link(self, offer_link):
        pids_not_available = [pid.strip().replace(" ", "-") for pid in self.stockxManager.pids_not_available]
        unwanted_titles = ['max-90', 'air-max-90']
        pids_not_available += unwanted_titles
        contains_pid = any(pid in offer_link for pid in pids_not_available)

        if contains_pid:
            return False
        return True

    def find_pid_pattern(self, soup, offer_link, brand):
        pattern = switch(brand, 'pattern')
        params_pid = [pid.text.split(':')[1] for pid in soup.find_all("li", "_f8818_2jDsV")
                      if 'Kod producenta' in pid.text]
        if params_pid:
            if self.validate_pid(params_pid[0], pattern):
                return params_pid[0]

        content = self.get_site_content(offer_link, soup)
        found_pid = re.findall(pattern, content)

        if found_pid:
            for pid in found_pid:
                if self.validate_pid(pid, pattern):
                    return pid

        return None

    def get_product_list(self, page_link, page):
        product_list = []
        uri = page_link + '&p={}'.format(page)
        print('PAGE: {} URI: {}'.format(page, uri))
        soup = self.siteSoup.make_soup(uri)
        if not soup:
            return None

        offers = soup.find_all(self.site_configuration['offer_title'][0], self.site_configuration['offer_title'][1])
        if not offers:
            # second class used by allegro
            offers = soup.find_all("div", class_='_9c44d_1ILhl _9c44d_1s124')
        for offer in offers:
            link = offer.find('a').get('href')
            # TODO handle local seller
            if 'lokalnie' not in link:
                product_list.append(link)
        # print(len(product_list))
        return product_list

    def get_product_list_webdriver(self, page_link, page):
        uri = page_link + '&p={}'.format(page)
        print('PAGE: {} URI: {}'.format(page, uri))
        product_list = self.allegro_driver.get_offers_urls(uri)
        return product_list

    def get_site_content(self, site_link, soup=None):
        if not soup:
            soup = self.siteSoup.make_soup(site_link)
        if not soup:
            print("Couldn't get site conent on link: {}".format(site_link))
            return None
        else:
            content = soup.find_all(self.site_configuration['title_class'][0],
                                    self.site_configuration['title_class'][1])[0].contents[0]
            for EachPart in soup.select('div[class*="_1voj4"]'):
                content += EachPart.text

            return content

    def create_source_product(self, soup, offer_link, brand, pid):
        available_sizes = self.get_available_sizes(soup)
        price = soup.find_all(self.site_configuration['price'][0], self.site_configuration['price'][1])[0] \
            .text.strip().replace('zł', '').replace(',', '.').replace(' ', '')
        auction_title = soup.find_all(self.site_configuration['title_class'][0],
                                      self.site_configuration['title_class'][1])[0].text

        source_product = SourceProduct(pid, auction_title, brand, 'Allegro', offer_link, price)
        source_product.available_sizes['EU'] = available_sizes
        # print(offer_link)

        source_product.available_sizes['US'] = source_product.eu_to_us(available_sizes, brand)

        return source_product

    def create_output_product(self, source_product, stockx_product, available_bids):

        output_product = OutputProduct(source_product.product_id, stockx_product.product_name, stockx_product.brand,
                                       'Allegro', stockx_product.stockx_link, source_product.product_link)
        output_product.retail = stockx_product.retail_price_pl
        output_product.offer_price = source_product.product_price['PLN']

        bid = available_bids[:1][0]['localAmount']
        bid_shoe_size = available_bids[:1][0]['shoeSize']
        payout = (bid * 0.885) - 10
        payout_pln = payout * USD_PLN
        profit = payout_pln - output_product.offer_price
        output_product.profit = profit

        if profit < -10:
            # print('Resell < 10 PLN for offer: {}. Offer price: {} Payout: {}'.
            #       format(output_product.offer_link, output_product.offer_price, payout))
            return None
        try:
            eu_size = output_product.us_to_eu([bid_shoe_size], source_product.brand)
            output_product.bid_size = {'EU': eu_size[0] if eu_size else None, 'US': bid_shoe_size}
            output_product.available_sizes = source_product.available_sizes
            output_product.payout = payout_pln
            current_size_highest_bid = available_bids[:1][0]
            output_product.current_size_hb = current_size_highest_bid['localAmount']
            output_product.highest_bid = bid
        except Exception as e:
            print(e)
            pass

        for bid in available_bids[:3]:
            pos = output_product.highest_bids['available']
            if bid['shoeSize'] not in pos.keys():
                pos[bid['shoeSize']] = [bid['localAmount']]
            else:
                pos[bid['shoeSize']].append(bid['localAmount'])
        for bid in stockx_product.available_bids[:3]:
            pos = output_product.highest_bids['all']
            if bid['shoeSize'] not in pos.keys():
                pos[bid['shoeSize']] = [bid['localAmount']]
            else:
                pos[bid['shoeSize']].append(bid['localAmount'])

        return output_product

    def start_process(self, start_page, end_page, brand):

        self.stockxManager.pids_not_available = open(switch(brand, 'file'), 'r').readlines()

        for p in range(start_page, end_page):
            self.stockxManager.file = open(switch(brand, 'file'), 'a')
            brand_page = AllegroConst.ALLEGRO_PAGES.get(brand)
            start_time = datetime.datetime.now()

            offer_links = self.get_product_list_webdriver(brand_page, p)
            if not offer_links:
                print('Didnt create soup for offer links, continuing')
                continue

            pids_processed = 0
            all_offers = len(offer_links)

            for offer_link in offer_links:

                is_offer_valid = self.validate_link(offer_link)
                if not is_offer_valid:
                    # print('SKIPPED LINK!!')
                    continue
                offer_soup = self.allegro_driver.make_soup_from_url(offer_link)
                # offer_soup = self.siteSoup.make_soup(offer_link)
                if not offer_soup:
                    print('Offer_soup is none, error occurred')
                    continue
                self.get_auction_seller_and_title(offer_soup)
                is_offer_valid = self.validate_offer(offer_soup, offer_link)
                if not is_offer_valid:
                    continue
                # find pid on allegro site
                pid = self.find_pid_pattern(offer_soup, offer_link, brand)
                if not pid:
                    continue
                # create sourceProduct
                source_product = self.create_source_product(offer_soup, offer_link, brand, pid)

                # get stockX productInfo
                stockx_product = self.stockxManager.get_stockx_product_info(source_product.product_id)
                if not stockx_product:
                    continue
                pids_processed += 1

                # get stockX product bids
                stockx_all_product_bids = self.stockxManager.get_stockx_product_bids(stockx_product)
                if not stockx_all_product_bids:
                    continue
                else:
                    stockx_product.available_bids = stockx_all_product_bids

                # SWITCH ON GENDER
                checked_sizes = check_sizes_on_gender(stockx_product, source_product, brand)
                available_bids = [bid for bid in stockx_all_product_bids if bid['shoeSize']
                                  in checked_sizes]

                if not available_bids:
                    print('No available bids')
                    continue

                # create output product
                output_product = self.create_output_product(source_product, stockx_product, available_bids)
                if output_product:
                    print(json.dumps(output_product.__dict__, indent=1))


            # time.sleep(30)
            end_time = datetime.datetime.now()
            diff = end_time - start_time
            print("All offers: {0} for page: {1} took: {2} seconds".format(all_offers, p, diff.seconds))

            self.stockxManager.file.close()
            print("pids processed: {}/{}".format(pids_processed, all_offers))


def check_sizes_on_gender(stockx_product, source_product, brand):
    gender = stockx_product.gender
    if gender == "men" and "M" not in brand:
        print('found wrong gender')
        correct_brand = brand.split('_')[0] + '_M'
        men_sizes = source_product.eu_to_us(source_product.available_sizes['EU'], correct_brand)

        return men_sizes

    elif gender == "women" and "W" not in brand:
        if 'reebok' in brand or 'balance' in brand:
            print('NOT SUPPORTED')
            return source_product.available_sizes['US']
        print('found wrong gender')
        correct_brand = brand.split('_')[0] + '_W'
        women_sizes = source_product.eu_to_us(source_product.available_sizes['EU'], correct_brand)

        return women_sizes

    elif gender == "child" and "GS" not in brand:
        if 'adidas' in brand or 'reebok' in brand or 'balance' in brand.lower():
            print('NOT SUPPORTED brand: {0}'.format(brand))
            return source_product.available_sizes['US']
        print('found wrong gender')
        # correct_brand = brand.split('_')[0] + '_GS'
        gs_sizes = source_product.eu_to_gs(source_product.available_sizes['EU'], brand)
        return gs_sizes

    else:
        return source_product.available_sizes['US']
