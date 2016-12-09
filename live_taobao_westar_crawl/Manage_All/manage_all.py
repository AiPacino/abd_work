#coding:utf-8
import multiprocessing
import time
import sys
sys.path.append('..')
from config import DYNAMIC_TIME
from live_basic.test_info import spider_basic
from live_dynamic.dynamic_main_task import start_dynamic_task as spider_dynamic
from live_danmu.danmu_main_task import start_danmu_task as spider_danmu
from goods_info.goods_main_task import start_goods_task as spider_goods
from zhubo_info.info_main_task import start_zhubo_info_task as spider_zhubo


def spider_zhubo_list():
    
    zhubo_list = list(sys.argv[1])
    print zhubo_list
    return zhubo_list

def spider_live_basic(zhubo_id):
    spider_basic(zhubo_id)

def spider_zhubo_info():
    spider_zhubo()

def spider_goods_info():
    spider_goods()

def spider_live_dynamic():
    while True:
        spider_dynamic()
        time.sleep(DYNAMIC_TIME)


def spider_live_danmu():
    spider_danmu()

def spider_all():

    zhubo_id_list = spider_zhubo_list()
    for each_zhubo in zhubo_id_list:
        print each_zhubo
        #first spider live_basic
        spider_live_basic(zhubo_id)


    #second spider zhubo_info
    spider_zhubo_info()

    #then spider the living info: danmu , dynamic , and goods
    danmu_process = multiprocessing.Process(target=spider_live_danmu)
    dynamic_process = multiprocessing.Process(target=spider_live_dynamic)
    goods_process = multiprocessing.Process(target=spider_goods_info)

    danmu_process.start()
    dynamic_process.start()
    goods_process.start()







if __name__ == '__main__':
    zhubo_id = sys.argv[1]
    spider_all()