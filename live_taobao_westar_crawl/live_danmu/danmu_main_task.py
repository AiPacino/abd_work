#coding:utf-8
import sys
sys.path.append("..")
from all_main.TASK_OBJECT import TASK_OBJECT
from Config.Config import LIVE_BASIC_TABLE as from_table
from Config.Config import LIVE_DANMU_TABLE as into_table
from live_danmu import spider_danmu


def start_danmu_task():
    param = {
        "from_table": from_table,
        "from_table_condition": "is_live=1",
        "need_to_update": True,
        "which_module": spider_danmu,
        "into_table": into_table,
        "need_to_return": False,
        "which_need_in_row": "zhubo_id",
        "update_into_table": False
    }
    danmu_task = TASK_OBJECT(**param)
    danmu_task.task_main()

if __name__ == '__main__':
    start_danmu_task()

        