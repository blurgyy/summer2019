#!/usr/bin/env -S python3 -u
# -*- coding: utf-8 -*-

import epi
from epi import misc
import sys
import os

# Global vars
userhome = os.environ['HOME']
cache_dir_base = os.path.join(userhome, ".cache/summer2019")
dl_dest = os.path.join(userhome, "Downloads/summer2019")


def dl(url: str, name: str, index: int):
    content = misc.r_get(url, binary=True)
    cache_dir = os.path.join(cache_dir_base, name)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    with open(os.path.join(cache_dir, "{:09d}".format(index)), 'wb') as f:
        f.write(content)


def parse(hlsdoc: str, name: str):
    srcs = [x.strip() for x in hlsdoc if misc.ists(x) and misc.isurl(x)]
    cache_dir = os.path.join(cache_dir_base, name)
    pm = epi.pm.parallel_manager(max_threads=6, retry=1)
    for i in range(len(srcs)):
        th = misc.myThread(target=misc.function_wrapper,
                           args=(dl, (srcs[i], name, i), pm))
        pm.append(th)
    pm.run(progress=True)
    print("Concatenating ..")
    with open(os.path.join(dl_dest, name + ".ts"), 'wb') as f:
        for i in range(len(srcs)):
            with open(os.path.join(cache_dir, "{:09d}".format(i)), 'rb') as ff:
                f.write(ff.read())
    print("Done")


def main():
    if len(sys.argv) == 1:
        print("No argument given")
        return

    filelist = [x for x in sys.argv[1:] if os.path.exists(x)]
    namelist = [x.split('/')[-1].split('.')[0] for x in filelist]

    if not os.path.exists(cache_dir_base):
        os.makedirs(cache_dir_base)
    if not os.path.exists(dl_dest):
        os.makedirs(dl_dest)

    for i in range(len(filelist)):
        x = filelist[i]
        print(f"Converting {x} ..")
        with open(x, 'r') as f:
            parse(f.readlines(), namelist[i])


if __name__ == '__main__':
    main()
