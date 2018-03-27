#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import random

import time

import requests
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from spider.RequestUsingProxy import RequestUsingProxy

search_detail_prefix = "http://www.qichacha.com/firm_%s.html"
search_intellect_prefix = "http://www.qichacha.com/cassets_%s"
search_code_prefix = "http://www.qichacha.com/search?key=%s"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
cookies = {"_uab_collina": "152137769263657528740817"}
all_firms_info = {}


# field_list = ['纳税人识别号', '组织结构代码', '经营状态', '经营范围', '网站信息', '行政处罚']
def is_legal(firm_name):
    return firm_name != '-'


def read_firm_list_from_json(file_path):
    firm_list = []
    with open(file_path, 'r') as file:
        data = file.read()
    dict = json.loads(data)
    for (key, value) in dict.items():
        if value == {}:
            continue
        else:
            firm_name = value['公司名称'.decode('utf-8')]
            if is_legal(firm_name):
                firm_list.append(firm_name)
    return firm_list


def request_code_from_web(firm):
    search_code_url = search_code_prefix % firm.decode('utf-8')
    print search_code_url
    html = do_send_request(search_code_url)
    soup = BeautifulSoup(html, 'html.parser')
    href = soup.find(attrs={'class': 'ma_h1'})['href']
    firm_code = extract_code_from_href(href)
    return firm_code


def do_send_request(search_code_url):
    data = requests.get(search_code_url, headers=headers).content
    print data
    return data
    # return RequestUsingProxy().make_request(search_code_url, headers, cookies)


def extract_code_from_href(href):
    try:
        firm_code = href[href.rfind("_") + 1:href.rfind(".")]
    except:
        print "extract firm code failed", href
        raise
    return firm_code


def request_detail_page(firm_code):
    search_detail_url = search_detail_prefix % firm_code
    print search_detail_url
    html = do_send_request(search_detail_url)
    return html


def parse_field_from_page(detail_page):
    firm_dict = {}
    soup = BeautifulSoup(detail_page, 'html.parser')
    table = soup.find_all('table', attrs={'class': 'ntable'})[1]
    for tr in table.findAll('tr'):
        results = tr.findAll('td')
        key_left = results[0].getText().replace('\n', '').replace(' ', '').strip()[:-1]
        value_left = results[1].getText().replace('\n', '').replace(' ', '').strip()
        firm_dict[key_left] = value_left
        if len(results) == 4:
            key_right = results[2].getText().replace('\n', '').replace(' ', '').strip()[:-1]
            value_right = results[3].getText().replace('\n', '').replace(' ', '').strip()
            firm_dict[key_right] = value_right


def write_to_file(content, output_file):
    with open(output_file, 'w') as file:
        file.write(content)


def output_firm_info(input_file, output_file):
    firm_list = read_firm_list_from_json(input_file)
    for firm in firm_list:
        try:
            firm_code = request_code_from_web(firm)
            detail_page = request_detail_page(firm_code)
            field_dict = parse_field_from_page(detail_page)
            all_firms_info[firm] = field_dict
            write_to_file(json.dumps(all_firms_info), output_file)
            time.sleep(random.randint(5, 10))
        except:
            print "extract firm info failed,firm is:", firm
            raise


# output_firm_info('p2p2018.json', 'result2018.json')
# do_send_request("http://www.qichacha.com/search?key=xiaomi")
do_send_request("http://www.qichacha.com/search?key=xiaomi")