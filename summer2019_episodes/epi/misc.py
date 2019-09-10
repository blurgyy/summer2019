#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random 
import re 
import requests 
import socket 
import struct 

def create_headers():
    ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)));
    req_headers = {
        # 'Origin': "http://www.fjisu.tv",
        'CLIENT-IP': ip,
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }

def iscomment(s):
    return not not re.match(r'^#.*?$', s);
def ism3u8(s):
    return not not re.match(r'^.*?\.m3u8$', s);
def ists(s):
    return not not re.match(r'^.*?\.ts$', s);
def isurl(s):
    return not not re.match(r'^https?://.*?$', s);

def read(s = "", pat = r''):
    ret = "";
    while(len(ret) == 0 or not re.match(pat, ret)):
        ret = input(s).strip(' \n');
    return ret;

def r_get(url, headers = create_headers(), encoding = 'utf-8', **kwargs):
    ret =  requests.get(url, headers = headers, **kwargs).content.decode(encoding);
    return ret;

def splithost(url):
    return re.findall(r'https?://(.*?)/.*?', url)[0];

def urljoin(host, loc):
    return host + loc;

def unescape(s):
    ret = s.replace('%', '\\');
    ret = ret.encode('latin-1').decode('unicode-escape').strip(" \n");
    return ret; 

def write(fname, text):
    with open(fname, 'w') as f:
        f.write(text);
