from Products.Product import Product


class StockxProduct(Product):
    def __init__(self, pid, name, brand, retail, stockx_link, stockx_pid):
        super().__init__(pid, name, brand)
        self.retail_price_pl = retail
        self.available_bids = None
        self.highest_bid = None
        self.lastSales = None
        self.stockx_link = stockx_link
        self.stockx_pid = stockx_pid
        self.gender = None

    def check_available_bids(self):
        pass
