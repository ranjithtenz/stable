# =============================================================================
# Import a record (with its chilren)
# =============================================================================
def set_doc(doclist, ovr=0, ignore=1, onupdate=1):
	import webnotes
	from webnotes.model.doc import Document
	from webnotes.model.code import get_obj
	from webnotes.model.code import get_server_obj
	from webnotes.model.meta import get_table_fields

	sql = webnotes.conn.sql

	if not doclist:
		return 'No Doclist'

	doc = Document(fielddata = doclist[0])
	orig_modified = doc.modified

	exists = webnotes.conn.exists(doc.doctype, doc.name)
	#print doc.doctype, doc.name
	if not webnotes.conn.in_transaction: 
		sql("START TRANSACTION")
	
	if exists:
		 
		if ovr:
			if doc.doctype == 'DocType':
				return merge_doctype(doclist, ovr, ignore, onupdate) 

			if doc.doctype == 'DocType Mapper':
				return merge_mapper(doclist, ovr, ignore, onupdate)

			if doc.doctype == 'Module Def':
				return merge_module_def(doclist, ovr, ignore, onupdate)
			
					
			# check modified timestamp
			# ------------------------
			ts = sql("select modified from `tab%s` where name=%s" % (doc.doctype, '%s'), doc.name)[0][0]
			if str(ts)==doc.modified:
				return doc.name + ": No update"

			# Replace the record
			# ------------------

			# remove main doc
			newname = '__overwritten:'+doc.name
			n_records = sql("SELECT COUNT(*) from `tab%s` WHERE name like '%s%%'" % (doc.doctype, newname))
			if n_records[0][0]:
				newname = newname + '-' + str(n_records[0][0])
				
			sql("UPDATE `tab%s` SET name='%s', docstatus=2 WHERE name = '%s' limit 1" % (doc.doctype, newname, doc.name))
			
			# remove child elements
			tf_list = get_table_fields(doc.doctype)
			for t in tf_list:
				sql("UPDATE `tab%s` SET parent='%s', docstatus=2 WHERE parent='%s' AND parentfield='%s'" % (t[0], 'oldparent:'+doc.name, doc.name, t[1]))
				
		else:
			if webnotes.conn.in_transaction: 
				sql("ROLLBACK")
			return doc.name + ": Exists / No change"

	# save main
	check_links = 1	
	if doc.doctype == 'Patch':
		doc.save(make_autoname = 0, new = 1, ignore_fields = ignore, check_links=0)
	else:
		doc.save(new = 1, ignore_fields = ignore, check_links=0)
	
	# save others
	dl = [doc]
	for df in doclist[1:]:
		try:
			d = Document(fielddata = df)
			d.save(new = 1, ignore_fields = ignore, check_links=0)
			dl.append(d)
		except:
			pass # ignore tables
	
	if onupdate:
		if doc.doctype=='DocType':
			import webnotes.model.doctype
			webnotes.model.doctype.update_doctype(dl)
		else:
			so = get_server_obj(doc, dl)
			if hasattr(so, 'on_update'):
				so.on_update()
			
		
	# reset modified
	webnotes.conn.set(doc, 'modified', orig_modified)

	if webnotes.conn.in_transaction: 
		sql("COMMIT")

	return doc.name + ': Completed'


