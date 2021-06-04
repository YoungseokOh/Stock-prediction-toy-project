from datetime import datetime


class util:
    def __init__(self):
        self.Krx_Char_folder_path = 'E:/Krx_Chart_folder'
        self.base_year = '2021-01-01'
        self.stock_name = "코리아센터"
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
