#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

from . import misc 
import re 
from urllib.parse import quote, unquote 

class mjw(object):
    def __init__(self, ):
        self.host = "http://91mjw.com";
        self.search_host = self.host + "/?s=";
    def pull(self, search_term, ):
        self.st = search_term;
        self.url = self.search_host + quote(self.st);
        self.get_list();
        return self.items;
    def get_list(self, ):
        html_text = misc.r_get(self.url);
        results = re.findall(r'(<article class="u-movie">[\s\S]*?</article>)', html_text);
        info = [re.findall(r'" href="(.*?)"[\s\S].*?<h2>(.*?)</h2>', x)[0] for x in results];
        self.items = [{'title': x[1], 'url': x[0]} for x in info];
        # tv_list = json.loads(json_text);
        # self.items = [{'title': x['title'], 'url': x['url']} for x in tv_list];

if(__name__ == '__main__'):
    import misc 
    x = mjw();
    x.pull("神盾局");
    print(x.items);
