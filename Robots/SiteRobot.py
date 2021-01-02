from GenericClasses.Soup import Soup
from GenericClasses.Stockx import Stockx
from GenericFunctions.Functions import *

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

    def validate_pid(self, found_pid, pid_pattern):
        if 4 < len(found_pid) < 11:
            hasnumber = any(char.isdigit() for char in found_pid)
            checked_pid = re.findall(pid_pattern, found_pid)
            if hasnumber and '%' not in found_pid and checked_pid:
                return True
        return False
