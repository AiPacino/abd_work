#coding:utf-8
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from live_dynamic import spider_dynamic
import logging
import time
import sys
sys.path.append("..")
from MySql_InterFace.mysql_interface import MYSQL
from update_live_basic.update_live_basic import get_update_state

MYSQL_COON = MYSQL()

def get_rows():
    b = []
    a = MYSQL_COON.select_from_table_where_condition("live_taobao_webstar_crawl_live_basic", "is_live=1",*b)

    for row in a:
        row = get_update_state(row)
        if row:
            yield row

def multiprocess_task(new_list):
    pool = ThreadPool()
    results = pool.map(spider_dynamic, new_list)
    pool.close()
    pool.join()
    return results

def insert_to_db(results):
    for each_result in results:
        try:
            MYSQL_COON.insert_into_table(each_result, "live_taobao_webstar_crawl_live_dynamic")
            #m = m + 1
            #logging.info("-----------------" + str(m) + "\t:dynamic had been in mysql")
        except Exception as e:
            logging.error(str(each_result))
            logging.error(e)

def task_main():

    rows = get_rows()
    # n = 0
    # for row in rows:
    #     n = n + 1
    #     print row["zhubo_id"]

    # logging.info("-----------{} zhubo is live----------".format(n))
    new_list = []
    n = 1
    m = 0
    for row in rows:
        new_list.append(row["zhubo_id"])

        if n % 20 == 0:
            results = multiprocess_task(new_list)
            new_list = []
            insert_to_db(results)
    
    results = multiprocess_task(new_list)
    new_list = []
    insert_to_db(results)


if __name__ == '__main__':

    n = 1
    while True:

        task_main()
        logging.info("########################{} times of all live".format(n))
        time.sleep(120)
        n = n + 1