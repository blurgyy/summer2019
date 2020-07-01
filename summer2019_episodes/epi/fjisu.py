#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import re
import requests
from . import misc
from urllib.parse import quote, unquote


class fjisu(object):
    def __init__(self, ):
        self.host = "http://v.mtyee.com"
        self.search_host = self.host + "/sssv.php?top=10&q="
        self.items = []

    def pull(
        self,
        search_term,
    ):
        self.st = search_term
        self.url = self.search_host + quote(self.st)
        try:
            self.get_list()
        except requests.exceptions.ReadTimeout:
            print(f"  ![{self.host}]")
        return self.items

    def get_list(self, ):
        json_text = misc.r_get(self.url,
                               headers={
                                   'Origin': "http://www.fjisu.tv"
                               },
                               encoding='utf-8-sig').strip()
        tv_list = json.loads(json_text)
        self.items = [{
            'self': self,
            'title': x['title'],
            'url': x['url']
        } for x in tv_list]

    class itempage(object):
        def __init__(self, item):
            self.info = item
            self.title = self.info['title']
            self.url = self.info['url']
            self.m3u8info = []
            self.id = self.url.strip('/').split('/')[-1]
            self.reqs = [
                f"http://t.mtyee.com/ps/s{self.id}.js",
                f"http://t.mtyee.com/ty/yj/s{self.id}.js",
                f"http://t.mtyee.com/ty/zd/s{self.id}.js"
            ]

        def __str__(self, ):
            return self.title

        def pull(self, ):
            cont = ""
            for req in self.reqs:
                cont += misc.r_get(req)
            m3u8info = re.findall(r'"(https?.*?),(.*?),(.*?)"', cont)
            if (len(m3u8info) == 0):
                return False
            self.m3u8info = [{
                **self.info, 'hls_url': x[0],
                'nonsense': x[1],
                'fname': misc.unescape(x[2]) + ".m3u8"
            } for x in m3u8info if misc.ism3u8(x[0])]
            return True


if (__name__ == '__main__'):
    x = fjisu()
    x.pull("神盾局")
