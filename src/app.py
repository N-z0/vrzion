#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "This is the program centerpiece,but need to use others modules"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "6.0.1"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### builtin modules
import os # use for exit status and path separators

### commonz modules
from commonz import logger
from commonz.fs import pathnames,checks#,actions

### local modules
import database
import indexer
import meta



PYTHON_MIMETYPE='text/x-python'
PYTHON_EXT='py'



class Application():
	"""software application as object"""
	def __init__(self,prog_name,cfg,dirs,data_pathnames,env):
		"""initialization of the application"""
		
		### setup names
		self.prog_name=prog_name
		self.user_name=env['USER']
		
		### setup path
		self.working_dir=dirs['cwd']
		self.home_dir=dirs['home']
		self.cache_dir=dirs['cache']
		
		### store configuration settings parameters
		app_cfg=cfg['APP']
		self.directory=app_cfg['directory']
		self.name=app_cfg['name']
		self.db_path=app_cfg['index']
		self.test=app_cfg['test']
		self.wipe=app_cfg['wipe']
		
		### keep datafiles
		self.data_pathnames= data_pathnames
	
	
	def run(self):
		"""operates the application object"""
		
		### get the list of files
		logger.log_debug(10)
		if self.name=="*" :
			files_list=pathnames.get_recursive_content(self.directory,includ_files=True,includ_directories=False,fullpath=True)
		else :
			files_list=pathnames.search_directory_content(self.directory,self.name,includ_files=True,includ_directories=False,fullpath=True)
		logger.log_info(11,[len(files_list)])
		
		### filter python files
		py_files_list= [ f for f in files_list if checks.get_mimetype(f)[0]==PYTHON_MIMETYPE or pathnames.get_name_ext(f)==[PYTHON_EXT] ]
		logger.log_info(12,[len(py_files_list)])
		
		### get a database
		db= database.Database()
		### if there is a database file load in it
		if not checks.file_pathname(self.db_path) :
			logger.log_warning(13,[self.db_path])
			database_path=self.db_path
		else:
			logger.log_debug(14)
			db.load_file(self.db_path)
			database_path=None
		
		### add into the database python files found
		### and retrieve the new or updated identities
		news={}
		for py_path in py_files_list :
			logger.log_debug(15)
			new_identity= db.add_py_version(py_path,update=True)
			if new_identity :
				news[py_path]=new_identity
				### introducing an old file can affect the versions of all newer
				### need to check if the new one is the last one
				### and eventually delete any newer versions
				timestamp= db.get_py_timestamp(py_path,new_identity)
				for other_identity in db.get_py_versions(py_path) :
					if timestamp < db.get_py_timestamp(py_path,other_identity) :
						logger.log_warning(16)
						if self.wipe is True :
							logger.log_warning(17)
							db.del_py_version(py_path,other_identity)
		
		### proceed for each new or updated files
		for item in news.items() :
			new_py_path=item[0]
			new_identity=item[1]
			### an indexer will sort all the files versions
			i=indexer.Indexer()
			### add in indexer all database python files
			logger.log_debug(18)
			for identity in db.get_py_versions(new_py_path) :
				timestamp= db.get_py_timestamp(new_py_path,identity)
				size= db.get_py_size(new_py_path,identity)
				summary= db.get_py_summary(new_py_path,identity)
				i.add_file(identity,size,summary,timestamp)
			### now let's put all the versions in pecking order
			i.make_versions_tree()
			### and then get the version of the new py file
			new_version=i.get_file_version(identity)
			### write the version or just print it
			if self.test is True :
				### only display the new version
				logger.log_info(19,[new_version])
			elif not new_identity in i.get_recent_identities(discard=0) :
				### this version is wrong do not write it
				logger.log_warning(20)
			elif meta.read_file_version(new_py_path)==new_version :
				### its not necessary to write version into the file
				logger.log_info(21,[new_version])
			else :
				### write version into the file
				logger.log_info(22,[new_version])
				meta.write_file_version(new_py_path,new_version)
				### because the version code is written inside the file
				### the hash and timestamps are modified
				### need to replace this in the database
				db.del_py_version(new_py_path,new_identity)
				db.add_py_version(new_py_path,update=True)
		
		### eventually write the database file
		if self.test is False :
			logger.log_debug(23)
			db.write_file(database_path)
		
		
		return os.EX_OK


