#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

import requests
import time

from bs4 import BeautifulSoup

from spider.IPPool import valid_ip_proxies


class IPPrxoyHelper(object):
    def __init__(self):
        pass

    def get_response_data(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}  # 构造头部
        while True:
            try:
                res = requests.get(url=url, headers=headers)
                if res.status_code != 200:
                    print "请求网页失败", res.content
                    raise
                else:
                    return res.content
            except Exception as e:
                print e
                time.sleep(random.choice(range(10, 20)))

    def get_proxies(self, url):
        """ Extract web IP address and port. """
        proxies = []  # proxy list
        data = self.get_response_data(url)
        soup = BeautifulSoup(data, 'html.parser')  # soup object
        trs = soup.find_all('tr')  # extract tr tag
        for tds in trs[1:]:
            td = tds.find_all('td')  # extract td tag
            proxies.append(str(td[1].contents[0]) + ":" + str(td[2].contents[0]))
        return self.filter_invalid_proxies(proxies)

    def filter_invalid_proxies(self, proxies):
        valid_proxies = []
        url = "http://ip.chinaz.com/getip.aspx"
        proxy_dict = {}
        for proxy in proxies:
            try:
                proxy_dict['http'] = 'http://' + proxy
                res = requests.get(url=url, timeout=5, proxies=proxy_dict)
                if (res.status_code == 200):
                    valid_proxies.append(proxy)
                    print "目前已经找到的有效代理:", valid_proxies
            except:
                continue
        return valid_proxies


if __name__ == '__main__':
    page_num = 10
    proxies = []
    helper = IPPrxoyHelper()
    for page_index in range(1, page_num):
        req_url = 'http://www.xicidaili.com/nn/%d' % page_index
        print req_url
        result = helper.get_proxies(req_url)
        proxies.append(result)
        print "已经找到的代理ip", proxies
    print '总共找到代理数:', len(proxies), proxies
