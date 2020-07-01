#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .misc import myThread
import time
import threading
from multiprocessing import cpu_count

default_conf = {'max_threads': 13, 'retry': 1}


class parallel_manager(object):
    def __init__(self, **kwargs):
        self.conf = default_conf
        self.conf = {**self.conf, **kwargs}
        self.funx = []
        # self.sups = [];
        self.threads = []
        self.semaphore = threading.BoundedSemaphore(self.conf['max_threads'])

    def append(self, th: myThread):
        self.funx.append(th)

    def run(self, ):
        while (len(self.funx) > 0):
            self.semaphore.acquire()
            th = self.funx.pop()
            th.start()
            self.threads.append(th)
        for th in self.threads:
            th.join()

    def run_with_retry(self, ):
        self.conf['retry'] = self.conf.get('retry', 1)
        for retry in range(0, self.conf['retry'] + 1):
            if (retry):
                print(f"\n Retrying on attempt [ {retry} ] ..")
            while (len(self.funx) > 0):
                self.semaphore.acquire()
                th = self.funx.pop()
                th.start()
                self.threads.append(th)
            for th in self.threads:
                th.join()
                if (th.fetch_result() == True):
                    continue
                retry_th = myThread(target=th.func, args=th.args)
                self.funx.append(retry_th)
            if (len(self.funx) == 0):
                break
