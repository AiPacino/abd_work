#coding:utf-8
import logging
import sys
import json
import re
sys.path.append("..")
from MySql_InterFace.mysql_interface import MYSQL
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from spider_zhubo import spider_zhubo

MySQL_COON = MYSQL()

def main():
    b = []
    a = MySQL_COON.select_from_table("live_taobao_webstar_crawl_live_basic", *b)
    n = 1
    m = 1
    list_url = []
    for row in a:
        #print row["daren_url"]
        user_info_json = row["user_info_json"]
        user_info_json = json.loads(user_info_json)
        zhubo_url = user_info_json["result"]["model"]["broadCaster"]["jumpUrl"]
        #zhubo_url = re.sub(r"//","",zhubo_url)
        #print zhubo_url
        n = n + 1
        list_url.append(zhubo_url)
        if n % 10 == 0:
            pool = ThreadPool(5)
            results = pool.map(spider_zhubo, list_url)
            pool.close()
            pool.join()
            list_url = []
            for each in results:
                MySQL_COON.insert_into_table(each, "live_taobao_webstar_crawl_zhubo_info")
            logging.info("######{}#####zhubo has been in db".format(n))
            m = m + 1
    pool = ThreadPool(5)
    results = pool.map(spider_zhubo, list_url)
    pool.close()
    pool.join()
    list_url = []
    for each in results:
        MySQL_COON.insert_into_table(each, "live_taobao_webstar_crawl_zhubo_info")
    logging.info("######{}#####zhubo has been in db".format(n))

    print n

    

if __name__ == '__main__':
    main()