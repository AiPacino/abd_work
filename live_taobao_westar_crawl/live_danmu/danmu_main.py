#coding:utf-8
#from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from live_danmu import spider_danmu
import logging
import time
import sys
sys.path.append("..")
from MySql_InterFace.mysql_interface import MYSQL
from update_live_basic.update_live_basic import get_update_state

MYSQL_COON = MYSQL()


def get_rows():
    b = []
    rows = MYSQL_COON.select_from_table_where_condition("live_taobao_webstar_crawl_live_basic", "is_live=1",*b)

    for row in rows:
        row = get_update_state(row)
        if row:
            yield row

def multiprocess_task(new_list):
    pool = ThreadPool(20)
    pool.map(spider_danmu, new_list)
    pool.close()
    pool.join()

def task_main():
    rows = get_rows()

    new_list = []
    n = 1
    m = 0
    for row in rows:
        new_list.append(row["zhubo_id"])
        if n % 20 == 0:
            multiprocess_task(new_list)
            new_list = []
    
    if new_list:
        multiprocess_task(new_list)

if __name__ == '__main__':
    task_main()
