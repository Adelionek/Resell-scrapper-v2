import time

from Robots.SiteRobot import SiteRobot
from Products.SourceProduct import SourceProduct
from Products.OutputProduct import OutputProduct
from GenericFunctions.Functions import *
from Const.Currency import *
import re
import json


class RunColorsRobot(SiteRobot):
    def __init__(self):
        super().__init__(request_headers={
            'authority': 'runcolors.pl',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'dnt': '1',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-dest': 'script',
            'referer': 'https://runcolors.pl/sneakers/marki/nike.html?page=1',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'getOnShopTime=1610973712; SID=ff3e0fb6ae620464b5717ab9a77f7073; _gcl_au=1.1.1195984573.1610973679; _ga=GA1.2.1481571813.1610973680; _gid=GA1.2.908537158.1610973680; _hjid=7d6a7cf5-8bbd-443b-8fa0-79cf3ea02715; _hjFirstSeen=1; getOnShopTime=1610973730; SID=b2224278086e6e94becb65522250627a'
        })
        self.pages = {
            "nike": "https://runcolors.pl/sneakers/marki/nike.html",
            "newBalance": "https://runcolors.pl/new_balance.html",
            "adidas": "https://runcolors.pl/sneakers/marki/adidas.html"
        }
        self.site_configuration = {
            "ul_list": ['ul', 'pList js--productListWrapper'],
            "sizes_tile": ['div', 'pList__item_big__variants--item js--variant--item']
        }

    def get_available_sizes(self, offer):
        available_sizes = []
        sizes = offer.find_all(self.site_configuration['sizes_tile'][0], self.site_configuration['sizes_tile'][1])
        for size in sizes:
            # TODO ADD PROPER HANDLING
            if 'X' in size.text:
                return available_sizes
            available_sizes.append(size.text.replace('.', ','))

        # for size in tiles:
        #     try:
        #         found_size = re.search(SIZE_PATTERN, size.text).group(0)
        #         if found_size:
        #             available_sizes.append(found_size)
        #     except Exception as e:
        #         pass

        return available_sizes

    def find_pid_pattern(self, offer, brand):
        brand = brand + '_M'
        pattern = switch(brand, 'pattern')
        pid = offer.find("img")['alt'].split(' ')[-1]
        if self.validate_pid(pid, pattern):
            return pid
        return None

    def get_product_list(self, page_link, page):
        uri = page_link + '?page={}'.format(page)
        print('PAGE: {} URI: {}'.format(page, uri))
        soup = self.siteSoup.make_soup(uri)
        # TODO ADD IF
        offers = soup.find(self.site_configuration['ul_list'][0],
                           class_=self.site_configuration['ul_list'][1]).findChildren("li")

        return offers

    def create_source_product(self, offer, brand, pid):
        available_sizes = self.get_available_sizes(offer)

        price = None

        try:
            price = offer.find('em').text[:-3]
            price = price if ',' not in price else int(price.split(',')[0])
        except AttributeError as e:
            print(e)

        list = offer.prettify().split('\n')[0].split(' ')
        offer_link = None
        for l in list:
            if 'brand' in l:
                brand = l.split('=')[1].strip("\"")
            if 'data-full-nice_url' in l:
                offer_link = l.split('=')[1].strip("\"")
            if not price and 'data-default-price' in l:
                price = l.split('=')[1].strip("\"")

        auction_title = offer.find("img")['alt']
        # TODO exttract brand later

        source_product = SourceProduct(pid, auction_title, brand, 'Runcolors', offer_link, price)
        source_product.available_sizes['EU'] = available_sizes
        print(offer_link)

        # source_product.available_sizes['US'] = source_product.eu_to_us(available_sizes, brand)

        return source_product

    def create_output_product(self, source_product, stockx_product, available_bids):

        output_product = OutputProduct(source_product.product_id, stockx_product.product_name, stockx_product.brand,
                                       'Allegro', stockx_product.stockx_link, source_product.product_link)
        output_product.retail = stockx_product.retail_price_pl
        output_product.offer_price = source_product.product_price['PLN']

        bid = available_bids[:1][0]['localAmount']
        print("Bid ", bid)
        bid_shoe_size = available_bids[:1][0]['shoeSize']
        payout = (bid * 0.885) - 10
        payout_pln = payout * EUR_PLN
        profit = payout_pln - output_product.offer_price
        output_product.profit = profit

        if profit < 10:
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
        # self.stockxManager.pids_not_available = open(switch(brand, 'file'), 'r').readlines()
        for p in range(start_page, end_page):
            # self.stockxManager.file = open(switch(brand, 'file'), 'a')
            brand_page = self.pages.get(brand)
            offers_list = self.get_product_list(brand_page, p)
            pids_processed = 0
            all_offers = len(offers_list)
            for offer in offers_list:
                # find pid in runcolors element
                pid = self.find_pid_pattern(offer, brand)
                if not pid:
                    continue
                # create sourceProduct
                source_product = self.create_source_product(offer, brand, pid)

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
                    continue

                # create output product
                output_product = self.create_output_product(source_product, stockx_product, available_bids)
                if output_product:
                    print(json.dumps(output_product.__dict__, indent=1))

            # self.stockxManager.file.close()
            print("pids processed: {}/{}".format(pids_processed, all_offers))


def check_sizes_on_gender(stockx_product, source_product, brand):
    gender = stockx_product.gender
    if gender == "men" and "M" not in brand:
        print('found wrong gender')
        correct_brand = brand.split('_')[0] + '_M'
        men_sizes = source_product.eu_to_us(source_product.available_sizes['EU'], correct_brand)
        return men_sizes
    elif gender == "women" and "W" not in brand:

        if 'reebok' in brand or 'new_balance' in brand:
            print('NOT SUPPORTED')
            return source_product.available_sizes['US']

        print('found wrong gender')
        correct_brand = brand.split('_')[0] + '_W'
        women_sizes = source_product.eu_to_us(source_product.available_sizes['EU'], correct_brand)
        return women_sizes
    elif gender == "child" and "GS" not in brand:
        if 'adidas' in brand or 'reebok' in brand or 'newBalance' in brand:
            print('NOT SUPPORTED')
            return source_product.available_sizes['US']
        print('found wrong gender')
        # correct_brand = brand.split('_')[0] + '_GS'
        gs_sizes = source_product.eu_to_gs(source_product.available_sizes['EU'], brand + '_M')
        return gs_sizes
    else:
        return source_product.available_sizes['US']


RunColors = RunColorsRobot()
#RunColors.start_process(1, 3, 'nike')
# RunColors.start_process(1, 3, 'newBalance')
RunColors.start_process(1, 2, 'adidas')
# brand_page = RunColors.pages.get('nike')
# offer_links = RunColors.get_product_list(brand_page, '1')
# print(offer_links)
