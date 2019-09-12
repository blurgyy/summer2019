#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .pm import parallel_manager as pm 
from .fjisu import fjisu 
from . import hls 
from .itempage import page 
from . import misc 
import os 
import time 

class client(object):
    def __init__(self, **kwargs):
        self.conf = kwargs;
        self.hosts = [fjisu()];
        self.search_term = self.conf['search_term'] \
                           if ('search_term' in self.conf and type(self.conf['search_term']) == str) \
                           else misc.read("Input search term> ");
        self.pull();
    def __str__(self, indent = 4, showid = True):
        ret = "";
        for i in range(len(self.pages)):
            ret += ' ' * indent;
            if(showid):
                ret += f"{i+1}. "; 
            ret += f"{self.pages[i].title}\n";
        return ret;
    def __len__(self, ):
        return len(self.pages);
    def pull(self, ):
        for host in self.hosts:
            host.pull(self.search_term);
        self.pages = [page(item) for item in host.items for host in self.hosts];
    def dumps(self, ):
        if(self.conf['slist_fname']):
            misc.write(self.conf['slist_fname'], self.__str__(indent=0, showid=False).replace('\t', ''));
    def select(self, ):
        sel = self.conf['sel_id'] \
              if('sel_id' in self.conf and type(self.conf['sel_id']) == str) \
              else misc.read("Select by id> ", r'^([\d ]+|\*|!)$');
        if(sel == '!'):
            print("Signal captured, abort");
            return [];
        elif(sel == '*'):
            sel = [i for i in range(1, len(self)+1)];
        else:
            sel = [int(x) for x in sel.split(' ') if(len(x) > 0 and int(x) in range(1, len(self)+1))];
        return sel;
    def descend(self, ):
        print(f"Search results ({len(self)})\n" + str(self));
        sel = self.select();
        self.pages = [self.pages[i-1] for i in sel if self.pages[i-1].pull()];
        if(len(self) == 0):
            return;
        print(f"Selected ({len(self)})\n" + str(self));
        self.m3u8s = [hls.m3u8(info) for page in self.pages for info in page.m3u8info];
        self.dm = pm();
        for m3u8 in self.m3u8s:
            th = misc.myThread(target = m3u8.pull, args = ());
            self.dm.append(th);
        self.dm.run();
        self.order_mtime();
    def order_mtime(self, ):
        for m3u8 in self.m3u8s:
            if(os.path.exists(m3u8.info['fname'])):
                os.utime(m3u8.info['fname']);
                time.sleep(0.05);

if(__name__ == "__main__"):
    x = client(search_term = "rick and morty");
    x.pull();
    print(x)
    for page in x.pages:
        print(page);
        page.pull();

    # print(x.pages[0].m3u8s[0])
