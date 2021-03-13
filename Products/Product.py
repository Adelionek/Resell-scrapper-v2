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

    def eu_to_gs(self, size_array, brand):
        size_chart = switch(brand, 'size_chart_GS')
        gs_array = []
        for size in size_array:
            try:
                gs_array.append(size_chart['EU_GS'][size])
            except Exception as e:
                # TODO primtlink
                print("size:{} eu_to_gs exception".format(e))

        return gs_array

    def gs_to_eu(self, size_array, brand):
        size_chart = switch(brand, 'size_chart_GS')
        eu_array = []
        for size in size_array:
            try:
                eu_array.append(size_chart['GS_EU'][size])
            except Exception as e:
                print("size:{} gs_to_eu exception".format(e))

        return eu_array