# =============================================================================
# Transfer DocType
# =============================================================================
def merge_doctype(doc_list, ovr, ignore, onupdate):
	import webnotes
	from webnotes.model.doc import Document
	from webnotes.model import doclist
	from webnotes.utils import cint
	from webnotes.utils import cstr
	
	doc_list = [Document(fielddata = d) for d in doc_list]
	
	doc = doc_list[0]
	orig_modified = doc.modified
	cur_doc = Document('DocType',doc.name)
	added = 0
	prevfield = ''
	prevlabel = ''
	idx = 0
	fld_lst = ''
	
	sql = webnotes.conn.sql

	# fields
	# ------
	for d in doclist.getlist(doc_list, 'fields'):
		fld = ''
		# if exists
		if d.fieldname:
			fld = sql("select name from tabDocField where fieldname=%s and parent=%s", (d.fieldname, d.parent))
		elif d.label: # for buttons where there is no fieldname
			fld = sql("select name from tabDocField where label=%s and parent=%s", (d.label, d.parent))

		if (not fld) and d.label: # must have label
			if prevfield:
				idx = sql("select idx from tabDocField where fieldname = %s and parent = %s",(prevfield,d.parent))[0][0]
			elif prevlabel and not prevfield:
				idx = sql("select idx from tabDocField where label = %s and parent = %s",(prevlabel,d.parent))[0][0]
			sql("update tabDocField set idx = idx + 1 where parent=%s and idx > %s", (d.parent, cint(idx)))					

			# add field
			nd = Document(fielddata = d.fields)
			nd.oldfieldname, nd.oldfieldtype = '', ''
			nd.idx = cint(idx)+1
			nd.save(new = 1, ignore_fields = ignore, check_links = 0)
			fld_lst += 'Label : '+cstr(d.label)+'	 ---	 Fieldtype : '+cstr(d.fieldtype)+'	 ---	 Fieldname : '+cstr(d.fieldname)+'	 ---	 Options : '+cstr(d.options)
			added += 1
			
		# clean up
		if d.fieldname:
			prevfield = d.fieldname
			prevlabel = ''
		elif d.label:
			prevfield = ''
			prevlabel = d.label
			
	# Print Formats
	# -------------
	for d in doclist.getlist(doc_list, 'formats'):
		fld = ''
		# if exists
		if d.format:
			fld = sql("select name from `tabDocFormat` where format=%s and parent=%s", (d.format, d.parent))
					
		if (not fld) and d.format: # must have label
			# add field
			nd = Document(fielddata = d.fields)
			nd.oldfieldname, nd.oldfieldtype = '', ''
			nd.save(new = 1, ignore_fields = ignore, check_links = 0)
			fld_lst = fld_lst + '\n'+'Format : '+cstr(d.format)
			added += 1
				
	# code
	# ----
	
	cur_doc.server_code_core = cstr(doc.server_code_core)
	cur_doc.client_script_core = cstr(doc.client_script_core)
	cur_doc.module = doc.module
	cur_doc.save(ignore_fields = ignore, check_links = 0)	
	

	# update schema
	# -------------
	import webnotes.model
	try:
		dl = webnotes.model.doc.get('DocType', doc.name)
		webnotes.model.doctype.update_doctype(dl)
	except:
		pass
	
	webnotes.conn.set(doc,'modified',orig_modified)
	
	if webnotes.conn.in_transaction: sql("COMMIT")
	
	if added == 0:
		added_fields = ''
	else:
		added_fields =	' Added Fields :'+ cstr(fld_lst)
		
	return doc.name + (' Upgraded: %s fields added' % added)+added_fields
	
	
# =============================================================================
# Transfer Mapper
# =============================================================================

