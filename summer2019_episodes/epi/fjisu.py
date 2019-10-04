#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

import json 
from . import misc 
from urllib.parse import quote, unquote 

class fjisu(object):
    def __init__(self, ):
        self.host = "http://v.mtyee.com";
        self.search_host = self.host + "/sssv.php?top=10&q=";
    def pull(self, search_term, ):
        self.st = search_term;
        self.url = self.search_host + quote(self.st);
        self.get_list();
        return self.items;
    def get_list(self, ):
        json_text = misc.r_get(self.url, headers = {'Origin': "http://www.fjisu.tv"}, encoding = 'utf-8-sig').strip();
        tv_list = json.loads(json_text);
        self.items = [{'title': x['title'], 'url': x['url']} for x in tv_list];

if(__name__ == '__main__'):
    x = fjisu();
    x.pull("神盾局");
    print(x.pages[0].url)
