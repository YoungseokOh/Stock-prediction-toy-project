import stockapi.stock_api as stock
import time
import telegramapi.telegram_api as telegram

stock_dict1 = {'name': '마크로젠', 'target_price': 34800}
stock_dict2 = {'name': 'SK하이닉스', 'target_price': 140000}
target_stock_dict_list = [stock_dict1, stock_dict2]

stock.login()  # 서버 로그인
all_stock_dict_list = stock.get_all_stock_list()  # 모든 종목명 조회

# shcode 셋팅
for stock_dict in target_stock_dict_list:
    stock_dict['shcode'] = stock.get_shcode_by_name(all_stock_dict_list, stock_dict.get('name'))

chat_id = telegram.get_chat_id('간다! 알리미')
idx = 0
while 1:
    for taget_stock_dict in target_stock_dict_list:
        stock_code = taget_stock_dict.get('shcode')
        stock_name = taget_stock_dict.get('name')
        stock_current_price = stock.get_stock_current_price(shcode=stock_code)  # 현재가 조회
        stock_target_price = taget_stock_dict.get('target_price')

        if int(stock_current_price) == int(stock_target_price):
            text_message = '종목명: ' + stock_name + ' / 현재가: ' + str(stock_current_price) + ' / 매수목표가: ' + str(stock_target_price)
            telegram.send_message(chat_id=chat_id, message=text_message)
        time.sleep(2)

    idx += 1
    print(idx)
    if idx == 30000:
        break
