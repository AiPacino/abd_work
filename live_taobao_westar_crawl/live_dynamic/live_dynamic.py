#coding:utf-8
import re
import sys
sys.path.append("..")
from Downloader.Downloader import Downloader
import logging
from datetime import datetime

DOWNLOADER = Downloader()

def try_except_block(return_dict, re_str, response, dict_key):
    try:
        dict_value = re.search(re_str, response.text).group(1)
        return_dict[dict_key] = dict_value
    except Exception as e:
        logging.error(response.url)
        logging.error(e)


def get_total_join_count(response):

    total_join_count_dict = {}

    try_except_block(total_join_count_dict, r'"totalJoinCount":(\d+)', response, "watching")

    return total_join_count_dict

def get_attention(response):

    attention_dict = {}

    try_except_block(attention_dict, r'"fansNum":(\d+)', response, "attention")

    return attention_dict

def get_live_id(response):

    live_id_dict = {}

    try_except_block(live_id_dict, r'"liveId":(\d+)', response, "live_id")
    
    return live_id_dict


def spider_dynamic(zhubo_id):
    url = "https://taobaolive.taobao.com/room/index.htm?userId=" + str(zhubo_id)
    try:
        response = DOWNLOADER.download_requests(url)
    except Exception as e:
        logging.error(zhubo_id)
        logging.error(e)
        return None
    
    
    watching_dict = get_total_join_count(response)
    attention_dict = get_attention(response)
    live_id_dict = get_live_id(response)

    watch_atten_dict = dict(watching_dict, **attention_dict)

    dynamic_dict = dict(watch_atten_dict, **live_id_dict)
    dynamic_dict["crawl_time"] = datetime.now()

    return dynamic_dict



if __name__ == '__main__':
    zhubo_id = 1063569743
    result = spider_dynamic(zhubo_id)
    print repr(result).decode("unicode-escape")