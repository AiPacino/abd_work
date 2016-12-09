from spider_goods import spider_goods
import re
import time, random
import logging
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import sys
sys.path.append("..")
from MySql_InterFace.mysql_interface import MYSQL

def get_rows():
    MYSQL_COON = MYSQL()
    b = []
    a = MYSQL_COON.select_from_table("live_taobao_webstar_crawl_live_goods", *b)

    n = 1
    goods_list = []
    for row in a:
        goods_id = row["goods_id"]
        yield goods_id
    MYSQL_COON.close_db()

def multiprocess_task(new_list):
    pool = ThreadPool()
    results = pool.map(spider_goods, new_list)
    pool.close()
    pool.join()
    return results

def insert_to_db(results):
    for each_result in results:
        try:
            MYSQL_COON.insert_into_table(each_result, "live_taobao_webstar_crawl_goods_info")
            #m = m + 1
            #logging.info("-----------------" + str(m) + "\t:dynamic had been in mysql")
        except Exception as e:
            logging.error(str(each_result))
            logging.error(e)

def task_main():

    rows = get_rows()

    new_list = []
    n = 1
    m = 0
    for row in rows:
        new_list.append(row)

        if len(new_list) % 20 == 0:
            results = multiprocess_task(new_list)
            new_list = []
            insert_into_table(results)

    results = multiprocess_task(new_list)
    new_list = []
    insert_to_db(results)


if __name__ == '__main__':
    
    task_main()