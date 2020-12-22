from Const.SizeChart import *


class Product:
    def __init__(self, pid, name, brand):
        self.product_id = pid
        self.product_name = name
        self.brand = brand

    def switch(self, argument):
        switcher = {
            'nike_M': nike_M,
            'adidas_M': adidas_M,
            'new_balance': None
        }
        return switcher.get(argument, "Invalid brand")

    def us_to_eu(self, size_array, brand):
        size_chart = self.switch(brand)
        eu_array = []
        for size in size_array:
            try:
                eu_array.append(size_chart['US_EU'][size])
            except Exception as e:
                print("size:{} us_to_eu exception".format(e))
                pass
        return eu_array

    def eu_to_us(self, size_array, brand):
        size_chart = self.switch(brand)
        us_array = []
        for size in size_array:
            try:
                us_array.append(size_chart['EU_US'][size])
            except Exception as e:
                try:
                    us_array.append(nike_M['EU_US'][size])
                except Exception as e:
                    print("size:{} eu_to_us exception".format(e))

        return us_array




