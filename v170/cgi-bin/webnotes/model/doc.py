import webnotes
import webnotes.model.meta

from webnotes.utils import *

# actually should be "BaseDocType" - deprecated. Only for v160
class SuperDocType:
	def __init__(self):
		pass
		
	def __getattr__(self, name):
		if self.__dict__.has_key(name):
			return self.__dict__[name]
		elif self.super and hasattr(self.super, name):
			return getattr(self.super, name)
		else:
			raise AttributeError, 'BaseDocType Attribute Error'

class Document:
	def __init__(self, doctype = '', name = '', fielddata = {}):
		self._roles = []
		self._perms = []
		self._user_defaults = {}
		
		if fielddata: 
			self.fields = fielddata
		else: 
			self.fields = {}
		
		if not self.fields.has_key('name'):
			self.fields['name']='' # required on save
		if not self.fields.has_key('doctype'):
			self.fields['doctype']='' # required on save			
		if not self.fields.has_key('owner'):
			self.fields['owner']='' # required on save			

		if doctype:
			self.fields['doctype'] = doctype
		if name:
			self.fields['name'] = name
		self.__initialized = 1

		if (doctype and name):
			self._loadfromdb(doctype, name)

	def __nonzero__(self):
		return True

	def __str__(self):
		return str(self.fields)

	# Load Document
	# ---------------------------------------------------------------------------

	def _loadfromdb(self, doctype = None, name = None):
		if name: self.name = name
		if doctype: self.doctype = doctype
				
		if webnotes.model.meta.is_single(self.doctype):
			self._loadsingle()
		else:
			dataset = webnotes.conn.sql('select * from `tab%s` where name="%s"' % (self.doctype, self.name.replace('"', '\"')))
			if not dataset:
				webnotes.msgprint('%s %s does not exist' % (self.doctype, self.name), 1)
				raise Exception, '[WNF] %s %s does not exist' % (self.doctype, self.name)
			self._load_values(dataset[0], webnotes.conn.get_description())

	# Load Fields from dataset
	# ---------------------------------------------------------------------------

	def _load_values(self, data, description):
		for i in range(len(description)):
			v = data[i]
			self.fields[description[i][0]] = webnotes.conn.convert_to_simple_type(v)

	def _merge_values(self, data, description):
		for i in range(len(description)):
			v = data[i]
			if v: # only if value, over-write
				self.fields[description[i][0]] = webnotes.conn.convert_to_simple_type(v)
			
	# Load Single Type
	# ---------------------------------------------------------------------------

	def _loadsingle(self):
		self.name = self.doctype
		dataset = webnotes.conn.sql("select field, value from tabSingles where doctype='%s'" % self.doctype)
		for d in dataset: self.fields[d[0]] = d[1]

	# Setter
	# ---------------------------------------------------------------------------
			
	def __setattr__(self, name, value):
		# normal attribute
		if not self.__dict__.has_key('_Document__initialized'): 
			self.__dict__[name] = value
		elif self.__dict__.has_key(name):
			self.__dict__[name] = value
		else:
			# field attribute
			f = self.__dict__['fields']
			f[name] = value

	# Getter
	# ---------------------------------------------------------------------------

	def __getattr__(self, name):
		if self.__dict__.has_key(name):
			return self.__dict__[name]
		elif self.fields.has_key(name):
			return self.fields[name]	
		else:
			return ''

	# Get Amendement number
	# ---------------------------------------------------------------------------
	
	def _get_amended_name(self):
		am_id = 1
		am_prefix = self.amended_from
		if webnotes.conn.sql('select amended_from from `tab%s` where name = "%s"' % (self.doctype, self.amended_from))[0][0] or '':
			am_id = cint(self.amended_from.split('-')[-1]) + 1
			am_prefix = '-'.join(self.amended_from.split('-')[:-1]) # except the last hyphen
			
		self.name = am_prefix + '-' + str(am_id)

	# Set Name
	# ---------------------------------------------------------------------------

	def _set_name(self, autoname, istable):
		self.localname = self.name

	
		# get my object
		import webnotes.model.code
		so = webnotes.model.code.get_server_obj(self, [])		

		# amendments
		if self.amended_from: self._get_amended_name()
		
		# by method
		elif so and hasattr(so, 'autoname'):
			r = webnotes.model.code.run_server_obj(so, 'autoname')
			if r: return r

		# based on a field
		elif autoname and autoname.startswith('field:'):
			n = self.fields[autoname[6:]]
			if not n:
				raise Exception, 'Name is required'
			self.name = n.strip()
			
		# given
		elif self.fields.get('__newname',''): self.name = self.fields['__newname']

		# call the method!
		elif autoname and autoname!='Prompt': self.name = make_autoname(autoname, self.doctype)

		# default name for table
		elif istable: self.name = make_autoname('#########', self.doctype)
	
	# Validate Name
	# ---------------------------------------------------------------------------
	
	def _validate_name(self, case):

		if webnotes.conn.sql('select name from `tab%s` where name=%s' % (self.doctype,'%s'), self.name):
			raise NameError, 'Name %s already exists' % self.name
		
		# no name
		if not self.name: return 'No Name Specified for %s' % self.doctype
		
		# new..
		if self.name.startswith('New '+self.doctype):
			return 'There were some errors setting the name, please contact the administrator'
		
		if case=='Title Case': self.name = self.name.title()
		if case=='UPPER CASE': self.name = self.name.upper()
		
		self.name = self.name.strip() # no leading and trailing blanks

		forbidden = ['%',"'",'"']
		for f in forbidden:
			if f in self.name:
				raise NameError, '%s not allowed in ID (name)' % f

	# Insert
	# ---------------------------------------------------------------------------
	
	def _makenew(self, autoname, istable, case='', make_autoname=1):
		# set owner
		if not self.owner: self.owner = webnotes.session['user']
		
		# set name
		if make_autoname:
			self._set_name(autoname, istable)
		
		# validate name
		self._validate_name(case)
				
		# insert!
		webnotes.conn.sql("""insert into `tab%s` (name, owner, creation, modified, modified_by) values ('%s', '%s', '%s', '%s', '%s')""" % (self.doctype, self.name, webnotes.session['user'], now(), now(), webnotes.session['user']))


	# Update Values
	# ---------------------------------------------------------------------------
	
	def _update_single(self, link_list):
		update_str = ["(%s, 'modified', %s)",]
		values = [self.doctype, now()]
		
		webnotes.conn.sql("delete from tabSingles where doctype='%s'" % self.doctype)
		for f in self.fields.keys():
			if not (f in ('modified', 'doctype', 'name', 'perm', 'localname', 'creation'))\
				and (not f.startswith('__')): # fields not saved

				# validate links
				if link_list and link_list.get(f):
					self.fields[f] = self._validate_link(link_list[f][0], self.fields[f])

				if self.fields[f]==None:
					update_str.append("(%s,%s,NULL)")
					values.append(self.doctype)
					values.append(f)
				else:
					update_str.append("(%s,%s,%s)")
					values.append(self.doctype)
					values.append(f)
					values.append(self.fields[f])
		webnotes.conn.sql("insert into tabSingles(doctype, field, value) values %s" % (', '.join(update_str)), values)

	# Validate Links
	# ---------------------------------------------------------------------------

	def validate_links(self, link_list):
		err_list = []
		for f in self.fields.keys():
			# validate links
			old_val = self.fields[f]
			if link_list and link_list.get(f):
				self.fields[f] = self._validate_link(link_list[f][0], self.fields[f])

			if old_val and not self.fields[f]:
				s = link_list[f][1] + ': ' + old_val
				err_list.append(s)
				
		return err_list

	def make_link_list(self):
		res = webnotes.model.meta.get_link_fields(self.doctype)

		link_list = {}
		for i in res: link_list[i[0]] = (i[1], i[2]) # options, label
		return link_list
	
	def _validate_link(self, dt, dn):
		if not dt: return dn
		if dt.lower().startswith('link:'):
			dt = dt[5:]
		if '\n' in dt:
			dt = dt.split('\n')[0]
		tmp = webnotes.conn.sql("""SELECT name FROM `tab%s` WHERE name = '%s' """ % (dt, dn))
		return tmp and tmp[0][0] or ''# match case

	# Update query
	# ---------------------------------------------------------------------------
		
	def _update_values(self, issingle, link_list, ignore_fields=0):
		if issingle:
			self._update_single(link_list)
		else:
			update_str, values = [], []
			# set modified timestamp
			self.modified = now()
			self.modified_by = webnotes.session['user']
			for f in self.fields.keys():
				if (not (f in ('doctype', 'name', 'perm', 'localname', 'creation'))) \
					and (not f.startswith('__')): # fields not saved
					
					# validate links
					if link_list and link_list.get(f):
						self.fields[f] = self._validate_link(link_list[f][0], self.fields[f])

					if self.fields[f]==None:
						update_str.append("`%s`=NULL" % f)
						if ignore_fields:
							try: r = webnotes.conn.sql("update `tab%s` set `%s`=NULL where name=%s" % (self.doctype, f, '%s'), self.name)
							except: pass
					else:
						values.append(self.fields[f])
						update_str.append("`%s`=%s" % (f, '%s'))
						if ignore_fields:
							try: r = webnotes.conn.sql("update `tab%s` set `%s`=%s where name=%s" % (self.doctype, f, '%s', '%s'), (self.fields[f], self.name))
							except: pass
			if values:
				if not ignore_fields:
					# update all in one query
					#webnotes.errprint(values)
					r = webnotes.conn.sql("update `tab%s` set %s where name='%s'" % (self.doctype, ', '.join(update_str), self.name), values)

	# Save values
	# ---------------------------------------------------------------------------
	
	def save(self, new=0, check_links=1, ignore_fields=0, make_autoname = 1):	
		res = webnotes.model.meta.get_dt_values(self.doctype, 'autoname, issingle, istable, name_case', as_dict=1)
		res = res and res[0] or {}

		# if required, make new
		if new or (not new and self.fields.get('__islocal')) and (not res.get('issingle')):
			r = self._makenew(res.get('autoname'), res.get('istable'), res.get('name_case'), make_autoname)
			if r: 
				return r
				
		# save the values
		self._update_values(res.get('issingle'), check_links and self.make_link_list() or {}, ignore_fields)
		self._clear_temp_fields()

	# check permissions
	# ---------------------------------------------------------------------------

	def _get_perms(self):
		if not self._perms:
			self._perms = webnotes.conn.sql("select role, `match` from tabDocPerm where parent=%s and ifnull(`read`,0) = 1 and ifnull(permlevel,0)=0", self.doctype)

	def _get_roles(self):
		# check if roles match
		if not self._roles:
			if webnotes.user:
				self._roles = webnotes.user.get_roles()
			else:
				self._roles = ['Guest']

	def _get_user_defaults(self):
		if not self._user_defaults:
			self._user_defaults = webnotes.user.get_defaults()

	def check_perm(self, verbose=0):
		import webnotes
		
		# find roles with read access for this record at 0
		self._get_perms()
		self._get_roles()
		self._get_user_defaults()
	
		has_perm, match = 0, []
		
		# loop through everything to find if there is a match
		for r in self._perms:
			if r[0] in self._roles:
				has_perm = 1
				if r[1] and match != -1:
					match.append(r[1]) # add to match check
				else:
					match = -1 # has permission and no match, so match not required!
		
		if has_perm and match and match != -1:
			for m in match:
				if self.fields.get(m, 'no value') in self._user_defaults.get(m, 'no default'):
					has_perm = 1
					break # permission found! break
				else:
					has_perm = 0
					if verbose:
						webnotes.msgprint("Value not allowed: '%s' for '%s'" % (self.fields.get(m, 'no value'), m))
					
	
		# check for access key
		if webnotes.form and webnotes.form.has_key('akey'):
			import webnotes.utils.encrypt
			if webnotes.utils.encrypt.decrypt(webnotes.form.getvalue('akey')) == self.name:
				has_perm = 1
				webnotes.response['print_access'] = 1
				
		return has_perm

	# Cleanup
	# ---------------------------------------------------------------------------
		
	def _clear_temp_fields(self):
		# clear temp stuff
		keys = self.fields.keys()
		for f in keys:
			if f.startswith('__'): 
				del self.fields[f]

	# Table methods
	# ---------------------------------------------------------------------------

	def clear_table(self, doclist, tablefield, save=0):
		import webnotes.model.doclist
		
		for d in webnotes.model.doclist.getlist(doclist, tablefield):
			d.fields['__oldparent'] = d.parent
			d.parent = 'old_parent:' + d.parent # for client to send it back while saving
			d.docstatus = 2
			if save and not d.fields.get('__islocal'):
				d.save()
		self.fields['__unsaved'] = 1

	def addchild(self, fieldname, childtype = '', local=0, doclist=None):
		if not childtype:
			childtype = db_getchildtype(self.doctype, fieldname)
	
		d = Document()
		d.parent = self.name
		d.parenttype = self.doctype
		d.parentfield = fieldname
		d.doctype = childtype
		d.docstatus = 0;
		d.name = ''
		d.owner = webnotes.session['user']
		
		if local:
			d.fields['__islocal'] = '1' # for Client to identify unsaved doc
		else: 
			d.save(new=1)
	
		if doclist != None:
			doclist.append(d)
	
		return d

