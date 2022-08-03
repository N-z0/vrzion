#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "sort python files in pecking order"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "4.0.1"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### from commonz
#from commonz import logger

### local modules
import summarize



IDENTITY_INDEX=0
SIZE_INDEX=1
SUMMARY_INDEX=2



class Indexer():
	"""software application as object"""
	def __init__(self):
		"""initialization of the application"""
		self.timestamps_index={}
		self.versions_tree={}
		self.versions_bond={}
	
	
	def check_moduls(self,old_moduls_list,new_moduls_list):
		"""returns True if there is any import of new modules"""
		for modul in new_moduls_list :
			if not modul in old_moduls_list :
				return True
		return False
	
	
	def check_constants(self,old_constants_list,new_constants_list):
		"""returns True if there is any new constants"""
		for constant in new_constants_list :
			if not constant in old_constants_list :
				return True
		return False
	

	def check_parameters(self,old_parameters_dico,new_parameters_dico):
		"""returns True if there is any change of parameters"""
		old_parameters_list=old_parameters_dico[summarize.PARAMETERS]
		new_parameters_list=new_parameters_dico[summarize.PARAMETERS]
		old_parameters_quantum=len(old_parameters_list)
		new_parameters_quantum=len(new_parameters_list)
		if new_parameters_quantum > old_parameters_quantum :
			return True
		for index in range(new_parameters_quantum) :
			if not old_parameters_list[index]==new_parameters_list[index] :
				return True
		if new_parameters_dico[summarize.ARGS] is True and old_parameters_dico[summarize.ARGS] is False :
			return True
		if new_parameters_dico[summarize.KWARGS] is True and old_parameters_dico[summarize.KWARGS] is False :
			return True
		return False
	
	
	def check_functions(self,old_functions_dico,new_functions_dico):
		"""returns True if there is any new function or with any new parameters"""
		old_functions_list=old_functions_dico.keys()
		new_functions_list=new_functions_dico.keys()
		for function in new_functions_list :
			if function in old_functions_list :
				old_parameters_dico=old_functions_dico[function]
				new_parameters_dico=new_functions_dico[function]
				if self.check_parameters(old_parameters_dico,new_parameters_dico) :
					return True
			else :
				return True
		return False
	
	
	def check_classes(self,old_classes_dico,new_classes_dico):
		"""returns True if there is any new class or with any new function or with any new parameters"""
		old_classes_list=old_classes_dico.keys()
		new_classes_list=new_classes_dico.keys()
		for classs in new_classes_list :
			if classs in old_classes_list :
				old_function_dico=old_classes_dico[classs]
				new_function_dico=new_classes_dico[classs]
				if self.check_functions(old_function_dico,new_function_dico) :
					return True
			else :
				return True
		return False
	
	
	def check_changes(self,old_summary,new_summary):
		"""returns False if new_summary import new modules,remove functions/classes/methods or have their parameters changed"""
		
		### check if any new module is imported
		old_moduls_list=old_summary[summarize.MODULS]
		new_moduls_list=new_summary[summarize.MODULS]
		if self.check_moduls(old_moduls_list,new_moduls_list) :
			return False
		
		### check if any constants as been removed
		old_constants_list=old_summary[summarize.CONSTANTS]
		new_constants_list=new_summary[summarize.CONSTANTS]
		if self.check_constants(new_constants_list,old_constants_list) :
			return False
		
		### check the remove of functions
		### and the change of any parameters
		old_functions_dico=old_summary[summarize.FUNCTIONS]
		new_functions_dico=new_summary[summarize.FUNCTIONS]
		if self.check_functions(new_functions_dico,old_functions_dico) :
			return False
		
		### check the remove of classes
		### and the change of any methods
		### and the change of any parameters
		old_classes_dico=old_summary[summarize.CLASSES]
		new_classes_dico=new_summary[summarize.CLASSES]
		if self.check_classes(new_classes_dico,old_classes_dico) :
			return False
		
		return True
	
	
	def get_timestamps_number(self):
		"""return how many different timestamp are stored"""
		return len(self.timestamps_index.keys())
	
	
	def get_recent_identities(self,discard=0):
		"""
		return the list the identities of the last py files
		discard is the number of last py files to skip
		(ex: with discard=3 the 4rd identity from the last py files will be returned)
		"""
		### make a list of all timestamps
		timestamps_list=list(self.timestamps_index.keys())
		### sort and reverse
		timestamps_list.sort()
		timestamps_list.reverse()
		### get the matching timestamp
		timestamp=timestamps_list[discard]
		### make the list of the identities
		identities_list=[]
		for data in self.timestamps_index[timestamp] :
			identity=data[IDENTITY_INDEX]
			identities_list.append(identity)
		return identities_list
	
	
	def make_versions_tree(self):
		"""
		for the given py_path put all stored identities in pecking order
		py_path select a python pathname already stored in the database
		"""
		### make and sort a timestamps list
		timestamps_list=list(self.timestamps_index.keys())
		timestamps_list.sort()
		
		### make a new tree for the given py_path
		tree=[]
		for timestamp in timestamps_list :
			for new_data in self.timestamps_index[timestamp] :
				new_identity=new_data[IDENTITY_INDEX]
				new_summary=new_data[SUMMARY_INDEX]
				
				### add a branch
				branch_quantum=len(tree)
				for branch_index in range(branch_quantum) :
					old_data= tree[branch_index][0][0]
					old_summary= old_data[SUMMARY_INDEX]
					if self.check_changes(old_summary,new_summary) :
						break
				else :
					branch_index=branch_quantum
					tree.append([])
				
				### add a twig
				twig_quantum=len(tree[branch_index])
				for twig_index in range(twig_quantum) :
					old_data= tree[branch_index][twig_index][0]
					old_summary= old_data[SUMMARY_INDEX]
					if self.check_changes(new_summary,old_summary) :
						break
				else :
					twig_index=twig_quantum
					tree[branch_index].append([])
				
				### add a leaf
				leaf_quantum= len(tree[branch_index][twig_index])
				leaf_index= leaf_quantum
				tree[branch_index][twig_index].append(new_data)
				
				### keep access to the version code number by the identity code number
				version=(branch_index,twig_index,leaf_index)
				self.versions_bond[new_identity]=version
		
		self.versions_tree=tree
	
	
	def get_branch_number(self):
		"""return how many branch are on the tree"""
		return len(self.versions_tree)
	
	
	def get_twig_number(self,branch_index):
		"""return how many twig are on the branch"""
		return len(self.versions_tree[branch_index])
	
	
	def get_leaf_number(self,branch_index,twig_index):
		"""return how many leaf are on the twig"""
		return len(self.versions_tree[branch_index][twig_index])
	
	
	def get_identity_from_tree(self,branch_index=0,twig_index=0,leaf_index=0):
		"""return an identity from the version tree for the given index"""
		data= self.versions_tree[branch_index][twig_index][leaf_index]
		return data[IDENTITY_INDEX]
	
	
	def get_file_version(self,identity):
		"""
		return version of the specified python file
		identity must be already stored in the database
		"""
		return self.versions_bond[identity]
	
	
	def add_file(self,identity,size,summary,timestamp):
		"""append a python file"""
		data= (identity,size,summary)
		### store by their timestamps
		self.timestamps_index.setdefault(timestamp,[])
		self.timestamps_index[timestamp].append(data)
	
	