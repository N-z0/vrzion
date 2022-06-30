#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "summarize python modules for indexing"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "2.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### Py parsers
import symtable



MODULS='moduls'
CLASS='class'
CONSTANTS='constants'
FUNCTIONS='functions'



def get_py_summary(py_path,py_name):
	"""return an index for the given python file"""
	modul_list=[]
	class_dico={}
	constant_list=[]
	function_dico={}

	py_file=open(py_path,'r')
	py_txt=py_file.read()
	
	### detection de moduls (from,import,as)
	### Damn !
	### the Symtable module could have done the trick
	### but for the Imorted Moduls it does not work
	### a "from math import *" is not "seen"
	### there is the has_import_star method but it bugs :S
	### and an import "this" as "that" gives "that" without "this"
	### so i do it "myself"
	for line in py_txt.splitlines() :
		line=line.replace(',',' ')
		lines=line.split(';')
		for line in lines :
			line=line.split()
			if len(line)>1 :
				if line[0]=='from' :
					for m in line[3:] :
						if m=='as' : break
						m=line[1]+'.'+m
						if not m in modul_list :
							modul_list.append( m )
				elif line[0]=='import' :
					for m in line[1:] :
						if m=='as' : break
						if not m in modul_list :
							modul_list.append( m )
				else :
					pass
	
	### use symtable for others things than imported modules
	st= symtable.symtable(py_txt,py_name,'exec')
	#print(dir(st))
	for s in st.get_symbols() :
		#print(s.get_name())
		#print(s.get_identifiers())
		#print(s.get_symbols())
		### skip symtable imported modules
		if s.is_imported()==True :
			pass
			#modul_list.append(s.get_name())
			#if s.has_import_star() : print('import *')
		### get others things
		elif s.is_assigned()==True :
			if s.is_namespace()==False :
				constant_list.append(s.get_name())
			else :
				st2=s.get_namespace()
				st2_tip=st2.get_type()
				if st2_tip=='function' :
					#print(dir(st2))
					function_dico[s.get_name()]=st2.get_parameters()
				elif st2_tip=='class' :
					metods={}
					#print(st2.get_symbols())
					for s2 in st2.get_symbols() :
						#print(s2)
						### to avoid that the default values "None,False,True" of arguments of the methods been considered as method themselves:
						###	(s2.is_assigned(),s2.is_local(),s2.is_namespace(),s2.is_referenced() )
						if s2.is_namespace()==True :
							st3=s2.get_namespace()
							metods[s2.get_name()]=st3.get_parameters()
					class_dico[s.get_name()]=metods

	index={MODULS:modul_list,CLASS:class_dico,CONSTANTS:constant_list,FUNCTIONS:function_dico}
	return index

