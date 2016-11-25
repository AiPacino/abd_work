#coding:utf-8
import MySQLdb
import logging
import sys
sys.path.append("..")
from Config.Config import MYSQL_CONFIG

class MYSQL:

    def __init__(self):
        
        self.coon = MySQLdb.connect(**MYSQL_CONFIG)
        self.cursor = self.coon.cursor()

    def insert_into_table(self, info_dict, table_name):

        columns = info_dict.keys()
        values = map(info_dict.get, columns)
        columns = ",".join(columns)
        #logging.info(columns)
        #logging.info(values)
        #logging.info(values+":\t"+str(len(values)))

        placeholders = ', '.join(['%s'] * len(info_dict))

        sql = """INSERT INTO {0}({1}) VALUES ({2})""".format(table_name, str(columns), placeholders)
        #print sql
        #logging.debug("insert into db, sql is \t{}".format(sql))
        try:
            #执行sql语句
            self.cursor.execute(sql, values)
            self.coon.commit()
        except Exception as e:
            #print "what"
            logging.error(e)
            self.coon.rollback()


    def select_info(self, table_name):

        cur = self.coon.cursor(MySQLdb.cursors.DictCursor)

        sql = """SELECT * FROM {0}""".format(table_name)

        try:
            cur.execute(sql)
            self.coon.commit()
            rows = cur.fetchall()
        except Exception as e:
            logging.error(e)
            self.coon.rollback()
            return None
        return rows

    def select_from_table(self, table_name, *args):
        #select args from table_name 

        cur = self.coon.cursor(MySQLdb.cursors.DictCursor)

        columns = ",".join(args)
        if len(columns) == 0:
            columns = "*"

        sql = """SELECT {0} from {1}""".format(columns, table_name)

        try:
            cur.execute(sql)
            for row in cur:
                yield row
            #self.coon.commit()
        except Exception as e:
            logging.error(e)
            #return None

    def select_from_table_where_condition(self, table_name, condition,*args):
        #select args from table_name 

        cur = self.coon.cursor(MySQLdb.cursors.DictCursor)

        columns = ",".join(args)
        if len(columns) == 0:
            columns = "*"

        sql = """SELECT {0} from {1} where {2}""".format(columns, table_name, condition)

        try:
            cur.execute(sql)
            for row in cur:
                yield row
            #self.coon.commit()
        except Exception as e:
            logging.error(e)
            #return None

    def update_live_basic_is_live_from_zhubo_id(self, zhubo_id):
        #update the is_live of the zhubo_id in the table, only 1 --> 0

        cur = self.coon.cursor(MySQLdb.cursors.DictCursor)

        sql = """UPDATE live_taobao_webstar_crawl_live_basic set is_live=0 where zhubo_id={}""".format(zhubo_id)

        try:
            cur.execute(sql)
            self.coon.commit()
        except Exception as e:
            logging.error(e)
            self.coon.rollback()

    def update_live_basic_is_live_from_live_id(self, live_id):
        #update the is_live of the zhubo_id in the table, only 1 --> 0

        cur = self.coon.cursor(MySQLdb.cursors.DictCursor)

        sql = """UPDATE live_taobao_webstar_crawl_live_basic set is_live=0 where live_id={}""".format(live_id)

        try:
            cur.execute(sql)
            self.coon.commit()
        except Exception as e:
            logging.error(e)
            self.coon.rollback()


    def close_db(self):
        #关闭数据库
        self.coon.close()

if __name__ == '__main__':
    mysql_coon = MYSQL()
    info_dict = {'logistics': u'4.7', 'service-rate': '1', 'description': u'4.7', 'service': u'4.7', 'title': u'大英自制 胸前斜纹中长气质百搭打底衫女针织毛衣女韩版修身', 'price': u'188.00', 'description-rate': '1', 'comment_summary': '[{"count": 109, "attribute": "620-11", "scm": "", "value": 1, "title": "\u8d28\u91cf\u597d"}, {"count": 44, "attribute": "1722-11", "scm": "", "value": 1, "title": "\u8863\u8863\u5f88\u8212\u670d"}, {"count": 40, "attribute": "622-11", "scm": "", "value": 1, "title": "\u539a\u5b9e"}, {"count": 20, "attribute": "520-11", "scm": "", "value": 1, "title": "\u4fbf\u5b9c"}, {"count": 18, "attribute": "1822-11", "scm": "", "value": 1, "title": "\u7a7f\u4e0a\u597d\u770b"}, {"count": 16, "attribute": "522-11", "scm": "", "value": 1, "title": "\u7248\u578b\u6f02\u4eae"}, {"count": 10, "attribute": "322-11", "scm": "", "value": 1, "title": "\u8272\u5f69\u5f88\u597d"}, {"count": 4, "attribute": "420-11", "scm": "", "value": 1, "title": "\u7269\u6d41\u5feb"}, {"count": 3, "attribute": "10120-11", "scm": "", "value": 1, "title": "\u670d\u52a1\u4e0d\u9519"}, {"count": 11, "attribute": "922-13", "scm": "", "value": -1, "title": "\u505a\u5de5\u8f83\u5dee"}]', 'comment_count': 419, 'crawl_time': datetime.datetime(2016, 11, 3, 18, 58, 1, 614066), 'id': 540401358656, 'logistics-rate': '0'}

    mysql_coon.insert_darenInfo(info_dict, "zhubo_goods")





