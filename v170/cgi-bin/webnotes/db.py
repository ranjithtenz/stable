# Database Module
# --------------------

import MySQLdb
from webnotes import defs
import webnotes

class Database:
	def __init__(self, host='', user='', password='', ac_name = '', use_default = 0):
		self.host = host or 'localhost'
		self.user = user or defs.db_login
		self.password = password or defs.db_password

		if ac_name:
			self.user = self.get_db_login(ac_name) or defs.db_login
		
		if use_default:
			self.user = defs.db_login
			self.password = defs.db_password

		self.is_testing = 0
		self.in_transaction = 0
		self.transaction_writes = 0
		self.testing_tables = []
		
		self.connect()
		if self.user !='root':		
			self.use(self.user)
				
		if webnotes.logger:
			webnotes.logger.debug('Database object initialized for:%s',self.user)

	def get_db_login(self, ac_name):
		import webnotes.db
		c = webnotes.db.Database(use_default = 1)
		res = None
		try:
			res = c.sql("select db_name, db_login from tabAccount where ac_name = '%s'" % ac_name)
		except:
			pass
		if res:
			return res[0][1] or res[0][0]

	def connect(self):
		self._conn = MySQLdb.connect(user=self.user, host=self.host, passwd=self.password)
		self._cursor = self._conn.cursor()
		
		return self._cursor
	
	def use(self, db_name):
		self._conn.select_db(db_name)
		self.cur_db_name = db_name
	
	def check_transaction_status(self, query):
		if query and query.strip().lower()=='start transaction':
			self.in_transaction = 1
			self.transaction_writes = 0

		if query and query.strip().lower() in ['commit', 'rollback']:
			self.in_transaction = 0

		if self.in_transaction and query[:6].lower() in ['update', 'insert']:
			self.transaction_writes += 1
			if self.transaction_writes > 5000:
				raise Exception, 'Bad Query!!! Too many writes'
				self.sql("ROLLBACK")
	
	def fetch_as_dict(self):
		result = self._cursor.fetchall()
		ret = []
		for r in result:
			dict = {}
			for i in range(len(r)):
				dict[self._cursor.description[i][0]] = r[i]
			ret.append(dict)
		return ret
	
	def validate_query(self, q):
		cmd = q.strip().lower().split()[0]
		if cmd in ['alter', 'drop', 'truncate'] and webnotes.user.name != 'Administrator':
			webnotes.msgprint('Not allowed to execute query')
			raise Execption

	# ======================================================================================
	
	def sql(self, query, values=(), as_dict = 0, as_list = 0, allow_testing = 1, ignore_no_table = 1):
			
		# in transaction validations
		self.check_transaction_status(query)
		
		# execute
		if values!=():
			if webnotes.logger and (self.user in defs.debug_log_dbs):
				webnotes.logger.debug('Executing SQL Query %s with values %s',query,values)
			self._cursor.execute(query, values)
		else:
			if webnotes.logger and (self.user in defs.debug_log_dbs):
				webnotes.logger.debug('Executing SQL Query %s without any values',query)
			self._cursor.execute(query)	

		# scrub output if required
		if as_dict:
			return self.fetch_as_dict()
		elif as_list:
			return self.convert_to_lists(self._cursor.fetchall())
		else:
			return self._cursor.fetchall()

	# Check whether the query is from metadata
	# ======================================================================================
	def _scrub_table(self, tn, adt_list):
		if tn.startswith('`'):
			tn = tn[1:-1]
			
		if tn.startswith('tab'):
			tn = tn[3:]

		if tn in adt_list:
			return 1
		else:
			return 0

	def parse_for_metadata(self, query, adt_list):
		#try:
		import sqlparse
		
		# parse
		tokens = sqlparse.parse(query)[0].tokens
		tablist = []
		
		# only for selects - never update or delete metadata
		if tokens[0].value.lstrip().lower() != 'select':
			return 0
		
		tflag = 0
		for t in tokens:

			if type(t).__name__ == 'Token' and str(t.ttype)=='Token.Keyword' and t.value.lower()=='from':
				tflag = 1

			# find tables from a list
			elif tflag and type(t).__name__=='IdentifierList':
				return self._scrub_table(str(t.get_identifiers()[0].tokens[0]), adt_list)
							
			# find the tables
			elif tflag and type(t).__name__=='Identifier':
				return self._scrub_table(t.tokens[0].value, adt_list)
		
		return 0
		
	# ======================================================================================

	def get_description(self):
		return self._cursor.description

	# ======================================================================================

	def convert_to_simple_type(self, v):
		try: import decimal # for decimal Python 2.5 onwards
		except: pass
		import datetime

		if type(v)==datetime.date:
			v = str(v)
		elif type(v)==datetime.timedelta:
			v = ':'.join(str(v).split(':')[:2])
		elif type(v)==datetime.datetime:
			v = str(v)
		elif type(v)==long: 
			v=int(v)

		try:
			if type(v)==decimal.Decimal: 
				v=float(v)
		except: pass
		
		return v

	# ======================================================================================

	def convert_to_lists(self, res):
		nres = []
		for r in res:
			nr = []
			for c in r:
				nr.append(self.convert_to_simple_type(c))
			nres.append(nr)
		return nres

	# ======================================================================================

	def replace_tab_by_test(self, query):
		if self.is_testing:
			tl = self.get_testing_tables()
			for t in tl:
				query = query.replace(t, 'test' + t[3:])
		return query
		
	def get_testing_tables(self):
		if not self.testing_tables:
			testing_tables = ['tab'+r[0] for r in self.sql('SELECT name from tabDocType where docstatus<2 and (issingle=0 or issingle is null)', allow_testing = 0)]
			testing_tables+=['tabSeries','tabSingles'] # tabSessions is not included here
		return self.testing_tables

	# ======================================================================================
	# get a single value from a record

	def get_value(self, doctype, docname, fieldname):
		if docname:
			try:
				r = self.sql("select `%s` from `tab%s` where name='%s'" % (fieldname, doctype, docname))
				return r and r[0][0] or ''
			except:
				return None
		else:
			r = self.sql("select value from tabSingles where field=%s and doctype=%s", (fieldname, doctype))
			return r and r[0][0] or None

	def set_value(self, dt, dn, field, val):
		if dn and dt!=dn:
			self.sql("update `tab"+dt+"` set `"+field+"`=%s where name=%s", (val, dn))
		else:
			if self.sql("select value from tabSingles where field=%s and doctype=%s", (field, dt)):
				self.sql("update tabSingles set value=%s where field=%s and doctype=%s", (val, field, dt))
			else:
				self.sql("insert into tabSingles(doctype, field, value) values (%s, %s, %s)", (dt, field, val))
				
	def set(self, doc, field, val):
		self.set_value(doc.doctype, doc.name, field, val)
		doc.fields[field] = val

	# ======================================================================================

	def set_global(self, key, val):
		res = self.sql('select defkey from `tabDefaultValue` where defkey=%s and parent = "__global"', key)
		if res:
			self.sql('update `tabDefaultValue` set defvalue=%s where parent = "__global" and defkey=%s', (str(val), key))
		else:
			self.sql('insert into `tabDefaultValue` (name, defkey, defvalue, parent) values (%s,%s,%s,"__global")', (key,key,str(val)))

	def get_global(self, key):
		g = self.sql("select defvalue from tabDefaultValue where defkey=%s and parent='__global'", key)
		return g and g[0][0] or None

	# ======================================================================================

	def begin(self):
		if not self.in_transaction:
			self.sql("start transaction")
	
	def commit(self):
		self.sql("commit")

	# ======================================================================================

	def field_exists(self, dt, fn):
		return self.sql("select name from tabDocField where fieldname=%s and parent=%s", (dt, fn))

	def exists(self, dt, dn):
		try:
			return self.sql('select name from `tab%s` where name=%s' % (dt, '%s'), dn)
		except:
			return None

	# ======================================================================================
	def close(self):
		if self._conn:
			self._conn.close()
