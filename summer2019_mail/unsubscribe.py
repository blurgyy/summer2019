#!/usr/bin/python3
# -*- coding: utf-8 -*-

import click 
import it 
import re 

@click.command()
@click.argument("mail-addr", type=str, default=None)
@click.argument("args", nargs=-1)
def main(mail_addr):
	if(not re.match(r'\w+@\w+(\.\w+)+', mail_addr)):
		return;
	conf = it.config.load();
	conf['to'] = list(set(conf['to']));
	if(mail_addr in conf['to']):
		conf['to'].remove(mail_addr);
	it.config.renew('to', conf['to']);

if(__name__ == '__main__'):
	main();
