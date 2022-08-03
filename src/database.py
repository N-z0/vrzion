#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "store python files summaries"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ ="4.0.1"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### builtin modules
#import string
#import os

import pickle
#import shelve

### from commonz
from commonz import logger
from commonz.fs import checks,hashers,timers,temps#,actions

### local modules
import summarize
import meta



SIZE="size"
TIMESTAMP="timestamp"
SUMMARY="summary"



class Database():
	"""Store python summaries as object"""
	def __init__(self):
		"""initialization of the Database"""
		self.database_path=None
		self.database={}
		self.summarizer=summarize.Summarizer()
	
	
	def load_file(self,database_path):
		"""load the database from a file"""
		self.database_path=database_path
		with open(database_path,'rb') as db_file:
			### The protocol version used is detected automatically, so we do not have to specify it.
			logger.log_info(30,[database_path])
			self.database= pickle.load(db_file)
	
	def write_file(self,database_path=None):
		"""
		write the database into a file
		or write into the previously loaded file if database_path is not given
		"""
		if database_path is None :
			database_path=self.database_path
		with open(database_path,'wb') as db_file :
			logger.log_info(31,[database_path])
			pickle.dump(self.database,db_file)
	
	
	def get_py_paths(self):
		"""return the list of stored python paths"""
		return self.database.keys()
	
	def get_py_versions(self,py_path):
		"""return the list of stored identities for the given python path"""
		return self.database[py_path].keys()
	
	
	def get_py_paths_number(self):
		"""return the number of stored python paths"""
		return len(self.database.keys())
	
	def get_py_versions_number(self,py_path):
		"""return number of stored identities for the given python path"""
		return len(self.database[py_path].keys())
	
	
	def get_py_size(self,py_path,identity):
		"""return the size of the file for the given python path and identity"""
		return self.database[py_path][identity][SIZE]
	
	def get_py_timestamp(self,py_path,identity):
		"""return the timestamp of the file for the given python path and identity"""
		return self.database[py_path][identity][TIMESTAMP]
	
	def get_py_summary(self,py_path,identity):
		"""return the summary of the file for the given python path and identity"""
		return self.database[py_path][identity][SUMMARY]
	
	
	def check_py_sizes(self,py_path,identity,size):
		"""return True if the given size match the stored size for the given python path and identity"""
		return self.database[py_path][identity][SIZE]==size
	
	def check_py_timestamps(self,py_path,identity,timestamp):
		"""return True if the given timestamp match the stored timestamp for the given python path and identity"""
		return self.database[py_path][identity][TIMESTAMP]==timestamp

	def check_py_summaries(self,py_path,identity,summary):
		"""return True if the given summary match the stored summary for the given python path and identity"""
		return self.database[py_path][identity][SUMMARY]==summary
	
	
	def del_py_path(self,py_path):
		"""remove the given python path and the all list of stored versions for the given python path"""
		del self.database[py_path]
	
	def del_py_version(self,py_path,identity):
		"""remove the data stored for the given python path and identity"""
		del self.database[py_path][identity]
	
	
	def add_py_version(self,py_path,update=False):
		"""
		append a python file into the database
		if update=True any already existing same version will have its timestamp renewed
		if update=False any already existing same version will keep its old timestamp
		for an added version the identity of it is returned otherwise None is returned
		"""
		timestamp= timers.get_modification_time(py_path)
		size=checks.file_size(py_path)
		summary=self.summarizer.get_py_file_summary(py_path)
		
		### we get a pure hash from temporary file with the version value masked
		with open(py_path,'r') as input_file :
			data=input_file.read()
		tmp_path=temps.get_secure_file(ext='py')
		with open(tmp_path,'w') as output_file :
			output_file.write(data)
		meta.write_file_version(tmp_path,"0.0.0")
		identity=hashers.get_file_md5(tmp_path,chunk_size=1000000,hexa=True)
		
		new_data={SIZE:size,TIMESTAMP:timestamp,SUMMARY:summary}
		
		### check if the python path is into the database
		if py_path in self.database :
			logger.log_info(32,[py_path])
		else:
			logger.log_info(33,[py_path])
			self.database[py_path]={}
		
		### check if the python file is into the database
		if identity in self.database[py_path] :
			logger.log_info(34,[identity])
			old_data= self.database[py_path][identity]
			### check if same size
			if not old_data[SIZE]==new_data[SIZE] :
				logger.log_error(35)
			### check if same timestamp
			elif old_data[TIMESTAMP]==new_data[TIMESTAMP] :
				logger.log_info(36)
			else :
					logger.log_warning(37)
					if update is False :
						logger.log_info(38,[old_data[TIMESTAMP]])
					else :
						logger.log_info(39,[new_data[TIMESTAMP]])
						self.database[py_path][identity][TIMESTAMP]=new_data[TIMESTAMP]
						return identity
		else:
			logger.log_info(40,[identity])
			self.database[py_path][identity]=new_data
			return identity
		
		### if nothing changed in the database
		return None
	
	