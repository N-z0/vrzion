#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "parse python modules file and put them in a nutshell"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "4.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### Py parsers
#import symtable
import ast # is more complex than symtable but gives more details



MODULS='moduls'
CONSTANTS='constants'
CLASSES='classes'
FUNCTIONS='functions'
PARAMETERS='parameters'
OPTION='option'
ARGS='*'
KWARGS='**'



class Summarizer():
	"""a Python summarizer object"""
	def __init__(self):
		"""initialization of the Summarizer"""
	
	def __get_py_imports_summary(self,ast_nodes):
		"""return the python imported modules in a nutshell"""
		
		modul_list=set()
		
		for node in ast_nodes :#ast.iter_child_nodes(ast_nodes)
			if isinstance(node,ast.Import) :
				for modul_node in node.names :#ast.iter_child_nodes(ast_nodes)
					#print(modul_node.asname)
					#print(modul_node.name)
					modul_list.add( modul_node.name )
			
			elif isinstance(node,ast.ImportFrom) :
				from_names=node.module
				#print(node.level)
				for modul_node in node.names :#ast.iter_child_nodes(ast_nodes)
					#print(modul_node.asname)
					#print(modul_node.name)
					modul_name=modul_node.name
					if modul_name=='*' :
						modul_list.add( from_names )
					else :
						modul_list.add( '.'.join([from_names,modul_name]) )
		
		return modul_list
	
	
	def __get_py_constants_summary(self,ast_nodes):
		"""return the python constants in a nutshell"""
		
		constants_list=set()
		
		for node in ast_nodes :#ast.iter_child_nodes(ast_nodes)
			if isinstance(node,ast.Assign) :
				#print(dir(node))
				#print(node.type_comment)
				for target_node in node.targets :#ast.iter_child_nodes(ast_nodes)
					#print(dir(target_node))
					#print("ID",target_node.id)
					constants_list.add( target_node.id )
				
				### it doesn't make much sens for me but it appears that value contents value of previous node
				#print(dir(node.value))
				if hasattr(node.value,'kind') and hasattr(node.value,'n') and hasattr(node.value,'s') :
					#print(node.value.kind) # dont know what it is
					#print(node.value.n)# contents value of the variable (same as s)
					#print(node.value.s)# contents value of the variable (same as n)
					pass
				else:
					#print(dir(node.value))
					pass
		
		return constants_list
	
	
	def __get_py_functions_summary(self,ast_nodes,method=False):
		"""return the python functions and their attributes in a nutshell"""
		
		fonctions_dico={}
		
		for node in ast_nodes :#ast.iter_child_nodes(ast_nodes)
			if isinstance(node,ast.FunctionDef) :
				#print(dir(node))
				function_name=node.name
				#print(node.type_comment)
				#print(node.decorator_list)
				#print(node.returns)
				#print("args:",dir(node.args))
				parameters_list=[]
				defaults_list=[]
				first=True
				for a in node.args.args :#ast.iter_child_nodes(ast_nodes)
					#print(dir(a))
					#print(a.annotation)
					attribute_name=a.arg
					if not (first is True and method is True and attribute_name=='self') :
						parameters_list.append(attribute_name)
					first=False
				### list of default values for arguments, that can be passed positionally.
				## they correspond to the last "n" arguments.
				for d in node.args.defaults :#ast.iter_child_nodes(ast_nodes)
					#print(dir(d))
					default_value= d.value
					defaults_list.append(default_value)
					#print(d.kind) # None
					#print(d.n) # same as value
					#print(d.s) # same as value
				#print(node.args.kw_defaults) # empty list
				#print(node.args.kwonlyargs) # empty list
				#print(node.args.posonlyargs) # empty list
				args=False
				kwargs=False
				### *arg mean a list of unknown numbers of parameters can be given to the function, or not at all
				if hasattr(node.args.vararg,'arg') :
					#print(node.args.vararg.arg) # None
					args=True
				### **arg mean a dictionary of unknown numbers of parameters can be given to the function, or not at all
				if hasattr(node.args.kwarg,'arg') :
					#print(node.args.kwarg.arg)
					kwargs=True
				defaults_number= len(defaults_list)
				fonctions_dico[function_name]={PARAMETERS:parameters_list,OPTION:defaults_number,ARGS:args,KWARGS:kwargs}
		
		return fonctions_dico
	
	
	def __get_py_classes_summary(self,ast_nodes):
		"""return the python classes and their attributes and methods in a nutshell"""
		
		classes_dico={}
		
		for node in ast_nodes : #ast.iter_child_nodes(ast_nodes)
			if isinstance(node,ast.ClassDef) :
				class_name=node.name
				methods= self.__get_py_functions_summary(node.body,method=True)
				classes_dico[class_name]=methods
		
		return classes_dico
	
	
	def get_py_file_summary(self,py_file):
		"""return the given python file in a nutshell"""
		
		with open(py_file,'r') as pf :
			### type_comments=False the type of variable can be declarer in python but its not usual for dynamic language
			tree = ast.parse(pf.read(),type_comments=False)
			#print(ast.dump(tree))
			
			### get the things
			moduls_list=self.__get_py_imports_summary(tree.body)
			constants_list=self.__get_py_constants_summary(tree.body)
			functions_dico=self.__get_py_functions_summary(tree.body)
			classes_dico=self.__get_py_classes_summary(tree.body)
			
		index={MODULS:moduls_list,CLASSES:classes_dico,CONSTANTS:constants_list,FUNCTIONS:functions_dico}
		return index
	
	