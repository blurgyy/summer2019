#!/usr/bin/python3
# -*- coding: utf-8 -*-

from . import misc 
import re 
import requests 

class article:
    def __init__(self, _url, ):
        self.base_url = "http://it.ouc.edu.cn";
        self.url = _url;
    def __str__(self, ):
        return self.title;
    def parse(self, ):
        html = requests.get(self.url).content.decode('utf-8');
        self.title = re.findall(r'<div class=[\'\"]content-tit+le[\'\"]>[\s\S]*?h1>(.*?)<\/h1>', html)[0];
        self.header = re.findall(r'<div class=[\'\"]content-sign[\'\"]>([\s\S]*?<\/div>)', html)[0];
        self.body = re.findall(r'<div class=[\'\"]content-article[\'\"]>([\s\S]*?)<\/form>', html)[0];
        img_urls = re.findall(r'.*?src=\"(.*?)\"', self.body);
        for img_url in img_urls:
            self.body = re.sub(img_url, misc.url_join(self.base_url, img_url), self.body);
        self.content = self.header + self.body;
        self.content += """<hr><a href="https://106.14.194.215/oucit">(un)*subscribe</a>""";
