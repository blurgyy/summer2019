#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os 
from os import environ as env 
import re 
import json 

def read_check(s, pat = '', return_type = str):
    while(True):
        ret = input(s).strip();
        if(len(ret) > 0 and re.match(pat, ret)):
            return return_type(ret);
        else:
            s = "Invalid format, reenter> ";

def load():
    conf_dir = os.path.join(env["HOME"], ".config");
    conf_fname = os.path.join(conf_dir, "summer2019_mail.json");
    if(os.path.exists(conf_fname)):
        with open(conf_fname) as f:
            config = json.load(f);
        print(f"loaded config from {conf_fname}");
    else:
        config = {};
        config['coding'] = 'utf-8';
        # config['cache_dir'] = os.path.join(env["HOME"], ".cache", "blurgy", "summer2019_mail");
        config['cache_dir'] = os.path.join(env["HOME"], ".cache", "summer2019_mail");
        config['checking_list'] = {
            "news": True, 
            "notice": True, 
            "activity": True
        }
        config['from'] = read_check("Sending emails from this EMAIL ADDRESS> ", r'\w+@\w+\.\w+');
        config['host'] = "smtp." + re.findall(r'@(.*?)\.', config['from'])[0] + ".com";
        config['content_type'] = "html";
        config['auth'] = read_check("AUTH> ");
        config['from_display'] = read_check("Receivers will see this NAME displayed as `sender`> ");
        to_fname = read_check("This FILE contains a mailing list> ");
        if(not os.path.exists(conf_dir)):
            os.makedirs(conf_dir);
        with open(to_fname) as f:
            lines = f.readlines();
            config['to'] = [x.strip(' \n') for x in lines if(len(x.strip(' \n')) > 0)];
        config['to_display'] = read_check("Receivers will see this NAME displayed as `receiver`> ")
        config['cycle'] = max(300, read_check("Script will check updates every ____ seconds> ", r'\d+', int));
        with open(conf_fname, 'w') as f:
            json.dump(config, f, indent=4);
        print(f"config saved to {conf_fname}");
    return config;
    # print(config);

def delete():
    conf_dir = os.path.join(env["HOME"], ".config");
    conf_fname = os.path.join(conf_dir, "summer2019_mail.json");
    if(os.path.exists(conf_fname)):
        os.remove(conf_fname);
        print(f"removed {conf_fname}");
    else:
        print("no configuration file found")

if(__name__ == "__main__"):
    delete()
    # print(load());
    pass;

