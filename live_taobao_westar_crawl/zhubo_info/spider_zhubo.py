#coding:utf-8
import re
import logging
import sys
sys.path.append("..")
from MySql_InterFace.mysql_interface import MYSQL
from Downloader.Downloader import Downloader
from Config.Config import ZHUBO_CSS, TITLE_DESC, INFO_MAP
import json

MySQL_COON = MYSQL()
download = Downloader()

def get_zhubo_url(zhubo_id):

    #zhubo_id = "http:" + zhubo_id
    user_info_json = json.loads(zhubo_id)
    zhubo_url = user_info_json["result"]["model"]["broadCaster"]["jumpUrl"]
    zhubo_url = "http:" + zhubo_url
    return zhubo_url

def spider_zhubo(zhubo_id):
    
    zhubo_info_dict = {}
    zhubo_url = get_zhubo_url(zhubo_id)

    try:
        zhubo_id = re.search(r"userId=(\d+)", zhubo_url).group(1)
    except Exception as e:
        zhubo_id = -1
        logging.error(zhubo_url)
        logging.error(e)
    zhubo_info_dict["zhubo_id"] = zhubo_id

    #get the driver
    driver = download.download_chrome(zhubo_url)

    #get daren url
    daren_url = download.find_element_by_css(driver, ZHUBO_CSS["daren_url"])
    if daren_url:
        daren_url = daren_url.get_attribute("href")
        zhubo_info_dict["zhubo_url"] = daren_url

    #get daren fans count
    daren_fans = download.find_element_by_css(driver, ZHUBO_CSS["daren_fans"])
    if daren_fans:
        try:
            daren_fans = str(re.search(r"\d+", daren_fans.text).group())
        except Exception as e:
            daren_fans = -1
            logging.error(zhubo_id)
            logging.error(e)
        zhubo_info_dict["zhubo_fans"] = daren_fans
    
    driver.quit()

    #spider in the homepage of zhubo
    driver_info = download.download_chrome(daren_url)
    contents = download.find_elements_by_css(driver_info, ZHUBO_CSS["daren_all_info"])

    if contents:
        for each in contents:
            title = each.find_element_by_css_selector(TITLE_DESC["title"])
            desc = each.find_element_by_css_selector(TITLE_DESC["desc"])
            #print title.text, desc.text
            if title.text in INFO_MAP.keys():
                zhubo_info_dict[INFO_MAP[title.text]] = desc.text

    driver_info.quit()
    print repr(zhubo_info_dict).decode("unicode-escape")
    # MySQL_COON.insert_into_table(zhubo_info_dict, "daren_info")
    # MySQL_COON.close_db()
    return zhubo_info_dict


if __name__ == '__main__':
    zhubo_url = "http://h5.m.taobao.com/daren/home.html?userId=100629294"
    spider_zhubo(zhubo_url)