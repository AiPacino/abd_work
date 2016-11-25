#coding:utf-8
import sys
sys.path.append("..")
from Downloader.Downloader import Downloader

DOWNLOAD = Downloader()

# def spider_danmu():
    
#     driver = DOWNLOAD.download_phantomjs("https://taobaolive.taobao.com/room/index.htm?userId=20290404")
#     while True:
#         elements = DOWNLOAD.find_element_by_css(driver, ".comment-outer")
#         print elements.text
#         # if elements:
#         #     joins = elements.find_elements_by_css_selector(".join")
#         #     print joins
#         #     if joins:
#         #         for join in joins:
#         #             print join.text
#         #print elements

def spider_douyu():
    driver = DOWNLOAD.download_chrome("https://www.douyu.com/78561")
    while True:
        elements = DOWNLOAD.find_element_by_xpath(driver, ".chat-cont")
        print elements.text


if __name__ == '__main__':
    #spider_danmu()
    spider_douyu()