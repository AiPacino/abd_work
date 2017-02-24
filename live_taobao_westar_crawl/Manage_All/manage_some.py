#coding:utf-8
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import threading
import sys
sys.path.append("..")
from config import DYNAMIC_TIME, UPDATE_GOODS_ID_TIME, GOODS_INFO_TIME, SLEEP_DETECT_TIME
from Config.Config import LIVE_GOODS_TABLE, LIVE_GOODS_TEMP_TABLE, GOODS_INFO_TABLE, LIVE_DYNAMIC_TABLE, ZHUBO_INFO_TABLE, ZHUBO_LIVE_TABLE, THREAD_NUM
from live_basic.test_info import spider_basic, get_goods_list
from live_dynamic.live_dynamic import spider_dynamic
from live_danmu.live_danmu import spider_danmu
from goods_info.spider_goods import spider_goods
from zhubo_info.spider_zhubo import spider_zhubo
from update_live_basic.update_live_basic import get_live_id
from MySql_InterFace.mysql_interface import MYSQL
import logging
import time

def sleep_and_detect(sleep_time, zhubo_id, live_id, which_module):
    area = int(sleep_time / SLEEP_DETECT_TIME)
    for times in range(area):
        logging.info("SLEEP {0} seconds... at {1} times.....{2}........".format(SLEEP_DETECT_TIME, times + 1, which_module))
        time.sleep(SLEEP_DETECT_TIME)
        if live_id == get_live_id(zhubo_id) != str(0):
            pass
        else:
            return False
    return True

def end_liveing(zhubo_id):
    MYSQL_CONN = MYSQL()
    logging.info("{} zhubo is not living!".format(zhubo_id))
    info_dict = {"zhubo_id":zhubo_id, "is_live": "0"}
    MYSQL_CONN.insert_into_table_exist_update(info_dict, ZHUBO_LIVE_TABLE, "is_live=0")


def from_live_goods_to_temp(live_id):
    goods_live_id_list = []
    MYSQL_CONN = MYSQL()
    live_goods_row = MYSQL_CONN.select_from_table(LIVE_GOODS_TABLE, "live_id={}".format(live_id))
    for each_goods in live_goods_row:
        goods_id = each_goods["goods_id"]
        live_id = each_goods["live_id"]
        each_item = {"goods_id": goods_id, "live_id": live_id}
        goods_live_id_list.append(each_item)
        #goods_live_id_dict[goods_id] = live_id
        #goods_id_list.append(goods_id)
    
    insert_to_db(goods_live_id_list, LIVE_GOODS_TEMP_TABLE)

def get_goods_id_list_from_temp(live_id):

    goods_id_list = []
    MYSQL_CONN = MYSQL()
    live_goods_row = MYSQL_CONN.select_from_table(LIVE_GOODS_TEMP_TABLE, "live_id={}".format(live_id))
    for each_goods in live_goods_row:
        goods_id = each_goods["goods_id"]
        goods_id_list.append(goods_id)
    return goods_id_list


def multiprocess_task(which_module, new_list):
    pool = ThreadPool(THREAD_NUM)
    results = pool.map(which_module, new_list)
    pool.close()
    pool.join()
    return results

def insert_to_db(results, which_table):
    MYSQL_CONN = MYSQL()
    for each_result in results:
        try:
            MYSQL_CONN.insert_into_table(each_result, which_table)
            logging.info("spider one item into {}".format(which_table))
        except Exception as e:
            logging.error(str(each_result))
            logging.error(e)

def delete_live_goods_temp(live_id):
    MYSQL_CONN = MYSQL()
    try:
        MYSQL_CONN.delete_from_table(LIVE_GOODS_TEMP_TABLE, "live_id={}".format(live_id))
    except Exception as e:
        logging.error(live_id)
        logging.error(e)

def spider_goods_info(zhubo_id, live_id):
    which_module = "goods_info module"
    while live_id == get_live_id(zhubo_id) != str(0):
        from_live_goods_to_temp(live_id)
        goods_id_list = get_goods_id_list_from_temp(live_id)
        results = multiprocess_task(spider_goods, goods_id_list)
        insert_to_db(results, GOODS_INFO_TABLE)
        #time.sleep(GOODS_INFO_TIME)
        if sleep_and_detect(GOODS_INFO_TIME, zhubo_id, live_id, which_module):
            pass
        else:
            break

    end_liveing(zhubo_id)
    delete_live_goods_temp(live_id)


