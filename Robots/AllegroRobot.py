import time

from Robots.SiteRobot import SiteRobot
from Products.SourceProduct import SourceProduct
from Products.OutputProduct import OutputProduct
from Const.Patterns import *
from GenericFunctions.Functions import *
from Const.Currency import *
import re
import json


class AllegroRobot(SiteRobot):
    def __init__(self):
        super().__init__(request_headers={
            'authority': 'allegro.pl',
            'accept': 'application/vnd.allegro.favourites.v1+json',
            'dnt': '1',
            'dpr': '2',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'viewport-width': '865',
            'service-name': 'opbox-showoffer-summary',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://allegro.pl/oferta/maska-na-twarz-ochronna-maseczka-kn95-filtr-kn95-9190663571?bi_c=C-maseczki-zdrowie-2020&',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',

            'cookie': '_cmuid=gx60jrxk-gpxc-510p-3twz-5gfjg2rnr0d4; _ga_2FTJ836HTM=GS1.1.1607275481.36.1.1607275611.6; _ga=GA1.1.1671861360.1606556139; RT="sl=5&ss=kidebk9f&tt=7bu&z=1&dm=allegro.pl&si=11639adf-aa61-4794-bc3c-9d93a4ebf91b&obo=2&rl=1"; _gcl_au=1.1.1811507559.1607275614'
        })
        self.pages = {
            "nike_M": "https://allegro.pl/kategoria/meskie-sportowe-257929?stan=nowe&dostawa-z-polski=tak&oryginalne"
                      "-opakowanie-producenta=pude%C5%82ko&marka=Nike&order=n&bmatch=dict20110-a-ctx-fd-fas-1-5-1125",
            "nike_W": "https://allegro.pl/kategoria/damskie-sportowe-257903?marka=Nike&dostawa-z-polski=tak&order=n&"
                      "freeReturn=1&stan=nowe&bmatch=dict20110-a-ctx-fd-fas-1-5-1125",
            'adidas_M': 'https://allegro.pl/kategoria/meskie-sportowe-257929?dostawa-z-polski=tak&marka=adidas&'
                        'freeReturn=1&oryginalne-opakowanie-producenta=pude%C5%82ko&stan=nowe&'
                        'bmatch=dict20120-m-ctx-fas-1-4-1203&order=n',
            'adidas_W': 'https://allegro.pl/kategoria/damskie-sportowe-257903?marka=adidas&dostawa-z-polski=tak&'
                        'freeReturn=1&stan=nowe&order=n&bmatch=dict201214-ctx-fas-1-2-1218',
            'new_balance_M': 'https://allegro.pl/kategoria/meskie-sportowe-257929?dostawa-z-polski=tak&marka=New%20'
                             'Balance&freeReturn=1&oryginalne-opakowanie-producenta=pude%C5%82ko&stan=nowe&b'
                             'match=dict20120-m-ctx-fas-1-2-1203&order=',
            'reebok_M': "https://allegro.pl/kategoria/meskie-sportowe-257929?dostawa-z-polski=tak&oryginalne-opakowanie"
                        "-producenta=pude%C5%82ko&order=n&bmatch=dict201214-ctx-fas-1-2-1218&stan=nowe"
                        "&stan=nowe%20bez%20metki&stan=nowe%20z%20defektem&marka=Reebok"
        }
        self.fake_sellers = ['xooreek', 'N1A_PL', 'TIGER_77', 'e-outletstore', 'sklepik_DandB', 'world-shop',
                             'macopoloshopping', 'superbutypl', 'kuipengzjz29703', 'lgxbvsa', 'xibao13324', 'Tzmark',
                             'GTshoes', 'AlleButy1819', 'Eski_Sports', 'ButicSport', 'Razor69996', 'Sneakers_On_Fire',
                             'sneakers_sale', 'mike__c', 'DIA-MOND-SHOP', 'GORDIOSpl', 'halfprices', 'mkshoes00',
                             'sklep_DandB', 'dgkein', 'DirkNowitzki', 'DongmeiTrade', 'Mrx_Shoes', 'sportowebuty24h',
                             'Taniejsieniedaa', 'GToutlet', 'wonderfully', 'Tiger_77', 'minouglobal',
                             'halfpricesplywak26', 'Start66FERRY', 'URSI151', 'harlemworldnyc', 'awmax', 'maciejmaspor',
                             'Fashion-styleLTD', 'sportella_pl', 'FreeSia333', 'handyshopping', 'Pewexolandia',
                             'Solo-Sport', 'laijiebd423209', 'MEGA-WYPRZEDAZE', 'LuxZone', 'jingxianb140725',
                             'TransMax97', 'Qijunlvyou', 'MegaSales', 'EverySize', 'EGGG', 'max-trade-ltd', 'xenehho',
                             'Razor69 996', 'littleyou', 'bangruowuren', 'lukaszmer', 'Modern_LondonONE-DESIGN',
                             'comewithme', 'Tanie-Kicksy', 'guger-online', 'RoseLee', 'Billa-shop', 'yubopid57777',
                             'CoolLabels', 'comewith', 'new_shoes_kicks', 'bestgood', 'jessciaaa', 'butyspecial_pl',
                             'Modern_London', 'yingying', 'ModenooBox', 'Paula_Shoes', 'KustoSeller3', 'CandySport',
                             'NaGiewoncie1409', 'CalceolarPL', 'KustoSeller32', 'alleo-promocje', 'chentaozo350604',
                             'luzhuangly653558', 'qiongyouyv098054', 'AnfiniHardaway', 'Janutzboots', 'Martunia_91',
                             'tarasofobia', 'ntulppma', 'Buty_UK', 'saleneo-com', 'saleneo_pl', 'dostawa-w-2tyg',
                             '4F_Sklep', 'cool_shoes_1993', 'Client:58508393', 'super_sneakers', 'Stasic77']

        self.site_configuration = {
            "title_class": ['h1', '_9a071_1Ux3M _9a071_3nB-- _9a071_1R3g4 _9a071_1S3No'],
            "nick_class": ['a', '_w7z6o _15mod _9a071_1BlBd'],
            "price": ['div', '_1svub _lf05o _9a071_2MEB_'],
            "ship_country": ['div', '_15mod _1vryf _34279_13Rv4'],
            "offer_title": ['h2', 'mgn2_14 m9qz_yp mqu1_16 mp4t_0 m3h2_0 mryx_0 munh_0'],
            "sizes_tile": ['div', '_9a071_1bSFU _1nfka'],
            "current_size": ['div', '_17qy1 _1vryf _f8818_1X1F-']
        }
        self.washed_titles = ['Pegasus Turbo', 'max 90', 'air max 90']

    def validate_bids(self, stockx_bids, available_bids):
        pass

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

    def validate_offer(self, soup, offer_link):
        try:
            seller_name = soup.find_all(self.site_configuration['nick_class'][0],
                                        self.site_configuration['nick_class'][1])[0].text.split(' ')[0].strip()
            auction_title = soup.find_all(self.site_configuration['title_class'][0],
                                          self.site_configuration['title_class'][1])[0].text
        except IndexError as e:
            print("IndexError: {}".format(e))
            return False

        if seller_name in self.fake_sellers:
            return False
        for washed in self.washed_titles:
            if washed in auction_title.lower():
                return False

        if 'lokalnie' in offer_link:
            print('Local offer, skipping')
            return False
        if any(elem.text in ['Chiny', 'Holandia'] for elem in soup.find_all(
                self.site_configuration['ship_country'][0], self.site_configuration['ship_country'][1])):
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
        # TODO ADD IF
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

        for bids in available_bids[:3]:
            # TODO ADD AS DICT size: bid
            output_product.highest_available_bids.append(bids['localAmount'])

        return output_product

    # brand example: adidas_M

    def start_process(self, start_page, end_page, brand):
        self.stockxManager.pids_not_available = open(switch(brand, 'file'), 'r').readlines()
        for p in range(start_page, end_page):
            self.stockxManager.file = open(switch(brand, 'file'), 'a')
            brand_page = self.pages.get(brand)
            offer_links = self.get_product_list(brand_page, p)
            pids_processed = 0
            all_offers = len(offer_links)
            for offer_link in offer_links:
                # time.sleep(2)
                offer_soup = self.siteSoup.make_soup(offer_link)
                if not offer_soup:
                    print('Offer_soup is none, error occurred')
                    continue
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
                pids_processed = pids_processed + 1

                # get stockX product bids
                stockx_all_product_bids = self.stockxManager.get_stockx_product_bids(stockx_product)
                if not stockx_all_product_bids:
                    continue
                else:
                    stockx_product.available_bids = stockx_all_product_bids

                # check if there are available bids
                available_bids = [bid for bid in stockx_all_product_bids if bid['shoeSize']
                                  in source_product.available_sizes['US']]
                if not available_bids:
                    continue

                # create output product
                output_product = self.create_output_product(source_product, stockx_product, available_bids)
                if output_product:
                    print(json.dumps(output_product.__dict__, indent=1))
            self.stockxManager.file.close()
            print("pids processed: {}/{}".format(pids_processed, all_offers))
    #  self.stockxManager.pids_not_available.close()
