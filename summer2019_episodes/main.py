#!/usr/bin/python3
# -*- coding: utf-8 -*-

import click 
import epi 
from urllib.parse import unquote 

@click.command()
@click.option("-s", type=str, default=None,
              help = "Specify search term")
@click.option("-m", type=int, default=None,
              help = "Sepcify selection")
@click.option("-w", type=str, default=None,
              help = "Output search list to file")
@click.option("--dump", type=str, default=None,
              help = "Dump client object into file (binary)")
@click.option("--load", type=click.Path(exists=True), default=None,
              help = "Load binary client object from file")
@click.argument("args", nargs=-1)
def main(s, m, w, dump, load, args):
    if(load):
        cli = epi.misc.load(load);
    else:
        cli = epi.client(search_term = unquote(s) if s != None else None, sel_id = m, slist_fname = w);
    if(dump):
        epi.misc.dump(dump, cli);
        return;
    cli.conf['sel_id'] = str(m) if(m != None) else None;
    cli.descend();

if(__name__ == "__main__"):
    main();

