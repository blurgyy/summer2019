#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import shutil

serverip = "47.101.132.200"


def url_join(host, loc):
    return host + loc


def clear_cache(config):
    if (os.path.exists(config['cache_dir'])):
        shutil.rmtree(config['cache_dir'])
