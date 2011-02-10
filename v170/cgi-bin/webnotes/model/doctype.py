# DocType module
# 
# This module has the DocType class that represents a "DocType" as metadata
# This is usually called by the form builder or report builder
#
# Key functions:
#	- manage cache - read / write
#	- merge client-side scripts
#	- compile server-side code
#	- call updation of database schema
#
# Cache management:
#	- Cache is stored in __DocTypeCache
#
# =================================================================


import webnotes
import webnotes.model
import webnotes.model.doclist
import webnotes.model.doc

from webnotes.utils import cstr

class _DocType:
	def __init__(self, name):
		self.name = name
	
	# is cache modified ?
	# =================================================================
	
	def is_modified(self):
		is_modified = 0
		
		# doctype modified
		modified = webnotes.model.meta.get_dt_values(self.name, 'modified')
		modified = modified and modified[0][0] or None

		# cache modified
		cache_modified = webnotes.conn.sql("SELECT modified from `__DocTypeCache` where name='%s'" % self.name)

		if not cache_modified or not (cache_modified and modified==cache_modified[0][0]):
			is_modified = 1

		return modified, is_modified, cache_modified

	# write to cache
	# =================================================================

	def _update_cache(self, is_cache_modified, modified, doclist):
		import zlib

		if not is_cache_modified:
			webnotes.conn.sql("INSERT INTO `__DocTypeCache` (`name`) VALUES ('%s')" % self.name)
		webnotes.conn.sql("UPDATE `__DocTypeCache` SET `modified`=%s, `content`=%s WHERE name=%s", (modified, zlib.compress(str([d.fields for d in doclist]),2), self.name))

		# cache the code
		self.compile_code(doclist[0])

	# read from cache
	# =================================================================

	def _load_from_cache(self):
		import zlib
	
		doclist = eval(zlib.decompress(webnotes.conn.sql("SELECT content from `__DocTypeCache` where name=%s", self.name)[0][0]))
		return [webnotes.model.doc.Document(fielddata = d) for d in doclist]

	# build client scripts
	# =================================================================

	def _get_client_script(self, match):		
		name = match.group('name')

		csc = str(webnotes.model.meta.get_dt_values(name, 'client_script_core')[0][0] or '')
		cs = str(webnotes.model.meta.get_dt_values(name, 'client_script')[0][0] or '')

		return csc + '\n' + cs
		
	def _build_client_script(self, doclist):
		client_script = [str(doclist[0].client_script_core or ''), str(doclist[0].client_script or '')]

		# make into a single script
		client_script = '\n'.join(client_script)
		
		# compile for import
		if client_script.strip():
			import re
			p = re.compile('\$import\( (?P<name> [^)]*) \)', re.VERBOSE)
	
			# load it in __client_script as it will not interfere with the doctype
			doclist[0]._client_script = p.sub(self._get_client_script, client_script)

	# load options for "link:" type 'Select' fields
	# =================================================================
			
	def _load_select_options(self, doclist):
		for d in doclist:
			if d.doctype=='DocField' and d.fieldtype=='Select' and d.options and d.options[:5].lower()=='link:':
				op = d.options.split('\n')
				if len(op)>1 and op[1][:4].lower() == 'sql:':
					ol = webnotes.conn.sql(op[1][4:].replace('__user', webnotes.session['user']))	
				else:
					t = op[0][5:].strip()
					op = op[1:]
					op = [oc.replace('__user', webnotes.session['user']) for oc in op]
					
					try:
						# select options will always come from the user db
						ol = webnotes.conn.sql("select name from `tab%s` where %s docstatus!=2 order by name asc" % (t, op and (' AND '.join(op) + ' AND ') or ''))
					except:
						ol = []
				ol = [''] + [o[0] or '' for o in ol]
				d.options = '\n'.join(ol)

	# clear un-necessary code from going to the client side
	# =================================================================

	def _clear_code(self, doclist):
		if self.name != 'DocType':
			if doclist[0].server_code: doclist[0].server_code = None
			if doclist[0].server_code_core: doclist[0].server_code_core = None
			if doclist[0].client_script: doclist[0].client_script = None
			if doclist[0].client_script_core: doclist[0].client_script_core = None

	# write code to cache
	#=================================================================================
	
	def _add_compiled_code_to_cache(self, code, dt, modified):
		import marshal
		if webnotes.conn.sql("select name from __DocTypeCache where name=%s", dt):
			webnotes.conn.sql("UPDATE __DocTypeCache set server_code_compiled = %s, modified=%s WHERE name=%s", (marshal.dumps(code), modified, dt))
		else:
			webnotes.conn.sql("INSERT INTO __DocTypeCache (name, modified, server_code_compiled) VALUES (%s, %s, %s)", (dt, modified, marshal.dumps(code)))
	
	# compile code and write it to cache
	#=================================================================================
	
	def compile_code(self, doc):
		std_code = '''class DocType:
		def __init__(self, d, dl):
			self.doc, self.doclist = d, dl'''
	
		c = [doc.server_code_core or '', doc.server_code or '']
	
		# add default code if no code
		# ---------------------------
		if not (c[0].strip() or c[1].strip()):
			c[0] = std_code
	
		code = None
			
		# compile code
		# ------------
		try:
			code = compile('\n'.join(c), '<string>', 'exec')
			webnotes.model.meta.set_dt_value(doc.name, 'server_code_error', ' ')
		except:
			webnotes.msgprint('Uncaught Server Script Error in ' + doc.name + '!')
			webnotes.msgprint(webnotes.utils.getTraceback())
					
		# add to cache
		# ------------
		if code:
			try:
				self._add_compiled_code_to_cache(code, doc.name, doc.modified)
			except Exception, e:
				if e.args[0]==1054:
					# column not yet made - remove after some time
					webnotes.conn.sql("commit")
					webnotes.conn.sql("alter table __DocTypeCache add `server_code_compiled` text")
					webnotes.conn.sql("start transaction")
					
					# retry
					self._add_compiled_code_to_cache(code, doc.name, doc.modified)
				else:
					raise e
		
	# build a list of all the records required for the DocType
	# =================================================================

	def make_doclist(self):
		tablefields = webnotes.model.meta.get_table_fields(self.name)
		modified, is_modified, is_cache_modified = self.is_modified()

		if is_modified:
			# yes
			doclist = webnotes.model.doc.get('DocType', self.name, 1)
			for t in tablefields: 
				doclist += webnotes.model.doc.get('DocType', t[0], 1)

			# don't save compiled server code
			doclist[0].server_code_compiled = None

			self._build_client_script(doclist)		
			self._update_cache(is_cache_modified, modified, doclist)
		else:
			doclist = self._load_from_cache()
	
		self._load_select_options(doclist)
		self._clear_code(doclist)

		return doclist

