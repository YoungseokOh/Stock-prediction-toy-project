from analysis.technical_indicator import *
from analysis.top_20_stocks import *
from analysis.stock_52_weeks import *
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import os
from util import util

matplotlib.rcParams['axes.unicode_minus'] = False

# 1. RSI statistical analysis
# 2. Analysis of 52 weeks high past history
# 3. BB_band

def stock_year_list(year):
    stcal_ex = util('E:/{}_Stocks'.format(year))
    Krx_Char_folder_path = stcal_ex.Krx_Char_folder_path
    start_date = '{}0101'.format(int(year)-1)
    end_date = '{}1231'.format(int(year)+1)
    print('{} ~ {}'.format(start_date, end_date))
    # Scratch from start_date to end_date
    if not os.path.exists(Krx_Char_folder_path):
        pykrx_scratch(start_date, end_date, Krx_Char_folder_path)
    else:
        print('Folder is existed. Path is {}'.format(Krx_Char_folder_path))
    stock_list = os.listdir(Krx_Char_folder_path)
    return stock_list, Krx_Char_folder_path

def plot_year_results(results_list, title_save):
    year_results = results_list
    fig = plt.figure()
    ax = fig.add_subplot(111)
    N = 5
    ind = np.arange(N)
    width = 0.25
    next_days = ax.bar(ind + 0.15, year_results[1], width=0.2, color='b', align='center')
    next_months = plt.bar(ind + 0.35, year_results[2], width=0.2, color='r', align='center')
    ax.set_ylabel('%')
    ax.set_xlabel('Year')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(year_results[0])
    ax.legend((next_days[0], next_months[0]), ('Next day', 'Next month'))
    ax.grid()
    ax.set_title('{} test by YoY'.format(title_save))
    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1 * h, '%.1f' % float(h) + '%',
                    ha='center', va='bottom', size=8)
    autolabel(next_days)

    autolabel(next_months)
    fig.gca()
    fig.savefig('../results/{}_year_results_+-version.png'.format(title_save))

def BB_band_year_test(year_list):
    year_results = []
    for year in year_list:
        stock_list, year_path = stock_year_list(year)
        stock_rsi_day = []
        stock_rsi_next_day = []
        stock_rsi_next_month = []
        for stock in tqdm(stock_list):
            stock_csv = cal_technical_indicator_name(stock, year_path)
            if stock_csv.empty:
                print('This stock is empty : {}'.format(stock))
                continue
            if '스팩' in stock:
                continue
            if len(stock_csv['date']) < 200:
                continue
            stock_bool = stock_csv['lower_band'] > stock_csv['close']
            stock_csv['bb_bool'] = stock_bool
            if stock_csv['bb_bool'].sum() == 0: # This stock had moved in BB
                continue
            bb_csv = stock_csv.iloc[stock_csv['bb_bool'].values == True]
            # print(bb_csv)
            bb_csv['bb_p'] = 100 - (bb_csv['close'] / bb_csv['lower_band'] * 100)
            bb_csv = sorting_by_column(bb_csv, 'bb_p', False, len(bb_csv))
            bb_csv = bb_csv.dropna(axis=0) # zero handling
            nx = stock_csv.loc[stock_csv['date'] == bb_csv['date'].iloc[0]].index
            # print('nx num : {}'.format(nx[0]))
            if nx[0] == (len(stock_csv['date']) - 1):
                continue
            stock_csv_next_day = stock_csv.loc[int(nx[0]) + 1]
            if stock_csv.index[-1] < int(nx[0]) + 15:
                continue
            # print(stock)
            # print(stock_csv.loc[int(nx[0]) + 15])
            stock_csv_next_month = stock_csv.loc[int(nx[0]) + 15]
            stock_rsi_next_day.append([str(stock), (((stock_csv_next_day['close'] - bb_csv['close'].iloc[0]) / bb_csv['close'].iloc[0]) * 100)])
            stock_rsi_next_month.append([str(stock), (((stock_csv_next_month['close'] - bb_csv['close'].iloc[0]) / bb_csv['close'].iloc[0]) * 100)])
            stock_rsi_next_day = pd.DataFrame(stock_rsi_next_day)
            stock_rsi_next_month = pd.DataFrame(stock_rsi_next_month)
        year_results.append([year, stock_rsi_next_day[1].sum() / len(stock_rsi_next_day), stock_rsi_next_month[1].sum() / len(stock_rsi_next_month)])
        print(stock_rsi_next_day[1].sum() / len(stock_rsi_next_day))
        print(stock_rsi_next_month[1].sum() / len(stock_rsi_next_month))
    year_results = pd.DataFrame(year_results)
    return year_results

