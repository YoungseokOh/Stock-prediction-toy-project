import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


BASE_URL = "https://finance.naver.com/sise/sise_market_sum.naver?sosok="
KOSPI_CODE = 0
KOSDAQ_CODE = 1
START_PAGE = 1
fields = []

def crawl(code, page):
    global fields
    data = {'menu':'market_sum',
            'fieldIds': fields,
            'returnUrl': BASE_URL + str(code) + "&page=" + str(page)}
    res = requests.post('https://finance.naver.com/sise/field_submit.nhn', data=data)
    page_soup = BeautifulSoup(res.text, 'lxml')
    table_html = page_soup.select_one('div.box_type_l')
    header_data = [item.get_text().strip() for item in table_html.select('thead th')][1:-1]
    inner_data = [item.get_text().strip() for item in table_html.find_all(lambda x:
                                                                          (x.name == 'a' and
                                                                           'tltle' in x.get('class', [])) or
                                                                          (x.name == 'td' and
                                                                           'number' in x.get('class', [])))]
    no_data = [item.get_text().strip() for item in table_html.select('td.no')]
    number_data = np.array(inner_data)
    number_data.resize(len(no_data), len(header_data))
    df = pd.DataFrame(data=number_data, columns=header_data)
    return df


def main(code):
    res = requests.get(BASE_URL + str(code) + "&page=" + str(START_PAGE))
    page_soup = BeautifulSoup(res.text, 'lxml')
    total_page_num = page_soup.select_one('td.pgRR > a')
    total_page_num = int(total_page_num.get('href').split('=')[-1])
    ipt_html = page_soup.select_one('div.subcnt_sise_item_top')
    global fields
    fields = [item.get('value') for item in ipt_html.select('input')]
    results = [crawl(code, str(page)) for page in range(1, total_page_num+1)]
    df = pd.concat(results, axis=0, ignore_index=True)
    if code == 0:
        save_name = 'KOSPI'
    elif code == 1:
        save_name = 'KOSDAQ'
    df.to_csv('./results/NaverFinance_data_{}.csv'.format(save_name))
    print('{} finance data is saved!'.format(save_name))

if __name__ == '__main__':
    CODE_LIST = [KOSPI_CODE, KOSDAQ_CODE]
    for i in CODE_LIST:
        main(i)
    print('Works are done!')