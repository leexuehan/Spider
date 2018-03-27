#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import traceback

import requests
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import xlrd
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARN)
handler = logging.FileHandler("./log/log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class QccHelper(object):
    def __init__(self):
        self.output_counter = 0
        self.each_company_info = {}
        self.final_output = {}

    def read_name_list_from_xls(self, file_path):
        data = xlrd.open_workbook(file_path)
        table = data.sheets()[0]
        row_num = table.nrows
        companies = []
        for row in range(0, row_num):
            content = table.cell(row, 0).value
            if str(content) != u'':
                companies.append(content.encode('utf-8'))
        return companies

    def get_register_capital(self, driver):
        register_capital = driver.find_element_by_xpath('//*[@id="Cominfo"]/table[2]/tbody/tr[1]/td[2]').text
        self.each_company_info['注册资本'] = register_capital
        return self.each_company_info

    def get_paid_capital(self, driver):
        paid_capital = driver.find_element_by_xpath('//*[@id="Cominfo"]/table[2]/tbody/tr[1]/td[4]').text
        self.each_company_info['实缴资本'] = paid_capital
        return self.each_company_info

    def get_operating_state(self, driver):
        address = driver.find_element_by_xpath('//*[@id="Cominfo"]/table[2]/tbody/tr[2]/td[2]').text
        self.each_company_info['经营状态'] = address
        return self.each_company_info

    def get_establishment_date(self, driver):
        established_date = driver.find_element_by_xpath('//*[@id="Cominfo"]/table[2]/tbody/tr[2]/td[4]').text
        self.each_company_info['成立日期'] = established_date
        return self.each_company_info

    def get_registration_number(self, driver):
        registration_num = driver.find_element_by_xpath('//*[@id="Cominfo"]/table[2]/tbody/tr[3]/td[2]').text
        self.each_company_info['注册号'] = registration_num

    def get_organization_code(self):
        pass

    def get_tax_id(self):
        pass

    def get_social_credit_id(self):
        pass

    def get_company_type(self, driver):
        company_type = driver.find_element_by_xpath('//*[@id="Cominfo"]/table[2]/tbody/tr[5]/td[2]').text
        self.each_company_info['公司类型'] = company_type
        return self.each_company_info

    def get_industry_belong(self, driver):
        industry_belong = driver.find_element_by_xpath('//*[@id="Cominfo"]/table[2]/tbody/tr[5]/td[4]').text
        self.each_company_info['所属行业'] = industry_belong
        return self.each_company_info

    def get_approval_date(self):
        pass

    def get_registration_authority(self):
        pass

    def get_area_belong(self, driver):
        province = driver.find_element_by_xpath('//*[@id="Cominfo"]/table[2]/tbody/tr[7]/td[2]').text
        self.each_company_info['所属地区'] = province

    def add_address_info(self, driver):
        address = driver.find_element_by_xpath('//*[@id="Cominfo"]/table[2]/tbody/tr[10]/td[2]').text
        self.each_company_info['地址'] = address
        return self.each_company_info

    def get_business(self, driver):
        business = driver.find_element_by_xpath('//*[@id="Cominfo"]/table[2]/tbody/tr[11]/td[2]').text
        self.each_company_info['经营范围'] = business

    def add_legal_person_name(self, driver):
        person_name = driver.find_element_by_xpath(
                '//*[@id="Cominfo"]/table[1]/tbody/tr[2]/td[1]/div/div[1]/div[2]/a[1]').text
        self.each_company_info['法人'] = person_name
        return self.each_company_info

    def add_business_risk_info(self, driver):
        # driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/header/div/div[4]/a').click()
        # time.sleep(2)
        # business_exception_info = driver.find_element_by_xpath(
        #         '/html/body/div[3]/div/div[1]/div[2]/section[1]/div/a[1]').text()
        # stock_pledge_info = driver.find_element_by_xpath(
        #         '/html/body/div[3]/div/div[1]/div[2]/section[1]/div/a[2]').text()
        # punish_info = driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div[2]/section[1]/div/a[3]').text()
        # print business_exception_info, stock_pledge_info, punish_info
        # self.each_company_info['经营异常'] = business_exception_info
        # self.each_company_info['股权出质'] = stock_pledge_info
        # self.each_company_info['行政惩罚'] = punish_info
        self.each_company_info['经营风险'] = driver.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/header/div/div[4]/a/span').text

    def add_intellectual_property_right_num(self, driver):
        self.each_company_info['知识产权'] = driver.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/header/div/div[6]/a/span').text

    def search_company_info(self, excel_path):
        company_name_list = self.read_name_list_from_xls(excel_path)
        driver = webdriver.Chrome()
        all_window_handles = []
        self.enter_search_page(driver)
        print company_name_list
        for company_name in company_name_list:
            try:
                top_search_box_input = driver.find_element_by_id('headerKey')
                top_search_box_input.clear()
                top_search_box_input.send_keys(company_name.decode('utf-8'))
                driver.find_element_by_xpath('/html/body/header/div/form/div/div/span/button').click()
                time.sleep(1)

                try:
                    driver.find_element_by_class_name('ma_h1').click()
                    time.sleep(2)
                except:
                    logger.warn('找不到该家企业信息,企业名:' + str(company_name))
                    print '找不到该家企业信息,企业名:' + str(company_name)
                    continue
                all_window_handles = driver.window_handles
                current_window = all_window_handles[-1]
                search_window = all_window_handles[0]
                driver.switch_to.window(current_window)
                self.fill_in_info(driver)
                # print json.dumps(company_info, ensure_ascii=False, encoding='utf-8')
                self.add_company_info(company_name)
                driver.close()
                driver.switch_to.window(search_window)
            except Exception:
                s = traceback.format_exc()
                logger.error("搜索公司信息时出错,公司名:" + str(company_name) + ",错误信息:\n" + s)
            time.sleep(5)
            # self.close_all_windows(driver, all_window_handles)

    def fill_in_info(self, driver):
        self.add_address_info(driver)
        self.add_legal_person_name(driver)
        self.add_business_risk_info(driver)
        self.add_intellectual_property_right_num(driver)
        self.get_area_belong(driver)
        self.get_business(driver)
        self.get_company_type(driver)
        self.get_area_belong(driver)
        self.get_establishment_date(driver)
        self.get_operating_state(driver)
        self.get_paid_capital(driver)
        self.get_register_capital(driver)
        self.get_registration_number(driver)
        self.get_industry_belong(driver)

    def add_company_info(self, company_name):
        self.final_output[company_name] = self.each_company_info
        self.each_company_info = {}
        self.output_results()

    def output_results(self):
        self.output_counter += 1
        output = json.dumps(self.final_output, encoding='utf-8', ensure_ascii=False)
        with open('output002.json', 'w') as output_file:
            output_file.write(output)
        print "**********输出第", self.output_counter, "家企业信息完成***********"

    def close_all_windows(self, driver, all_window_handles):
        for handle in all_window_handles:
            driver.switch_to.window(handle)
            driver.close()

    def enter_search_page(self, driver):
        driver.get("http://www.qichacha.com")
        driver.find_element_by_id('searchkey').send_keys('company')
        driver.find_element_by_id('V3_Search_bt').click()
        self.wait_util_login(driver)

    def wait_util_login(self, driver):
        while self.is_in_login_page(driver) is True:
            print "在登陆界面等待登陆,5秒后执行检查"
            time.sleep(5)

    def is_in_login_page(self, driver):
        try:
            driver.find_element_by_class_name('text-dark-lter')
            return True
        except:
            return False


if __name__ == '__main__':
    helper = QccHelper()
    # print helper.read_name_list_from_xls('./input/input.xlsx')
    # helper.search_company_info('./input/input.xlsx')
    helper.search_company_info('./input/enterprise332.xlsx')
    # helper.test_exception()
