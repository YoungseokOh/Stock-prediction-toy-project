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

# 1. RSI statistical analysis
# 2. Analysis of 52 weeks high past history

def plot_rsi_year_results(results_list):
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
    ax.set_title('RSI test by YOY')
    fig.savefig('../results/rsi_year_results.png')

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1 * h, '%.1f' % float(h) + '%',
                    ha='center', va='bottom', size=8)
    autolabel(next_days)
    autolabel(next_months)

def rsi_year_test(year_list):
    year_results = []
    for year in year_list:
        stcal_ex = util('E:/{}_Stocks'.format(year))
        Krx_Char_folder_path = stcal_ex.Krx_Char_folder_path
        start_date = '{}0101'.format(year)
        end_date = '{}1231'.format(year)
        # Scratch from start_date to end_date
        if not os.path.exists(Krx_Char_folder_path):
            pykrx_scratch(start_date, end_date, Krx_Char_folder_path)
        else:
            print('Folder is existed. Path is {}'.format(Krx_Char_folder_path))
        stock_list = os.listdir(Krx_Char_folder_path)
        stock_rsi_day = []
        stock_rsi_next_day = []
        stock_rsi_next_month = []
        for stock in tqdm(stock_list):
            stock_csv = cal_technical_indicator_name(stock, Krx_Char_folder_path)
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

year_list = ['2014', '2015', '2016', '2017', '2018']
year_results = rsi_year_test(year_list)
print('work is done!')
