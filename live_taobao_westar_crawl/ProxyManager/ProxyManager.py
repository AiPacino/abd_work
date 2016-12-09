import requests
import logging
import time

SESSION = requests.session()


def get_proxy():
    ##now it only get one proxy a time
    kuaidaili = "http://svip.kuaidaili.com/api/getproxy/?orderid=957036584239526&num=1&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_ha=1&sp1=1&quality=2&sort=2&format=json&sep=1"
    try:
        proxy_json = requests.get(kuaidaili)
        data_json = proxy_json.json()
        proxy = data_json["data"]["proxy_list"][0]
    except Exception as e:
        logging.error(e)
        return None
    

    proxies = {
        "http" : proxy,
    }

    return proxies

def main(goods_id):
    GOODS = {
    "comment_count": "https://rate.taobao.com/detailCount.do?callback=jsonp101&itemId={}".format(goods_id),
    "detail": "https://item.taobao.com/item.htm?id={}".format(goods_id),
    "comment_summary": "https://rate.taobao.com/detailCommon.htm?auctionNumId={}&callback=json_tbc_rate_summary".format(goods_id),
    #"sell_count": "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId={}&modules=,xmpPromotion,soldQuantity&callback=onSibRequestSuccess".format(goods_id)
    }
    kuaidaili = "http://svip.kuaidaili.com/api/getproxy/?orderid=957036584239526&num=1&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_ha=1&sp1=1&quality=2&sort=2&format=json&sep=1"
    
    proxy_json = SESSION.get(kuaidaili)
    data_json = proxy_json.json()
    proxy = data_json["data"]["proxy_list"][0]
    
    proxy = "124.88.67.24:81"
    proxies = {
        "http": proxy,
    }
    print proxy
    for url in GOODS.values():
        response = SESSION.get(url, proxies=proxies)

        print response.status_code

if __name__ == '__main__':
    goods_id = 535540164414
    main(goods_id)