def spider_live_dynamic(zhubo_id, live_id):
    which_module = "dynamic module"
    while live_id == get_live_id(zhubo_id) != str(0):
        #MYSQL_CONN = MYSQL()
        result_dict = spider_dynamic(zhubo_id)
        results = [result_dict]
        insert_to_db(results, LIVE_DYNAMIC_TABLE)
        #time.sleep(DYNAMIC_TIME)
        if sleep_and_detect(DYNAMIC_TIME, zhubo_id, live_id, which_module):
            pass
        else:
            break
    end_liveing(zhubo_id)

def spider_live_danmu(zhubo_id):
    spider_danmu(zhubo_id)

def spider_zhubo_info(zhubo_id):
    result_dict = spider_zhubo(zhubo_id)
    results = [result_dict]
    insert_to_db(results, ZHUBO_INFO_TABLE)

def update_goods_id(zhubo_id, live_id):
    which_module = "update_goods_id moduel"
    while get_live_id(zhubo_id) != str(0):
        #time.sleep(UPDATE_GOODS_ID_TIME)
        if sleep_and_detect(UPDATE_GOODS_ID_TIME, zhubo_id, live_id, which_module):
            pass
        else:
            break
        url_goods_list = "https://taobaolive.taobao.com/api/item_list/1.0?type=0&liveId="
        #live_id = get_live_id(zhubo_id)
        goods_json_dict = get_goods_list(url_goods_list, live_id)

    end_liveing(zhubo_id)

def start_liveing(zhubo_id):
    info_dict = {"zhubo_id": zhubo_id, "is_live": "1"}
    MYSQL_CONN = MYSQL()
    MYSQL_CONN.insert_into_table_exist_update(info_dict, ZHUBO_LIVE_TABLE, "is_live=1")

def spider_some(zhubo_id):
    #first spider basic
    spider_basic(zhubo_id)

    '''
    spider danmu
    spider dynamic
    spider goods_info
    spider zhubo_info
    '''
    live_id = get_live_id(zhubo_id)
    if live_id == str(0):
        end_liveing(zhubo_id)
    else:
        start_liveing(zhubo_id)
        goods_info_process = threading.Thread(target=spider_goods_info, args=(zhubo_id, live_id,))
        danmu_process = threading.Thread(target=spider_live_danmu, args=(zhubo_id,))
        dynamic_process = threading.Thread(target=spider_live_dynamic, args=(zhubo_id, live_id,))
        update_goods_process = threading.Thread(target=update_goods_id, args=(zhubo_id, live_id,))
        goods_info_process.start()
        danmu_process.start()
        dynamic_process.start()
        update_goods_process.start()
    zhubo_info_process = threading.Thread(target=spider_zhubo_info, args=(zhubo_id,))
    zhubo_info_process.start()

    #     goods_info_process = multiprocessing.Process(target=spider_goods_info, args=(zhubo_id, live_id,))
    #     danmu_process = multiprocessing.Process(target=spider_live_danmu, args=(zhubo_id,))
    #     dynamic_process = multiprocessing.Process(target=spider_live_dynamic, args=(zhubo_id, live_id,))
    #     update_goods_process = multiprocessing.Process(target=update_goods_id, args=(zhubo_id, live_id,))
    #     goods_info_process.start()
    #     danmu_process.start()
    #     dynamic_process.start()
    #     update_goods_process.start()
    # zhubo_info_process = multiprocessing.Process(target=spider_zhubo_info, args=(zhubo_id,))
    # zhubo_info_process.start()

# def spider_some(zhubo_id):
#     with My_Context(zhubo_id):
#         spider_one(zhubo_id)

# # def make_is_live_to_zero(zhubo_id):
# #     MYSQL_CONN = MYSQL()
# #     MYSQL_CONN.insert_into_table_exist_update()

# class My_Context(object):
#     """docstring for My_Context"""
#     def __init__(self, arg):
#         super(My_Context, self).__init__()
#         self.arg = arg
    
#     def __enter__(self):
#         pass

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         end_liveing(self.arg)

if __name__ == '__main__':
    zhubo_id = sys.argv[1]
    
    spider_some(zhubo_id)