import sys
sys.path.append("..")
from MySql_InterFace.mysql_interface import MYSQL
from update_live_basic.update_live_basic import get_update_state
from multiprocessing.dummy import Pool as ThreadPool
from Config.Config import THREAD_NUM
import logging

class TASK_OBJECT(object): 
    '''
    This class has 6 parameters.
    from_table: the module is begin from which table to get the data
    from_table_condition: select from the table's condition, the default is empty list
    need_to_update: the module's begin need to update the table or not
    which_module: which module you need to start
    into_table: the module's results is need to insert into which table
    need_to_return: the module's multiprocessing need to return the data or not
    '''
    def __init__(self, from_table, from_table_condition, need_to_update, which_module, into_table, need_to_return, which_need_in_row, update_into_table):
        super(TASK_OBJECT, self).__init__()

        self.MYSQL_CONN = MYSQL()
        self.from_table = from_table
        self.from_table_condition = from_table_condition
        self.need_to_update = need_to_update
        self.which_module = which_module
        self.into_table = into_table
        self.need_to_return = need_to_return
        self.which_need_in_row = which_need_in_row
        self.update_into_table = update_into_table
 
    def get_rows(self):

        rows = self.MYSQL_CONN.select_from_table(self.from_table, self.from_table_condition)

        for row in rows:
            if self.need_to_update:
                row = get_update_state(row)
            if row:
                yield row

    def multiprocess_task(self,new_list):
        pool = ThreadPool()
        if self.need_to_return:
            results = pool.map(self.which_module, new_list)
        else:
            pool.map(self.which_module, new_list)
        pool.close()
        pool.join()
        if self.need_to_return:
            return results

    def insert_to_db(self,results):

        for each_result in results:
            try:
                if self.update_into_table:
                    self.MYSQL_CONN.insert_into_table_with_replace(each_result, self.into_table)
                else:
                    self.MYSQL_CONN.insert_into_table(each_result, self.into_table)
            except Exception as e:
                logging.error(str(each_result))
                logging.error(e)

    def task_main(self):
        
        rows = self.get_rows()

        new_list = []

        for row in rows:
            new_list.append(row[self.which_need_in_row])
            if len(new_list) % THREAD_NUM == 0:
                if self.need_to_return:
                    results = self.multiprocess_task(new_list)
                    self.insert_to_db(results)
                else:
                    self.multiprocess_task(new_list)
                new_list = []
        if new_list:
            if self.need_to_return:
                results = self.multiprocess_task(new_list)
                self.insert_to_db(results)
            else:
                self.multiprocess_task(new_list)
            new_list = []
