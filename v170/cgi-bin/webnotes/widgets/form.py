import webnotes
import webnotes.model.doc
import webnotes.model.meta

def getdoc():
	import webnotes
	
	form = webnotes.form
	doctype, docname = form.getvalue('doctype'), form.getvalue('name')

	if not (doctype and docname):
		raise Exception, 'doctype and name required!'
	
	doclist = []
	doclist = load_single_doc(doctype, docname, (form.getvalue('user') or webnotes.session['user']))
	
	# get comments
	webnotes.response['no_of_comments'] = get_comments(doctype, docname)
	
	if form.getvalue('getdoctype'):
		import webnotes.model.doctype
		doclist += webnotes.model.doctype.get(doctype)

	webnotes.response['docs'] = doclist

def get_comments(doctype, docname):
	try:
		return int(webnotes.conn.sql("select count(*) from `tabComment Widget Record` where comment_doctype=%s and comment_docname=%s", (doctype, docname))[0][0])
	except Exception, e:
		if e.args[0]==1146:
			# no table
			return -1
		else:
			raise e
	

#===========================================================================================

def getdoctype():
	# load parent doctype too
	import webnotes.model.doctype
	
	form, doclist = webnotes.form, []
	
	dt = form.getvalue('doctype')
	with_parent = form.getvalue('with_parent')

	# with parent (called from report builder)
	if with_parent:
		parent_dt = webnotes.model.meta.get_parent_dt(dt)
		if parent_dt:
			doclist = webnotes.model.doctype.get(parent_dt)
			webnotes.response['parent_dt'] = parent_dt
	
	if not doclist:
		doclist = webnotes.model.doctype.get(dt)
	
	# if single, send the record too
	if doclist[0].issingle:
		doclist += webnotes.model.doc.get(dt)

	# load search criteria for reports (all)
	doclist += webnotes.model.meta.get_search_criteria(dt)

	webnotes.response['docs'] = doclist

#===========================================================================================

def load_single_doc(dt, dn, user):
	import webnotes.model.code

	if not dn: dn = dt
	dl = webnotes.model.doc.get(dt, dn)

	try:
		so = webnotes.model.code.get_server_obj(dl[0], dl)
		r = webnotes.model.code.run_server_obj(so, 'onload')
		if hasattr(so, 'custom_onload'):
			r = webnotes.model.code.run_server_obj(so, 'custom_onload')
		if r: 
			webnotes.msgprint(r)
	except Exception, e:
		webnotes.errprint(webnotes.utils.getTraceback())
		webnotes.msgprint('Error in script while loading')
		raise e

	if dl and not dn.startswith('_'):
		webnotes.user.update_recent(dt, dn)

	# load search criteria ---- if doctype
	if dt=='DocType':
		dl += webnotes.model.meta.get_search_criteria(dt)

	return dl

# Check Guest Access
#===========================================================================================
def check_guest_access(doc):
	if webnotes.session['user']=='Guest' and not webnotes.conn.sql("select name from tabDocPerm where role='Guest' and parent=%s and ifnull(`read`,0)=1", doc.doctype):
		webnotes.msgprint("Guest not allowed to call this object")
		raise Exception

# Runserverobj - run server calls from form
#===========================================================================================

def runserverobj():
	import webnotes.model.code
	import webnotes.model.doclist
	from webnotes.utils import cint

	form = webnotes.form

	method = form.getvalue('method')
	doclist, clientlist = [], []
	arg = form.getvalue('arg')
	dt = form.getvalue('doctype')
	dn = form.getvalue('docname')
		
	if dt: # not called from a doctype (from a page)
		if not dn: dn = dt # single
		so = webnotes.model.code.get_obj(dt, dn)
	else:
		clientlist = webnotes.model.doclist.expand(form.getvalue('docs'))

		# find main doc
		for d in clientlist:
			if cint(d.get('docstatus')) != 2 and not d.get('parent'):
				main_doc = webnotes.model.doc.Document(fielddata = d)
	
		# find child docs
		for d in clientlist:
			doc = webnotes.model.doc.Document(fielddata = d)
			if doc.fields.get('parent'):
				doclist.append(doc)	
	
		so = webnotes.model.code.get_server_obj(main_doc, doclist)

	# check integrity
	if not check_integrity(so.doc):
		return
		
	check_guest_access(so.doc)
				
	if so:
		r = webnotes.model.code.run_server_obj(so, method, arg)
		doclist = so.doclist # reference back [in case of null]
		if r:
			try:
				if r['doclist']:
					clientlist += r['doclist']
			except:
				pass
			
			#build output as csv
			if cint(webnotes.form.getvalue('as_csv')):
				make_csv_output(r, so.doc.doctype)
			else:
				webnotes.response['message'] = r
		
		if clientlist:
			doclist.append(main_doc)
			webnotes.response['docs'] = doclist

