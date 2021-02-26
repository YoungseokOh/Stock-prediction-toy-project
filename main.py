# Requirement
# python 3.7
# Tensorflow <= 1.14
# finta, matplotlib, pandas, pykrx

from py_krx_wr_script import *
from datetime import datetime
import pandas as pd
from py_system_check import Monitor
from finta import TA
from finta.utils import resample_calendar
from py_plot_chart import *

if __name__ == '__main__':

    From_date = '20190101'
    stock_name = "코리아센터"
    Today_date = datetime.today().strftime("%Y%m%d")
    # Test...
    monitor = Monitor(10) #GPU Monitor
    monitor.stop()
    #pykrx_scratch(From_date, Today_date) # KOSPI & KOSDAQ all stock scratch
    # pykrx_daily_update()
    stock_csv = pykrx_read_csv(stock_name)
    #trainer = Model(opt)

    # Showing chart test...
    print(TA.RSI(stock_csv).tail())
    print(TA.EMA(stock_csv, 20).tail())
    print(TA.EMA(stock_csv, 60).tail())
    print(TA.EMA(stock_csv, 120).tail())
    #plot_technical_indicators(stock_csv, 30)

    ### To do list ###
    # 1. Krx daily chart update (clear)
    # 2. Reading train set (Clear)
    # 3. Showing chart
    # 4. Feature extraction
    # 5. Technical Indicator save in csv
    # 6. Beat or lose
    # 7. EPS/DIV ... save in csv
    # 8. Searching 52 weeks high - highest price