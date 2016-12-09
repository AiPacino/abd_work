#coding:utf-8
import sys
sys.path.append("..")
from all_main.TASK_OBJECT import TASK_OBJECT
from Config.Config import LIVE_BASIC_TABLE as from_table
from Config.Config import ZHUBO_INFO_TABLE as into_table
from spider_zhubo import spider_zhubo


def start_zhubo_info_task():
    param = {
        "from_table": from_table,
        "from_table_condition": "",
        "need_to_update": False,
        "which_module": spider_zhubo,
        "into_table": into_table,
        "need_to_return": True,
        "which_need_in_row": "user_info_json",
        "update_into_table": True
    }
    zhubo_info_task = TASK_OBJECT(**param)
    zhubo_info_task.task_main()

if __name__ == '__main__':
    start_zhubo_info_task()
