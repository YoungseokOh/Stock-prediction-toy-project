# 52 weeks analysis python

from datetime import datetime, timedelta
from krx_wr_script import *
import os

def stock_52w_gap_percentage(stock_name, one_year_ago):
    stock_csv = pykrx_read_csv(stock_name)
    one_year_ago = datetime.now() - timedelta(days=365)
    stock_52w = stock_csv[stock_csv['date'] >= (one_year_ago).strftime("%Y-%m-%d")]
    high_price_52w = max(stock_52w['high'].to_numpy())
    close_price_day = stock_csv.iloc[len(stock_csv) - 1]['close']
    gap_percentage = (close_price_day / high_price_52w) * 100
    return gap_percentage, high_price_52w

def stock_52w_update(Krx_Char_folder_path):
    krx_list = os.listdir(Krx_Char_folder_path)
    one_year_ago = datetime.now() - timedelta(days=365)
    stock_list_52w = []
    count = 0
    for stock_name in krx_list:
        if '스팩' in stock_name:
            continue
        stock_csv = pykrx_read_csv(stock_name)
        close_price_day = stock_csv.iloc[len(stock_csv) - 1]['close']
        stock_52w_csv = stock_csv[stock_csv['date'] >= (one_year_ago).strftime("%Y-%m-%d")]
        high_price_52w = max(stock_52w_csv['high'].to_numpy())
        if high_price_52w == 0:
            print('This stock has issue for administration.')
            continue
        stock_date_52w = stock_52w_csv[stock_52w_csv['high'] == max(stock_52w_csv['high'])]['date']
        #print(stock_date_52w)
        if high_price_52w > close_price_day:
            gap_percentage = round(((high_price_52w / close_price_day) * 100) - 100, 4)
            stock_list_52w.append([str(stock_name), str(stock_date_52w.iloc[0]), float(gap_percentage), high_price_52w])
            print('Stock : {}, 52w high date : {}, Gap : {}%, 52w high price : {}'.format(stock_name, stock_date_52w.iloc[0], gap_percentage, high_price_52w))
            count += 1
        elif high_price_52w < close_price_day:
            gap_percentage = round(((close_price_day / high_price_52w) * 100) - 100, 4)
            print('{} is already hit the 52 weeks target! Going up {}%'.format(stock_name, gap_percentage))
    df = pd.DataFrame(stock_list_52w)
    df = df.rename(columns={0 :'stock', 1 : 'date', 2: 'gap', 3 : 'high'})
    df_csv = df.sort_values(by='gap', ascending=True)
    df_csv.to_csv('results/' + '52_weeks_analysis_{}.csv'.format(datetime.today().strftime("%Y-%m-%d")), encoding='utf-8', index=False, header=True)
    return df_csv

