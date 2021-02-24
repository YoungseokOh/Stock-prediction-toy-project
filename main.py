from py_krx_wr_script import *
from datetime import datetime
import pandas as pd
from py_system_check import Monitor

def print(name):
    print(f'Hi, {name}')

if __name__ == '__main__':

    #GPU Monitor
    monitor = Monitor(10)
    monitor.stop()
    From_date = '20190101'
    Today_date = datetime.today().strftime("%Y%m%d")
    print('PyCharm')
    # Test...
    #pykrx_scratch(From_date, Today_date)
    stock_name = "코리아센터"
    #stock_csv = pykrx_read_csv(stock_name)
    pykrx_daily_update()

    #trainer = Model(opt)


    ### To do list ###
    # 1. Krx daily chart update (clear)
    # 2. Reading train set (Clear)
    # 3. Showing chart
    # 4. Feature extraction
    # 5. Technical Indicator csv save
    # 6. Beat or lose
    # 7. EPS/DIV ... csv
