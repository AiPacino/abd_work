#coding:utf-8
import re
import sys
sys.path.append("..")
from MySql_InterFace.mysql_interface import MYSQL
from Downloader.Downloader import Downloader

MYSQL_COON = MYSQL()
DOWNLOADER = Downloader()

def update_live_from_zhubo_id(zhubo_id):

    MYSQL_COON.update_live_basic_is_live(zhubo_id)

def update_live_from_live_id(live_id):
    MYSQL_COON.update_live_basic_is_live_from_live_id(live_id)

def get_live_id(zhubo_id):
    
    url = "https://taobaolive.taobao.com/room/index.htm?userId=" + str(zhubo_id)
    response = DOWNLOADER.download_requests(url)
    live_id = re.search(r'"liveId":(\d+)', response.text).group(1)

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
    update()