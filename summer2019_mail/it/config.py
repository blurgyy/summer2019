#!/usr/bin/python3
# -*- coding: utf-8 -*-

from getpass import getpass
import os
from os import environ as env
import re
import json


def read_check(s, pat='', return_type=str, hidden=False):
    while (True):
        if (hidden):
            ret = getpass(s)
        else:
            ret = input(s).strip()
        if (len(ret) > 0 and re.match(pat, ret)):
            return return_type(ret)
        else:
            s = "Invalid format, reenter> "


def load():
    if (os.name == "posix"):
        conf_dir = os.path.join(env["HOME"], ".config")
    else:
        conf_dir = os.path.join(os.getcwd(), ".config")
    conf_fname = os.path.join(conf_dir, "summer2019_mail.json")
    if (os.path.exists(conf_fname)):
        with open(conf_fname) as f:
            config = json.load(f)
        config['cycle'] = max(config['cycle'], 300)
        config['cycle'] = min(config['cycle'], 86400)
        config['to'] = [x.lower() for x in list(set(config['to']))]
        with open(conf_fname, 'w') as f:
            json.dump(config, f, indent=4)
        # print(f"loaded configuration from {conf_fname}");
    else:
        config = {}
        config['coding'] = 'utf-8'
        # config['cache_dir'] = os.path.join(env["HOME"], ".cache", "blurgy", "summer2019_mail");
        if (os.name == "posix"):
            config['cache_dir'] = os.path.join(env["HOME"], ".cache",
                                               "summer2019_mail")
        else:
            config['cache_dir'] = os.path.join(os.getcwd(), ".cache",
                                               "summer2019_mail")
        config['checking_list'] = {
            "news": True,
            "notice": True,
            "activity": True
        }
        config['from'] = read_check("Sending emails from this EMAIL ADDRESS> ",
                                    r'\w+@\w+(\.\w+)')
        config['host'] = "smtp." + re.findall(r'@(.*?)\.',
                                              config['from'])[0] + ".com"
        config['content_type'] = "html"
        config['auth'] = read_check("AUTH> ", hidden=True)
        config['from_display'] = read_check(
            "Receivers will see this NAME displayed as `sender`> ")
        to_fname = read_check("This FILE contains a mailing list> ")
        if (not os.path.exists(conf_dir)):
            os.makedirs(conf_dir)
        with open(to_fname) as f:
            lines = f.readlines()
            config['to'] = [
                x.lower() for x in list(
                    set([
                        x.strip(' \n') for x in lines
                        if (len(x.strip(' \n')) > 0)
                    ]))
            ]
        config['to_display'] = read_check(
            "Receivers will see this NAME displayed as `receiver`> ")
        config['cycle'] = read_check(
            "Script will check updates every ____ seconds> ", r'\d+', int)
        config['cycle'] = max(config['cycle'], 300)
        config['cycle'] = min(config['cycle'], 86400)
        with open(conf_fname, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"configuration saved to {conf_fname}")
    return config
    # print(config);


def renew(key, val):
    if (os.name == "posix"):
        conf_dir = os.path.join(env["HOME"], ".config")
    else:
        conf_dir = os.path.join(os.getcwd(), ".config")
    conf_fname = os.path.join(conf_dir, "summer2019_mail.json")
    config = load()
    config[key] = val
    with open(conf_fname, 'w') as f:
        json.dump(config, f, indent=4)


def delete():
    if (os.name == "posix"):
        conf_dir = os.path.join(env["HOME"], ".config")
    else:
        conf_dir = os.path.join(os.getcwd(), ".config")
    conf_fname = os.path.join(conf_dir, "summer2019_mail.json")
    if (os.path.exists(conf_fname)):
        os.remove(conf_fname)
        print(f"removed {conf_fname}")
    else:
        print("no configuration file found")


if (__name__ == "__main__"):
    delete()
    # print(load());
    pass
