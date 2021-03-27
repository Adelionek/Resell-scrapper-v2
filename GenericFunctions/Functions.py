from Const.Patterns import *
from Const.SizeChart import *
import os


def switch(brand, type):
    current_dir = os.path.join(os.getcwd(), 'txt')

    switcher = {
        'nike_M': {
            'pattern': nike,
            'file': os.path.join(current_dir, 'nike_PID_not_available.txt'),
            'size_chart': nike_M,
            'size_chart_GS': nike_GS
        },
        'nike_W': {
            'pattern': nike,
            'file': os.path.join(current_dir, 'nike_W_PID_not_available.txt'),
            'size_chart': nike_W,
            'size_chart_GS': nike_GS
        },
        'adidas_M': {
            'pattern': adidas,
            'file': os.path.join(current_dir, 'adidas_PID_not_available.txt'),
            'size_chart': adidas_M
        },
        'adidas_W': {
            'pattern': adidas,
            'file': os.path.join(current_dir, 'adidas_W_PID_not_available.txt'),
            'size_chart': adidas_W
        },
        'newBalance_M': {
            'pattern': new_balance,
            'file': os.path.join(current_dir, 'new_balance_PID_not_available.txt'),
            'size_chart': new_balance_M
        },
        'newBalance_W': {
            'pattern': new_balance,
            'file': os.path.join(current_dir, 'new_balance_W_PID_not_available.txt'),
            'size_chart': new_balance_W
        },
        'reebok_M': {
            'pattern': reebok,
            'file': os.path.join(current_dir, 'reebok_PID_not_available.txt'),
            'size_chart': reebok_M
        },
        'reebok_W': {
            'pattern': reebok,
            'file': os.path.join(current_dir, 'reebok_W_PID_not_available.txt'),
            'size_chart': reebok_W
        }
    }
    return switcher[brand][type]
