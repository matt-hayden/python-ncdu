#! /usr/bin/env python

import codecs

def parse_escape_sequences(*args, **kwargs):
	b, _ = codecs.escape_decode(bytes(*args, **kwargs))
	return b.decode('utf-8') # outgoing code
