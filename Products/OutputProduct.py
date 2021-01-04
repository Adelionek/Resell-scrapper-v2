from Products.Product import Product


class OutputProduct(Product):
    def __init__(self, pid, name, brand, site_name, stockx_link, offer_link):
        super().__init__(pid, name, brand)
        self.profit = None
        self.site_name = site_name
        self.offer_link = offer_link
        self.stockx_link = stockx_link
        self.available_sizes = {'EU': [], 'US': []}
        self.highest_bid = None
        self.highest_bids = {'available': dict(), 'all': dict()}
        self.retail = None
        self.offer_price = None
        self.payout = None
        self.bid_size = None
        self.current_size_hb = None

    def __repr__(self):
        return {
            'product_name': self.product_name,
            'profit': self.profit,
            'offer_link': self.offer_link,
            'stockx_link': self.stockx_link,
            'payout': self.payout,
            "current_size_hb": self.current_size_hb,
            'bid_size': self.bid_size,
            'stockx_prod_hb': self.highest_bid,
            'current_size_hb': self.current_size_hb,
            'product_id': self.product_id
        }