def merge_mapper(doc_list, ovr, ignore, onupdate):
	import webnotes
	from webnotes.model.doc import Document
	from webnotes.model import doclist
	from webnotes.model.code import get_obj
	from webnotes.utils import cint
	from webnotes.utils import cstr
	import webnotes.db
	doc_list = [Document(fielddata = d) for d in doc_list]
	doc = doc_list[0]
	orig_modified = doc.modified
	cur_doc = Document('DocType Mapper',doc.name)
	added = 0
	fld_lst = ''
		
	sql = webnotes.conn.sql
	
	# Field Mapper Details fields
	# ------
	for d in doclist.getlist(doc_list, 'field_mapper_details'):
		fld = ''
		# if exists
		if d.from_field and d.to_field:
			fld = sql("select name from `tabField Mapper Detail` where from_field=%s and to_field=%s and parent=%s", (d.from_field, d.to_field, d.parent))
					
		if (not fld) and d.from_field and d.to_field: # must have label
			# add field
			nd = Document(fielddata = d.fields)
			nd.oldfieldname, nd.oldfieldtype = '', ''
			nd.save(new = 1, ignore_fields = ignore, check_links = 0)
			fld_lst += '\n'+'From Field : '+cstr(d.from_field)+'	 ---	 To Field : '+cstr(d.to_field)
			added += 1
			
	# Table Mapper Details fields
	# ------
	for d in doclist.getlist(doc_list, 'table_mapper_details'):
		fld = ''
		# if exists
		if d.from_table and d.to_table: 
			fld = sql("select name from `tabTable Mapper Detail` where from_table=%s and to_table = %s and parent=%s", (d.from_table, d.to_table, d.parent))
					
		if (not fld) and d.from_table and d.to_table: # must have label
			# add field
			nd = Document(fielddata = d.fields)
			nd.oldfieldname, nd.oldfieldtype = '', ''
			nd.save(new = 1, ignore_fields = ignore, check_links = 0)
			fld_lst += '\n'+'From Table : '+cstr(d.from_table)+'	 ---	 To Table : '+cstr(d.to_table)
			added += 1
					 
	cur_doc.save(ignore_fields = ignore, check_links = 0)
	
	if onupdate:
		so = get_obj('DocType Mapper', doc.name, with_children = 1)
		if hasattr(so, 'on_update'):
			so.on_update()
	
	webnotes.conn.set(doc,'modified',orig_modified)
	
	if webnotes.conn.in_transaction: sql("COMMIT")
	
	if added == 0:
		added_fields = ''
	else:
		added_fields =	' Added Fields:'+ cstr(fld_lst)
	return doc.name + ('Upgraded: %s fields added' % added)+added_fields

	added = 0
	fld_lst = ''
		
	sql = webnotes.conn.sql
	
	# Field Mapper Details fields
	# ------
	for d in doclist.getlist(doc_list, 'field_mapper_details'):
		fld = ''
		# if exists
		if d.from_field and d.to_field:
			fld = sql("select name from `tabField Mapper Detail` where from_field=%s and to_field=%s and parent=%s", (d.from_field, d.to_field, d.parent))
					
		if (not fld) and d.from_field and d.to_field: # must have label
			# add field
			nd = Document(fielddata = d.fields)
			nd.oldfieldname, nd.oldfieldtype = '', ''
			nd.save(new = 1, ignore_fields = ignore, check_links = 0)
			fld_lst += '\n'+'From Field : '+cstr(d.from_field)+'	 ---	 To Field : '+cstr(d.to_field)
			added += 1
			
	# Table Mapper Details fields
	# ------
	for d in doclist.getlist(doc_list, 'table_mapper_details'):
		fld = ''
		# if exists
		if d.from_table and d.to_table: 
			fld = sql("select name from `tabTable Mapper Detail` where from_table=%s and to_table = %s and parent=%s", (d.from_table, d.to_table, d.parent))
					
		if (not fld) and d.from_table and d.to_table: # must have label
			# add field
			nd = Document(fielddata = d.fields)
			nd.oldfieldname, nd.oldfieldtype = '', ''
			nd.save(new = 1, ignore_fields = ignore, check_links = 0)
			fld_lst += '\n'+'From Table : '+cstr(d.from_table)+'	 ---	 To Table : '+cstr(d.to_table)
			added += 1
					 
	cur_doc.save(ignore_fields = ignore, check_links = 0)
	
	if onupdate:
		so = get_obj('DocType Mapper', doc.name, with_children = 1)
		if hasattr(so, 'on_update'):
			so.on_update()
	
	webnotes.conn.set(doc,'modified',orig_modified)
	
	if webnotes.conn.in_transaction: sql("COMMIT")
	
	if added == 0:
		added_fields = ''
	else:
		added_fields =	' Added Fields:'+ cstr(fld_lst)
	return doc.name + ('Upgraded: %s fields added' % added)+added_fields

