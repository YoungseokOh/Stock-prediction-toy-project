from datetime import datetime

class util:
    Krx_Char_folder_path = 'E:/Krx_Chart_folder'

    def __init__(self, path):
        self.Krx_Char_folder_path = path

    def get_today_ymd(self):
        return datetime.today().strftime("%Y%m%d")

    def compare_timestamp_a_to_b(self, a, b):
        return b - a

    def nextday_timestamp_a_to_b(self, a):
        return a + 1

    def nextmonth_timestamp_a_to_b(self, a):
        return a + 30
