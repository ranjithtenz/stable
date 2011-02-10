import webnotes
import webnotes.db

import module_manager
import transfer
import os

# Accounts Manager
# ==============================================================================================================================

class AccountsManager(object):
	def __init__(self, ignore_accounts = ['brownie_copy']):
		self.account_list = []
		self.ignore_accounts = ignore_accounts
			
	#========================================================================================================================
	
	# load list of applications
	# ----------------------------------
	def load_account_list(self, al=[]):
		account_conn = webnotes.db.Database(use_default=1)
		
		ignore_acc = '"'+'","'.join(self.ignore_accounts)+'"'
		accepted_acc = al and ' and ac_name in ("'+'","'.join(al)+'")' or ''
		al = [[d[0], d[1], d[2]] for d in account_conn.sql("select ac_name, db_name, db_login from tabAccount where ac_name not in (%s) %s" % (ignore_acc, accepted_acc))]
		account_conn.close()
		
		for a in al:
			self.account_list.append(Account(a[0], a[1], a[2]))

			
	# get all modules
	#-----------------------------------------
	def get_all_modules(self, ignore_modules):
		if not ignore_modules:
			ignore_modules = ['Development', 'Recycle Bin']
		all_modules = os.listdir(os.path.join(webnotes.get_index_path(), 'modules'))
		modules = list(set(all_modules).difference(ignore_modules))
		return modules


	# sync all the accounts (account_list -> ac_names , mod_list -> modules, dt_list -> [doctypes,docname])
	# -----------------------------------------------------------------------------------------------
	def sync_accounts(self, account_list=[], modules = [], dt_list = [], ignore_modules = [], execute_patches = 1, sync_cp = 0):
		self.account_list, self.dt_list = [], []
		self.load_account_list(account_list)

		for account in self.account_list:
			if not modules and not dt_list:
				modules = self.get_all_modules(ignore_modules)
				
			# sync accounts
			account.sync_from_files(modules, dt_list, execute_patches, sync_cp)
			
		print "Completed syncing accounts"



	# sync control panel
	# -------------------
	def sync_cp(self, account_list=[]):
		self.account_list = []
		self.load_account_list(account_list)
				
		for account in self.account_list:
			try:
				account.connect()
				webnotes.conn = account.conn
				print module_manager.sync_control_panel()
				account.close()
			except Exception, e:
				account.close()
				raise e
			#finally:


			
	#========================================================================================================================

	# execute patches in accounts
	# ----------------------------
	def execute_pathes(self, patch_list = [], account_list = []):
		self.account_list = []
		self.load_account_list(account_list)
		record_list = []
		for d in patch_list:
			record_list.append(['Patch', d])

		for account in self.account_list:
			try:
				account.connect()
				print transfer.execute_patches([], record_list)
				account.close()
			except Exception, e:
				account.close()
				raise e
			#finally:



	#========================================================================================================================

	# create a new account
	# ----------------------------------
	def new_account(self, ac_name, source):
		import webnotes.setup

		# setup
		print 'Creating new application...'
		ret = webnotes.setup.create_account(ac_name, source)
		ret, db_name = ret.split(',')
		print ac_name + ' created !!!'
	

	# create multiple accounts
	# ----------------------------------
	def create_accounts(self, n, source):
		acc_conn = webnotes.db.Database(use_default=1)
		curr_ac_name = acc_conn.sql("select ac_name from tabAccount where ac_name like 'AC%' Order by ac_name desc limit 1")
		curr_ac_name = curr_ac_name and curr_ac_name[0][0] or 0
		if curr_ac_name:
			curr_ac_name = int(curr_ac_name[2:])
		acc_conn.close()
		for i in range(n):
			self.new_account('AC%05d' % (curr_ac_name + i + 1), source)
	

	#=============================================================================================================================

	# Delete account List
	# -----------------
	def delete_account_list(self, al=[]):
		import webnotes.defs
		import webnotes.utils
		import webnotes.db
		root_conn, acc_conn = None, None
		if webnotes.defs.root_login:
			root_conn = webnotes.db.Database(user=webnotes.defs.root_login, password=webnotes.defs.root_password)
			acc_conn = webnotes.db.Database(use_default=1)		
			for a in al:
				db = acc_conn.sql('select db_name from tabAccount where ac_name = "%s"' % (a))
				db = db and webnotes.utils.cstr(db[0][0]) or ''
				if db:
					try:
					#	root_conn.sql("DROP DATABASE %s" % (db))
						print "Database : "+db+" deleted"
						print "-------------------------------------"
					except:
						print "Database "+db+" not found"
						pass
					#finally:
					#root_conn.sql('drop user "%s"@"localhost"' % (db))
					print "User"+db+"deleted"

			#acc_conn.sql("START TRANSACTION")
			#acc_conn.sql("delete from tabAccount where ac_name IN %s" % ("('"+"','".join(al)+"')"))
			#acc_conn.sql("COMMIT")
			print "No more unwanted Databases !!!"
			root_conn.close()
			acc_conn.close()
		
		

	# Delete Unwanted Database
	# --------------------------
	def delete_accounts(self, accounts=[]):
		if not accounts:
			from webnotes.utils.webservice import FrameworkServer
			fw = FrameworkServer('www.iwebnotes.com','/','__system@webnotestech.com','password')
			accounts = fw.runserverobj('App Control','App Control','delete_apps',app_list)
			if accounts['exc']:
				print accounts['exc']
			accounts = accounts['message']
		self.delete_account_list(accounts)
		msg = "Following accounts has been deleted: "+ NEWLINE + cstr(accounts)
		self.send_email(['nabin@iwebnotes.com', 'saumil@iwebnotes.com'], 'Expired Accounts Deletion', msg)
		
	def send_email(self, email=[], subject='', message=''):
		sendmail(email, sender = 'info@iwebnotes.com', subject = subject , parts = [['text/html', message]],cc=[],attach=[])
		print "Mail Sent"
		


