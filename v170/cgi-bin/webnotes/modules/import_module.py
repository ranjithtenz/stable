# ==============================================================================
# Import from files
# =============================================================================
def import_from_files(modules = [], record_list = [], execute_patches = 0, sync_cp = 0, target_db=None, target_ac=None):

	if target_db or target_ac:
		init_db_login(target_ac, target_db)

	from webnotes.utils import transfer
	# Get paths of folder which will be imported
	folder_list = get_folder_paths(modules, record_list)
	ret = []
		
	if folder_list:
		# get all doclist
		all_doclist = get_all_doclist(folder_list)
	
		# import doclist
		ret += accept_module(all_doclist)
	
		# import attachments
		for m in modules:
			import_attachments(m)
	
		# execute patches
		#if execute_patches:
		#	ret += transfer.execute_patches(modules,record_list)
		
		# sync control panel
		if sync_cp:
			ret.append(sync_control_panel())
	else:
		ret.append("Module/Record not found")
		
	return ret


# ==============================================================================
# Get list of folder path
# =============================================================================
# record_list in format [[module,dt,dn], ..]
def get_folder_paths(modules, record_list):
	import os
	import webnotes
	import fnmatch
	import webnotes.defs
	from webnotes.modules import transfer_types

	folder_list=[]

	# get the folder list
	if record_list:
		for record in record_list:
			folder_list.append(os.path.join(webnotes.defs.modules_path, \
				record[0], record[1], record[2].replace('/','-')))

	if modules:
		# system modules will be transferred in a predefined order and before all other modules
		sys_mod_ordered_list = ['Roles', 'System', 'Application Internal', 'Mapper', 'Settings']
		all_mod_ordered_list = [t for t in sys_mod_ordered_list if t in modules] + list(set(modules).difference(sys_mod_ordered_list))
		for module in all_mod_ordered_list:
			mod_path = os.path.join(webnotes.defs.modules_path, module)
			types_list = listfolders(mod_path, 1)
			
			# list of types
			types_list = list(set(types_list).difference(['Control Panel']))
			all_transfer_types =[t for t in transfer_types if t in types_list] + list(set(types_list).difference(transfer_types))
			
			# build the folders
			for d in all_transfer_types:
				if d != 'files':
					# get all folders inside type
					folder_list+=listfolders(os.path.join(webnotes.defs.modules_path, module, d))

	return folder_list

	
# ==============================================================================
# Get doclist for all folder
# =============================================================================


def get_all_doclist(folder_list):
	import fnmatch
	import os
		
	doclist = []
	all_doclist = []

	# build into doclist
	for folder in folder_list:
		# get the doclist
		file_list = os.listdir(folder)
		for each in file_list:

			if fnmatch.fnmatch(each,'*.txt'):
				doclist = eval(open(os.path.join(folder,each),'r').read())
				# add code
				all_doclist.append(add_code_from_files(doclist, folder))
	
	return all_doclist
	


# ==============================================================================
# Add code to doclist
# =============================================================================
def add_code_from_files(doclist, folder):
	import webnotes
	import os
	# code will be in the parent only
	code_fields = webnotes.code_fields_dict.get(doclist[0]['doctype'], [])
	code = ''
	for code_field in code_fields:
		# see if the file exists
		name_extn = ''
		if code_field[0]=='static_content':
			name_extn += ' Static'
		fname = os.path.join(folder, os.path.basename(folder)+name_extn+'.'+code_field[1])
		
		code = ''
		try:
			code = open(fname,'r').read()
		except Exception, e:
			if e.args[0]==2:
				pass
			else:
				raise e
		
		doclist[0][code_field[0]] = code
	return doclist


# =============================================================================
# Get the deepmost folder with files in the given path tree....
# =============================================================================
def listfolders(path, only_name=0):
	import os
	out = []
	for each in os.listdir(path):
		temp = os.path.join(path,each)

		if os.path.isdir(temp) and not each.startswith('.'):
			if only_name: out.append(each)
			else: out.append(temp)
	return out
	

# ==============================================================================
# accept a module coming from a remote server
# ==============================================================================
def accept_module(super_doclist):
	import webnotes
	import webnotes.utils
	from webnotes.utils import transfer
	msg, i = [], 0
	
	for dl in super_doclist:
		msg.append(transfer.set_doc(dl, 1, 1, 1))
		
		if dl[0]['doctype']=='Module Def':
			update_module_timestamp(dl[0]['name'])

	if not webnotes.conn.in_transaction:
		webnotes.conn.sql("START TRANSACTION")

	# clear over-written records / deleted child records
	webnotes.utils.clear_recycle_bin()
	
	# clear cache
	webnotes.conn.sql("DELETE from __DocTypeCache")
	webnotes.conn.sql("COMMIT")
	
	return msg

# =============================================================================
# Update timestamp in Module Def table
# =============================================================================
def update_module_timestamp(mod):
	import webnotes, webnotes.defs, os
	
	file = open(os.path.join(webnotes.defs.modules_path, mod, 'module.info'), 'r')
	module_info = eval(file.read())
	file.close()
	
	# update in table
	try:
		update_module_timestamp_query(mod, module_info['update_date'])
	except Exception, e:
		if e.args[0]==1054: # no column
			# add column
			webnotes.conn.sql("alter table `tabModule Def` add column last_updated_date varchar(40)")
			
			# try again
			update_module_timestamp_query(mod, module_info['update_date'])
		else:
			raise e

# =============================================================================

def update_module_timestamp_query(mod, timestamp):
	import webnotes
	webnotes.conn.sql("start transaction")
	webnotes.conn.sql("update `tabModule Def` set last_updated_date=%s where name=%s", (timestamp, mod))
	webnotes.conn.sql("commit")

# =============================================================================
# Sync control panel
# =============================================================================
def import_control_panel():
	from webnotes.utils import transfer
	import os
	import webnotes.defs
	
	startup_code = startup_css = ''
	folder = os.path.join(webnotes.defs.modules_path, 'System','Control Panel','Control Panel')
	
	# js
	try:
		file = open(os.path.join(folder, 'Control Panel.js'),'r')
		startup_code = file.read()
		file.close()
	except OSError, e:
		pass
	
	# css
	try:
		file = open(os.path.join(folder, 'Control Panel.css'),'r')
		startup_css = file.read()
		file.close()
	except OSError, e:
		pass


	transfer.sync_control_panel(startup_code, startup_css)
	return "Control Panel Synced"

# =============================================================================
# Import Attachments
# =============================================================================

def import_attachments(m):
	import os, webnotes.defs
	import webnotes.utils.file_manager
	
	out = []
	
	# get list
	try:
		folder = os.path.join(webnotes.defs.modules_path, m, 'files')
		fl = os.listdir(folder)
	except OSError, e:
		if e.args[0]==2:
			return
		else:
			raise e
	
	# import files
	for f in fl:
		if not os.path.isdir(os.path.join(folder, f)):
			# delete
			webnotes.utils.file_manager.delete_file(f)
		
			# import
			file = open(os.path.join(folder, f),'r')
			webnotes.utils.file_manager.save_file(f, file.read(), m)
			file.close()
			
			out.append(f)
	
	return out
