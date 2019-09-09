#!/usr/bin/python3
# -*- coding = utf-8 -*-

import smtplib 
from email.mime.text import MIMEText 
import time 

class mail:
    def __init__(self, _art, ):
        self.art = _art;
        self.art.parse();
    def send(self, config, ):
        try:
            if(not hasattr(self.art, "content")):
                self.art.parse();
            smtp = smtplib.SMTP_SSL(config['host']);
            # smtp.set_debuglevel(1);
            smtp.login(config['from'], config['auth']);
            mail = MIMEText(self.art.content, config['content_type'], config['coding']);
            mail['subject'] = self.art.title;
            mail['From'] = config['from_display'];
            mail['To'] = config['to_display'];
            # smtp.sendmail(config['from'], config['to'], mail.as_string());
            for i in range(0, len(config['to']), 5):
                smtp.sendmail(config['from'], config['to'][i: i+5], mail.as_string());
                time.sleep(5);
            smtp.quit();
            print(f">>> {self.art}");
            return True;
        except Exception as e:
            print(e);
            return False;

if(__name__ == "__main__"):
    from . import art 
    from . import config 
    from . import oucit 
    conf = config.load();
    it = oucit.oucit(conf);
    it.parse();
    it.clear_cache();
    urls = it.update();
    arts = [art.article(x) for x in urls];
    mails = [mail(x) for x in arts];
    for x in mails:
        x.send(conf);
