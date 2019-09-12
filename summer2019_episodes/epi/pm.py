#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .misc import myThread 
import time 

default_conf = {
	'max_threads': 4,
	'running': False,
	'running_threads': 0
}

class parallel_manager(object):
	def __init__(self, conf=default_conf):
		self.conf = conf;
		self.funx = [];
		self.sups = [];
	def append(self, th: myThread):
		self.funx.append(th);
	def supervisor(self, th, ):
		while(self.conf['running_threads'] > self.conf['max_threads']):
			time.sleep(0.1);
		th.start();
		self.conf['running_threads'] += 1;
		th.join();
		self.conf['running_threads'] -= 1;
	def run(self, ):
		self.conf['running'] = True;
		self.conf['running_threads'] = 0;
		for th in self.funx:
			sup = myThread(target = self.supervisor, args = (th, ));
			sup.start();
			self.sups.append(sup);
		for sup in self.sups:
			sup.join();
		self.conf['running'] = False;
