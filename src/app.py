#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "provide a user interface for the main module."#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "5.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = ["Rob xxx", "Peter xxx", "Gavin xxxx",	"Matthew xxxx"]#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### import the required modules

import os # use for exit status

### for output messages to logs systems
from commonz import logger

import main



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
		
		### setup datafiles
		self.data_pathnames= data_pathnames
		
		### test main module class instance
		logger.log_debug(6)
		self.o=main.Advanced_Main(adv_main_template_argument=3,main_template_argument=1)


	def run(self):
		"""operates the application object"""

		### test module function and class instance
		logger.log_debug(7,[main.TEMPLATE_CONSTANTE])
		self.o.template_method(3)
		self.o.adv_template_method(3)
		logger.log_debug(8)
		
		return os.EX_OK
	
