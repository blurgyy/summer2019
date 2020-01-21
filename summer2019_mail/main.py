#!/usr/bin/python3
# -*- coding: utf-8 -*-

import it 
import time 
import requests 

def main():
    conf = it.config.load();
    spider = it.oucit(conf);
    mails = [];
    # it.clear_cache(conf);
    while(True):
        current_time = time.asctime(time.localtime(time.time()));
        try:
            urls = spider.check();
            arts = [it.article(url) for url in urls];
            updated = [it.mail(art) for art in arts];
            mails += updated;
            print(f"[{current_time}]: {len(updated)} update(s) posted, sending {len(mails)} item(s)");
            mails = [mail for mail in mails if(not mail.send(conf))];
        except requests.exceptions.ConnectionError as e:
            print(f"[{current_time}]: exception occurred (connection error), retrying in {conf['cycle']} second(s)");
        time.sleep(conf['cycle']);
        conf = it.config.load();
        spider.load(conf);

if(__name__ == "__main__"):
    main();

