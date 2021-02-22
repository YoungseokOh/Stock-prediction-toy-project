from datetime import datetime
from pykrx import stock
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import MinMaxScaler
import os, glob

Krx_Char_folder_path = 'E:/Krx_Chart_folder'

def pykrx_scratch(date_Start, date_End):
    print("Reading Daily Chart ... {} - {}".format(date_Start, date_End))
    # create main folder
    if not os.path.exists(Krx_Char_folder_path):
        os.mkdir(Krx_Char_folder_path)
    # ticker scratch
    for ticker in stock.get_market_ticker_list(market="ALL"):
        stock_name = stock.get_market_ticker_name(ticker)
        stock_folder_name = stock_name + '_' + ticker
        #print(stock_name, ticker)
        df = stock.get_market_ohlcv_by_date(date_Start, date_End, ticker)
        df = df.reset_index()
        #print(len(df))
        df.insert(5, '종가2', df['종가'])
        # folder check
        if not os.path.exists(Krx_Char_folder_path + '/' + stock_name):
            os.mkdir(Krx_Char_folder_path + '/' + stock_name)
        df.to_csv(Krx_Char_folder_path + '/' + stock_name + '/' + ticker + '.csv', sep=',', na_rep='0', index=False, header=False)
        print('{} Daily chart is written! ==== ticker is : {}'.format(stock_name, ticker))
    print('Scratching daily chart is done!')

def search(data_path, extension):
    """Returns the list of files have extension (only current directory)
    Args:
        data_path (str): data path
        extension (str): extension
    Returns:
        file_list (list): file list with path
   """
    file_list = []
    for filename in os.listdir(data_path):
        ext = os.path.splitext(filename)[-1]
        if ext == extension:
            file_list.append(data_path+'/'+filename)
    return file_list

def pykrx_read_csv(stock_name):
    folder_list = os.listdir(Krx_Char_folder_path)
    condition = '.csv'
    csv_file_path = search(Krx_Char_folder_path + '/' + stock_name, condition)
    if os.path.exists(csv_file_path[0]):
        stock_csv = pd.read_csv(csv_file_path[0])
    else:
        print('Can''t find csv file!')
    return stock_csv
    print('read done!')

def pykrx_read_train_set():

    # print(df.iloc[:, 4:5].tail())
    # minmax = MinMaxScaler().fit(df.iloc[:, 4:5].astype('float32'))  # Close index
    # df_log = minmax.transform(df.iloc[:, 4:5].astype('float32'))  # Close index
    # df_log = pd.DataFrame(df_log)
    # df_log.head()
    # df_train = df_log
    # df.shape, df_train.shape
    print('read done!')
