#coding:utf-8
import multiprocessing
import sys
sys.path.append("..")
from MySql_InterFace.mysql_interface import MYSQL
from Config.Config import ZHUBO_LIVE_TABLE
from config import UPDATE_ZHUBO_LIVE_TIME, PROCESS_NUM
from update_live_basic.update_live_basic import get_live_id
from manage_some import spider_some
import logging
import time


def find_how_many_is_spider():
    MYSQL_CONN = MYSQL()
    zhubo_rows = MYSQL_CONN.select_from_table(ZHUBO_LIVE_TABLE, "is_live = 1")
    len_is_live = []
    for zhubo_row in zhubo_rows:
        len_is_live.append(zhubo_row)
    return len(len_is_live)

def update_zhubo_from_db():
    MYSQL_CONN = MYSQL()
    #pool = multiprocessing.Pool(processes=10)
    zhubo_rows =   MYSQL_CONN.select_from_table(ZHUBO_LIVE_TABLE, "is_live != 1")
    zhubo_id_list = []
    
    for zhubo_row in zhubo_rows:
        zhubo_id = zhubo_row["zhubo_id"]
        #zhubo_id_list.append(zhubo_id)
        if str(0) != get_live_id(zhubo_id):
            logging.info("{} is living!.........".format(zhubo_id))
            yield zhubo_id
        else:
            logging.info("{} is not living!".format(zhubo_id))

def start_task():
    pool = multiprocessing.Pool(processes=PROCESS_NUM)
    while True:
        if find_how_many_is_spider() < PROCESS_NUM:
            for zhubo_id in update_zhubo_from_db():
                if find_how_many_is_spider() < PROCESS_NUM:
                    pool.apply_async(spider_some, (zhubo_id,))
            #time.sleep(UPDATE_ZHUBO_LIVE_TIME)
        #time.sleep(UPDATE_ZHUBO_LIVE_TIME)

if __name__ == '__main__':
    start_task()