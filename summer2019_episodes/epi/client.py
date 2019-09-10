#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .fjisu import fjisu 
from . import hls 
from .itempage import page 
from . import misc 

class client(object):
    """
    - attributes:
        hosts: list
        search_term: str
        pages: page
    - methods:
        __init__()
        pull()
        select()
    """
    def __init__(self, **kwargs):
        self.hosts = [fjisu()];
        self.search_term = kwargs['search_term'] \
                           if ('search_term' in kwargs and type(kwargs['search_term']) == str)\
                           else misc.read("Input search term> ");
        self.pull();
    def __str__(self, ):
        ret = "Search results(%d): \n" % (len(self.pages));
        for i in range(len(self.pages)):
            ret += f"\t{i+1}. {self.pages[i].title}\n";
        return ret;
    def __len__(self, ):
        return len(self.pages);
    def pull(self, ):
        for host in self.hosts:
            host.pull(self.search_term);
        self.pages = [page(item) for item in host.items for host in self.hosts];
    def select(self, **kwargs):
        sel = kwargs['sel'] \
              if('sel' in kwargs and type(kwargs['sel']) == str) \
              else misc.read("Select by id> ", r'([\d ]+|\*|!)');
        if(sel == '!'):
            print("Signal captured, abort");
            return [];
        elif(sel == '*'):
            sel = [i for i in range(1, len(self)+1)];
        else:
            sel = [int(x) for x in sel.split(' ') if(len(x) > 0 and int(x) in range(1, len(self)+1))];
        return sel;
    def descend(self, **kwargs):
        print(self);
        sel = self.select(**kwargs);
        self.pages = [self.pages[i-1] for i in sel if self.pages[i-1].pull()];
        self.m3u8s = [hls.m3u8(info) for page in self.pages for info in page.m3u8info];
        for m3u8 in self.m3u8s:
            # print(m3u8.url);
            m3u8.save();

if(__name__ == "__main__"):
    x = client(search_term = "rick and morty");
    x.pull();
    print(x)
    for page in x.pages:
        print(page);
        page.pull();

    # print(x.pages[0].m3u8s[0])
