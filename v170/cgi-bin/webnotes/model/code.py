
#=================================================================================

def execute(code, doc=None, doclist=[]):

	# functions used in server script of DocTypes
	# --------------------------------------------------	
	from webnotes.utils import add_days, add_months, add_years, cint, cstr, date_diff, default_fields, flt, fmt_money, formatdate, generate_hash, getTraceback, get_defaults, get_first_day, get_last_day, getdate, has_common, month_name, now, nowdate, replace_newlines, sendmail, set_default, str_esc_quote, user_format, validate_email_add
	from webnotes.model import db_exists
	from webnotes.model.doc import Document, addchild, removechild, getchildren, make_autoname, SuperDocType
	from webnotes.model.doclist import getlist, copy_doclist
	from webnotes import session, form, is_testing, msgprint, errprint

	import webnotes

	set = webnotes.conn.set
	sql = webnotes.conn.sql
	get_value = webnotes.conn.get_value
	in_transaction = webnotes.conn.in_transaction
	convert_to_lists = webnotes.conn.convert_to_lists
	if webnotes.user:
		get_roles = webnotes.user.get_roles
	locals().update({'get_obj':get_obj, 'get_server_obj':get_server_obj, 'run_server_obj':run_server_obj, 'updatedb':updatedb, 'check_syntax':check_syntax})
		
	version = 'v170'
	NEWLINE = '\n'
	BACKSLASH = '\\'

	# execute it
	# -----------------
	exec code in locals()
	
	# if doc
	# -----------------
	if doc:
		d = DocType(doc, doclist)
		return d
		
	if locals().get('page_html'):
		return page_html

	if locals().get('out'):
		return out

#=================================================================================

def get_recompiled_code(dt):
	# clear from cache
	import webnotes
	webnotes.conn.sql("delete from __DocTypeCache where name=%s", dt)
	
	# compile
	import webnotes.model.doctype
	webnotes.model.doctype.get(dt)

	# load
	return webnotes.conn.sql("select server_code_compiled from __DocTypeCache where name=%s", dt)[0][0]

#=================================================================================

def get_server_obj(doc, doclist = [], basedoctype = ''):
	import marshal
	import webnotes
	
	dt = basedoctype and basedoctype or doc.doctype

	# load from application or main
	sc_compiled = None
	
	try:
		# get compiled code
		sc_compiled = webnotes.conn.sql("select server_code_compiled from __DocTypeCache where name=%s", dt)[0][0]
		#	sc_compiled = None
			
	except:
		# no code yet
		sc_compiled = None

	if not sc_compiled:
		sc_compiled = get_recompiled_code(dt)

	try:
		return execute(marshal.loads(sc_compiled), doc, doclist)
	except TypeError, e:
		# error? re-compile

		sc_compiled = get_recompiled_code(dt)
		return execute(marshal.loads(sc_compiled), doc, doclist)
		
#=================================================================================

def get_obj(dt = None, dn = None, doc=None, doclist=[], with_children = 0):
	if dt:
		import webnotes.model.doc
	
		if not dn:
			dn = dt
		if with_children:
			doclist = webnotes.model.doc.get(dt, dn, from_get_obj=1)
		else:
			doclist = webnotes.model.doc.get(dt, dn, with_children = 0, from_get_obj=1)
		return get_server_obj(doclist[0], doclist)
	else:
		return get_server_obj(doc, doclist)

#=================================================================================

def run_server_obj(server_obj, method_name, arg=None):
	if server_obj and hasattr(server_obj, method_name):
		if arg:
			return getattr(server_obj, method_name)(arg)
		else:
			return getattr(server_obj, method_name)()


# deprecated methods to keep v160 apps happy
#=================================================================================

def updatedb(doctype, userfields = [], args = {}):
	pass

def check_syntax(code):
	return ''