# =============================================================================
# Transfer Module Def
# =============================================================================
def merge_module_def(doc_list, ovr, ignore, onupdate):
	import webnotes
	from webnotes.model.doc import Document
	from webnotes.model import doclist
	from webnotes.model.code import get_obj
	from webnotes.utils import cint
	from webnotes.utils import cstr
	import webnotes.db
	doc_list = [Document(fielddata = d) for d in doc_list]
	doc = doc_list[0]
	orig_modified = doc.modified
	cur_doc = Document('Module Def',doc.name)
	added, idx = 0, 0
	fld_lst, prev_dt, prev_dn, prev_dis_name = '', '', '', ''
		
	sql = webnotes.conn.sql
	
	# Module Def Item table fields
	for d in doclist.getlist(doc_list, 'items'):
		fld = ''
		# if exists
		if d.doc_type and d.doc_name:
			fld = sql("select name from `tabModule Def Item` where doc_type=%s and doc_name=%s and ifnull(display_name,'') = %s and parent=%s", (d.doc_type, d.doc_name, cstr(d.display_name), d.parent))
					
		if (not fld) and d.doc_type and d.doc_name:
			if prev_dt and prev_dn:
				idx = sql("select idx from `tabModule Def Item` where doc_type = %s and doc_name = %s and ifnull(display_name,'') = %s and parent = %s",(prev_dt, prev_dn, cstr(prev_dis_name), d.parent))[0][0]
			sql("update `tabModule Def Item` set idx = idx + 1 where parent=%s and idx > %s", (d.parent, cint(idx)))
			# add field
			nd = Document(fielddata = d.fields)
			nd.oldfieldname, nd.oldfieldtype = '', ''
			nd.idx = cint(idx)+1
			nd.save(new = 1, ignore_fields = ignore, check_links = 0)
			fld_lst += '\n'+'Doc Type : '+cstr(d.doc_type)+'   ---	 Doc Name : '+cstr(d.doc_name)+'   ---	 Display Name : '+cstr(d.display_name)
			added += 1

		# clean up
		prev_dt = d.doc_type
		prev_dn = d.doc_name
		prev_dis_name = cstr(d.display_name)

	cur_doc.widget_code = cstr(doc.widget_code)
	cur_doc.save(ignore_fields = ignore, check_links = 0)
	
	if onupdate:
		so = get_obj('Module Def', doc.name, with_children = 1)
		if hasattr(so, 'on_update'):
			so.on_update()
	
	webnotes.conn.set(doc,'modified',orig_modified)
	
	if webnotes.conn.in_transaction: sql("COMMIT")
	
	if added == 0:
		added_fields = ''
	else:
		added_fields =	' Added Fields:'+ cstr(fld_lst)
	return doc.name + ('Upgraded: %s fields added' % added)+added_fields
	
	
# =============================================================================
# Execute Patches
# =============================================================================
def execute_patches(modules,record_list):
	import webnotes
	from webnotes.model import code
	
	ret = {}
	try:
		patch_list, ret = get_patch_list(modules, record_list, ret)
	except Exception, e:
		if e.args[0]==1146:
			return 'No table Patch'
		else:
			raise e
	
	for d in patch_list:
		try:
			if not webnotes.conn.in_transaction:
				webnotes.conn.sql("START TRANSACTION")
			#print 'Patch: ' + d[0]
			ret_msg = code.execute(d[1])
			webnotes.conn.sql("update tabPatch set status = 'Executed' where name = %s", d[0])
			webnotes.conn.sql("COMMIT")
		except Exception, e:
			ret_msg = e
		#finally: #Only works on python 2.5+
		ret[d[0]] = ret_msg

	return ret


# =============================================================================
# Get patch list
# =============================================================================
def get_patch_list(modules, record_list, ret):
	import webnotes
	patch_list = [] 
	if modules:
		for each in modules:
			patch_list += [[d[0], d[1]] for d in webnotes.conn.sql("select name, patch_code from `tabPatch` where module = %s and status = 'Ready'",each)]

	if record_list:
		for each in record_list:
			if each[0] == 'Patch':
				cd = webnotes.conn.sql("select patch_code from tabPatch where name = %s and status = 'Ready'", each[1])
				if cd:
					patch_list.append([each[1], cd[0][0]]) 
				else:
					ret[each[1]] = 'Patch is not ready'
					
	return patch_list, ret
	
	
# =============================================================================
# Sync control panel
# =============================================================================
def sync_control_panel(startup_code, startup_css):
	import webnotes
	webnotes.conn.sql("start transaction")
	webnotes.conn.set_value('Control Panel', None, 'startup_code', startup_code)
	webnotes.conn.set_value('Control Panel', None, 'startup_css', startup_css)
	webnotes.conn.sql("commit")
