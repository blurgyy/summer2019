#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

import json 
from . import misc 
from .itempage import page 
import re 
import requests 
from urllib.parse import quote, unquote 

class fjisu(object):
    """
    - attributes:
        host: str 
        search_host: str 
        st: str 
        url: str 
        items: list 
    - methods:
        __init__()
        pull(search_term)
        get_list()
    """
    def __init__(self, ):
        """ http://v.mtyee.com/sssv.php """
        self.host = "http://v.mtyee.com";
        self.search_host = self.host + "/sssv.php?top=10&q=";
    def pull(self, search_term, ):
        self.st = search_term;
        self.url = self.search_host + quote(self.st);
        self.get_list();
    def get_list(self, ):
        json_text = misc.r_get(self.url, headers = {'Origin': "http://www.fjisu.tv"}, encoding = 'utf-8-sig').strip();
        # print(json_text)
        tv_list = json.loads(json_text);
        self.items = [{'title': x['title'], 'url': x['url']} for x in tv_list];
        # self.pages = [page(item) for item in self.items];
        # return self.items;

if(__name__ == '__main__'):
    x = fjisu();
    x.pull("神盾局");
    print(x.pages[0].url)
