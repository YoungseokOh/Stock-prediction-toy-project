# 52 weeks analysis python
from tqdm import tqdm
from datetime import datetime, timedelta
from krx_wr_script import *
from util import *
import os

util_52w = util()


def search_listed_stock(year):
    base_date = ['0101', '1231']
    base_year = str(year) + base_date[1]
    one_year_ago = str(year - 1) + base_date[0]


def stock_52w_gap_percentage(stock_name, one_year_ago, Krx_Char_folder_path):
    stock_csv = pykrx_read_csv(stock_name, Krx_Char_folder_path)
    stock_52w = stock_csv[stock_csv['date'] >= (one_year_ago).strftime("%Y-%m-%d")]
    high_price_52w = max(stock_52w['high'].to_numpy())
    close_price_day = stock_csv.iloc[len(stock_csv) - 1]['close']
    gap_percentage = (close_price_day / high_price_52w) * 100
    return gap_percentage, high_price_52w


def stock_52w_update(path, date):
    krx_list = os.listdir(path)
    today_date = util_52w.get_today_ymd()
    if date == today_date:
        one_year_ago = datetime.now() - timedelta(days=365)
    else:
        one_year_ago = util_52w.strdate_convert(date) - timedelta(days=365)
    stock_list_52w = []
    count = 0
    for stock_name in tqdm(krx_list):
        if '스팩' in stock_name:
            continue
        if '리츠' in stock_name:
            continue
        stock_csv = pykrx_read_csv(stock_name, path)
        if not (stock_csv['date'] <= date).any():
            continue
        stock_csv = stock_csv[stock_csv['date'] <= date]
        close_price_day = stock_csv.iloc[len(stock_csv) - 1]['close']
        stock_52w_csv = stock_csv[stock_csv['date'] >= one_year_ago.strftime("%Y-%m-%d")]
        high_price_52w = max(stock_52w_csv['high'].to_numpy())
        last_open_day = stock_csv['date'].tail(1)
        stock_date_52w = stock_52w_csv[stock_52w_csv['high'] == max(stock_52w_csv['high'])]['date']
        if high_price_52w == 0:
            # print('This stock has issue for administration.')
            continue
        if last_open_day.iloc[0] == stock_date_52w.iloc[0]:
            continue
        # print(stock_date_52w)
        if high_price_52w > close_price_day:
            gap_percentage = round(((high_price_52w / close_price_day) * 100) - 100, 4)
            stock_list_52w.append([str(stock_name), str(stock_date_52w.iloc[0]), float(gap_percentage), high_price_52w])
            # print('Stock : {}, 52w high date : {}, Gap : {}%, 52w high price : {}'.format(stock_name,
            # stock_date_52w.iloc[0], gap_percentage, high_price_52w))
            count += 1
        elif high_price_52w < close_price_day:
            gap_percentage = round(((close_price_day / high_price_52w) * 100) - 100, 4)
            # print('{} is already hit the 52 weeks target! Going up {}%'.format(stock_name, gap_percentage))
    df = pd.DataFrame(stock_list_52w)
    df = df.rename(columns={0: 'stock', 1: 'date', 2: 'gap', 3: 'high'})
    df_csv = df.sort_values(by='gap', ascending=True)
    df_csv.to_csv('results/this_year/' + '52_weeks_analysis_{}.csv'.format(date),
                  encoding='utf-8', index=False, header=True)
    return df_csv


def base_year_high_52_weeks(df, base_year, date):
    stock_csv = df
    stock_date_52w = stock_csv[stock_csv['high'] == max(stock_csv['high'])]['date']
    stock_csv = stock_csv[stock_csv['date'] < base_year]
    if not os.path.exists('results/base_year/{}'.format(base_year)):
        os.makedirs('results/base_year/{}'.format(base_year))
    stock_csv.to_csv(
        'results/base_year/{}'.format(base_year) + '/' + '52_weeks_analysis_{}_before_{}.csv'.format(date,
                                                                           base_year),
        encoding='utf-8', index=False, header=True)
    return stock_csv


