from krx_wr_script import *
from stock_52_weeks_analysis import *
from datetime import datetime, timedelta
import pandas as pd
from system_check import Monitor
from finta import TA
from finta.utils import resample_calendar
from plot_chart import *

Krx_Char_folder_path = 'E:/Krx_Chart_folder'

if __name__ == '__main__':
    From_date = '20190101'
    base_year = '2021-01-01' # When youu don't wanna know this year 52 weeks high price
    stock_name = "부광약품"
    listed_year = 2021
    today_date = datetime.today().strftime("%Y%m%d")
    # Test...
    # monitor = Monitor(10) #GPU Monitor
    # monitor.stop()
    pykrx_scratch(From_date, today_date) # KOSPI & KOSDAQ all stock scratch
    # pykrx_daily_update()
    # stock_csv = pykrx_read_csv(stock_name)
    # trainer = Model(opt)

    # Showing chart test...
    # print(TA.RSI(stock_csv).tail())
    # print(TA.EMA(stock_csv, 20).tail())
    # # print(TA.EMA(stock_csv, 60).tail())
    # print(TA.EMA(stock_csv, 120).tail())
    # #plot_technical_indicators(stock_csv, 30)

    # 52 weeks high price test...
    one_year_ago = datetime.now() - timedelta(days=365)
    gap_prcentage, high_price_52w = stock_52w_gap_percentage(stock_name, one_year_ago)
    print('Gap is {}% from {}원'.format(round(gap_prcentage,4), format(high_price_52w, ',')))
    results_52w_csv = 'results/' + '52_weeks_analysis_' + datetime.today().strftime("%Y-%m-%d") + '.csv'
    if not os.path.exists(results_52w_csv):
        df_52w_csv = stock_52w_update(Krx_Char_folder_path)
    else:
        df_52w_csv = pd.read_csv(results_52w_csv)

    # Make an exception of daily hit the high price
    base_52w_csv = base_year_52_weeks_update(df_52w_csv, base_year)

    #search_listed_stock(listed_year)