def rsi_year_test(year_list):
    year_results = []
    for year in year_list:
        stock_list, year_path = stock_year_list(year)
        stock_rsi_day = []
        stock_rsi_next_day = []
        stock_rsi_next_month = []
        for stock in tqdm(stock_list):
            stock_csv = cal_technical_indicator_name(stock, year_path)
            if stock_csv.empty:
                print('This stock is empty : {}'.format(stock))
                continue
            if '스팩' in stock:
                continue
            if len(stock_csv['date']) < 200:
                continue
            stock_csv_rsi = sorting_by_column(stock_csv, 'rsi', True, 20)
            stock_csv_rsi = stock_csv_rsi.dropna(axis=0) # zero handling
            nx = stock_csv.loc[stock_csv['date'] == stock_csv_rsi['date'].iloc[0]].index
            if nx[0] == (len(stock_csv['date']) - 1):
                continue
            stock_csv_next_day = stock_csv.loc[int(nx[0]) + 1]
            if stock_csv.index[-1] <= int(nx[0]) + 15:
                continue
            stock_csv_next_month = stock_csv.loc[int(nx[0]) + 15]
            stock_rsi_next_day.append([str(stock), (((stock_csv_next_day['close'] - stock_csv_rsi['close'].iloc[0]) / stock_csv_rsi['close'].iloc[0]) * 100)])
            stock_rsi_next_month.append([str(stock), (((stock_csv_next_month['close'] - stock_csv_rsi['close'].iloc[0]) / stock_csv_rsi['close'].iloc[0]) * 100)])
            stock_rsi_next_day = pd.DataFrame(stock_rsi_next_day)
            stock_rsi_next_month = pd.DataFrame(stock_rsi_next_month)
        year_results.append([year, stock_rsi_next_day[1].sum() / len(stock_rsi_next_day), stock_rsi_next_month[1].sum() / len(stock_rsi_next_month)])
        print(stock_rsi_next_day[1].sum() / len(stock_rsi_next_day))
        print(stock_rsi_next_month[1].sum() / len(stock_rsi_next_month))
    year_results = pd.DataFrame(year_results)
    return year_results

def uo_year_test(year_list):
    year_results = []
    for year in year_list:
        stock_list, year_path = stock_year_list(year)
        stock_rsi_day = []
        stock_rsi_next_day = []
        stock_rsi_next_month = []
        for stock in tqdm(stock_list):
            stock_csv = cal_technical_indicator_high_class(stock, year_path)
            if stock_csv.empty:
                print('This stock is empty : {}'.format(stock))
                continue
            if '스팩' in stock:
                continue
            if len(stock_csv['date']) < 200:
                continue
            stock_csv_uo = sorting_by_column(stock_csv, 'uo', True, 20)
            stock_csv_uo = stock_csv_uo.dropna(axis=0) # zero handling
            nx = stock_csv.loc[stock_csv['date'] == stock_csv_uo['date'].iloc[0]].index
            if nx[0] == (len(stock_csv['date']) - 1):
                continue
            stock_csv_next_day = stock_csv.loc[int(nx[0]) + 1]
            if stock_csv.index[-1] <= int(nx[0]) + 15:
                continue
            stock_csv_next_month = stock_csv.loc[int(nx[0]) + 15]
            stock_rsi_next_day.append([str(stock), (((stock_csv_next_day['close'] - stock_csv_uo['close'].iloc[0]) / stock_csv_uo['close'].iloc[0]) * 100)])
            stock_rsi_next_month.append([str(stock), (((stock_csv_next_month['close'] - stock_csv_uo['close'].iloc[0]) / stock_csv_uo['close'].iloc[0]) * 100)])
            stock_rsi_next_day = pd.DataFrame(stock_rsi_next_day)
            stock_rsi_next_month = pd.DataFrame(stock_rsi_next_month)
        year_results.append([year, stock_rsi_next_day[1].sum() / len(stock_rsi_next_day), stock_rsi_next_month[1].sum() / len(stock_rsi_next_month)])
        print(stock_rsi_next_day[1].sum() / len(stock_rsi_next_day))
        print(stock_rsi_next_month[1].sum() / len(stock_rsi_next_month))
    year_results = pd.DataFrame(year_results)
    return year_results