def make_csv_output(res, dt):
	import webnotes
	from webnotes.utils import getCSVelement

	txt = []
	if type(res)==list:
		for r in res:
			txt.append(','.join([getCSVelement(i) for i in r]))
		
		txt = '\n'.join(txt)
	
	else:
		txt = 'Output was not in list format\n' + r
					
	webnotes.response['result'] = txt
	webnotes.response['type'] = 'csv'
	webnotes.response['doctype'] = dt.replace(' ','')						


# Document Save
#===========================================================================================

def _get_doclist(clientlist):
	# converts doc dictionaries into Document objects

	from webnotes.model.doc import Document
	form = webnotes.form

	midx = 0
	for i in range(len(clientlist)):
		if clientlist[i]['name'] == form.getvalue('docname'):
			main_doc = Document(fielddata = clientlist[i])
			midx = i
		else:
			clientlist[i] = Document(fielddata = clientlist[i])

	del clientlist[midx]
	return main_doc, clientlist

def _do_action(doc, doclist, so, method_name, docstatus=0):
	from webnotes.model.code import run_server_obj
	set = webnotes.conn.set

	if so and hasattr(so, method_name):
		errmethod = method_name
		run_server_obj(so, method_name)
		if hasattr(so, 'custom_'+method_name):
			run_server_obj(so, 'custom_'+method_name)
		errmethod = ''

	# set docstatus for all children records
	if docstatus:
		for d in [doc] + doclist:
			if int(d.docstatus or 0) != 2:
				set(d, 'docstatus', docstatus)

def check_integrity(doc):
	import webnotes
		
	if (not webnotes.model.meta.is_single(doc.doctype)) and (not doc.fields.get('__islocal')):
		tmp = webnotes.conn.sql('SELECT modified FROM `tab%s` WHERE name="%s"' % (doc.doctype, doc.name))
		if tmp and str(tmp[0][0]) != str(doc.modified):
			webnotes.msgprint('Document has been modified after you have opened it. To maintain the integrity of the data, you will not be able to save your changes. Please refresh this document. [%s/%s]' % (tmp[0][0], doc.modified))
			return 0
			
	return 1

#===========================================================================================

def savedocs():
	import webnotes.model.doclist

	from webnotes.model.code import get_server_obj
	from webnotes.model.code import run_server_obj
	import webnotes.utils

	from webnotes.utils import cint

	sql = webnotes.conn.sql
	form = webnotes.form

	# action
	action = form.getvalue('action')
	
	# get docs	
	doc, doclist = _get_doclist(webnotes.model.doclist.expand(form.getvalue('docs')))

	# get server object	
	server_obj = get_server_obj(doc, doclist)

	# check integrity
	if not check_integrity(doc):
		return
	
	if not doc.check_perm(verbose=1):
		webnotes.msgprint("Not enough permission to save %s" % doc.doctype)
		return
	
	# validate links
	ret = webnotes.model.doclist.validate_links_doclist([doc] + doclist)
	if ret:
		webnotes.msgprint("[Link Validation] Could not find the following values: %s. Please correct and resave. Document Not Saved." % ret)
		return

	# saving & post-saving
	try:
		# validate befor saving and submitting
		if action in ('Save', 'Submit') and server_obj:
			if hasattr(server_obj, 'validate'):	
				t = run_server_obj(server_obj, 'validate')
			if hasattr(server_obj, 'custom_validate'):
				t = run_server_obj(server_obj, 'custom_validate')
				
		# set owner and modified times
		is_new = cint(doc.fields.get('__islocal'))
		if is_new and not doc.owner:
			doc.owner = form.getvalue('user')
		
		doc.modified, doc.modified_by = webnotes.utils.now(), webnotes.session['user']
		
		# save main doc
		try:
			t = doc.save(is_new)
		except NameError, e:
			webnotes.msgprint('%s "%s" already exists' % (doc.doctype, doc.name))
			if webnotes.conn.sql("select docstatus from `tab%s` where name=%s" % (doc.doctype, '%s'), doc.name)[0][0]==2:
				webnotes.msgprint('[%s "%s" has also been trashed / cancelled]' % (doc.doctype, doc.name))
			webnotes.errprint(webnotes.utils.getTraceback())
			raise e
		
		# save child docs
		for d in doclist:
			deleted, local = d.fields.get('__deleted',0), d.fields.get('__islocal',0)
	
			if cint(local) and cint(deleted):
				pass
			elif d.fields.has_key('parent'):
				if d.parent and (not d.parent.startswith('old_parent:')):
					d.parent = doc.name # rename if reqd
					d.parenttype = doc.doctype
				d.modified, d.modified_by = webnotes.utils.now(), webnotes.session['user']
				d.save(new = cint(local))
	
		# on_update
		if action in ('Save','Submit') and server_obj:
			# special for DocType, DocType
			if doc.doctype == 'DocType':
				import webnotes.model.doctype
				webnotes.model.doctype.update_doctype([doc] + doclist)
				
			else:				
				if hasattr(server_obj, 'on_update'):
					t = run_server_obj(server_obj, 'on_update')
					if t: webnotes.msgprint(t)
	
				if hasattr(server_obj, 'custom_on_update'):
					t = run_server_obj(server_obj, 'custom_on_update')
					if t: webnotes.msgprint(t)
				
		# on_submit
		if action == 'Submit':
			_do_action(doc, doclist, server_obj, 'on_submit', 1)

		# on_submit
		if action == 'Update':
			_do_action(doc, doclist, server_obj, 'on_update_after_submit', 0)
				
		# on_cancel
		if action == 'Cancel':
			_do_action(doc, doclist, server_obj, 'on_cancel', 2)
		
		# On Trash
		if action == 'Trash':
			_do_action(doc, doclist, server_obj, 'on_trash', 2)
			# validate
			validate_trash_doc(doc, doclist)

		# update recent documents
		webnotes.user.update_recent(doc.doctype, doc.name)

		# send updated docs
		webnotes.response['saved'] = '1'
		webnotes.response['main_doc_name'] = doc.name
		webnotes.response['docname'] = doc.name
		webnotes.response['docs'] = [doc] + doclist

	except Exception, e:
		webnotes.msgprint('Did not save')
		webnotes.errprint(webnotes.utils.getTraceback())
		raise e

