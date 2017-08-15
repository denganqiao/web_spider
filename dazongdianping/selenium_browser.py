# -*- coding: utf-8 -*-
import re
import os
from selenium import webdriver
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
from urllib.parse import parse_qs
import random
from selenium.common import exceptions
import traceback
import logging

logging.basicConfig(level=logging.NOTSET)
bs = lambda src: BeautifulSoup(src)
qs = lambda query, name: parse_qs(query)[name][0]
re_s = re.compile(r"\s{2,}")
r = lambda s: lambda_res_sub(s)

def lambda_res_sub(s):
    str = None
    try:
        str = re_s.sub(" ", s)
    except:
        str = ''
    return str

def convert_time(s):
    if "月" in s:
        t = datetime.today()
        return t.strftime("%Y-") + s.replace("月", "-").replace("日", "")
    elif "今天" in s:
        t = datetime.today()
        return s.replace("今天", t.strftime("%Y-%m-%d "))
    elif " " in s:
        return s
    else:
        t = datetime.today()
        s = int(s.replace("分钟前", ""))
        d = timedelta(minutes=s)
        s = t - d
        return s.strftime("%Y-%m-%d %H:%M")

class Browser:
    def __init__(self):
        chrome_options='--disable-web-security'
        options = webdriver.ChromeOptions()
        options.add_argument('--args --disable-web-security')
        chromedriver = "E:/pyworkspace/net_adver/net_adver/chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.browser = Chrome(chrome_options=options,executable_path=chromedriver)
        self.browser.maximize_window()

        # self.browser = Chrome("E:/pyworkspace/net_adver/net_adver/chromedriver.exe")
        # self.browser.set_page_load_timeout(600)
        # self.browser.maximize_window()

    @property
    def source(self):
        return self.browser.page_source

    @property
    def url(self):
        return self.browser.current_url

    def get(self, url):
        try:
            self.browser.get(url)
        except exceptions.TimeoutException:
            pass
        sleep(5)

    def execute(self, js):
        self.browser.execute_script(js)

    def wait_elem_away(self, selector, text=None):
        continue_account = 0
        while True:
            try:
                elems = self.browser.find_elements_by_css_selector(selector)
                if text is not None:
                    cnt = 0
                    for elem in elems:
                        if elem.text == text:
                            break
                        else:
                            cnt += 1
                    if cnt == len(elems):
                        return
                sleep(5)
            except exceptions.NoSuchElementException:
                if continue_account == 3:
                    return
                continue_account += 1
            except exceptions.StaleElementReferenceException:
                return

    def wait_elem_come(self, selector):
        continue_account = 0
        while True:
            try:
                #print(self.browser.page_source)
                #print(self.browser.current_url)
                elem = self.browser.find_element_by_css_selector(selector)
                #print(elem.is_displayed())
                #print(elem.is_enabled())
                return
            except exceptions.NoSuchElementException:
                if continue_account == 3:
                    return
                continue_account += 1
                sleep(5)

    def wait_elem_come_two(self, selector1, selector2):
        continue_account = 0
        while True:
            try:
                #print(self.browser.page_source)
                #print(self.browser.current_url)
                #print('selector:'+selector)
                elem = self.browser.find_element_by_css_selector(selector1)
                #print(elem.is_displayed())
                #print(elem.is_enabled())
                return 1
            except exceptions.NoSuchElementException:
                return 2
                # try:
                #     elem = self.browser.find_element_by_css_selector(selector2)
                #     print('wait_elem_come_two:', selector2)
                #
                # except exceptions.NoSuchElementException:
                #     print('no such element')
                #     sleep(5)

    def wait_elem_come_by_xpath(self, selector):
        continue_account = 0
        while True:
            try:
                elem = self.browser.find_element_by_xpath(selector)
                #print(elem.is_displayed())
                #print(elem.is_enabled())
                return
            except exceptions.NoSuchElementException:
                if continue_account == 3:
                    return
                continue_account += 1
                sleep(5)

    def fill_name(self, name, value):
        self.browser.find_element_by_name(name).send_keys(value)

    def click_xpath(self, xpath, begin = 2, end = 8):
        try:
            elem = self.browser.find_element_by_xpath(xpath)
            elem.click()
        except:
            return
        sleep(random.randint(begin, end))


    def click_by_css(self, css, begin = 8, end = 15):
        try:
            elem = self.browser.find_element_by_css_selector(css)
            elem.click()
        except:
            return
        sleep(random.randint(begin, end))


    def fill_xpath(self, xpath, value):
        try:
            elem = self.browser.find_element_by_xpath(xpath)
            elem.send_keys(value)
        except:
            return

    def get_elem(self, selector):
        return self.browser.find_element_by_css_selector(selector)

    def get_elem_xpath(self, xpath):
        return self.browser.find_element_by_xpath(xpath)

    def get_elems(self, selector):
        return self.browser.find_elements_by_css_selector(selector)

    def send_keys_by_xpath(self, name, value):
        try:
            elem = self.browser.find_element_by_xpath(name)
            elem.send_keys(value)
        except:
            exstr = traceback.format_exc()
            print(exstr)
            return None

    def send_keys_by_css(self, name, value):
        try:
            elem = self.browser.find_element_by_css_selector(name)
            elem.send_keys(value)
        except:
            exstr = traceback.format_exc()
            print(exstr)
            return None

    def execute_Script_Click(self, name):
        try:
            elementToClick = self.browser.find_element_by_css_selector(name)
            self.browser.execute_script("arguments[0].click();", elementToClick)
        except exceptions.NoSuchElementException:
            exstr = traceback.format_exc()
            print(exstr)
            return None

    def close_window_handles(self):
        winBeforeHandle = self.browser.current_window_handle
        #print("winBeforeHandle==",winBeforeHandle)
        winHandles = self.browser.window_handles
        #print("winHandles==",winHandles)
        for handle in winHandles:
            if winBeforeHandle != handle:
                self.browser.switch_to.window(winBeforeHandle)
                self.browser.close()
                self.browser.switch_to.window(handle)
                break

    def close(self):
        #self.browser.close()
        self.browser.quit()