def stock_52w_stock_date_check(stock_name, base_year, date):
    date = util_52w.strdate_convert(date)
    base_date = date - timedelta(days=365)
    stock_list_52w = []
    if type(stock_name) == type(str()):
        stock_csv = pykrx_read_csv(stock_name, util_52w.Krx_Char_folder_path)
        nx = stock_csv.loc[stock_csv['date'] == str(date.date())].index
        if nx.empty:
            return None
        stock_csv = stock_csv.loc[:nx[0]]
        close_price_day = stock_csv.iloc[nx[0]]['close']
        stock_52w_csv = stock_csv[stock_csv['date'] >= base_date.strftime("%Y-%m-%d")]
        high_price_52w = max(stock_52w_csv['high'].to_numpy())
        last_open_day = stock_csv['date'].tail(nx[0]-1)
        stock_date_52w = stock_52w_csv[stock_52w_csv['high'] == max(stock_52w_csv['high'])]['date']
        if '스팩' in stock_name:
            pass
        if '리츠' in stock_name:
            pass
        if high_price_52w == 0:
            # print('This stock has issue for administration.')
            pass
        if last_open_day.iloc[0] == stock_date_52w.iloc[0]:
            pass
        # print(stock_date_52w)
        if high_price_52w > close_price_day:
            gap_percentage = round(((high_price_52w / close_price_day) * 100) - 100, 4)
            stock_list_52w.append([str(stock_name), str(stock_date_52w.iloc[0]), float(gap_percentage), high_price_52w])
            # print('Stock : {}, 52w high date : {}, Gap : {}%, 52w high price : {}'.format(stock_name, stock_date_52w.iloc[0], gap_percentage, high_price_52w))
        elif high_price_52w < close_price_day:
            gap_percentage = round(((close_price_day / high_price_52w) * 100) - 100, 4)
            # print('{} is already hit the 52 weeks target! Going up {}%'.format(stock_name, gap_percentage))
    elif type(stock_name) == type(list()):
        for stock_tic in stock_name:
            stock_52w_stock_date_check(stock_tic, base_year, date)
    df = pd.DataFrame(stock_list_52w)
    df = df.rename(columns={0: 'stock', 1: 'date', 2: 'gap', 3: 'high'})
    return df

def dolpa_stock_date_check(stock_name, base_year, date):
        date = util_52w.strdate_convert(date)
        base_date = date - timedelta(days=365)
        stock_list_52w = []
        if type(stock_name) == type(str()):
            stock_csv = pykrx_read_csv(stock_name, util_52w.Krx_Char_folder_path)
            nx = stock_csv.loc[stock_csv['date'] == str(date.date())].index
            if nx.empty:
                return None
            stock_csv = stock_csv.loc[:nx[0]]
            close_price_day = stock_csv.iloc[nx[0]]['close']
            stock_52w_csv = stock_csv[stock_csv['date'] >= base_date.strftime("%Y-%m-%d")]
            high_price_52w = max(stock_52w_csv['high'].to_numpy())
            last_open_day = stock_csv['date'].tail(nx[0] - 1)
            stock_date_52w = stock_52w_csv[stock_52w_csv['high'] == max(stock_52w_csv['high'])]['date']
            if '스팩' in stock_name:
                pass
            if '리츠' in stock_name:
                pass
            if high_price_52w == 0:
                # print('This stock has issue for administration.')
                pass
            if last_open_day.iloc[0] == stock_date_52w.iloc[0]:
                pass
            # print(stock_date_52w)
            if high_price_52w > close_price_day:
                gap_percentage = round(((high_price_52w / close_price_day) * 100) - 100, 4)
                stock_list_52w.append([str(stock_name), str(stock_date_52w.iloc[0]), float(gap_percentage), high_price_52w])
                # print('Stock : {}, 52w high date : {}, Gap : {}%, 52w high price : {}'.format(stock_name, stock_date_52w.iloc[0], gap_percentage, high_price_52w))
            elif high_price_52w < close_price_day:
                gap_percentage = round(((close_price_day / high_price_52w) * 100) - 100, 4)
                # print('{} is already hit the 52 weeks target! Going up {}%'.format(stock_name, gap_percentage)
        elif type(stock_name) == type(list()):
            for stock_tic in stock_name:
                stock_52w_stock_date_check(stock_tic, base_year, date)
        df = pd.DataFrame(stock_list_52w)
        df = df.rename(columns={0: 'stock', 1: 'date', 2: 'gap', 3: 'high'})
        return df

