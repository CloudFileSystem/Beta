#!/usr/bin/env python
import os
from errno import EACCES
from os.path import realpath
from sys import argv, exit
from threading import Lock
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

class Loopback(LoggingMixIn, Operations):
	def __init__(self):
		self.root = realpath('/home/naoya.d')
		self.rwlock = Lock()

	def __call__(self, op, path, *args):
		return super(Loopback, self).__call__(op, self.root + path, *args)

	# +============================================================================
	# | Filesystem method
	# +============================================================================
	def access(self, path, mode):
		print "ACCESS (path=%s, mode=%s)" %(path, mode)
		if not os.access(path, mode):
			raise FuseOSError(EACCES)

	def chmod(self, path, mode):
		print "CHMOD (path=%s, mode=%s)" %(path, mode)
		return os.chmod(path, mode)

	def chown(self, path, mode):
		print "CHOWN (path=%s, mode=%s)" %(path, mode)
		return os.chown(path, mode)

	def getattr(self, path, fh=None):
		print "GETATTR (path=%s, fh=%s)" %(path, fh)
		st = os.lstat(path)
		return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
		'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid', 'st_dev', 'st_ino'))

	#def getxattr(self, path, fh=None):
	#	print "GETXATTR (path=%s, fh=%s)" %(path, fh)

	def readdir(self, path, fh):
		print "READDIR (path=%s, fh=%s)" %(path, fh)
		return ['.', '..'] + os.listdir(path)

	def readlink(self, path):
		print "READLINK (path=%s)" %(path)
		return os.readlink(path)

	def mknod(self, path, mode, dev):
		print "MKNOD (path=%s, mode=%s, dev=%s)" %(path, mode, dev)
		return os.mknod(path, mode, dev)

	def mkdir(self, path, mode):
		print "MKDIR (path=%s, mode=%s)" %(path, mode)
		return os.mkdir(path, mode)

	def rmdir(self, path):
		print "RMDIR (path=%s)" %(path)
		return os.rmdir(path)

	def statfs(self, path):
		print "STATFS (path=%s)" %(path)
		stv = os.statvfs(path)
		return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
			'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
			'f_frsize', 'f_namemax'))

	def symlink(self, target, source):
		print "STATFS (target=%s, source=%s)" %(target, source)
		return os.symlink(source, target)

	def rename(self, old, new):
		print "STATFS (old=%s, new=%s)" %(old, new)
		return os.rename(old, self.root + new)

	def link(self, target, source):
		print "LINK (target=%s, source=%s)" %(target, source)
		return os.link(source, target)

	def utimens(self, path, times=None):
		print "UTIMENS (path=%s, times=%s)" %(path, times)
		return os.utime(path, times)

	# +============================================================================
	# | File method
	# +============================================================================
	def open(self, path, flags):
		print "OPEN (path=%s, flags=%s)" %(path, flags)
		return os.open(path, flags)

	def create(self, path, mode):
		print "CREATE (path=%s, mode=%s)" %(path, mode)
		return os.open(path, os.O_WRONLY | os.O_CREAT, mode)

	def read(self, path, size, offset, fh):
		print "READ (path=%s, size=%s, offset=%s, fh=%s)" %(path, size, offset, fh)
		with self.rwlock:
			os.lseek(fh, offset, 0)
			return os.read(fh, size)

	def write(self, path, data, offset, fh):
		print "WRITE (path=%s, data=%s, offset=%s, fh=%s)" %(path, data, offset, fh)
		with self.rwlock:
			os.lseek(fh, offset, 0)
			return os.write(fh, data)

	def truncate(self, path, length, fh=None):
		print "TRUNCATE (path=%s, length=%s, fh=%s)" %(path, length, fh)
		with open(path, 'r+') as f:
			f.truncate(length)
			unlink = os.unlink
			utimens = os.utime

	def flush(self, path, fh):
		print "FLUSH (path=%s, fh=%s)" %(path, fh)
		return os.fsync(fh)

	def release(self, path, fh):
		print "RELEASE (path=%s, fh=%s)" %(path, fh)
		return os.close(fh)

	def fsync(self, path, datasync, fh):
		print "FSYNC (path=%s, datasync=%s, fh=%s)" %(path, datasync, fh)
		return os.fsync(fh)

if __name__ == '__main__':
	mntpoint = os.path.abspath('%s/../mnt' %(os.path.dirname(os.path.abspath(__file__))))
	print "I will mount %s" %(mntpoint)
	FUSE(Loopback(), '/home/naoya', foreground=True, nonempty=True)

