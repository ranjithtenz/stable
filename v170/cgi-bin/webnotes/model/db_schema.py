# Set Column Types
# ----------------

import webnotes
import webnotes.model.meta

def getcoldef(ftype, length=''):
	t=ftype.lower()
	if t in ('date','text','time'):
		dt = t
	elif t == 'int':
		dt = 'int'
		if not length: length = '11'
	elif t in ('currency'): 
		dt = 'decimal'
		if not length: length = '14,2' 
	elif t in ('float'): 
		dt = 'decimal' 
		if not length: length = '14,6' 
	elif t == 'check':
		dt = 'int'
		if not length: length = '1' 
	elif t in ('small text', 'long text', 'code', 'text editor'): 
		dt = 'text';
	elif t in ('data', 'link', 'password', 'select', 'read only'):
		dt = 'varchar';
		if not length: length = '180' 
	elif t == 'blob':
		dt = 'longblob'
	else: dt = ''
	
	if length:
		dt += ('(%s)' % length)
	
	return dt

# Add Columns In Database
# -----------------------

def _validate_column_name(n):
	n = n.replace(' ','_').strip().lower()
	import re
	if not re.match("[a-zA-Z_][a-zA-Z0-9_]*$", n):
		webnotes.msgprint('err:%s is not a valid fieldname.<br>A valid name must contain letters / numbers / spaces.<br><b>Tip: </b>You can change the Label after the fieldname has been set' % n)
		raise Exception
	return n
	
def _add_column(f, dt):		
	ftype =  getcoldef(f[2], f[3])
	if ftype:
		fn = _validate_column_name(f[1]) # name or label
		# always user db
		webnotes.conn.sql("alter table `tab%s` add `%s` %s" % (dt, fn, ftype))

		
# Update Columns In Database
# -----------------------

def _validate_type_change(new, old):
	if not old:
		return
	if ((old.lower() in ['text','small text','code','text editor']) and (new.lower() not in ['text', 'small text', 'code', 'text editor'])) or ((old.lower() in ['data','select','link']) and (new.lower() in ['date','int','currency','float','time','table'])):
		webnotes.msgprint('Coversion from %s to %s is not allowed. Please contact your Administrator' % (new, old))
		raise Exception		

def _change_column(f, dt, col_def):
	if col_def and f[0]:
		# always user db
		try:
			webnotes.conn.sql("alter table `tab%s` change `%s` `%s` %s" % (dt, f[0], _validate_column_name(f[1]), col_def))
		except Exception, e:
			if e.args[0] == 1054:
				_add_column(f, dt)
			if e.args[0] == 1060:
				pass # duplicate column (already exists by another name)
			else:
				raise e
		#webnotes.msgprint("Column Changed: `%s` to `%s` %s" % (f[0], _validate_column_name(f[1]), col_def))


def updatecolumns(doctype):

	flist = webnotes.model.meta.get_dt_fields(doctype)


	# list of existing columns - always from user db
	cur_fields = webnotes.conn.sql("DESC `tab%s`" % (doctype))

	for f in flist:
		change = 0

		# not in current fields
		if not (f[1] in [e[0] for e in cur_fields]):
			_add_column(f, doctype)
		
		# type or length has changed
		col_def = getcoldef(f[2], f[3])
		
		# find exisiting def
		cur_def = ''
		for e in cur_fields:
			if e[0]==f[1]:
				cur_def = e[1]
				break
		
		# changed
		if change or (cur_def and col_def.lower() != cur_def.lower()):
			# validate type change
			if f[4]:
				_validate_type_change(f[2], f[4])				
				_change_column(f, doctype, col_def)
	
	# update the "old" columns
	webnotes.conn.sql("start transaction")
	webnotes.model.meta.update_oldfield_values(doctype)


# Add Indices
# -----------

def updateindex(doctype):
	addlist = webnotes.model.meta.get_index_fields(doctype, 1)
	
	# get keys
	kl = [i[4] for i in webnotes.conn.sql("show keys from `tab%s`" % doctype)]

	for f in addlist:
		try:
			if not f[0] in kl: # if not exists
				webnotes.conn.sql("alter table `tab%s` add index %s(%s)" % (doctype, f[0], f[0]))
		except:
			pass

	# remove
	droplist = webnotes.model.meta.get_index_fields(doctype, 0)
	for f in droplist:
		try:
			if f[0] in kl: # if exists
				webnotes.conn.sql("alter table `tab%s` drop index %s" % (doctype, f[0]))
		except:
			pass

# update engine
# -------------

def update_engine(doctype=None, engine='InnoDB'):
	if doctype:
		webnotes.conn.sql("ALTER TABLE `tab%s` ENGINE = '%s'" % (doctype, engine))
	else:
		for t in webnotes.conn.sql("show tables"):
			webnotes.conn.sql("ALTER TABLE `%s` ENGINE = '%s'" % (t[0], engine))

def create_table(dt):
	
	# get fields specified from docfields
	add_fields, add_index = [], []
	
	# build
	flist = webnotes.model.meta.get_dt_fields(dt)
	fname_list = []
	for f in flist:
		ft = getcoldef(f[2], f[3])
		if f[1] and ft and (f[1] not in ['name','creation','modified','modified_by','owner','docstatus','parent','parenttype','parentfield','idx']):
			
			if not f[1] in fname_list: # check for duplicate
				add_fields.append('`' + f[1] + '` ' + ft)
				
				fname_list.append(f[1])
				
				if f[5]:
					if not ft.startswith('text'):
						add_index.append('index `' + f[1] + '`(`' + f[1] + '`)')

	add_fields = add_fields and (', '.join(add_fields) + ', ') or ''
	
	# add indexes
	add_fields += add_index and (', '.join(add_index) + ', ') or ''

	# add indexes

	# make the query
	q = """create table `tab%s` (
			name varchar(120) not null primary key, 
			creation datetime, 
			modified datetime, 
			modified_by varchar(40), 
			owner varchar(40), 
			docstatus int(1) default 0, 
			parent varchar(120), 
			parentfield varchar(120), 
			parenttype varchar(120), 
			idx int(8),
			%s
			index parent(parent)) ENGINE=InnoDB""" % (dt, add_fields)
		
	# execute
	webnotes.conn.sql(q)

def updatedb(dt):
	# if single type, nothing to do
	if webnotes.model.meta.is_single(dt):
		return

	# create table
	names = [rec[0].lower() for rec in webnotes.conn.sql('SHOW TABLES')]
	if not (('tab'+dt).lower() in names):  
		create_table(dt)

	else:
		# update columns
		updatecolumns(dt)
	
		# update index
		updateindex(dt)

