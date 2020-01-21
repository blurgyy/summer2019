#!/usr/bin/python3
# -*- coding: utf-8 -*-

from . import misc 
import os 
import re 
import warnings 

warnings.filterwarnings('ignore', r'.*?Unverified HTTPS request is being made.*?');

class m3u8(object):
    def __init__(self, info):
        self.info = info;
        self.url = self.info['hls_url'];
        self.epname = self.info['fname'][:-5];
    def __str__(self, ):
        ret = "";
        ret += self.doc + '\n[';
        if(not self.check()):
            ret += "un";
        ret += "playable hls document]\n"
        return ret;
    def pull(self, patience = True, ):
        try:
            if(patience):
                if(not hasattr(self, "doc") or not self.check()):
                    self.load();
                    self.unify();
                if(self.unique()):
                    if(self.check()):
                        self.save();
                        return True;
                    return False;
                else:
                    print(f" -- {self.savpath()} exists");
                    return True;
            else:
                if(not os.path.exists(self.savpath())):
                    if(not hasattr(self, "doc") or not self.check()):
                        self.load();
                        self.unify();
                    if(self.check()):
                        self.save();
                        return True;
                    return False;
                else:
                    print(f" -- {self.savpath()} exists");
                    return True;
        except Exception as e:
            print(e)
            return False;
    def unique(self, ):
        if(not os.path.exists(self.savpath())):
            return True;
        if(misc.read_file(self.savpath()) == self.doc):
            return False;
        self.info['idx'] = 1;
        while(os.path.exists(self.savpath())):
            if(misc.read_file(self.savpath()) == self.doc):
                return False;
            self.info['idx'] += 1;
        return True;
    def savpath(self, ):
        idx = self.info.get('idx', 0);
        if(idx > 0):
            self.info['fname'] = f"{self.epname}({idx}).m3u8";
        return os.path.join(self.info['title'], self.info['fname']);
    def load(self, ):
        if(self.url):
            self.doc = misc.r_get(self.url, verify=False);
            if(not self.check()):
                self.host = misc.splithost(self.url);
        else:
            print("hls: no source specified");
        self.doc = self.doc.strip(' \n');
    def save(self, ):
        savdir = self.info['title'];
        if(not os.path.exists(savdir)):
            os.makedirs(savdir);
        misc.write(self.savpath(), self.doc);
        print(f" -- {self.savpath()}");
        return True;
    def check(self, ):
        for line in self.doc.splitlines():
            if(re.match(r'^#.*$', line) or re.match(r'^https?.*$', line) and re.match(r'^.*?\.ts$', line)):
                continue;
            return False;
        return True;
    def unify(self, ):
        if(self.check()):
            return;
        lines = self.doc.splitlines();
        if(not misc.ists(lines[-1])):
            if(lines[-1][0] == '/'):
                self.url = misc.urljoin(self.host, lines[-1]);
            else:
                self.url = self.url.replace(self.url.split('/')[-1], lines[-1]);
            self.load();
        lines = self.doc.splitlines();
        doc = "";
        for line in lines:
            if(not misc.isurl(line) and misc.ists(line)):
                if(line[0] == '/'):
                    line = self.host + line;
                else:
                    line = self.url.replace(self.url.split('/')[-1], line);
            doc += line + '\n';
        self.doc = doc;

