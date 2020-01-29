#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .misc import myThread 
import time 
import threading 
from multiprocessing import cpu_count 

default_conf = {
    'max_threads': cpu_count() * 3 + 1
}

class parallel_manager(object):
    def __init__(self, **kwargs):
        self.conf = default_conf;
        self.conf = {**self.conf, **kwargs};
        self.funx = [];
        # self.sups = [];
        self.threads = [];
        self.semaphore = threading.BoundedSemaphore(self.conf['max_threads']);
    def append(self, th: myThread):
        self.funx.append(th);
    def run(self, ):
        while(len(self.funx) > 0):
            self.semaphore.acquire();
            th = self.funx.pop();
            th.start();
            self.threads.append(th);
        for th in self.threads:
            th.join();
