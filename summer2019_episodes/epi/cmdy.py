#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

import json 
import re 
from . import misc 
from .pm import parallel_manager 
# import misc 
# from pm import parallel_manager 
from urllib.parse import quote, unquote 

class cmdy(object):
    def __init__(self, ):
        self.host = "https://www.cmdy5.com";
        self.search_host = self.host + "/index.php?m=vod-search";
        self.items = [];
    def pull(self, search_term, ):
        self.st = search_term;
        form = {
            'wd': self.st
        }
        html_text = misc.r_post(self.search_host, data = form);
        with open("test.html", 'w') as f:
            f.write(html_text);
        try:
            self.get_list(html_text);
        except:
            print(f"  ![{self.host}]")
        return self.items;
    def get_list(self, html_text):
        index_area = re.findall(r'index-area clearfix([\s\S]*?)</div>', html_text)[0];
        results = re.findall(r'<li([\s\S]*?)</li>', index_area);
        info = [re.findall(r'link-hover[\'\"] href=[\'\"](.*?)[\'\"] title=[\'\"](.*?)[\'\"]', x)[0] for x in results];
        self.items = [{'self': self, 'title': x[1], 'url': self.host+x[0]} for x in info];
    class itempage(object):
        def __init__(self, item):
            self.info = item;
            self.title = self.info['title'];
            self.url = self.info['url'];
            self.m3u8info = [];
            videourl_list = re.findall(r'videourl clearfix[\'\"]([\s\S]*?)</div>', misc.r_get(self.url));
            self.links_info = [];
            for vlist in videourl_list:
                self.links_info.extend(re.findall(r'title=[\'\"](.*?)[\'\"][\s\S]*?href=[\'\"](.*?)[\'\"]', vlist));
            if(len(self.links_info) > 0):
                html_text = misc.r_get(self.links_info[0][1]);
                self.req = self.info['self'].host + re.findall(r'src="(/upload/playdata/\d+/\d+/\d+\.js)"', html_text)[0];
        def __str__(self, ):
            return self.title;
        def pull(self, ):
            js_text = misc.r_get(self.req);
            js_text = unquote(js_text);
            js_text = misc.unescape(js_text);
            m3u8_list = re.findall(r'mac_url=unescape\(\'(.*?)\'\)', js_text)[0].split('#');
            m3u8info = [(x.split('$')[0], x.split('$')[1]) for x in m3u8_list];
            self.m3u8info = [
                    {
                    **self.info,
                    'fname': misc.unescape(x[0])+".m3u8", 
                    'hls_url': x[1]
                }
                for x in m3u8info if misc.ism3u8(x[1])
            ];
            return True;

if(__name__ == '__main__'):
    x = cmdy();
    x.pull("1917");
    page = [x.itempage(item) for item in x.items];
    print(*page)
