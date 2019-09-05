#!/usr/bin/python3
#-*- coding: utf--8 -*-

from pymongo import MongoClient 
import json 

db = MongoClient()['test']['douban'];

# fname = "douban.json";
# with open(fname) as f:
# 	info = json.loads(f.read())['subjects'];

# for item in info:
# 	db.insert_one(item)

while(True):
	name = input();
	if(len(name)):
		break;
x = db.find({'title': name});
print(x[0]['rate'])

