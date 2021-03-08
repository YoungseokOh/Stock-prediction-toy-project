import stockapi.stock_api as stock
import time
import telegramapi.telegram_api as telegram
from datetime import datetime

stock_dict1 = {'name': '강원랜드', 'target_price': 26700}
stock_dict2 = {'name': '바텍', 'target_price': 27600}
stock_dict3 = {'name': '마크로젠', 'target_price': 35000}
target_stock_dict_list = [stock_dict1, stock_dict2, stock_dict3]

stock.login()  # 서버 로그인
all_stock_dict_list = stock.get_all_stock_list()  # 모든 종목명 조회

# shcode 셋팅
for stock_dict in target_stock_dict_list:
    stock_dict['shcode'] = stock.get_shcode_by_name(all_stock_dict_list, stock_dict.get('name'))

chat_id = telegram.get_chat_id('간다! 알리미')
idx = 0
today_ymd = datetime.today().strftime("%Y/%m/%d")  # YYYY/mm/dd 형태의 시간 출력
first_message = "★ " + today_ymd + " 모니터링 시작 ★\n"
for target_stock_dict in target_stock_dict_list:
    stock_code = target_stock_dict.get('shcode')
    stock_name = target_stock_dict.get('name')
    stock_current_price = stock.get_stock_current_price(shcode=stock_code)  # 현재가 조회
    stock_target_price = target_stock_dict.get('target_price')
    first_message += "[" + stock_name + "] " + str(stock_current_price) + " -> " + str(stock_target_price) + "\n"

telegram.send_message(chat_id=chat_id, message=first_message)
while 1:
    for target_stock_dict in target_stock_dict_list:
        stock_code = target_stock_dict.get('shcode')
        stock_name = target_stock_dict.get('name')
        stock_current_price = stock.get_stock_current_price(shcode=stock_code)  # 현재가 조회
        stock_target_price = target_stock_dict.get('target_price')

        if int(stock_current_price) == int(stock_target_price):
            text_message = '종목명: ' + stock_name + ' / 현재가: ' + str(stock_current_price) + ' / 매수목표가: ' + str(stock_target_price)
            telegram.send_message(chat_id=chat_id, message=text_message)
        time.sleep(2)

    idx += 1
    print(idx)
    if idx == 30000:
        break