# validate if linked to another document
#========================================
def validate_trash_doc(doc, doclist):
	import webnotes
	conn = webnotes.conn
	# Fetch docs contains link of trash doc
	parent_mast = conn.sql("select t1.parent, t1.fieldname from tabDocField t1, tabDocType t2 where ((t1.fieldtype = 'Link' and t1.options = '%s') or (t1.fieldtype = 'Select' and t1.options = 'link:%s')) and t1.parent not like 'old%%' and ifnull(t2.allow_trash, 0) = 1 and t1.parent = t2.name" % (doc.doctype, doc.doctype))
	for d in parent_mast:
		# check if records
		check_if_rec_exist(doc, d[0], d[1])

		#Child table contains link of trash doc
		ch_table = webnotes.model.meta.get_table_fields(d[0])
		for c in ch_table:
			# fieldname
			fld = conn.sql("select fieldname from tabDocField where ((fieldtype = 'Link' and options = '%s') or (fieldtype = 'Select' and options = 'link:%s')) and parent not like 'old%%' and parent = '%s'" % (doc.doctype, doc.doctype, c[0]))
			for f in fld:
				# check if records
				check_if_rec_exist(doc, c[0], f[0], d[0])
				
# Check whether record exists using trash doc
#=============================================
def check_if_rec_exist(doc, dtname, fname, par_dtname = ''):
	import webnotes

	if not par_dtname: par_dtname = dtname
	# exists?
	exists = [r[0] for r in webnotes.conn.sql('select name from `tab%s` where docstatus != 2 and %s = "%s"' % (dtname, fname, doc.name))]
	if exists:
		webnotes.msgprint("This record exists in %s : %s. Hence you cannot move %s : %s to trash." %(dtname, exists, doc.doctype, doc.name))
		raise Exception


# Print Format
#===========================================================================================
def _get_print_format(match):
	name = match.group('name')
	return webnotes.model.meta.get_print_format_html(name)

def get_print_format():
	import re
	import webnotes

	html = webnotes.model.meta.get_print_format_html(webnotes.form.getvalue('name'))

	p = re.compile('\$import\( (?P<name> [^)]*) \)', re.VERBOSE)
	if html: out_html = p.sub(_get_print_format, html)

	webnotes.response['message'] = out_html
	
# remove attachment
#===========================================================================================

def remove_attach():
	import webnotes
	import webnotes.utils.file_manager
	
	fid = webnotes.form.getvalue('fid')
	webnotes.utils.file_manager.delete_file(fid, verbose=1)

# Get Fields - Counterpart to $c_get_fields
#===========================================================================================
def get_fields():
	import webnotes
	r = {}
	args = {
		'select':form.getvalue('select')
		,'from':form.getvalue('from')
		,'where':form.getvalue('where')
	}
	ret = webnotes.conn.sql("select %(select)s from `%(from)s` where %(where)s limit 1" % args)
	if ret:
		fl, i = webnotes.form.getvalue('fields').split(','), 0
		for f in fl:
			r[f], i = ret[0][i], i+1
	webnotes.response['message']=r

# validate link
#===========================================================================================
def validate_link():
	import webnotes
	import webnotes.utils
	
	value, options, fetch = webnotes.form.getvalue('value'), webnotes.form.getvalue('options'), webnotes.form.getvalue('fetch')

	# no options, don't validate
	if not options or options=='null' or options=='undefined':
		webnotes.response['message'] = 'Ok'
		return
		
	if webnotes.conn.sql("select name from `tab%s` where name=%s" % (options, '%s'), value):
	
		# get fetch values
		if fetch:
			webnotes.response['fetch_values'] = [webnotes.utils.parse_val(c) for c in webnotes.conn.sql("select %s from `tab%s` where name=%s" % (fetch, options, '%s'), value)[0]]
	
		webnotes.response['message'] = 'Ok'
