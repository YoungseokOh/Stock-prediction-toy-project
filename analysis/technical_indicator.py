from finta import TA
from krx_wr_script import *

def cal_technical_indicator_name(stock_name, path):
    stock_csv = pykrx_read_csv(stock_name, path)
    stock_csv['ema12'] = TA.EMA(stock_csv, 12)
    stock_csv['ema25'] = TA.EMA(stock_csv, 25)
    stock_csv['ema99'] = TA.EMA(stock_csv, 99)
    stock_csv['upper_band'] = TA.BBANDS(stock_csv)['BB_UPPER']
    stock_csv['lower_band'] = TA.BBANDS(stock_csv)['BB_LOWER']
    stock_csv['rsi'] = TA.RSI(stock_csv, 14)
    return stock_csv

def cal_technical_indicator_personal(stock_name, path, st, mt, lt, BB, rsi_d):
    stock_csv = pykrx_read_csv(stock_name, path)
    stock_csv['ema{}'.format(str(st))] = TA.EMA(stock_csv, st)
    stock_csv['ema{}'.format(str(mt))] = TA.EMA(stock_csv, mt)
    stock_csv['ema{}'.format(str(lt))] = TA.EMA(stock_csv, lt)
    if BB == True:
        stock_csv['upper_band'] = TA.BBANDS(stock_csv)['BB_UPPER']
        stock_csv['lower_band'] = TA.BBANDS(stock_csv)['BB_LOWER']
    stock_csv['rsi_{}'.format(str(rsi_d))] = TA.RSI(stock_csv, rsi_d)
    return stock_csv

def cal_technical_indicator_high_class(stock_name, path):
    stock_csv = pykrx_read_csv(stock_name, path)
    stock_csv['uo'] = TA.UO(stock_csv)
    stock_csv['trix'] = TA.TRIX(stock_csv, 30)
    stock_csv['mom'] = TA.MOM(stock_csv)
    return stock_csv

