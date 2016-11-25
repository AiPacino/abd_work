import sys
sys.path.append("..")
from Config.Config import *


#All the table name
'''
the table name of mysql
'''
GOODS_INFO = "live_taobao_webstar_crawl_goods_info"
LIVE_BASIC = "live_taobao_webstar_crawl_live_basic"
LIVE_DANMU = "live_taobao_webstar_crawl_live_danmu"
LIVE_DYNAMIC = "live_taobao_webstar_crawl_live_dynamic"
LIVE_GOODS = "live_taobao_webstar_crawl_live_goods"
ZHUBO_INFO = "live_taobao_webstar_crawl_zhubo_info"


#All the mysql config
'''
table_name:select table and insert table
column:  column from the table which you select
'''
WHICH_MODULE = {
    "live_dynamic":{
        "select_process":{
            "table_name": LIVE_BASIC,
            "select_row":["zhubo_id",],
            "row_key_value":"zhubo_id",
        },
        "insert_process":{
            "table_name":LIVE_DYNAMIC,
        },
    },
    "goods_info":{
        "select_process":{
            "table_name":"",
            "select_row":""
        },
        "insert_process":{
            "table_name":"",
        },
    },
}