def addchild(parent, fieldname, childtype = '', local=0, doclist=None):
	return parent.addchild(fieldname, childtype, local, doclist)

# Remove Child
# ------------

def removechild(d, is_local = 0):
	if not is_local:
		set(d, 'docstatus', 2)
		set(d, 'parent', 'old_parent:' + d.parent)
	else:
		d.parent = 'old_parent:' + d.parent
		d.docstatus = 2
			
# Naming
# ------

def make_autoname(key, doctype=''):
	n = ''
	l = key.split('.')
	for e in l:
		en = ''
		if e.startswith('#'):
			digits = len(e)
			en = getseries(n, digits, doctype)
		elif e=='YY': 
			import time
			en = time.strftime('%y')
		elif e=='MM': 
			import time
			en = time.strftime('%m')		
		elif e=='YYYY': 
			import time
			en = time.strftime('%Y')		
		else: en = e
		n+=en
	return n

# Get Series for Autoname
# -----------------------

def getseries(key, digits, doctype=''):
	ttl = webnotes.conn.get_testing_tables()

	# series created ?
	if webnotes.conn.sql("select name from tabSeries where name='%s'" % key, allow_testing = (doctype in ttl) and 0 or 1):

		# yes, update it
		webnotes.conn.sql("update tabSeries set current = current+1 where name='%s'" % key, allow_testing = (doctype in ttl) and 0 or 1)

		# find the series counter
		r = webnotes.conn.sql("select current from tabSeries where name='%s'" % key, allow_testing = (doctype in ttl) and 0 or 1)
		n = r[0][0]
	else:
	
		# no, create it
		webnotes.conn.sql("insert into tabSeries (name, current) values ('%s', 1)" % key, allow_testing = (doctype in ttl) and 0 or 1)
		n = 1
	return ('%0'+str(digits)+'d') % n


