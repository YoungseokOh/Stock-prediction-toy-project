import os
import pandas as pd
from util import *


class Finance(util):
    def __init__(self):
        self.bt_fin_data = "./results"
        self.str_KOSPI = "KOSPI"
        self.str_KOSDAQ = "KOSDAQ"
        self.filter_words = ["스팩, 리츠"]


    def load_data(self, path, code=0):
        fd_path = path + os.path.join('/', 'NaverFinance_data.csv')
        finance_csv = pd.read_csv(fd_path, parse_dates=True)
        return finance_csv


    def refine_data(self, data, words):
        return 0
