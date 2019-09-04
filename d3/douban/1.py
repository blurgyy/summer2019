#!/usr/bin/python

import requests 
import json
import sys

# url = "https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=200&page_start=1"

# text = requests.get(url).text;
fname = "douban.json";
# with open(fname, 'w') as f:
#     f.write(text);
with open(fname) as f:
    text = f.read()

d = json.loads(text)['subjects'];

if(len(sys.argv) == 2):
    name = sys.argv[1];
else:
    while(True):
        name = input();
        if(len(name) > 0):
            break;

not_found = True;
for i in d:
    if(i['title'] == name):
        print(i['rate']);
        not_found = False;
if(not_found):
    print("not found");

