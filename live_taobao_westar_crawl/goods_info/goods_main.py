from spider_goods import spider_goods
import re
import time, random
import logging
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import sys
sys.path.append("..")
from MySql_InterFace.mysql_interface import MYSQL


MYSQL_COON = MYSQL()

def process_list():
    b = []
    a = MYSQL_COON.select_from_table("live_taobao_webstar_crawl_live_goods", *b)

    n = 1
    goods_list = []
    for row in a:
        goods_id = row["goods_id"]
        yield goods_id

def main():

    goods_id = process_list()


    new_line = []
    n = 1
    m = 0
    start_map_time = time.time()
    for each_goods in goods_id:
        new_line.append(each_goods)

        if n % 10 == 0:
            pool = ThreadPool()
            
            results = pool.map(spider_goods, new_line)
            pool.close()
            pool.join()
            new_line = []
            for each_result in results:
                try:
                    MYSQL_COON.insert_into_table(each_result, "live_taobao_webstar_crawl_goods_info")
                    m = m + 1
                    logging.info("-----------------" + str(m) + "\t:goods had been in mysql")
                except Exception as e:
                    logging.error(str(each_goods))
                    logging.error(e)
        n = n + 1


    ##The rest of the goods
    pool = ThreadPool()
    results = pool.map(spider_goods, new_line)
    pool.close()
    pool.join()
    new_line = []
    for each_result in results:
        try:
            MYSQL_COON.insert_into_table(each_result, "live_taobao_webstar_crawl_goods_info")
            m = m + 1
            logging.info("-----------------" + str(m) + "\t:goods had been in mysql")
        except Exception as e:
            logging.error(str(each_goods))
            logging.error(e)

    end_map_time = time.time()

    time_for_map = end_map_time - start_map_time
    #time_for_insert = end_sql_time - start_sql_time
    logging.info("#######Spider time is {}".format(time_for_map))
    logging.info("#######Insert into mysql Done!!!!!#######")


if __name__ == '__main__':
    main()