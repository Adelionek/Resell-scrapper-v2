from GenericClasses.Soup import Soup
from GenericClasses.Stockx import Stockx


class SiteRobot:
    def __init__(self, request_headers):
        self.request_headers = request_headers
        self.output_products = []
        self.pages = None
        self.site_configuration = None
        self.siteSoup = Soup(request_headers)
        self.stockxManager = Stockx()

    def start_process(self):
        pass

    def get_product_list(self):
        pass

    def get_product_details(self):
        pass

    def find_pid_pattern(self, site_text):
        pass

    def get_site_content(self, site_link):
        pass
