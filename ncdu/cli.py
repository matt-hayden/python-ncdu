#! /usr/bin/env python

import ncdu
from ncdu.util import *

import codecs
import os, os.path
import sys

def printf_cli(*args):
	if not args:
		args = sys.argv[1:]
	ncdu_file, printf_spec = args
	n = ncdu.load(ncdu_file)
	spec = parse_escape_sequences(printf_spec, 'utf-8') # incoming code
	print( ''.join(n.tree.printf(spec)) )
#
if __name__ == '__main__':
	if __debug__:
		import cProfile
		cProfile.run('printf_cli()')
	else:
		printf_cli()
