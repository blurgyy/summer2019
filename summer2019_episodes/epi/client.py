#!/usr/bin/python3
# -*- coding: utf-8 -*-

from fjisu import fjisu 
from itempage import page 
from subitempage import subpage 
import misc 

class client(object):
    """
    - attributes:
        hosts: list
        search_term: str
    - methods:
        __init__()
        pull()
    """
    def __init__(self, **kwargs):
        self.hosts = [fjisu()];
        self.search_term = kwargs['search_term'] \
                           if ('search_term' in kwargs and type(kwargs['search_term']) == str)\
                           else misc.read("Input search term> ");
        self.pull();
    def pull(self, ):
        for host in self.hosts:
            host.pull(self.search_term);
        self.pages = [page(item) for item in host.items for host in self.hosts];

if(__name__ == "__main__"):
    x = client(search_term = "rick and morty");
    x.pull();
    print(x.pages[0])
    x.pages[0].descend();
    x.pages[0].m3u8s[0].pull()
    # print(x.pages[0].m3u8s[0])
