from analysis.stock_52_weeks import *
from plot_chart import *
from analysis.technical_indicator import *
from analysis.top_20_stocks import *
from krx_wr_script import *
from analysis.bot_strategy import *
from datetime import datetime, timedelta
from util import *
import pandas as pd
from pykrx import stock
import matplotlib.pyplot as plt
from finta import TA
import yfinance as yf

if __name__ == '__main__':
    util_m = util()
    # Pykrx scratch Test...
    pykrx_scratch(util_m.from_date, util_m.today_date, util_m.Krx_Char_folder_path) # KOSPI & KOSDAQ all stock scratch
    # pykrx_daily_update(util_m.Krx_Char_folder_path) # Today update
    stock_csv = pykrx_read_csv(util_m.stock_name, util_m.Krx_Char_folder_path)
    # trainer = Model(opt)

    # technical indicator high class
    stock_csv = cal_technical_indicator_high_class(util_m.stock_name, util_m.Krx_Char_folder_path)

    # Base technical indicator
    stock_csv = cal_technical_indicator_name(util_m.stock_name, util_m.Krx_Char_folder_path)
    fig = plot_technical_indicators(util_m.stock_name, stock_csv, 300)
    fig.savefig('results/{}.png'.format(util_m.stock_name))
    # Personal technical indicator
    # stock_csv_p = cal_technical_indicator_personal(stock_name, util.Krx_Char_folder_path, 10, 50, 120, False, )
    # fig = plot_technical_indicators(stock_name, stock_csv_p, 300)

    # 52 weeks high price test...
    one_year_ago = datetime.now() - timedelta(days=365)
    gap_prcentage, high_price_52w = stock_52w_gap_percentage(util_m.stock_name, one_year_ago, util_m.Krx_Char_folder_path)
    # print('Gap is {}% from {}원'.format(round(gap_prcentage,4), format(high_price_52w, ',')))

    base_date = '2021-09-01'
    results_52w_csv = 'results/this_year/' + '52_weeks_analysis_' + base_date + '.csv'
    if not os.path.exists(results_52w_csv):
        # Hit the high in 52 weeks until today
        print('{} - 52 weeks high update for analysis ...'.format(base_date))
        time.sleep(0.5)
        # df_52w_csv = stock_52w_update(util_m.Krx_Char_folder_path, util_m.get_today_ymd())
        df_52w_csv = stock_52w_update(util_m.Krx_Char_folder_path, base_date)

        # Hit the high in 52 weeks before 2021/01/01 (base year)
        base_52w_csv = base_year_high_52_weeks(df_52w_csv, util_m.base_year, base_date)
    else:
        print('File is existed in results/this_year {}'.format(base_date))
        df_52w_csv = pd.read_csv(results_52w_csv)

    # Make an exception of daily hit the high price
    # search_listed_stock(listed_year)

    # Evolution strategy analysis - base year test
    # base_year_52w_csv_path = 'results/base_year/' + '52_weeks_analysis_' + datetime.today().strftime("%Y-%m-%d") + '_before_{}'.format(base_year) +'.csv'
    # base_year_52w_csv = pd.read_csv(base_year_52w_csv_path)
    # top_10_base_year_52w = base_year_52w_csv.head(10)
    # investment = []
    # for stock in top_10_base_year_52w['stock']:
    #     stock_csv = pykrx_read_csv(stock, util.Krx_Char_folder_path)
    #     close = stock_csv.close.values.tolist()
    #     window_size = 60
    #     skip = 1
    #     l = len(close) - 1
    #     model = Model(window_size, 1000, 3)
    #     agent = Agent(model, 1000000, 5, 5, window_size, close, skip)
    #     agent.fit(500, 10)
    #     fig = agent.buy(stock)
    #     fig.savefig('results/base_year/base_year_strategy_results/{}/{}_plot_histroy.png'.format(today_date, stock))

    # Evolution strategy analysis - stock_name test
    # stock_csv = pykrx_read_csv(stock_name, util.Krx_Char_folder_path)
    # close = stock_csv.close.values.tolist()
    # window_size = 60
    # skip = 1
    # l = len(close) - 1
    # model = Model(window_size, 1000, 3)
    # agent = Agent(model, 1000000, 5, 5, window_size, close, skip)
    # agent.fit(500, 10)
    # fig = agent.buy(stock)

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