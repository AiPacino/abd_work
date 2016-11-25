#coding:utf-8
import json
import sys
sys.path.append("..")
from MySql_InterFace.mysql_interface import MYSQL

MySQL_COON = MYSQL()

def get_live_goods(goods_json, live_id):
    # b = []
    # a = MySQL_COON.select_from_table("live_taobao_webstar_crawl_live_basic", *b)
    # n = 1
    # m = 1
    # list_url = []

    # for row in a:

    goods_info_json = goods_json
    goods_info_json = json.loads(goods_info_json)
    goods_info_json = goods_info_json["result"]["data"]["itemList"]
    n = 1
    for each_goods in goods_info_json:         
        each = each_goods["goodsList"][0]   

        live_goods = {}
        live_goods["live_id"] = live_id
        
        live_goods["goods_id"] = each["itemId"]
        live_goods["goods_title"] = each["itemName"]
        #print repr(live_goods).decode("unicode-escape")
        print n
        MySQL_COON.insert_into_table(live_goods, "live_taobao_webstar_crawl_live_goods")
        n = n + 1


if __name__ == '__main__':
    get_live_goods()