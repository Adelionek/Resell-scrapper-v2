from Const.Patterns import *
from Const.SizeChart import *

# TODO check if gs per brand is really needed
def switch(brand, type):
    switcher = {
        'nike_M': {
            'pattern': nike,
            'file': 'D:\\Projects\\Python\\ResellScraperv2\\txt\\nike_PID_not_available.txt',
            'size_chart': nike_M,
            'size_chart_GS': nike_GS
        },
        'nike_W': {
            'pattern': nike,
            'file': 'D:\\Projects\\Python\\ResellScraperv2\\txt\\nike_W_PID_not_available.txt',
            'size_chart': nike_W,
            'size_chart_GS': nike_GS
        },
        'adidas_M': {
            'pattern': adidas,
            'file': 'D:\\Projects\\Python\\ResellScraperv2\\txt\\adidas_PID_not_available.txt',
            'size_chart': adidas_M
        },
        'adidas_W': {
            'pattern': adidas,
            'file': 'D:\\Projects\\Python\\ResellScraperv2\\txt\\adidas_W_PID_not_available.txt',
            'size_chart': adidas_W
        },
        'newBalance_M': {
            'pattern': new_balance,
            'file': 'D:\\Projects\\Python\\ResellScraperv2\\txt\\new_balance_PID_not_available.txt',
            'size_chart': new_balance_M
        },
        'reebok_M': {
            'pattern': reebok,
            'file': 'D:\\Projects\\Python\\ResellScraperv2\\txt\\reebok_PID_not_available.txt',
            'size_chart': reebok_M
        }
    }
    return switcher[brand][type]
