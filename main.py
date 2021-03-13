from analysis_stock_52_weeks import *
from plot_chart import *
from analysis_technical_indicator import *
from analysis_top_20_stocks import *
from krx_wr_script import *
from analysis_bot_strategy import *
from datetime import datetime, timedelta
import pandas as pd
from pykrx import stock
import matplotlib.pyplot as plt
from finta import TA
import yfinance as yf

Krx_Char_folder_path = 'E:/Krx_Chart_folder'

if __name__ == '__main__':
    From_date = '20190101'
    base_year = '2021-01-01' # When you don't wanna know this year 52 weeks high price
    stock_name = "GS리테일"
    listed_year = 2021
    today_date = datetime.today().strftime("%Y%m%d")
    # Pykrx scratch Test...
    # pykrx_scratch(From_date, today_date) # KOSPI & KOSDAQ all stock scratch
    # pykrx_daily_update()
    stock_csv = pykrx_read_csv(stock_name)
    # trainer = Model(opt)

    # Base technical indicator
    # stock_csv = cal_technical_indicator_name(stock_name)
    # fig = plot_technical_indicators(stock_name, stock_csv, 300)
    # fig.savefig('results/{}.png'.format(stock_name))
    # Personal technical indicator
    # stock_csv_p = cal_technical_indicator_personal(stock_name, 10, 50, 120, False)
    # fig = plot_technical_indicators(stock_name, stock_csv_p, 300)

    # Evolution strategy analysis
    close = stock_csv.close.values.tolist()
    window_size = 60
    skip = 1
    l = len(close) - 1
    model = Model(window_size, 1000, 3)
    agent = Agent(model, 1000000, 20, 20, window_size, close, skip)
    agent.fit(500, 10)
    agent.buy()

    # 52 weeks high price test...
    one_year_ago = datetime.now() - timedelta(days=365)
    gap_prcentage, high_price_52w = stock_52w_gap_percentage(stock_name, one_year_ago)
    # print('Gap is {}% from {}원'.format(round(gap_prcentage,4), format(high_price_52w, ',')))
    results_52w_csv = 'results/this_year/' + '52_weeks_analysis_' + datetime.today().strftime("%Y-%m-%d") + '.csv'
    if not os.path.exists(results_52w_csv):
        # Hit the high in 52 weeks until today
        print('{} - 52 weeks high update for analysis ...'.format(datetime.today().strftime("%Y-%m-%d")))
        df_52w_csv = stock_52w_update(Krx_Char_folder_path)
        # Hit the high in 52 weeks before 2021/01/01 (base year)
        base_52w_csv = base_year_52_weeks_update(df_52w_csv, base_year)
    else:
        print('File is existed in results/this_year {}'.format(datetime.today().strftime("%Y-%m-%d")))
        df_52w_csv = pd.read_csv(results_52w_csv)
    # Make an exception of daily hit the high price
    #search_listed_stock(listed_year)



    # Volume & change test...
    '''
    df = daily_data_read('20210305') #today_date
    # Volume sorting TOP20
    df_sorting_volume = sorting_by_column(df, '거래량', False, 20)
    df_change = ticker_to_stockname(df_sorting_volume)
    print(df_change)
    # Trading value sorting TOP20
    df_sorting_t_value = sorting_by_column(df, '거래대금', False, 20)
    df_t_value = ticker_to_stockname(df_sorting_t_value)
    print(df_t_value)
    # sorting TOP20
    df_sorting_f_rate = sorting_by_column(df, '등락률', False, 20)
    df_f_rate = ticker_to_stockname(df_sorting_f_rate)
    print(df_f_rate)
    '''