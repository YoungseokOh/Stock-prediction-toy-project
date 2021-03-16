import pandas as pd
from pykrx import stock
from datetime import datetime, timedelta
pd.set_option('mode.chained_assignment',  None)

def daily_data_read(today_date):
    df = stock.get_market_ohlcv_by_ticker(today_date, market="ALL")
    # df = stock.get_market_price_change_by_ticker("20210304", today_date)
    df = df.reset_index()
    # KOSPI... KOSDAQ
    KONEX_ticker_list = stock.get_market_ticker_list(market="KONEX")
    KONEX = pd.DataFrame(KONEX_ticker_list)
    KONEX.columns = ['ticker']
    KONEX = KONEX.reset_index()
    df = df[~df['티커'].isin(KONEX['ticker'])]
    df = df.reset_index()
    return df

def ticker_to_stockname(df):
    count = 0
    df_change = df
    for ticker in df_change['티커']:
        stock_name = stock.get_market_ticker_name(ticker)
        df_change['티커'].iloc[count] = stock_name
        count += 1
    return df_change

def sorting_by_column(df, by_criteria, ascending, top_num):
    df_change = df.sort_values(by=by_criteria, ascending=ascending).head(top_num)  # 등락률
    return df_change

