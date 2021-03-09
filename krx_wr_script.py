from datetime import datetime
from pykrx import stock
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import MinMaxScaler
import os, glob
from datetime import datetime
from tqdm import tqdm
import numpy as np
Krx_Char_folder_path = 'D:/Krx_Chart_folder'
condition = '.csv'

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

def pykrx_save_csv(ticker, date_Start, date_End):
    stock_name = stock.get_market_ticker_name(ticker)
    stock_folder_name = stock_name + '_' + ticker
    df = stock.get_market_ohlcv_by_date(date_Start, date_End, ticker)
    df = df.reset_index()
    df = df.rename(columns={'날짜': 'date', '시가': 'open', '고가': 'high', '저가': 'low', '종가': 'close', '거래량': 'volume'})
    if not os.path.exists(Krx_Char_folder_path + '/' + stock_name):
        os.mkdir(Krx_Char_folder_path + '/' + stock_name)
    df.to_csv(Krx_Char_folder_path + '/' + stock_name + '/' + ticker + '.csv', sep=',', na_rep='0',
              index=False, header=True)
    # print('{} Daily chart saved! ==== ticker is : {}'.format(stock_name, ticker))

def pykrx_scratch(date_Start, date_End):
    print("Reading Daily Chart ... {} - {}".format(date_Start, date_End))
    # create main folder
    if not os.path.exists(Krx_Char_folder_path):
        os.mkdir(Krx_Char_folder_path)
    # ticker scratch
    KOSPI_ticker_list = stock.get_market_ticker_list(market="KOSPI")
    KOSDAQ_ticker_list = stock.get_market_ticker_list(market="KOSDAQ")
    # KOSPI save as csv
    print('Reading KOSPI...')
    for ticker_KOSPI in tqdm(KOSPI_ticker_list):
        pykrx_save_csv(ticker_KOSPI, date_Start, date_End)
    # KOSDAQ save as csv
    print('Reading KOSDAQ...')
    for ticker_KOSDAQ in tqdm(KOSDAQ_ticker_list):
        pykrx_save_csv(ticker_KOSDAQ, date_Start, date_End)
    print('Scratching daily chart is done!')

def pykrx_daily_update():
    #today_date = datetime.today().strftime("%Y%m%d")
    today_date = '20210223'
    df = stock.get_market_ohlcv_by_ticker(today_date, market="ALL")
    df = df.reset_index()
    del df['거래대금']
    del df['등락률']
    df_format = df
    #df.insert(5, '수정종가', df['종가'])
    count = 0
    for ticker in df['티커']:
        stock_name = stock.get_market_ticker_name(ticker)
        ticker_csv = pykrx_read_csv(stock_name)
        df_list = list(np.array(df.iloc[count].tolist()))
        df_list[0] = datetime.today().strftime("%Y-%m-%d")
        df_save = ticker_csv.append(pd.Series(df_list, index=ticker_csv.columns), ignore_index=True)
        df_save.to_csv(Krx_Char_folder_path + '/' + stock_name + '/' + ticker + '.csv', sep=',', na_rep='0', index=False,
                  header=False)
        print('{} Daily chart update is done!'.format(stock_name))
        count += 1

def pykrx_read_csv(stock_name):
    csv_file_path = search(Krx_Char_folder_path + '/' + stock_name, condition)
    if os.path.exists(csv_file_path[0]):
        stock_csv = pd.read_csv(csv_file_path[0], parse_dates=True)
    else:
        print('Can''t find csv file!')
    return stock_csv
    print('read done!')

def pykrx_read_train_set(stock_csv):
     df = stock_csv
     print(df.iloc[:, 4:5].tail())
     # df.insert(5, '수정종가', df['종가'])
     minmax = MinMaxScaler().fit(df.iloc[:, 4:5].astype('float32'))  # Close index
     df_log = minmax.transform(df.iloc[:, 4:5].astype('float32'))  # Close index
     df_log = pd.DataFrame(df_log)
     df_log.head()
     df_train = df_log
     df.shape, df_train.shape
     print('read done!')

     return df_train