# Account Instance
# ===========================================================================================================================
class Account(object):
	def __init__(self, ac_name, db_name, db_login):
		self.ac_name = ac_name
		self.db_name = db_name
		self.db_login = db_login

	# ===========================================================================================================================

	# make connections to account
	# ----------------------------------
	def connect(self):
		print "---------------------------------------"
		print "Connecting to account: "+self.ac_name
		print "---------------------------------------"
		webnotes.set_as_admin()
		self.conn = webnotes.db.Database(ac_name = self.ac_name)
		self.conn.use(self.db_name or self.db_login)

	
	# close
	# ----------------------------------
	def close(self):
		self.conn.close()

	# ===========================================================================================================================
	
	# sync application doctypes
	# ----------------------------------
	def sync_from_files(self, modules, dt_list, execute_patches, sync_cp):
		try:
			self.connect()
			webnotes.conn = self.conn	
			print module_manager.import_from_files(modules, dt_list, execute_patches, sync_cp)
			self.clear_cache()
		except Exception,e:
			print webnotes.utils.getTraceback()
			print e
		#finally:
		self.close()
		
				
	# Clear Cache
	# -----------
	def clear_cache(self):
		import webnotes.utils
		self.conn.sql("start transaction")
		self.conn.sql("delete from __DocTypeCache")
		self.conn.sql("delete from __SessionCache")
		webnotes.conn = self.conn
		webnotes.utils.clear_recycle_bin()
		self.conn.sql("commit")

			

# ===========================================================================================================================

def do_transfer(dt_list = [], account_list = [], mod_list = []):
	webnotes.conn = webnotes.db.Database(use_default = 1)
	webnotes.set_as_admin()
	account = AccountManager()
	account.sync_accounts(dt_list = dt_list, account_list = account_list, modules = mod_list)
