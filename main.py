from py_krx_wr_script import *
from datetime import datetime
import pandas as pd

def print_hi(name):
    print(f'Hi, {name}')

if __name__ == '__main__':

    From_date = '20190101'
    Today_date = datetime.today().strftime("%Y%m%d")
    print_hi('PyCharm')
    #pykrx_scratch(From_date, Today_date)
    stock_name = "코리아센터"
    stock_csv = pykrx_read_csv(stock_name)

    # 오줌이바보
    # 1. Krx daily chart update
    # 2. Reading train set
    # 3. Showing chart
    # 4. Feature extraction
