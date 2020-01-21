#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

from . import misc 
from .pm import parallel_manager 
import re 
from urllib.parse import quote, unquote 

class mjw(object):
    def __init__(self, ):
        self.host = "http://91mjw.com";
        self.search_host = self.host + "/?s=";
        self.items = [];
    def pull(self, search_term, ):
        self.st = search_term;
        self.url = self.search_host + quote(self.st);
        try:
            self.get_list();
        except:
            print(f"  ![{self.host}]");
        return self.items;
    def get_list(self, ):
        html_text = misc.r_get(self.url);
        try:
            content_block = re.findall(r'list-content([\s\S]*?)widget widget_hot', html_text)[0];
        except:
            content_block = html_text;
        results = re.findall(r'(<article class="u-movie">[\s\S]*?</article>)', content_block);
        # TODO: remove hot list from results
        info = [re.findall(r'" href="(.*?)"[\s\S].*?<h2>(.*?)</h2>', x)[0] for x in results];
        self.items = [{'self': self, 'title': x[1], 'url': x[0]} for x in info];
        # tv_list = json.loads(json_text);
        # self.items = [{'title': x['title'], 'url': x['url']} for x in tv_list];
    class itempage(object):
        def __init__(self, item):
            self.info = item;
            self.title = self.info['title'];
            self.url = self.info['url'];
            self.m3u8info = [];
            self.id = self.url.strip('/').split('/')[-1].split('.')[0];
            vlists_info = re.findall(r'<div id="video_list_li" class="video_list_li">([\s\S]*?)</div>', misc.r_get(self.url));
            self.links_info = [];
            for vlist in vlists_info:
                if("vlink" in vlist):
                    links_info = [(f"https://91mjw.com/vplay/{x[0]}.html", x[1])
                             for x in re.findall(r'<a.*?id="(.*?)">(.*?)</a>', vlist)];
                else:
                    links_info = [(f"https://91mjw.com/video/{self.id}.htm{x[0]}", x[1])
                             for x in re.findall(r'<a.*?href="(.*?)">(.*?)</a>', vlist)];
                self.links_info = [*self.links_info, *links_info];
        def __str__(self, ):
            return self.title;
        def pull(self, ):
            pm = parallel_manager();
            items = [];
            sz = 0;
            for x in self.links_info:
                x = (*x, sz)
                sz += 1;
                th = misc.myThread(target = lambda x : items.append((misc.r_get(x[0]), x[1], x[2])), args = (x, ));
                pm.append(th);
            pm.run();
            items.sort(key = lambda x : x[2]);
            m3u8info = [(unquote(re.findall(r'vid="(.*?\.m3u8)"', x[0])[0]), x[1])
                        for x in items];
            if(len(m3u8info) == 0):
                return False;
            self.m3u8info = [
                    {
                    **self.info,
                    'hls_url': x[0],
                    'fname': misc.unescape(x[1])+".m3u8"
                }
                for x in m3u8info if misc.ism3u8(x[0])
            ];
            return True;

if(__name__ == '__main__'):
    import misc 
    x = mjw();
    x.pull("神盾局");
    print(x.items);
