#coding:utf-8
from config import WHICH_MODULE
import sys
sys.path.append("..")
from live_dynamic.live_dynamic import spider_dynamic
from MySql_InterFace.mysql_interface import MYSQL

MYSQL_COON = MYSQL()
which_module = WHICH_MODULE["live_dynamic"]

def get_row():
    select_process = which_module["select_process"]
    rows = MYSQL_COON.select_from_table(select_process["table_name"], select_process["select_row"])
    for row in rows:
        key_value = row[select_process["row_key_value"]]
        yield key_value

def 


if __name__ == '__main__':
    main()