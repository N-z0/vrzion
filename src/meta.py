#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "read and write python __version__ metadata"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ ="1.0.1"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022-07-30"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### builtin modules
import os
#import string

### from commonz
#from commonz import logger
#from commonz.fs import checks,hashers,timers,temps



#DOCSTRINGS=('__doc__','__status__','__version__','__license__','__date__','__author__','__maintainer__','__credits__','__contact__')



def get_it(line):
	"""
	return related data if __version__ is found in the give line
	otherwise nothing is returned
	"""
	line=line.rstrip()#remove trailing newline
	code_comment=line.partition('#')
	code_value= code_comment[0]
	if '=' in code_value :
		code_value= code_value.partition('=')
		code= code_value[0]+code_value[1]
		value= code_value[2]
		comment= code_comment[1]+code_comment[2]
		if '__version__' in code :
			return [code,value,comment,os.linesep]


def convert2numbers(string):
	"""return a list of numbers from a string representing the version"""
	string= string.strip('\' \"')# remove useless chars around
	version= [int(n) for n in string.split('.')]
	return version


def convert2string(numbers):
	"""return a string from a list of numbers representing the version"""
	version= '.'.join( [str(n) for n in numbers] )
	return '"'+version+'"'# add necessary chars around


def read_file_version(py_path):
	"""
	return as a list of numbers the __version__ information found in the given python file
	py_path must be a python file location with value for __version__ metadata
	"""
	with open(py_path,'r') as input_file :
		for line in input_file.readlines() :
			data=get_it(line)
			if data :
				version= convert2numbers(data[1])
				return version


def write_file_version(py_path,version):
	"""
	change the __version__ metadata information found in the given python file
	py_path must be a python file location with value for __version__ metadata
	version must be a list or tuple with the new version numbers
	"""
	### first read the py file and change the __version__ line
	new_lines=[]
	with open(py_path,'r') as py_file :
		for line in py_file.readlines() :
			data=get_it(line)
			if data :
				version= convert2string(version)
				data[1]=version
				line=''.join(data)
			new_lines.append(line)
	### then write the py file with the changed the __version__ line
	with open(py_path,'w') as py_file :
		py_file.writelines(new_lines)


