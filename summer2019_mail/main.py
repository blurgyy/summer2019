#!/usr/bin/python3
# -*- coding: utf-8 -*-

import it 
import time 

def main():
    conf = it.config.load();
    spider = it.oucit(conf);
    mails = [];
    it.clear_cache(conf);
    while(True):
        urls = spider.check();
        arts = [it.article(url) for url in urls];
        updated = [it.mail(art) for art in arts];
        mails += updated;
        current_time = time.asctime(time.localtime(time.time()));
        print(f"[{current_time}]: {len(updated)} update(s) posted, sending {len(mails)} item(s)");
        mails = [mail for mail in mails if(not mail.send(conf))];
        print();
        time.sleep(conf['cycle']);
        conf = it.config.load();

if(__name__ == "__main__"):
    main();

