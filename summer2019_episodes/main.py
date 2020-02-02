#!/usr/bin/python3
# -*- coding: utf-8 -*-

import click 
from urllib.parse import unquote 
import os 
import epi 

@click.command()
@click.option("-s", type=str, default=None,
              help = "Specify search term")
@click.option("-m", type=str, default=None,
              help = "Sepcify selection")
@click.option("-w", type=str, default=None,
              help = "Output search list to file")
@click.option("-n", "--no-patience", is_flag = True, 
              help = "Deactivate -n flag (default) to prevent overwriting files which should not have been overwritten (possibly slower due to more network usage)")
@click.option("--dump", type=str, default=None,
              help = "Dump client object into file (binary)")
@click.option("--load", type=click.Path(exists=True), default=None,
              help = "Load binary file as client object")
@click.option("--save-path", type=click.Path(exists=True), default=".", 
              help = "Set save path")
@click.argument("args", nargs=-1)
def main(s, m, w, no_patience, dump, load, save_path, args):
    if(load):
        cli = epi.misc.load(load);
    else:
        cli = epi.client(search_term = unquote(s) if s != None else None, 
                         patience = not no_patience, 
                         sel_id = m, slist_fname = w);
    if(dump):
        epi.misc.dump(dump, cli);
        cli.dumps();
        return;
    # assuming `m` is not empty
    cli.conf['sel_id'] = m if m != None else None;
    os.chdir(save_path);
    cli.descend();

if(__name__ == "__main__"):
    main();

