#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .hls import m3u8 
from . import misc 
from .pm import parallel_manager 
import re 
from urllib.parse import quote, unquote 

class page(object):
    def __init__(self, item):
        self.info = item;
        self.title = self.info['title'];
        self.url = self.info['url'];
        if("fjisu" in misc.splithost(self.url)):
            self.id = self.url.strip('/').split('/')[-1];
            self.reqs = [
                f"http://t.mtyee.com/ps/s{self.id}.js",
                f"http://t.mtyee.com/ty/yj/s{self.id}.js",
                f"http://t.mtyee.com/ty/zd/s{self.id}.js"
            ];
        elif("91mjw" in misc.splithost(self.url)):
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
        elif("kukanwu" in misc.splithost(self.url)):
            self.id = self.url.strip('/').split('/')[-1];
            self.reqs = [
                f"http://t.mtyee.com/ps/s{self.id}.js",
                f"http://t.mtyee.com/ty/yj/s{self.id}.js",
                f"http://t.mtyee.com/ty/zd/s{self.id}.js"
            ];
    def __str__(self, ):
        return self.title;
    def pull(self, ):
        if("fjisu" in misc.splithost(self.url)):
            self.pull_fjisu();
        elif("91mjw" in misc.splithost(self.url)):
            self.pull_91mjw();
        elif("kukanwu" in misc.splithost(self.url)):
            self.pull_kk();
        return True;
    def pull_fjisu(self, ):
        cont = "";
        for req in self.reqs:
            cont += misc.r_get(req);
        m3u8info = re.findall(r'"(https?.*?),(.*?),(.*?)"', cont);
        if(len(m3u8info) == 0):
            return False;
        self.m3u8info = [
                {
                **self.info,
                'hls_url': x[0], 
                'nonsense': x[1], 
                'fname': self.info['title']+'/'+misc.unescape(x[2])+".m3u8"
            }
            for x in m3u8info if misc.ism3u8(x[0])
        ];
    def pull_91mjw(self, ):
        pm = parallel_manager(max_threads = 8);
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
        self.m3u8info = [
                {
                **self.info,
                'hls_url': x[0],
                'fname': self.info['title']+'/'+misc.unescape(x[1])+".m3u8"
            }
            for x in m3u8info if misc.ism3u8(x[0])
        ];
    def pull_kk(self, ):
        link_list = re.findall(r'<ul class="urlli">[\s\S]*?</ul', misc.r_get(self.url))[0];
        links = [misc.splithost(self.url) + x for x in re.findall(r'<a href="(.*?)">', link_list)];
        self.reqs.extend([x for link in links for x in re.findall(r'(http://t\.mtyee\.com/ps/.*?\.js)', misc.r_get(link))]);
        self.reqs = list(set(self.reqs));
        self.pull_fjisu();


if(__name__ == '__main__'):
    item = {
        'title': "shd",
        'url': "https://91mjw.com/video/183.htm"
    }
    x = page(item);
    x.pull();
    print(x.m3u8info);
