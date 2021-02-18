from py_krx_wr_script import *
from datetime import datetime
import pandas as pd

def print_hi(name):
    print(f'Hi, {name}')

if __name__ == '__main__':

    From_date = '20190101'
    Today_date = datetime.today().strftime("%Y%m%d")
    print_hi('PyCharm')
    pykrx_scratch(From_date, Today_date)
    # 1. krx daily chart update
    # 2. reading train set