# Get Children
# ------------

def getchildren(name, childtype, field='', parenttype='', from_doctype=0):
	import webnotes
	
	tmp = ''
	
	if field: 
		tmp = ' and parentfield="%s" ' % field
	if parenttype: 
		tmp = ' and parenttype="%s" ' % parenttype

	dataset = webnotes.conn.sql("select * from `tab%s` where parent='%s' %s order by idx" % (childtype, name, tmp))
	desc = webnotes.conn.get_description()

	l = []
	
	for i in dataset:
		d = Document()
		d.doctype = childtype
		d._load_values(i, desc)
		l.append(d)
	
	return l

# Check if "Guest" is allowed to view this page
# ---------------------------------------------

def check_page_perm(dn):
	if dn=='Login Page': 
		return
	if not webnotes.conn.sql("select name from `tabPage Role` where parent=%s and role='Guest'", dn):
		webnotes.response['exc_type'] = 'PermissionError'
		raise Exception, '[WNF] No read permission for %s %s' % ('Page', dn)		

# called from everywhere
# load a record and its child records and bundle it in a list - doclist
# ---------------------------------------------------------------------

def get(dt, dn='', with_children = 1, from_get_obj = 0):
	import webnotes 
	import webnotes.model
	import webnotes.defs

	dn = dn or dt

	# load the main doc
	doc = Document(dt, dn)

	# check permission - for doctypes, pages
	if (dt in ('DocType', 'Page', 'Control Panel', 'Search Criteria')) or (from_get_obj and webnotes.session.get('user') != 'Guest'):
		if dt=='Page' and webnotes.session['user'] == 'Guest':
			check_page_perm(dn)
	else:
		if not doc.check_perm():
			webnotes.response['exc_type'] = 'PermissionError'
			raise Exception, '[WNF] No read permission for %s %s' % (dt, dn)

	# scrub for code
	if dt in webnotes.code_fields_dict.keys() and getattr(webnotes.defs,'developer_mode',None):
		import webnotes.modules.code_sync
		webnotes.modules.code_sync.sync(doc)

	if not with_children:
		# done
		return [doc,]
	
	# get all children types
	tablefields = webnotes.model.meta.get_table_fields(dt)

	# load chilren
	doclist = [doc,]
	for t in tablefields:
		doclist += getchildren(doc.name, t[0], t[1], dt)

	return doclist
