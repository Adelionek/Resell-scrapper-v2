from Products.Product import Product
from Const.Currency import *


class SourceProduct(Product):
    def __init__(self, pid, name, brand, site_name, product_link, product_price):
        super().__init__(pid, name, brand)
        self.site_name = site_name
        self.product_link = product_link
        self.product_price = {'PLN': float(product_price), 'EURO': float(product_price) * PLN_EUR}
        self.available_sizes = {'EU': [], 'US': []}

    def validate_offer(self):
        pass
