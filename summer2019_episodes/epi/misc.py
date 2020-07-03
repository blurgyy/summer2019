#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pickle
import random
import re
import requests
import socket
import struct
import threading


class myThread(threading.Thread):
    def __init__(
            self,
            target,
            args=(),
    ):
        super(myThread, self).__init__()
        self.func = target
        self.args = args

    def run(self, ):
        try:
            self.result = self.func(*self.args)
        except requests.ConnectionError as e:
            print("{} when executing function {} with args{}".format(
                e, self.func.__name__(), self.args))
        except requests.exceptions.ReadTimeout as e:
            print("{} when executing function {} with args{}".format(
                e, self.func.__name__(), self.args))

    def fetch_result(self, ):
        threading.Thread.join(self)
        return self.result


def function_wrapper(func, args, pmobject):
    ret = func(*args)
    pmobject.semaphore.release()
    return ret


def create_headers():
    ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    req_headers = {
        'CLIENT-IP':
        ip,
        'User-Agent':
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    return req_headers


def iskey(s: str):
    #EXT-X-KEY:METHOD=AES-128,URI="key.key"
    return not not re.match(r'^#EXT-X-KEY.*$', s.strip())


def findkey(s: str):
    if (not iskey(s)):
        return ""
    return re.findall(r'URI.*[\'"](.*)[\'"]$', s.strip())[0]


def iscomment(s: str):
    return not not re.match(r'^#.*?$', s.strip())


def ism3u8(s: str):
    return not not re.match(r'^.*?\.m3u8$', s.strip())


def ists(s: str):
    return not not re.match(r'^.*?\.ts(\?.*?)?$', s.strip())


def isurl(s: str):
    return not not re.match(r'^https?://.*?$', s.strip())


def read(s="", pat=r''):
    ret = ""
    while (len(ret) == 0 or not re.match(pat, ret)):
        ret = input(s).strip(' \n')
    return ret


def r_get(url,
          headers=create_headers(),
          binary=False,
          encoding='utf-8',
          timeout=9.9,
          **kwargs):
    if binary:
        ret = requests.get(url, headers=headers, timeout=timeout,
                           **kwargs).content
    else:
        ret = requests.get(url, headers=headers, timeout=timeout,
                           **kwargs).content.decode(encoding)
    return ret


def r_post(url,
           data=None,
           binary=False,
           headers=create_headers(),
           encoding='utf-8',
           timeout=9.9,
           **kwargs):
    if binary:
        ret = requests.post(url,
                            data=data,
                            headers=headers,
                            timeout=timeout,
                            **kwargs).content
    else:
        ret = requests.post(url,
                            data=data,
                            headers=headers,
                            timeout=timeout,
                            **kwargs).content.decode(encoding)
    return ret


def splithost(url):
    return re.findall(r'(https?://.*?)/.*?', url)[0]


def urljoin(host, loc):
    return host + loc


def unescape(s):
    ret = s.replace('%', '\\')
    ret = ret.encode('latin-1',
                     errors='ignore').decode('unicode-escape',
                                             errors='ignore').strip(" \n")
    return ret


def write(fname, text):
    with open(fname, 'w') as f:
        f.write(text)


def load(fname):
    with open(fname, 'rb') as f:
        return pickle.load(f)


def dump(fname, obj):
    with open(fname, 'wb') as f:
        pickle.dump(obj, f)


def read_file(fname):
    with open(fname, 'r') as f:
        return f.read()
