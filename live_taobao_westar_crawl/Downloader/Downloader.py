#coding:utf-8
import sys
import os
import requests
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
sys.path.append("..")
from Config.Config import USE_PROXY, HEADERS, TIME_WAIT
from ProxyManager.ProxyManager import get_proxy

class Downloader():
    #下载类

    def __init__(self):
        #self.log = Log("Downloader")
        # self.SESSION = requests.session()
        # self.SESSION.headers.update(HEADERS)
        pass

    def download_chrome(self, url):
        #chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        driver = webdriver.Chrome(service_log_path=os.path.devnull)
        driver.get(url)
        return driver

    def download_phantomjs(self, url):
        #phantomjs_path = r"C:\Python27\phantomjs-2.1.1-windows\bin\phantomjs.exe"
        #driver = webdriver.PhantomJS(executable_path=phantomjs_path, service_log_path=os.path.devnull)
        driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
        driver.get(url)
        return driver

    def download_firefox(self, url):
        driver = webdriver.Firefox()
        driver.get(url)
        return driver

    def close_phantomjs(self, driver):
        driver.close()

    def download_requests(self, url):
        #A regular requests.get
        while True:
            if USE_PROXY:
                response = requests.get(url, headers=HEADERS, proxies=get_proxy())
                if response.status_code == 200:
                    return response
            else:
                response = requests.get(url, headers=HEADERS)
                return response

    def download_requests_sell_count(self, url, goods_id):
        #A regular requests.get with a special headers
        headers = {
            'GET': '',
            'Host': "detailskip.taobao.com",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
            "Referer": "https://item.taobao.com/item.htm?spm=a1z10.3-c-s.w4002-14571456174.29.gtuu1n&id={}".format(goods_id),
        }
        # headers = headers
        # headers["Referer"] += str(goods_id)
        # logging.info('REFERER:\t'+headers["Referer"])
        while True:
            if USE_PROXY:
                response = requests.get(url, headers=headers, proxies=get_proxy())
                if response.status_code == 200:
                    return response
            else:
                response = requests.get(url, headers=headers)
                return response

    def find_element_by_css(self, driver, css):
        try:
            element = WebDriverWait(driver, TIME_WAIT).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css))
            )
        except Exception as e:
            logging.error(e)
            return None
        return element

    def find_elements_by_css(self, driver, css):
        try:
            elements = WebDriverWait(driver, TIME_WAIT).until(
                EC.visibility_of_any_elements_located((By.CSS_SELECTOR, css))
            )
        except Exception as e:
            logging.error(e)
            return None
        return elements


    def find_element_by_xpath(self, driver, xpath):
        try:
            element = WebDriverWait(driver, TIME_WAIT).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
        except Exception as e:
            logging.error(e)
            return None
        return element

    def scroll_page(self, driver, seconds):
        for i in range(seconds):
            time.sleep(1)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
