#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import json 
from . import misc 
import os 
from os import environ as env 
import re 
import requests 
import shutil 

class oucit:
    def __init__(self, config, ):
        self.base_url = "http://it.ouc.edu.cn";
        self.load(config);
        self.default_refresh_count = 1;
    def load(self, config, ):
        self.cache_dir = config['cache_dir'];
        self.checking_list = config['checking_list'];
    def parse(self, ):
        html = requests.get(self.base_url).text;
        if(self.checking_list['news']):
            news = re.findall(r'(<div id="wp_news_w8">[\s\S]*?</div>)', html)[0];
            news = re.findall(r'<a href=[\'\"](.*?)[\'\"] target=[\'\"]_blank[\'\"] title=[\'\"].+[\'\"]>.*?<\/a>', news);
            self.news = [misc.url_join(self.base_url, x) for x in news];
            assert len(self.news) == len(list(set(self.news))), "at least 1 news article duplicated"
        if(self.checking_list['notice']):
            notice = re.findall(r'(<div id="wp_news_w12">[\s\S]*?</div>)', html)[0];
            notice = re.findall(r'<a href=[\'\"](.*?)[\'\"] target=[\'\"]_blank[\'\"] title=[\'\"].+[\'\"]>.*?<\/a>', notice);
            self.notice = [misc.url_join(self.base_url, x) for x in notice];
            assert len(self.notice) == len(list(set(self.notice))), "at least 1 notice article duplicated"
        if(self.checking_list['activity']):
            activity = re.findall(r'(<div id="wp_news_w14">[\s\S]*?</div>)', html)[0];
            activity = re.findall(r'<a href=[\'\"](.*?)[\'\"] target=[\'\"]_blank[\'\"] title=[\'\"].+[\'\"]>.*?<\/a>', activity);
            self.activity = [misc.url_join(self.base_url, x) for x in activity];
            assert len(self.activity) == len(list(set(self.activity))), "at least 1 activity article duplicated"
    def check(self, ):
        self.parse();
        ret = [];
        if(self.checking_list['news']):
            fname = os.path.join(self.cache_dir, "news.json");
            if(not os.path.exists(self.cache_dir)):
                os.makedirs(self.cache_dir);
            if(os.path.exists(fname)):
                with open(fname) as f:
                    cached = json.load(f);
                ret += [x for x in self.news if(not x in cached)];
            else:
                ret += [self.news[i] for i in range(self.default_refresh_count)];
            with open(fname, 'w') as f:
                json.dump(self.news, f, indent=4);
        if(self.checking_list['notice']):
            fname = os.path.join(self.cache_dir, "notice.json");
            if(not os.path.exists(self.cache_dir)):
                os.makedirs(self.cache_dir);
            if(os.path.exists(fname)):
                with open(fname) as f:
                    cached = json.load(f);
                ret += [x for x in self.notice if(not x in cached)];
            else:
                ret += [self.notice[i] for i in range(self.default_refresh_count)];
            with open(fname, 'w') as f:
                json.dump(self.notice, f, indent=4);
        if(self.checking_list['activity']):
            fname = os.path.join(self.cache_dir, "activity.json");
            if(not os.path.exists(self.cache_dir)):
                os.makedirs(self.cache_dir);
            if(os.path.exists(fname)):
                with open(fname) as f:
                    cached = json.load(f);
                ret += [x for x in self.activity if(not x in cached)];
            else:
                ret += [self.activity[i] for i in range(self.default_refresh_count)];
            with open(fname, 'w') as f:
                json.dump(self.activity, f, indent=4);
        return ret;

if(__name__ == "__main__"):
    from . import config 
    conf = config.load();
    # print(conf['host'])
    x = oucit(conf);
    x.clear_cache();
    x.parse();
    print(x.check());
