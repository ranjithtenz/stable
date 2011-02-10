# code sync - syncs code from files and is called from webnotes.model.doc.get

def sync(doc):
	import webnotes
	
	# check if all code is updated
	for code_field in webnotes.code_fields_dict[doc.doctype]:
		file_timestamp = get_file_timestamp(doc, code_field)

		if file_timestamp and (file_timestamp != get_system_timestamp(doc, code_field)):
			update_code(doc, code_field, file_timestamp)

# -------------------------------------------------

def get_file_timestamp(doc, code_field):
	import os
	try:
		return str(os.stat(get_code_path(doc, code_field)).st_mtime)			
	except OSError, e:
		if e.args[0]!=2:
			raise e
		else:
			return None

# -------------------------------------------------

def get_system_timestamp(doc, code_field):
	import webnotes
	
	try:
		webnotes.conn.sql("select `timestamp` from __CodeFileTimeStamps where doctype=%s and name=%s and code_field=%s", (doc.doctype, doc.name, code_field[0]))[0][0]
	except IndexError, e:
		return None
	except Exception, e:
		if e.args[0]==1146: # no table
			make_table()
			return None
		else:
			raise e

# -------------------------------------------------

def make_table():
	import webnotes
	
	webnotes.conn.sql("create table `__CodeFileTimeStamps` (name VARCHAR(120), doctype VARCHAR(120), code_field VARCHAR(120), `timestamp` VARCHAR(120))")
	
	
# -------------------------------------------------

def update_code(doc, code_field, file_timestamp):
	import webnotes, os, webnotes.utils, webnotes.defs
	
	# get the code
	fn = get_code_path(doc, code_field)
	file = open(fn,'r')
	code = file.read()
	file.close()
	
	# update in database, clear cache
	if doc.doctype=='Control Panel':
		webnotes.conn.set_value('Control Panel',None,code_field[0],code)
	else:
		webnotes.conn.sql("update tab%s set %s=%s, modified=%s where name=%s" % (doc.doctype, code_field[0], '%s', '%s', '%s'), (code, doc.name, webnotes.utils.now()))
		webnotes.conn.sql("delete from __DocTypeCache")
	
	# update in doc
	doc.fields[code_field[0]] = code
	
	# update timestamp
	update_timestamp(doc, code_field, file_timestamp)

# -------------------------------------------------

def update_timestamp(doc, code_field, file_timestamp):
	import webnotes
	# update or insert
	if webnotes.conn.sql("select name from __CodeFileTimeStamps where doctype=%s and name=%s and code_field=%s", (doc.doctype, doc.name, code_field[0])):
		webnotes.conn.sql("update __CodeFileTimeStamps set `timestamp`=%s where doctype=%s and name=%s and code_field=%s", (file_timestamp, doc.doctype, doc.name, code_field[0]))
	else:
		webnotes.conn.sql("insert into __CodeFileTimeStamps (`timestamp`, doctype, name, code_field) values (%s, %s, %s, %s)", (file_timestamp, doc.doctype, doc.name, code_field[0]))

# -------------------------------------------------

def get_code_path(doc, code_field):
	import webnotes.defs, os
	fname = doc.name
	if code_field[0]=='static_content':
		fname+=' Static'

	return os.path.join(webnotes.defs.modules_path, doc.module or 'System', doc.doctype, doc.name, fname) \
		+ '.' + code_field[1]
