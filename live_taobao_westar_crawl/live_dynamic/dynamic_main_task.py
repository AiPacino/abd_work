#coding:utf-8
import sys
sys.path.append("..")
from all_main.TASK_OBJECT import TASK_OBJECT
from Config.Config import LIVE_BASIC_TABLE as from_table
from Config.Config import LIVE_DYNAMIC_TABLE as into_table
from live_dynamic import spider_dynamic
import logging


def start_dynamic_task():
    param = {
        "from_table": from_table,
        "from_table_condition": "is_live=1",
        "need_to_update": True,
        "which_module": spider_dynamic,
        "into_table": into_table,
        "need_to_return": True,
        "which_need_in_row": "zhubo_id",
        "update_into_table": False
    }
    dynamic_task = TASK_OBJECT(**param)
    dynamic_task.task_main()

if __name__ == '__main__':
    n = 1
    while True:
        start_dynamic_task()
        logging.info("########################{} times of all live".format(n))
        n = n + 1

        