# Called when "DocType" form is saved - scrubs field names, clears cache, updates schema
#=======================================================================================

def update_doctype(doclist):
	doc = doclist[0]
	
	# make field name from label
	scrub_field_names(doclist)
	
	# make schma changes
	import db_schema
	db_schema.updatedb(doc.name)
	
	# reload record
	for d in doclist:
		try:
			d.loadfromdb()
		except:
			pass

	# change modifed of parent doctype (to clear the cache)
	clear_cache()

def scrub_field_names(doclist):
	restricted = ('name','parent','idx','owner','creation','modified','modified_by','parentfield','parenttype')
	
	for d in doclist:
		if d.parent and d.fieldtype:
			if (not d.fieldname) and (d.fieldtype.lower() in ('data', 'select', 'int', 'float', 'currency', 'table', 'text', 'link', 'date', 'code', 'check', 'read only', 'small text', 'time', 'text editor')):
				d.fieldname = d.label.strip().lower().replace(' ','_')
				if d.fieldname in restricted:
					d.fieldname = d.fieldname + '1'
				webnotes.model.meta.set_fieldname(d.name, d.fieldname)

def clear_cache():
	webnotes.conn.sql("delete from __DocTypeCache")
	
# Load "DocType" - called by form builder, report buider and from code.py (when there is no cache)
#=================================================================================================

def get(dt):
	doclist = _DocType(dt).make_doclist()
		
	return doclist
	 
