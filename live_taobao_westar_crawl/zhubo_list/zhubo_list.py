#coding:utf-8
import requests
import random
import json
import sys
sys.path.append("..")
from Config.Config import USER_AGENTS
#from Downloader.Downloader import Downloader

def main(url):
    list_url = "https://taobaolive.taobao.com/api/get_videos/1.0?sortType=hot"
    HEADERS = {
        "User-Agent": random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        "Referer": url,
    }

    response = requests.get(list_url)
    print response.text


def get_list():
    with open("json_list", "r") as f:
        line = f.readline()

    print type(line)
    json_line = json.loads(line)
    dataList = json_line["result"]["model"]["dataList"]
    user_ids = []
    for each in dataList:
        user_ids.append(each["data"]["accountId"])

    print user_ids
    print type(json_line)



if __name__ == '__main__':
    # url = "https://taobaolive.taobao.com/room/index.htm?spm=a21tn.8216370.2278281.1.Hl9HdW&userId=1063569743"
    # main(url)

    get_list()