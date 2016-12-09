#coding:utf-8
import sys
sys.path.append("..")
from all_main.TASK_OBJECT import TASK_OBJECT
from Config.Config import LIVE_GOODS_TABLE as from_table
from Config.Config import GOODS_INFO_TABLE as into_table
from spider_goods import spider_goods


def start_goods_task():
    param = {
        "from_table": from_table,
        "from_table_condition": "",
        "need_to_update": False,
        "which_module": spider_goods,
        "into_table": into_table,
        "need_to_return": True,
        "which_need_in_row": "goods_id",
        "update_into_table": False
    }
    goods_task = TASK_OBJECT(**param)
    goods_task.task_main()

if __name__ == '__main__':
    start_goods_task()

        