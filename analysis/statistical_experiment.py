from krx_wr_script import *
from datetime import datetime
from datetime import timedelta
from analysis.technical_indicator import *
from util import *
from top_20_stocks import *
from tqdm import tqdm
import os

# 1. RSI statistical analysis
# 2. Analysis of 52 weeks high past history

stcal_ex = util('E:/2018_Stocks')
Krx_Char_folder_path = stcal_ex.Krx_Char_folder_path
start_date = '20180101'
end_date = '20181231'
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
    else:
        stock_csv_next_day = stock_csv.loc[int(nx[0]) + 1]
    stock_rsi_day.append([str(stock), int(stock_csv_rsi['close'].iloc[0]), int(stock_csv_rsi['rsi'].iloc[0])])
    # stock_rsi_next_day.append([str(stock), int(stock_csv_next_day['close']), int(stock_csv_next_day['rsi'])])
    # print(stock_rsi_day)
# df = pd.DataFrame(stock_rsi_day)
print('work is done!')
