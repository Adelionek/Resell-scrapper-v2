from Const.SizeChart import *


class Product:
    def __init__(self, pid, name, brand):
        self.product_id = pid
        self.product_name = name
        self.brand = brand

    def us_to_eu(self, size_array):
        eu_array = []
        for size in size_array:
            try:
                eu_array.append(US_EU[size])
            except Exception as e:
                print("size:{} us_to_eu exception".format(e))
                pass
        return eu_array

    def eu_to_us(self, size_array):
        us_array = []
        for size in size_array:
            try:
                us_array.append(EU_US[size])
            except Exception as e:
                print("size:{} eu_to_us exception".format(e))
                pass
        return us_array



