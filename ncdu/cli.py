#! /usr/bin/env python

from reader import NcduReader as read
from util import *

import codecs
import json
import os, os.path
import sys

def printf_cli(*args):
	if not args:
		args = sys.argv[1:]
	ncdu_file, printf_spec = args
	with open(ncdu_file) as fi:
		n = read(json.load(fi))
	spec = parse_escape_sequences(printf_spec, 'utf-8') # incoming code
	print( ''.join(n.tree.printf(spec)) )
#
if __name__ == '__main__':
	printf_cli()
