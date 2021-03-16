import stockapi.stock_api as stock
import time
import telegramapi.telegram_api as telegram
import util
from datetime import datetime

target_stock_dict_list = [
    {'name': '강원랜드', 'target_price': 26700},
    {'name': '강남제비스코', 'target_price': 26500},
    {'name': '마크로젠', 'target_price': 35000},
    {'name': '용평리조트', 'target_price': 5200},
    {'name': '코리아센터', 'target_price': 9790},
    {'name': '나노캠텍', 'target_price': 2155},
    {'name': '대한약품', 'target_price': 34700},
    {'name': 'GS리테일', 'target_price': 38300},
    {'name': 'BGF리테일', 'target_price': 181000},
    {'name': '아스트', 'target_price': 6730},
    {'name': '셀리버리', 'target_price': 139900},
    {'name': '현대그린푸드', 'target_price': 9990},
    {'name': 'GS홈쇼핑', 'target_price': 149000},
    {'name': '국도화학', 'target_price': 60000},
    {'name': '금화피에스시', 'target_price': 30200},
    {'name': '코텍', 'target_price': 10600},
    {'name': '씨큐브', 'target_price': 8900},
    {'name': '신한지주', 'target_price': 37850},
    {'name': '삼익악기', 'target_price': 1730},
    {'name': '우리금융지주', 'target_price': 10750},
    {'name': '코리안리', 'target_price': 8900},
    {'name': 'GKL', 'target_price': 18150},
    {'name': '퍼시스', 'target_price': 31500},
    {'name': '신송홀딩스', 'target_price': 4930},
    {'name': '금호타이어', 'target_price': 4280}
]

stock.login()  # 서버 로그인
all_stock_dict_list = stock.get_all_stock_list()  # 모든 종목명 조회

# shcode 기본셋팅
for stock_dict in target_stock_dict_list:
    stock_dict['shcode'] = stock.get_shcode_by_name(all_stock_dict_list, stock_dict.get('name'))

chat_id = -1001413647771  # 간다! 알리미


def send_start_push_message():
    today_ymd = datetime.today().strftime("%Y/%m/%d")
    first_message = "★ " + today_ymd + " 돌파매매 모니터링 리스트 ★\n(아래 표기된 가격을 돌파하면 뭐다? 간다!)\n"
    idx = 1
    for target_stock_dict in target_stock_dict_list:
        stock_name = target_stock_dict.get('name')
        stock_target_price = target_stock_dict.get('target_price')
        first_message += str(idx) + " [" + stock_name + "] " + str(stock_target_price) + "\n"
        idx += 1

    telegram.send_message(chat_id=chat_id, message=first_message)


def run_main_monitoring():
    idx = 0
    while 1:
        for target_stock_dict in target_stock_dict_list:
            stock_code = target_stock_dict.get('shcode')
            stock_name = target_stock_dict.get('name')
            stock_current_price = stock.get_stock_current_price(shcode=stock_code)  # 현재가 조회
            stock_target_price = target_stock_dict.get('target_price')

            now_time = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
            print(now_time + " [" + stock_name + "] " + str(stock_current_price) + " -> " + str(stock_target_price))
            if int(stock_current_price) >= int(stock_target_price):  # 현재가격 >= 돌파가격 이면
                text_message = '★ 매수알림 [' + stock_name + '] / 현재가: ' + str(stock_current_price) + ' / 돌파가: ' + str(
                    stock_target_price)
                telegram.send_message(chat_id=chat_id, message=text_message)  # 매수 알림
                print(text_message)
                target_stock_dict_list.remove(target_stock_dict)  # 매수알림 후 타겟 리스트에서 제거
            time.sleep(0.2)  # api 제약: 1초당 5건 조회 제한으로 인해 0.2초씩 중지

        idx += 1
        print(idx)
        if idx > 99999:
            break
        market_end_time = datetime.strptime(util.get_today_ymd() + " 15:30:00", "%Y%m%d %H:%M:%S").timestamp()
        diff_time = util.compare_timestamp_a_to_b(datetime.now().timestamp(), market_end_time)
        if diff_time < 0:
            break


# ------------------------------run main script----------------------------------------
send_start_push_message()
run_main_monitoring()
