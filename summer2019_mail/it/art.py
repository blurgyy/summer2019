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
        html = requests.get(self.url).content.decode('utf-8', 'replace');
        self.title = re.findall(r'<div class=[\'\"]content-tit+le[\'\"]>[\s\S]*?h1>(.*?)<\/h1>', html)[0];
        self.header = re.findall(r'<div class=[\'\"]content-sign[\'\"]>([\s\S]*?<\/div>)', html)[0];
        self.body = re.findall(r'<div class=[\'\"]content-article[\'\"]>([\s\S]*?)<\/form>', html)[0];
        links = set(re.findall(r'\"(/_.*?)\"', self.body));
        for link in links:
            self.body = re.sub(link, misc.url_join(self.base_url, link), self.body);
        self.content = "<!DOCTYPE html>\n<html>\n<body>\n";
        self.content += self.header + self.body;
        self.content += """<hr>\n<a href="https://106.14.194.215/index/oucit">(un)?subscribe</a>\n""" + "<br>"*5;
        self.content += "</body>\n</html>";
