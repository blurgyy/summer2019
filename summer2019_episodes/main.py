#!/usr/bin/python3
# -*- coding: utf-8 -*-

import click 
import epi 

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
def main(s, m, w, dump, load):
    if(load):
        cli = misc.load(load);
    else:
        cli = epi.client(search_term = s, sel_id = m, slist_fname = w);
    cli.descend();
    if(dump):
        misc.dump(dump, cli);

if(__name__ == "__main__"):
    main();

