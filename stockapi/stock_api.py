import win32com.client
import pythoncom
from pathlib import Path


# ----------------------------------------------------------------------------
# login
# ----------------------------------------------------------------------------
class XASessionEventHandler:
    login_state = 0

    def OnLogin(self, code, msg):
        if code == "0000":
            print("로그인 성공")
            XASessionEventHandler.login_state = 1
        else:
            print("로그인 실패")


def login():
    user_id = "db0043"
    user_passwd = "Dbrhkd22"
    cert_passwd = ""
    instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEventHandler)
    instXASession.ConnectServer("demo.ebestsec.co.kr", 20001)  # hts.ebestsec.co.kr / demo.ebestsec.co.kr
    instXASession.Login(user_id, user_passwd, cert_passwd, 0, 0)

    while XASessionEventHandler.login_state == 0:
        pythoncom.PumpWaitingMessages()


# ----------------------------------------------------------------------------
# t1102 주식 현재가(시세) 조회
# ----------------------------------------------------------------------------
class XAQueryEventHandlerT1102:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT1102.query_state = 1


def get_stock_info_by_shcode(shcode):
    path = Path(__file__).parent / "xingapi/t1102.res"
    path = str(path).replace("\\", "\\\\")
    instXAQueryT1102 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT1102)
    instXAQueryT1102.ResFileName = path
    instXAQueryT1102.SetFieldData("t1102InBlock", "shcode", 0, shcode)
    instXAQueryT1102.Request(0)

    while XAQueryEventHandlerT1102.query_state == 0:
        pythoncom.PumpWaitingMessages()

    XAQueryEventHandlerT1102.query_state = 0
    return instXAQueryT1102


def get_stock_current_price(shcode):
    stock_info = get_stock_info_by_shcode(shcode)
    return stock_info.GetFieldData("t1102OutBlock", "price", 0)


# ----------------------------------------------------------------------------
# T8430 주식종목조회
# ----------------------------------------------------------------------------
class XAQueryEventHandlerT8430:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT8430.query_state = 1


def get_all_stock_list():
    path = Path(__file__).parent / "xingapi/t8430.res"
    path = str(path).replace("\\", "\\\\")
    instXAQueryT8430 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT8430)
    instXAQueryT8430.ResFileName = path
    instXAQueryT8430.SetFieldData("t8430InBlock", "gubun", 0, 0)  # 구분> 0:전체 / 1:코스피 / 2:코스닥
    instXAQueryT8430.Request(0)

    while XAQueryEventHandlerT8430.query_state == 0:
        pythoncom.PumpWaitingMessages()

    block_count = instXAQueryT8430.GetBlockCount("t8430OutBlock")
    all_stock_list = []
    for i in range(block_count):
        hname = instXAQueryT8430.GetFieldData("t8430OutBlock", "hname", i)
        shcode = instXAQueryT8430.GetFieldData("t8430OutBlock", "shcode", i)

        stock_dict = {'name': hname, 'shcode': shcode}
        all_stock_list.append(stock_dict)

    return all_stock_list


def get_shcode_by_name(stock_dict_list, stock_name):
    for stock_dict in stock_dict_list:
        if stock_name == stock_dict.get('name'):
            return stock_dict.get('shcode')