#==============================================================================
# Return module names present in File System
#==============================================================================
def get_modules_from_filesystem():
	import os, webnotes.defs
	from import_module import listfolders
	
	modules = listfolders(webnotes.defs.modules_path, 1)
	out = []
	modules.sort()
	modules = filter(lambda x: x!='patches', modules)
	
	for m in modules:
		file = open(os.path.join(webnotes.defs.modules_path, m, 'module.info'), 'r')
		out.append([m, eval(file.read()), get_last_update_for(m), \
			webnotes.conn.exists('Module Def',m) and 'Installed' or 'Not Installed'])
		file.close()

	return out

#==============================================================================
	
def get_module_details(m):
	from export_module import get_module_items
	return {'in_files': get_module_items_from_files(m), \
		'in_system':[[i[0], i[1], get_modified(i[0], i[1])] for i in get_module_items(m)]}

#==============================================================================

def get_modified(dt, dn):
	import webnotes
	try:
		return str(webnotes.conn.sql("select modified from `tab%s` where name=%s" % (dt,'%s'), dn)[0][0])
	except:
		pass

#==============================================================================

def get_module_items_from_files(m):
	import os, webnotes.defs
	from import_module import listfolders

	items = []
	for item_type in listfolders(os.path.join(webnotes.defs.modules_path, m), 1):
		for item_name in listfolders(os.path.join(webnotes.defs.modules_path, m, item_type), 1):
			# read the file
			file = open(os.path.join(webnotes.defs.modules_path, m, item_type, item_name, item_name)+'.txt','r')
			doclist = eval(file.read())
			file.close()
			
			# append
			items.append([item_type, doclist[0]['name'], doclist[0]['modified']])
			
	return items

#==============================================================================
	
def get_last_update_for(mod):
	import webnotes
	try:
		return webnotes.conn.sql("select last_updated_date from `tabModule Def` where name=%s", mod)[0][0]
	except:
		return ''

#==============================================================================

def init_db_login(ac_name, db_name):
	import webnotes
	import webnotes.db
	import webnotes.profile
	
	if ac_name:
		webnotes.conn = webnotes.db.Database(ac_name = ac_name)
		webnotes.conn.use(webnotes.conn.user)
	elif db_name:
		webnotes.conn = webnotes.db.Database(user=db_name)
		webnotes.conn.use(db_name)
	else:
		webnotes.conn = webnotes.db.Database(use_default=1)
			
	webnotes.session = {'user':'Administrator'}
	webnotes.user = webnotes.profile.Profile()
	