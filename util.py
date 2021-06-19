from datetime import datetime


class util:
    def __init__(self):
        self.Krx_Char_folder_path = './Krx_Chart_folder'
        self.base_year_results_path = './results/base_year'
        self.this_year_results_path = './results/this_year'
        self.base_year = '2021-01-01'
        self.stock_name = "GS리테일"
        self.from_date = '20190101'
        self.today_date = datetime.today().strftime("%Y%m%d")

    def get_today_ymd(self):
        return datetime.today().strftime("%Y-%m-%d")

    def compare_timestamp_a_to_b(self, a, b):
        return b - a

    def nextday_timestamp_a_to_b(self, a):
        return a + 1

    def nextmonth_timestamp_a_to_b(self, a):
        return a + 30

    def strdate_convert(self, date):
        return datetime.strptime(date, "%Y-%m-%d")

    def cal_percent(self, a, b):
        if a > b:
            return round((((a / b) * 100) - 100), 2)
        else:
            return round(-(((b / a) * 100) - 100), 2)
