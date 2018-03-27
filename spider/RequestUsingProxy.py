#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

import requests
import time

from spider.IPPool import valid_ip_proxies


class RequestUsingProxy(object):
    def make_request(self, url, headers, cookies):
        proxy_param_list = self.build_proxies()
        while True:
            index = random.randint(0, len(proxy_param_list) - 1)
            proxy_param = proxy_param_list[index]
            print '使用代理', proxy_param
            response = requests.get(url, proxies=proxy_param, headers=headers)
            if response.status_code == 200:
                return response.content
            else:
                print "request error!", response.status_code, response.content
                print "请求失败,更换代理重新请求"
                time.sleep(2)

    def build_proxies(self):
        proxy_param_list = []
        proxies = valid_ip_proxies
        for proxy in proxies:
            proxy_param_list.append({'http': 'http://' + proxy})
        return proxy_param_list


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}  # 构造头部
    print random.randint(5, 10)
    # print RequestUsingProxy().make_request('http://www.baidu.com', headers=headers)
