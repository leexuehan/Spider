#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import random
import sys
import time
import traceback

import requests
from bs4 import BeautifulSoup

from spider.IPPool import valid_ip_proxies
from spider.RequestUsingProxy import RequestUsingProxy

reload(sys)
sys.setdefaultencoding('utf-8')


class WdzjHelper(object):
    def __init__(self):
        self.all_plat_url = 'https://www.wdzj.com/wdzj/html/json/dangan_search.json'
        self.problem_plat_url = 'https://shuju.wdzj.com/problem-list-all.html?year=%d'
        self.plat_basic_detail_url = 'https://www.wdzj.com/dangan/%s/'
        self.plat_gongshang_detail_url = 'https://www.wdzj.com/dangan/%s/gongshang/'
        self.extract_gongshang_fields = ['公司名称', '统一社会信用代码', '法人代表', '公司类型', '注册地址', '开业日期', '营业期限'
            , '经营范围', '备案域名', '备案单位名称', 'ICP备案号', '备案单位性质', 'ICP经营许可证', '备案时间']
        self.final_output = {}
        self.ip_proxies = valid_ip_proxies

    # load data from website only use once
    def load_all_plat_info(self):
        response = requests.get(self.all_plat_url)
        if response.status_code == 200:
            with open('p2p_table_info.json', 'w') as table:
                table.write(response.content)
        else:
            print response.status_code, response.content
            print "get all plat info failed"

    # load problem plat data from website only use once
    def get_all_problem_plats_by_year(self, year):
        url = self.problem_plat_url % year
        print url
        response = requests.get(url)
        if response.status_code == 200:
            file_name = 'problem_p2p_info%d.json' % year
            with open('./plat/' + file_name, 'w') as table:
                table.write(response.content)
        else:
            print response.status_code, response.content
            print "get problem plat failed"

    def get_plat_pin_by_platname(self, platname):
        with open('p2p_table_info.json', 'r') as file:
            data_list = json.loads(file.read())
        for data in data_list:
            if data['platName'] == platname:
                return data['platPin']

    def add_basic_info(self, platname, each_plat_info_dict):
        pin = self.get_plat_pin_by_platname(platname)
        if pin is None:
            print "找不到平台的pin值:", platname
        else:
            request_url = self.plat_basic_detail_url % pin
            print request_url
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}  # 构造头部
            html = RequestUsingProxy().make_request(headers=headers, url=request_url)
            self.parse_basic_html_with_soup(html, each_plat_info_dict)

    def add_gongshang_info(self, platname, each_plat_info_dict):
        pin = self.get_plat_pin_by_platname(platname)
        if pin is None:
            print "找不到pin值:", platname
        else:
            request_url = self.plat_gongshang_detail_url % pin
            print request_url
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}  # 构造头部
            html = RequestUsingProxy().make_request(headers=headers, url=request_url)
            self.parse_gongshang_html_with_soup(html, each_plat_info_dict)

    def parse_basic_html_with_soup(self, html, each_plat_info_dict):
        soup = BeautifulSoup(html, 'html.parser')
        tag = soup.find_all("h1")
        each_plat_info_dict['平台名称'] = tag[0].string
        each_plat_info_dict['收益率'] = soup.find_all(attrs={'class': 'tab_common_data'})[0].string + "%"
        each_plat_info_dict['投资期限'] = soup.find_all(attrs={'class': 'tab_common_data'})[1].string + "月"
        each_plat_info_dict['昨日成交量'] = soup.find_all(attrs={'class': 'tab_common_data'})[2].string + "万"
        each_plat_info_dict['昨日待还余额'] = soup.find_all(attrs={'class': 'tab_common_data'})[3].string + "万"
        tag = soup.find_all(attrs={'class': 'bgbox-bt zzfwbox'})[0]
        each_plat_info_dict['注册资金'] = tag.find(attrs={'class': 'r'}).string.replace(
                '\n', '').replace(' ', '').strip()
        each_plat_info_dict['保障模式'] = soup.select(
                'body > div.mt10.mb10 > div > div.dabox-left > div.bgbox-bt.zzfwbox > dl:nth-of-type(2) > dd:nth-of-type(4) > div.r')[
            0].string.strip()
        each_plat_info_dict['风险准备金存管'] = soup.select(
                'body > div.mt10.mb10 > div > div.dabox-left > div.bgbox-bt.zzfwbox > dl:nth-of-type(2)'
                ' > dd:nth-of-type(5) > div.r > span.p')[0].string

    def parse_gongshang_html_with_soup(self, html, each_plat_info_dict):
        soup = BeautifulSoup(html, 'html.parser')
        # links = soup.find_all('td', attrs={'class': 't'})
        self.extract_basic_gongshang_info(soup, each_plat_info_dict)
        each_plat_info_dict['经营异常'] = self.extract_yichangjingying_info(soup)
        each_plat_info_dict['股权信息'] = self.extract_stock_info(soup)

    def extract_basic_gongshang_info(self, soup, each_plat_info_dict):
        links = soup.find_all('td')
        for link in links:
            if link.string in self.extract_gongshang_fields:
                each_plat_info_dict[link.string] = link.next_sibling.next_sibling.string

    def add_plat_info_to_file(self, platname, each_plat_info_dict, filename):
        self.final_output[platname] = each_plat_info_dict
        output = json.dumps(self.final_output, encoding='utf-8', ensure_ascii=False)
        with open(filename, 'w') as output_file:
            output_file.write(output)
            print "输出%s企业信息完成" % platname

    def extract_yichangjingying_info(self, soup):
        business_exception = {}
        ths = []
        tds = []
        table = soup.find_all('table', attrs={'class': 'table-ic'})[-1]
        if table.find('td', attrs={'class': 'nodata'}):
            return "暂无数据"
        else:
            for idx, tr in enumerate(table.find_all('tr')):
                if idx == 0:
                    ths = tr.find_all('th')
                else:
                    tds = tr.find_all('td')
                    item = {ths[1].string: tds[1].string, ths[2].string: tds[2].string, ths[3].string: tds[3].string,
                            ths[4].string: tds[4].string, ths[5].string: tds[5].string, ths[6].string: tds[6].string}
                    business_exception[idx] = item
            return business_exception

    def extract_stock_info(self, soup):
        stock_info = {}
        ths = []
        tds = []
        table = soup.find_all('table', attrs={'class': 'table-ic'})[0]
        if table.find('td', attrs={'class': 'nodata'}):
            return "暂无数据"
        else:
            for idx, tr in enumerate(table.find_all('tr')):
                if idx == 0:
                    ths = tr.find_all('th')
                else:
                    tds = tr.find_all('td')
                    item = {ths[0].string: tds[0].string, ths[1].string: tds[1].string, ths[2].string: tds[2].string}
                    # print idx, item
                    stock_info[idx] = item
            return stock_info

    def output_plat_info_by_platname(self, platname, filename):
        each_plat_info_dict = {}
        helper.add_basic_info(platname, each_plat_info_dict)
        time.sleep(random.randint(5, 10))
        helper.add_gongshang_info(platname, each_plat_info_dict)
        helper.add_plat_info_to_file(platname, each_plat_info_dict, filename)

    def output_all_plats_info(self, problem_type, filename):
        platnames = self.get_plat_list(problem_type)
        for platname in platnames:
            try:
                self.output_plat_info_by_platname(platname, filename)
            except:
                s = traceback.format_exc()
                print "查询平台信息异常", platname, s

    def get_plat_list(self, problem_type):
        platname_list = []
        with open('plat/problem_p2p_info2018.json', 'r') as file:
            data = file.read()
        dict = json.loads(data)
        plat_info_list = dict['problemList']
        for plat in plat_info_list:
            if plat['type'] == problem_type.decode('utf-8'):
                platname_list.append(plat['platName'])
        return platname_list


if __name__ == '__main__':
    helper = WdzjHelper()
    platname = '汇善金融'.decode('utf-8')
    # helper.load_all_plat_info()
    # helper.get_all_problem_plats_by_year(2017)
    # print len(helper.get_plat_list('跑路'))
    helper.output_all_plats_info('跑路', 'p2p2018.json')
    # print helper.extract_stock_info(BeautifulSoup(open('example_gongshang.html'),'html.parser'))
