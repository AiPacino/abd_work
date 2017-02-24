#coding:utf-8
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import time
import sys
sys.path.append('..')
from config import UPDATE_ZHUBO_INFO_TIME, UPDATE_GOODS_INFO_TIME
from Config.Config import ZHUBO_INFO_TABLE, LIVE_GOODS_TABLE, GOODS_INFO_TABLE, THREAD_NUM
from goods_info.spider_goods import spider_goods
from zhubo_info.spider_zhubo import spider_zhubo
from MySql_InterFace.mysql_interface import MYSQL
import logging

def multiprocess_task(which_module, new_list):
    pool = ThreadPool(THREAD_NUM)
    results = pool.map(which_module, new_list)
    pool.close()
    pool.join()
    return results

def get_goods_id_list():

    goods_id_list = []
    MYSQL_CONN = MYSQL()
    live_goods_row = MYSQL_CONN.select_from_table(LIVE_GOODS_TABLE, [])
    for each_goods in live_goods_row:
        goods_id = each_goods["goods_id"]
        goods_id_list.append(goods_id)
    return goods_id_list

def get_zhubo_id_list():
    zhubo_id_list = []
    MYSQL_CONN = MYSQL()
    zhubo_id_row = MYSQL_CONN.select_from_table(ZHUBO_INFO_TABLE, [])
    for each_zhubo in zhubo_id_row:
        zhubo_id = each_zhubo["zhubo_id"]
        zhubo_id_list.append(zhubo_id)

    return zhubo_id_list

def spider_goods_info():

    goods_id_list = get_goods_id_list()
    results = multiprocess_task(spider_goods, goods_id_list)
    insert_to_db(results, GOODS_INFO_TABLE)

def spider_zhubo_info():

    zhubo_id_list = get_zhubo_id_list()
    results = multiprocess_task(spider_zhubo, zhubo_id_list)
    insert_to_db(results, ZHUBO_INFO_TABLE)

def insert_to_db(results, which_table):
    MYSQL_CONN = MYSQL()
    for each_result in results:
        try:
            if "zhubo_info" in which_table:
                MYSQL_CONN.insert_into_table_with_replace(each_result, which_table)
            else:
                MYSQL_CONN.insert_into_table(each_result, which_table)
            logging.info("spider one item into {}".format(which_table))
        except Exception as e:
            logging.error(str(each_result))
            logging.error(e)

def update_zhubo_info():
    while True:
        spider_zhubo_info()
        time.sleep(UPDATE_ZHUBO_INFO_TIME)

def update_goods_info():
    while True:
        spider_goods_info()
        #print "**********************************88what******************************"
        time.sleep(UPDATE_GOODS_INFO_TIME)

def spider_all():

    """
    update zhubo info and goods_info

    """
    update_zhubo_info_process = multiprocessing.Process(target=update_zhubo_info)

    update_goods_info_process = multiprocessing.Process(target=update_goods_info)

    update_zhubo_info_process.start()

    update_goods_info_process.start()

if __name__ == '__main__':
    # zhubo_id = sys.argv[1]
    spider_all()