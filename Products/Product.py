from GenericFunctions.Functions import *


class Product:
    def __init__(self, pid, name, brand):
        self.product_id = pid
        self.product_name = name
        self.brand = brand

    def us_to_eu(self, size_array, brand):
        size_chart = switch(brand, 'size_chart')
        eu_array = []
        for size in size_array:
            try:
                eu_array.append(size_chart['US_EU'][size])
            except Exception as e:
                print("size:{} us_to_eu exception".format(e))
                pass
        return eu_array

    def eu_to_us(self, size_array, brand):
        size_chart = switch(brand, 'size_chart')
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