def uo_year_test(year_list):
    year_results = []
    for year in year_list:
        stock_list, year_path = stock_year_list(year)
        stock_rsi_day = []
        stock_rsi_next_day = []
        stock_rsi_next_month = []
        for stock in tqdm(stock_list):
            stock_csv = cal_technical_indicator_high_class(stock, year_path)
            if stock_csv.empty:
                print('This stock is empty : {}'.format(stock))
                continue
            if '스팩' in stock:
                continue
            if len(stock_csv['date']) < 200:
                continue
            stock_csv_uo = sorting_by_column(stock_csv, 'uo', True, 20)
            stock_csv_uo = stock_csv_uo.dropna(axis=0) # zero handling
            nx = stock_csv.loc[stock_csv['date'] == stock_csv_uo['date'].iloc[0]].index
            if nx[0] == (len(stock_csv['date']) - 1):
                continue
            stock_csv_next_day = stock_csv.loc[int(nx[0]) + 1]
            if stock_csv.index[-1] <= int(nx[0]) + 15:
                continue
            stock_csv_next_month = stock_csv.loc[int(nx[0]) + 15]
            stock_rsi_next_day.append([str(stock), (((stock_csv_next_day['close'] - stock_csv_uo['close'].iloc[0]) / stock_csv_uo['close'].iloc[0]) * 100)])
            stock_rsi_next_month.append([str(stock), (((stock_csv_next_month['close'] - stock_csv_uo['close'].iloc[0]) / stock_csv_uo['close'].iloc[0]) * 100)])
            stock_rsi_next_day = pd.DataFrame(stock_rsi_next_day)
            stock_rsi_next_month = pd.DataFrame(stock_rsi_next_month)
        year_results.append([year, stock_rsi_next_day[1].sum() / len(stock_rsi_next_day), stock_rsi_next_month[1].sum() / len(stock_rsi_next_month)])
        print(stock_rsi_next_day[1].sum() / len(stock_rsi_next_day))
        print(stock_rsi_next_month[1].sum() / len(stock_rsi_next_month))
    year_results = pd.DataFrame(year_results)
    return year_results

def cal_golden_percent(stock_csv, date, nx_num):
    if not (stock_csv['date'] == date).any():
        return 0
    else:
        nx = stock_csv.loc[stock_csv['date'] == date].index
        stock_ti_by_date = stock_csv.loc[int(nx[0]) + int(nx_num)]
        upper_percentage = util_s.cal_percent(int((stock_ti_by_date['upper_band'])), int(stock_ti_by_date['close']))
        short_golden = util_s.cal_percent(int(stock_ti_by_date['ema7']), int(stock_ti_by_date['ema50']))
        mid_golden = util_s.cal_percent(int(stock_ti_by_date['ema50']), int(stock_ti_by_date['ema99']))
        long_golden = util_s.cal_percent(int(stock_ti_by_date['ema7']), int(stock_ti_by_date['ema99']))
        return list([stock_ti_by_date['date'], stock_ti_by_date['close'], upper_percentage, short_golden, mid_golden, long_golden, round(stock_ti_by_date['rsi'], 2)])

