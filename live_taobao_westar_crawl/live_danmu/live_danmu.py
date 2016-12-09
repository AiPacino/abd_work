#coding:utf-8
import sys
sys.path.append("..")
from Downloader.Downloader import Downloader
from Config.Config import DANMU
import Queue
import copy
import re
from collections import defaultdict
from MySql_InterFace.mysql_interface import MYSQL
from update_live_basic.update_live_basic import get_update_state
import logging
from datetime import datetime
from pyvirtualdisplay import Display

DOWNLOAD = Downloader()
#MYSQL_COON = MYSQL()


def get_cha_list(list_parent, list_sub):
    
    count = defaultdict(int)
    for each in list_parent:
        count[each] += 1

    for each in list_sub:
        count[each] -= 1
    
    cha_list = []
    for each in list_parent:
        if count[each] > 0:
            count[each] -= 1
            cha_list.append(each)

    return cha_list


def process_comment_list(comment_list, live_id):
    MYSQL_COON = MYSQL()
    for each_comment in comment_list:
        danmu_dict = {}
        split_comment = each_comment.split(" ", 1)
        # print type(split_comment[1])
        # print type(DANMU.keys()[1])
        if split_comment[1] in DANMU.keys():
            danmu_dict["action"] = DANMU[split_comment[1]]
        else:
            danmu_dict["action"] = 3
        danmu_dict["live_id"] = live_id
        danmu_dict["crawl_time"] = datetime.now()
        danmu_dict["comment"] = split_comment[1]
        danmu_dict["user_name"] = split_comment[0]
        logging.info(each_comment)
        MYSQL_COON.insert_into_table(danmu_dict, "live_taobao_webstar_crawl_live_danmu")


def spider_danmu(zhubo_id):

    before_comments = []
    url = "https://taobaolive.taobao.com/room/index.htm?userId={}".format(zhubo_id)
    driver = DOWNLOAD.download_chrome(url)

    display = Display(visible=0, size=(800,800))
    display.start()
    #get live id
    response = DOWNLOAD.download_requests(url)
    try:
        live_id = re.search(r'"liveId":(\d+)', response.text).group(1)
    except Exception as e:
        live_id = 0
        logging.error(url)
        logging.error(e)

    comment_outer = DOWNLOAD.find_element_by_css(driver, ".comment-inner")

    while comment_outer:
        try:
            live_done = driver.find_element_by_css_selector(".lr-video-err-mask")
        except Exception as e:
            if live_id == 0:
                driver.close()
                break
            comment_text = re.sub(r":\n", " ", comment_outer.text)
            all_comments = comment_text.splitlines()

            cha_set_list = get_cha_list(all_comments, before_comments)

            if cha_set_list:
                process_comment_list(cha_set_list, live_id)
                #print repr(cha_set_list).decode("unicode-escape")
            before_comments = copy.deepcopy(all_comments)
        else:
            driver.close()
            break
        #print live_done



        
        
    logging.info("This {} didn't living!".format(zhubo_id))


if __name__ == '__main__':

    zhubo_id = sys.argv[1]
    spider_danmu(zhubo_id)
    #spider_douyu()
    ##from pyvirtualdisplay import Display
    ##display = Display(visible=0, size=(800,800))
    ##display.start()