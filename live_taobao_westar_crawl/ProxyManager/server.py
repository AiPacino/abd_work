#!/usr/bin/env python
# coding=utf-8

import datetime
import json
import logging
import random
import requests
import sys
import threading
from collections import OrderedDict
from functools import partial
from traceback import print_exc

import flask
import grequests
from abd.concurrency import sync_dict
from abd.misc import force_str, default_if_null
from typing import Iterable, List, Union

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO, filename='/home/ubuntu/crawl/server_log/server_1.log')

logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

block_size = 800


def fetch_kuaidaili():
    url = 'http://svip.kuaidaili.com/api/getproxy'
    params = {
        'orderid': '957036584239526',
        'num': block_size,
        'area_ex': '台湾,香港,澳门',
        'sort': 1,
        'format': 'json',
        'quality': 2,
    }
    _json = requests.get(url, params=params).json()
    if _json['code'] == 0:
        return ['http://{}'.format(p) for p in _json['data']['proxy_list']]
    else:
        logging.error('Cannot fetch kuaidaili proxies: %s', force_str(_json['msg']))
        return []


def fetch_daili666():
    url = 'http://tpv.daxiangdaili.com/ip/'
    params = {
        'tid': '556550714338467',
        'num': block_size,
        'delay': '1',
        'foreign': 'none'
    }
    r = requests.get(url, params=params)
    return ['http://{}'.format(p) for p in r.text.split()]


def filter_proxies(proxies, timeout):
    # type: (Iterable[Union[str, unicode]], Union[int, float]) -> List[Union[str, unicode]]

    def _exception_handler(req, exc):
        pass

    test_url = 'http://weibo.com'
    proxy_settings = [{'http': p} for p in proxies]
    async_requests = [grequests.get(test_url, proxies=ps, timeout=timeout) for ps in proxy_settings]
    responses = grequests.map(async_requests, exception_handler=_exception_handler)
    ok_proxies = [p for p, r in zip(proxies, responses)
                  if r and r.status_code == 200 and 'Sina Visitor System' in r.content]
    return ok_proxies


filter_proxies_N_secs = partial(filter_proxies, timeout=10)

glb = sync_dict({'proxies': [], 'update_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


def auto_update_proxies():
    while True:
        try:
            logging.info('Start updating proxies...')
            new_proxies = set()
            new_proxies.update(filter_proxies_N_secs(fetch_kuaidaili()))
            new_proxies.update(filter_proxies_N_secs(fetch_daili666()))
            new_proxies.difference_update(glb['proxies'])

            oldest_proxies = glb['proxies'][:block_size]
            renewed_proxies = filter_proxies_N_secs(oldest_proxies)
            untouched_proxies = glb['proxies'][block_size:]

            with glb:
                glb['proxies'] = untouched_proxies
                glb['proxies'].extend(new_proxies)
                glb['proxies'].extend(renewed_proxies)
                glb['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                logging.info('Proxies updated: total_num = {}'.format(len(glb['proxies'])))
        except Exception:
            print_exc()


class JSONResponse(flask.Response):
    default_mimetype = 'application/json; charset=utf-8'


app = flask.Flask(__name__)
app.response_class = JSONResponse
app.debug = True


@app.route('/', methods=['GET'])
def get_proxies():
    arg_max_num = int(default_if_null(flask.request.args.get('max_num'), sys.maxint))

    with glb:
        response = OrderedDict()
        response['update_time'] = glb['update_time']
        _proxies = list(glb['proxies'])
        response['total_num'] = len(_proxies)
        if len(_proxies) <= arg_max_num:
            response['num'] = len(_proxies)
            response['proxies'] = _proxies
        else:
            response['num'] = arg_max_num
            random.shuffle(_proxies)
            response['proxies'] = _proxies[:arg_max_num]

        return json.dumps(response)


if __name__ == '__main__':
    threading.Thread(target=auto_update_proxies).start()
    app.run(host='0.0.0.0', port=9001, use_reloader=False)
