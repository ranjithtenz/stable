# webnotes init (all shared variables come here)
code_fields_dict = {
	'Page':[('script', 'js'), ('content', 'html'), ('style', 'css'), ('static_content', 'html')],
	'DocType':[('server_code_core', 'py'), ('client_script_core', 'js')],
	'Search Criteria':[('report_script', 'js'), ('server_script', 'py'), ('custom_query', 'sql')],
	'Patch':[('patch_code', 'py')],
	'Control Panel':[('startup_code', 'js'), ('startup_css', 'css')]
}


version = 'v170'
form_dict = {}
auth_obj = None
conn = None
form = None
session = None
user = None
is_testing = None
incoming_cookies = {}
add_cookies = {}
cookies = {}

# for applications
app_conn = None
adt_list = ['DocType', 'DocField', 'DocPerm']

# json response object
response = {'message':'', 'exc':''}

debug_log, message_log = [], []

import os
import defs

def getTraceback():
	import sys, traceback, string
	type, value, tb = sys.exc_info()
	body = "Traceback (innermost last):\n"
	list = traceback.format_tb(tb, None) \
	        + traceback.format_exception_only(type, value)
	body = body + "%-20s %s" % (string.join(list[:-1], ""), list[-1])
	return body



def errprint(msg):
	debug_log.append(str(msg or ''))

def msgprint(msg, small=0):
	message_log.append((small and '__small:' or '')+str(msg or ''))

def is_apache_user():
	import os
	if os.environ.get('USER') == 'apache':
		return 1

def get_index_path():
	import os
	return os.sep.join(os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-2])

def get_files_path():
	global conn
	import defs, os

	if not conn:
		raise Exception, 'You must login first'

	if defs.files_path:
		return os.path.join(defs.files_path, conn.cur_db_name)
	else:
		return os.path.join(get_index_path(), 'user_files', conn.cur_db_name)
	
def create_folder(path):
	import os
	
	try:
		os.makedirs(path)
	except Exception, e:
		if e.args[0]==17: 
			pass
		else: 
			raise e

def set_as_admin(db_name=None, ac_name=None):
	import os
	if is_apache_user():
		raise Exception, 'Not for web users!'

	global conn
	global session
	global user
	
	import webnotes.db
	if ac_name:
		conn = webnotes.db.Database(ac_name = ac_name)
	else:
		conn = webnotes.db.Database(use_default=1)
		if db_name:
			conn.use(db_name)
		
	session = {'user':'Administrator'}
	import webnotes.profile
	user = webnotes.profile.Profile('Administrator')

# Logging
# -----------------------------------------------------------

logger = None

def setup_logging():
	import logging
	import logging.handlers

	global logger

	LOG_FILENAME = os.path.join(defs.log_file_path,'wnframework.log')
	if not os.path.exists(LOG_FILENAME):
		open(LOG_FILENAME).close()
	
	
	logger = logging.getLogger('WNLogger')
	logger.setLevel(eval(defs.log_level))
	
	
	log_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,maxBytes = defs.log_file_size,backupCount = defs.log_file_backup_count)
	
	console_handler = logging.StreamHandler()
	
	
	formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
	
	log_handler.setFormatter(formatter)
	logger.addHandler(log_handler)
	logger.info('Importing Webnotes')

if getattr(defs, 'log_file_path', None):
	setup_logging()
	
