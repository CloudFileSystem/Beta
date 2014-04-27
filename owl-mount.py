#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from owl import Loopback

# get program name
program_name = sys.argv[0]

# show usage of mount
def usage(ret):
	print "Usage: %s /path/to/fuse/fs /path/of/mountpoint [-o options]" % program_name
	sys.exit(ret)

def main():
	# initial sanity check
	argc = len(sys.argv)
	if argc < 3 or sys.argv[2] != "-o":
		usage(1)

	# get arguments
	pyfile = sys.argv[0]
	mountpoint = sys.argv[1]

	# confirm file is exist
	if not os.path.isfile(pyfile):
		print "%s: file %s doesn't exist, or is not a file" % (program_name, pyfile)
		sys.exit(1)

	# get python file path
	pypath = os.path.abspath(pyfile)

	# all seems ok - run our fuse fs as a child
	if os.fork() == 0:
		mntpoint = os.path.abspath('%s/root' %(os.path.dirname(os.path.abspath(__file__))))
		FUSE(Loopback(mntpoint), mountpoint, foreground=True, nonempty=True, allow_other=True)
	else:
		pass

if __name__ == '__main__':
	main()

