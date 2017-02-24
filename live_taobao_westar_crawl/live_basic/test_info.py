#coding:utf-8
import requests
import random
import re
import json
from datetime import datetime
import sys
sys.path.append("..")
from MySql_InterFace.mysql_interface import MYSQL
from Config.Config import USER_AGENTS
from live_goods.live_goods import get_live_goods
from ProxyManager.ProxyManager import get_proxy
from Config.Config import USE_PROXY, LIVE_BASIC_TABLE
import logging
# from Config.Config import HEADERS

user_ids = [10309611, 2534582702, 510755320, 195779035, 631300490, 63239528, 1776349514, 20994568, 167019901, 2104259273]

SESSION = requests.Session()

def session_get(url):
    while True:
        if USE_PROXY:
            response = SESSION.get(url, proxies=get_proxy())
            if response.status_code == 200:
                return response
        else:
            response = SESSION.get(url)
            #if response.status_code == 200:
            return response

def get_info(url_info):
    
    info_json_dict = {}
    response = session_get(url_info)
    info_json = json.loads(response.text)
    info_json = json.dumps(info_json)
    #print type(info_json)

    info_json_dict["user_info_json"] = info_json

    return info_json_dict
    

def get_goods_list(url_goods_list, live_id):
    #get the goods json and insert into the db
    goods_json_dict = {}
    url = url_goods_list + live_id
    response = session_get(url)
    goods_json = json.loads(response.text)
    goods_json = json.dumps(goods_json)
    goods_json_dict["goods_json"] = goods_json

    get_live_goods(goods_json, live_id)
    
    return goods_json_dict

def get_goods_json(user_id):

    pass


def spider_basic(user_id):

    MYSQL_COON = MYSQL()

    url_info = "https://taobaolive.taobao.com/api/broadcaster_info/1.0?accountId={}".format(user_id)
    url_goods_list = "https://taobaolive.taobao.com/api/item_list/1.0?type=0&liveId="
    url_live = "https://taobaolive.taobao.com/room/index.htm?userId={}".format(user_id)

    HEADERS = {
        "User-Agent": random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        #'Host': "taobaolive.taobao.com",
        "Referer":"https://taobaolive.taobao.com/room/index.htm?userId={}".format(user_id)
    }

    SESSION.headers.update(HEADERS)

    response = session_get(url_live)
    response_text = response.text
    #print response_text
    live_id = re.search(r'liveId":(\d+)', response_text).group(1)
    # print live_id == str(0)

    #live_basic_info = {}

    goods_json_dict = get_goods_list(url_goods_list, live_id)
    info_json_dict = get_info(url_info)

    live_basic_info = dict(goods_json_dict, **info_json_dict)
    live_basic_info["zhubo_id"] = user_id

    live_basic_info["live_id"] = live_id

    if live_id == str(0):
        live_basic_info["is_live"] = 0
    else:
        live_basic_info["is_live"] = 1
    
    live_basic_info["crawl_time"] = datetime.now()

    live_basic_info["live_url"] = url_live

    #return live_basic_info
    #print repr(live_basic_info).decode("unicode-escape")
    logging.info("Spider one item into {}".format(LIVE_BASIC_TABLE))
    MYSQL_COON.insert_into_table(live_basic_info, LIVE_BASIC_TABLE)





if __name__ == '__main__':
    n = 1
    for user_id in user_ids:
        if n < 20:
            spider_basic(user_id)
        else:
            pass
        n = n + 1
