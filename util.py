from datetime import datetime


def get_today_ymd():
    return datetime.today().strftime("%Y%m%d")


def compare_timestamp_a_to_b(a, b):
    return b - a
