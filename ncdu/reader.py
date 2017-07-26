#! /usr/bin/env python
import os, os.path
import shlex
import re

class NcduFile: # leaf
	def __init__(self, attribs):
		self.__dict__.update(attribs)
	@property
	def size(self):
		try:
			return self.asize
		except:
			return 0
class NcduNode:
	def __init__(self, attribs, children):
		self.__dict__.update(attribs)
		self.children = children
	def __iter__(self):
		return iter(self.children)
	def __len__(self): # total size
		"""
		l = 0
		for _, _, fs in self.walk():
			l += sum(f.size for f in fs)
		return l
		"""
		return sum(sum(f.size for f in fs) for _, _, fs in self.walk())
	def walk(self, prefix=''):
		if prefix:
			assert self.name
			r = os.path.join(prefix, self.name)
		else:
			r = self.name
		f, d = [], []
		for c in self:
			if isinstance(c, NcduFile):
				f.append(c)
			elif isinstance(c, NcduNode):
				d.append(c)
		yield r, d, f
		# d can be modified in-place
		for c in d:
			yield from c.walk(prefix=r)
	def printf(self, spec=('%q\n')):
		if isinstance(spec, str):
			spec = [ p for p in re.split('([%].)', spec) if p ]
		for r, ds, fs in self.walk():
			for f in fs:
				result = []
				y = result.append
				for s in spec:
					if s == '%f':
						y(f.name)
					elif s == '%h':
						y(r)
					elif s == '%i':
						y(f.ino)
					elif s == '%p':
						y(os.path.join(r, f.name))
					elif s == '%q':
						y( shlex.quote(os.path.join(r, f.name)) )
					elif s == '%s':
						y(f.size)
					elif s == '%t':
						y(f.timestamp)
					elif s == '%%':
						y('%')
					else:
						y(s)
				yield ''.join(str(r) for r in result)
			
def parse_node(entry):
	if isinstance(entry, list): # node
		return NcduNode(entry.pop(0), [ parse_node(e) for e in entry ])
	else:
		return NcduFile(entry)
class NcduReader:
	def __init__(self, serialized, ignore_root=None):
		self.version = serialized[:2]
		self.attribs = serialized[2]
		self.tree = parse_node(serialized[3])
		if (ignore_root is None):
			ignore_root = not os.path.exists(self.tree.name)
		if (ignore_root):
			self.tree.name = ''
