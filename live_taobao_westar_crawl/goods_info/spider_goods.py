#coding:utf-8
import sys
import requests
import logging
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
sys.path.append("..")
from Downloader.Downloader import Downloader
from Config.Config import LOW_HIGH_EQUAL, TMALL_LOW_HITGH_EQUAL, SHOP_SCORE

download = Downloader()

def translate_jsonp_json(jsonp):
    jsonp = jsonp.strip()
    if jsonp.endswith(")"):
        logging.info("endswith )")
        data_json = jsonp.strip("jsonp(").strip(")")
        data_json = json.loads(data_json)
        return data_json
    elif jsonp.endswith(");"):
        logging.info("endswith );")
        data_json = jsonp.strip("jsonp(").strip(");")
        data_json = json.loads(data_json)
        return data_json
    else:
        logging.info("endswith unknown")
        data_json = json.laods(jsonp)
        return data_json

def get_comment_count(url):
    comment_count = {}

    try:
        response = download.download_requests(url)
        data = response.text
        data_json = translate_jsonp_json(data)
        comment_count["comment_count"] = data_json[u"count"]
    except Exception as e:
        logging.error(url)
        logging.error(e)

    return comment_count


def get_detail(url):
    detail = {}

    try:
        response = download.download_requests(url)
        html = response.text

        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logging.error(url)
        logging.error(e)
    
    #goods title
    #Has been in the live_goods
    # try:
    #     main_title = soup.select(".tb-main-title")
    #     main_title = main_title[0].get_text()
    #     detail["title"] = main_title.strip()
    # except Exception as e:
    #     logging.error(url)
    #     logging.error(e)
    

    #goods price
    try:
        taobao_price = soup.select("#J_StrPrice")
        price = taobao_price[0].get_text()[1:]
        detail["goods_price"] = price
    except Exception as e:
        logging.error(url)
        logging.error(e)

    #tmall goods price
    if detail.has_key("goods_price"):
        pass
    else:

        try:
            page_html = ''.join(html.split())
            price = re.search(r'"defaultItemPrice":"(.*?)"', page_html).group(1)
            detail["goods_price"] = price
        except Exception as e:
            logging.error(url)
            logging.error(e)
    

    #shop rate
    try:
        rate_low_low_equal = soup.select(".tb-shop-rate dl")
    
        for each in rate_low_low_equal:
            dt = each.select("dt")[0].get_text().strip()
            dd = each.select("dd")[0].get_text().strip()
            detail[SHOP_SCORE[dt]] = dd
            for rate, select in LOW_HIGH_EQUAL.items():
                if each.select(select):
                    dt_rate = SHOP_SCORE[dt] + "_rate"
                    detail[dt_rate] = rate
    except Exception as e:
        logging.error(url)
        logging.error(e)

    #tmall shop rate
    try:
        rate_low_low_equal = soup.select(".shopdsr-item")

        for each in rate_low_low_equal:
            shop_title = each.select(".shopdsr-title")[0].get_text().strip()
            shop_title = ''.join(shop_title.split())
            shop_rate = each.select(".shopdsr-score-con")[0].get_text().strip()
            detail[SHOP_SCORE[shop_title]] = shop_rate
            for rate, select in TMALL_LOW_HITGH_EQUAL.items():
                if each.select(select):
                    title_rate = SHOP_SCORE[shop_title] + "_rate"
                    detail[title_rate] = rate
    except Exception as e:
        logging.error(url)
        logging.error(e)

    print repr(detail).decode("unicode-escape")
    return detail

def get_comment_summary(url):
    try:
        response = download.download_requests(url)
        data = response.text
        data_json = translate_jsonp_json(data)
        impress = data_json["data"]["impress"]
        impress = json.dumps(impress)
    except Exception as e:
        impress = "[]"
        logging.error(url)
        logging.error(e)
    comment_summary = {"comment_summary":impress}
    return comment_summary

##sell_count and taobao_price
def get_sell_count(url, goods_id):

    count_price = {}
    try:
        response = download.download_requests_sell_count(url, goods_id)

        data = response.text
    
        data_json = translate_jsonp_json(data)
        data_json = data_json["data"]

        ##sell_count
        sell_count = data_json["soldQuantity"]
        new_sell_count = {}
        try:
            new_sell_count["confirm_goods_count"] = sell_count["confirmGoodsCount"]
            new_sell_count["sold_total_count"] = sell_count["soldTotalCount"]
        except Exception as e:
            logging.error(url)
            logging.error(e)
        #print new_sell_count
        count_price.update(new_sell_count)

        #sell_price
        sell_price = data_json["promotion"]["promoData"]
        sell_price = json.dumps(sell_price)
        count_price["different_price"] = sell_price
    except Exception as e:
        logging.error(url)
        logging.error(e)

    return count_price

def spider_goods(goods_id):

    GOODS = {
    "comment_count": "https://rate.taobao.com/detailCount.do?callback=jsonp&itemId={}".format(goods_id),
    "detail": "https://item.taobao.com/item.htm?id={}".format(goods_id),
    "comment_summary": "https://rate.taobao.com/detailCommon.htm?auctionNumId={}&callback=jsonp".format(goods_id),
    "sell_count": "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId={}&modules=,xmpPromotion,soldQuantity&callback=jsonp".format(goods_id)
    }

    comment_count = get_comment_count(GOODS["comment_count"])
    #logging.error() comment_count

    detail = get_detail(GOODS["detail"])
    #logging.error() detail

    comment_summary = get_comment_summary(GOODS["comment_summary"])
    #rint comment_summary

    sell_count = get_sell_count(GOODS["sell_count"], goods_id)

    all_detail = dict(comment_count, **detail)
    all_info = dict(all_detail, **comment_summary)
    all_info.update(sell_count)

    all_info["goods_id"] = goods_id
    all_info["crawl_time"] = datetime.now()


    return all_info

if __name__ == '__main__':
    #goods_id = 540401358656
    logging.basicConfig(level=logging.INFO)
    #goods_id = 539421273992
    goods_id = sys.argv[1]
    all_info = spider_goods(goods_id)
    print repr(all_info).decode("unicode-escape")
    # test()
