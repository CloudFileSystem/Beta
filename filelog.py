#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import MetaData
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()
Base.metadata = MetaData()

class FileLog(Base):
	__tablename__ = 'filelog'

	id		= Column(Integer, primary_key=True)
	operation	= Column(Text)
	path		= Column(Text)
	date		= Column(DateTime)

	def __init__(self, operation, path):
		self.operation	= operation
		self.path	= path
		self.date	= datetime.now()

	def __str__(self):
		return "[operation=%s, path=%s, date=%s]" %(self.name, self.path, self.date)

def getMySQLSession(username, hostname, password, database):
	uri = 'mysql://%s:%s@%s/%s' %(password, username, hostname, database)
	engine = create_engine(uri)
	MySQLSession = sessionmaker(bind=engine)

	FileLog.metadata.create_all(engine)

	return MySQLSession

