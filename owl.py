#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from errno import EACCES
from os.path import realpath
from sys import argv, exit
from threading import Lock
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

from filelog import getMySQLSession
from filelog import FileLog

class Loopback(LoggingMixIn, Operations):
	def __init__(self, root):
		self.root = root
		self.rwlock = Lock()

		self.getMySQLSession = getMySQLSession('root', 'localhost', 'root', 'FILELOG')
	getMySQLSession = None

	def __call__(self, op, path, *args):
		return super(Loopback, self).__call__(op, self.root + path, *args)

	# +============================================================================
	# | Filesystem method
	# +============================================================================
	def access(self, path, mode):
		self.__log__('access', path)
		print "ACCESS (path=%s, mode=%s)" %(path, mode)
		if not os.access(path, mode):
			print "RAISE EACCESS"
			raise FuseOSError(EACCES)

	def chmod(self, path, mode):
		self.__log__('chmod', path)
		print "CHMOD (path=%s, mode=%s)" %(path, mode)
		return os.chmod(path, mode)

	def chown(self, path, mode):
		self.__log__('chown', path)
		print "CHOWN (path=%s, mode=%s)" %(path, mode)
		return os.chown(path, mode)

	def getattr(self, path, fh=None):
		self.__log__('getattr', path)
		print "GETATTR (path=%s, fh=%s)" %(path, fh)
		st = os.lstat(path)
		return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
		'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid', 'st_dev', 'st_ino'))

	def readdir(self, path, fh):
		self.__log__('readdir', path)
		print "READDIR (path=%s, fh=%s)" %(path, fh)
		return ['.', '..'] + os.listdir(path)

	def readlink(self, path):
		self.__log__('readlink', path)
		print "READLINK (path=%s)" %(path)
		return os.readlink(path)

	def mknod(self, path, mode, dev):
		self.__log__('mknod', path)
		print "MKNOD (path=%s, mode=%s, dev=%s)" %(path, mode, dev)
		return os.mknod(path, mode, dev)

	def mkdir(self, path, mode):
		self.__log__('mkdir', path)
		print "MKDIR (path=%s, mode=%s)" %(path, mode)
		return os.mkdir(path, mode)

	def rmdir(self, path):
		self.__log__('rmdir', path)
		print "RMDIR (path=%s)" %(path)
		return os.rmdir(path)

	def statfs(self, path):
		self.__log__('statfs', path)
		print "STATFS (path=%s)" %(path)
		stv = os.statvfs(path)
		return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
			'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
			'f_frsize', 'f_namemax'))

	def symlink(self, target, source):
		self.__log__('syslink', path)
		print "STATFS (target=%s, source=%s)" %(target, source)
		return os.symlink(source, target)

	def rename(self, old, new):
		self.__log__('rename old', old)
		self.__log__('rename new', new)
		print "STATFS (old=%s, new=%s)" %(old, new)
		return os.rename(old, self.root + new)

	def link(self, target, source):
		self.__log__('link target', target)
		self.__log__('link source', source)
		print "LINK (target=%s, source=%s)" %(target, source)
		return os.link(source, target)

	def unlink(self, path):
		self.__log__('unlink', path)
		print "UNLINK (path=%s)" %(path)
		return os.unlink(path)

	def utimens(self, path, times=None):
		self.__log__('utimes', path)
		print "UTIMENS (path=%s, times=%s)" %(path, times)
		return os.utime(path, times)

	# +============================================================================
	# | File method
	# +============================================================================
	def open(self, path, flags):
		self.__log__('open', path)
		print "OPEN (path=%s, flags=%s)" %(path, flags)
		return os.open(path, flags)

	def create(self, path, mode):
		self.__log__('create', path)
		print "CREATE (path=%s, mode=%s)" %(path, mode)
		return os.open(path, os.O_WRONLY | os.O_CREAT, mode)

	def read(self, path, size, offset, fh):
		self.__log__('read', path)
		print "READ (path=%s, size=%s, offset=%s, fh=%s)" %(path, size, offset, fh)
		with self.rwlock:
			os.lseek(fh, offset, 0)
			return os.read(fh, size)

	def write(self, path, data, offset, fh):
		self.__log__('write', path)
		print "WRITE (path=%s, offset=%s, fh=%s)" %(path, offset, fh)
		with self.rwlock:
			os.lseek(fh, offset, 0)
			return os.write(fh, data)

	def truncate(self, path, length, fh=None):
		self.__log__('truncate', path)
		print "TRUNCATE (path=%s, length=%s, fh=%s)" %(path, length, fh)
		with open(path, 'r+') as f:
			f.truncate(length)
			unlink = os.unlink
			utimens = os.utime

	def flush(self, path, fh):
		self.__log__('flush', path)
		print "FLUSH (path=%s, fh=%s)" %(path, fh)
		return os.fsync(fh)

	def release(self, path, fh):
		self.__log__('release', path)
		print "RELEASE (path=%s, fh=%s)" %(path, fh)
		return os.close(fh)

	def fsync(self, path, datasync, fh):
		self.__log__('fsync', path)
		print "FSYNC (path=%s, datasync=%s, fh=%s)" %(path, datasync, fh)
		return os.fsync(fh)

	def __log__(self, operation, path):
		session = self.getMySQLSession()
		session.add(FileLog(operation, path))
		session.commit()

if __name__ == '__main__':
	mntpoint  = os.path.abspath('%s/mnt' %(os.path.dirname(os.path.abspath(__file__))))
	rootpoint = os.path.abspath('%s/root' %(os.path.dirname(os.path.abspath(__file__))))
	FUSE(Loopback(mntpoint), rootpoint, foreground=True, nonempty=True)

