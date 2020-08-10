#!/usr/bin/env -S python3 -u
# -*- coding: utf-8 -*-

import epi
from epi import misc
import sys
import os

# Global vars
if os.name == "posix":
    userhome = os.environ['HOME']
    cache_dir_base = os.path.join(userhome, ".cache/summer2019")
    dl_dest = os.path.join(userhome, "Downloads/summer2019")
else:
    cache_dir_base = os.path.join(".", "cache")
    dl_dest = os.path.join(".", "downloads")


def piece_name(index: int):
    return "{:09d}".format(index)


def check_finish(name: str, cnt: int):
    cache_dir = os.path.join(cache_dir_base, name)
    for i in range(cnt):
        if not os.path.exists(os.path.join(cache_dir, piece_name(i))):
            return False
    return True


def dl(url: str, name: str, index: int):
    content = misc.r_get(url, binary=True)
    cache_dir = os.path.join(cache_dir_base, name)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    with open(os.path.join(cache_dir, piece_name(index)), 'wb') as f:
        f.write(content)


def concatentate(name: str, cnt: int, key: bytes):
    if key:
        from Crypto.Cipher import AES
        cryptor = AES.new(key, AES.MODE_CBC, key)
    cache_dir = os.path.join(cache_dir_base, name)
    dest_fname = os.path.join(dl_dest, name + ".ts")
    with open(dest_fname, 'wb') as f:
        for i in range(cnt):
            with open(os.path.join(cache_dir, piece_name(i)), 'rb') as ff:
                if key:
                    f.write(cryptor.decrypt(ff.read()))
                else:
                    f.write(ff.read())


def parse(hlsdoc: str, name: str):
    srcs = []
    key = None
    for x in hlsdoc:
        if misc.ists(x) and misc.isurl(x):
            srcs.append(x.strip())
        if misc.iskey(x):
            key = misc.r_get(misc.findkey(x), binary=True)
    cache_dir = os.path.join(cache_dir_base, name)

    # Download pieces
    pm = epi.pm.parallel_manager(max_threads=6, retry=1)
    while not check_finish(name, len(srcs)):
        for i in range(len(srcs)):
            if not os.path.exists(os.path.join(cache_dir, piece_name(i))):
                th = misc.myThread(target=misc.function_wrapper,
                                   args=(dl, (srcs[i], name, i), pm))
                pm.append(th)
        pm.run(progress=True)

    # Concatenate, decrypt if necessary
    print("Concatenating ..")
    concatentate(name, len(srcs), key)
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

    print("""
Starting, cache directory is '{}'
destination directory is '{}'
""".format(cache_dir_base, dl_dest))

    for i in range(len(filelist)):
        x = filelist[i]
        print(f"Converting {x} ..")
        with open(x, 'r') as f:
            parse(f.readlines(), namelist[i])


if __name__ == '__main__':
    main()
