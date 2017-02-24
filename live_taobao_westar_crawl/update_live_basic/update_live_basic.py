
#coding:utf-8
import re
import sys
sys.path.append("..")
from MySql_InterFace.mysql_interface import MYSQL
from Downloader.Downloader import Downloader
import logging

MYSQL_COON = MYSQL()
DOWNLOADER = Downloader()

def update_live_from_zhubo_id(zhubo_id):

    MYSQL_COON.update_live_basic_is_live_from_zhubo_id(zhubo_id)

def update_live_from_live_id(live_id):
    MYSQL_COON.update_live_basic_is_live_from_live_id(live_id)

def get_live_id(zhubo_id):
    
    url = "https://taobaolive.taobao.com/room/index.htm?userId=" + str(zhubo_id)
    response = DOWNLOADER.download_requests(url)
    try:
        live_id = re.search(r'"liveId":(\d+)', response.text).group(1)
    except Exception as e:
        live_id = 0
        logging.error(zhubo_id)
        logging.error(e)

    return live_id

def get_update_state(row):
    
    live_id = get_live_id(row["zhubo_id"])
    if live_id == str(0):
        update_live_from_zhubo_id(row["zhubo_id"])
        return None
    elif live_id != row["live_id"]:
        update_live_from_live_id(row["live_id"])
        return None

    return row


if __name__ == '__main__':
    zhubo_id = sys.argv[1]
    print get_live_id(zhubo_id)