def base_year_each_stock_analysis(stock_name, base_year, date, data_path ,nx_num):
    stock_base_year = stock_52w_stock_date_check(stock_name, base_year, date)
    stock_ti = cal_technical_indicator_name(stock_base_year['stock'][0], data_path)
    if cal_golden_percent(stock_ti, date, nx_num) == 0:
        return None
    else:
        golden_list_today = cal_golden_percent(stock_ti, date, nx_num)
    stock_base_year = stock_base_year.values.tolist()
    stock_base_year[0].extend(golden_list_today)
    df = pd.DataFrame(stock_base_year)
    df = df.rename(columns={0: 'stock', 1: 'high_date', 2: 'gap', 3: 'high', 4: 'close_date', 5: 'close', 6: 'upper_percent', 7:'short_golden', 8: 'mid_golden', 9: 'long_golden', 10: 'rsi'})
    return df


util_s = util()
stock_name = util_s.stock_name
base_year = util_s.base_year
date = '2021-03-11'
path = util_s.Krx_Char_folder_path
# stock_csv = base_year_each_stock_analysis(stock_name, base_year, date, path, 0) # zero means 'today'

date = util_s.strdate_convert('2021-01-10') # from 2021.1.1
timed = datetime.today() - date
time_inv = [0, 1, 2, 7, 14]

for i in tqdm(range(int(timed.days))):
    date_i = str(date.date())
    date += timedelta(days=i)
    print(date)
    results_52w_csv = 'results/this_year/' + '52_weeks_analysis_' + date_i + '.csv'
    results_52w_base_year_csv = 'results/base_year/' + '52_weeks_analysis_' + date_i + '_before_' + base_year + '.csv'
    results_path = util_s.base_year_results_path + '/' + 'daily_top10_results' + '/' + date_i
    if not os.path.exists(results_52w_csv):
        df_52w_csv = stock_52w_update(util_s.Krx_Char_folder_path, str(date.date()))
    else:
        df_52w_csv = pd.read_csv(results_52w_csv)
    if not os.path.exists(results_52w_base_year_csv):
        base_52w_csv = base_year_high_52_weeks(df_52w_csv, util_s.base_year, str(date.date()))
    else:
        base_52w_csv = pd.read_csv(results_52w_base_year_csv)
    base_52w_csv_top_10 = base_52w_csv[:10]['stock'].values.tolist()
    for j in base_52w_csv_top_10:
        # path exist check
        if not os.path.exists(results_path + '/' + j):
            os.makedirs(results_path + '/' + j)
        stock_results_list = []
        for k in time_inv:
            stock_csv = base_year_each_stock_analysis(j, base_year, date_i, path, k)
            if stock_csv is None:
                continue
            else:
                stock_results_list.append(stock_csv.values.tolist()[0])
        df_save = DataFrame(stock_results_list, columns=['stock', 'high_date', 'gap', 'high', 'close_date',
                                                         'close', 'upper_percent', 'short_golden', 'mid_golden', 'long_golden', 'rsi'])
        df_save.to_csv(results_path + '/' + j + '/' + date_i + '_results.csv', sep=',', na_rep='0', index=False,
                  header=False)





# Must move to main work's!
# year_list = ['2014', '2015', '2016', '2017', '2018']
# # rsi test
# year_results_rsi = rsi_year_test(year_list)
# plot_year_results(year_results_rsi, 'rsi')
# # bb test
# year_results_bb = BB_band_year_test(year_list)
# plot_year_results(year_results_bb, 'Bollinger_band')
# # # uo test
# year_results_uo = uo_year_test(year_list)
# plot_year_results(year_results_uo, 'Ultimate_oscillator')
# print('work is done!')
