from krx_wr_script import *
from datetime import datetime
from datetime import timedelta
from analysis.technical_indicator import *
from util import *
from top_20_stocks import *
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib
import os
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

year_list = ['2014', '2015', '2016', '2017', '2018']
# rsi test
year_results_rsi = rsi_year_test(year_list)
plot_year_results(year_results_rsi, 'rsi')
# bb test
year_results_bb = BB_band_year_test(year_list)
plot_year_results(year_results_bb, 'Bollinger_band')
# # uo test
year_results_uo = uo_year_test(year_list)
plot_year_results(year_results_uo, 'Ultimate_oscillator')
print('work is done!')
