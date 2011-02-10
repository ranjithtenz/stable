class DocType:
	def __init__(self,d,dl):
		self.doc, self.doclist = d,dl
  
	# Profile fields to display
	def fetch_display_fields(self):
		#return sql("select label, fieldname, fieldtype, options from `tabDocField` where parent='Profile' and search_index=1 order by idx asc",as_dict=1)
		return [{'options': '', 'fieldname': '', 'fieldtype': 'Section Break', 'label': 'Details'}, {'options': None, 'fieldname': None, 'fieldtype': 'Column Break', 'label': 'Contact'}, {'options': None, 'fieldname': 'first_name', 'fieldtype': 'Data', 'label': 'First Name'}, {'options': None, 'fieldname': 'last_name', 'fieldtype': 'Data', 'label': 'Last Name'}, {'options': 'Email', 'fieldname': 'email', 'fieldtype': 'Data', 'label': 'Email'}, {'options': None, 'fieldname': 'birth_date', 'fieldtype': 'Date', 'label': 'Birth Date'}, {'options': '\nMale\nFemale', 'fieldname': 'gender', 'fieldtype': 'Select', 'label': 'Gender'}, {'options': None, 'fieldname': 'occupation', 'fieldtype': 'Data', 'label': 'Designation'}, {'options': None, 'fieldname': 'bio', 'fieldtype': 'Text', 'label': 'About me'}]

		
	# Enable profile	
	def enable_profile(self, id):
		sql("update tabProfile set enabled=1 where name=%s", id)
		return 1
		
	# Disable profile
	def disable_profile(self, id):
		if id=='Administrator':
			return 'Cannot disable Administrator'

		sql("update tabProfile set enabled=0 where name=%s", id)
		return 0
		
	# All roles of Role Master
	def get_all_roles(self):
		r_list=sql("select name from `tabRole` where name not in ('All','Guest') and docstatus != 2")
		if r_list[0][0]:
			r_list = [x[0] for x in r_list]
		return r_list
		
	# Get all permissions for given role	
	def get_permission(self,role):
		perm = sql("select distinct t1.`parent`, t1.`read`, t1.`write`, t1.`create`, t1.`submit`,t1.`cancel`,t1.`amend` from `tabDocPerm` t1, `tabDocType` t2 where t1.`role` ='%s' and t1.docstatus !=2 and t1.permlevel = 0 and t1.`read` = 1 and t1.`write` = 1 and t2.module != 'Recycle Bin' and t1.parent=t2.name "%role)
		return perm or ''

	# Get roles for given user
	def get_user_roles(self,usr):
		r_list=sql("select role from `tabUserRole` where parent=%s and role not in ('All','Guest')",usr)
		if r_list:
			return [r[0] for r in r_list]
		else:
			return ''

	# Update roles of given user
	def update_roles(self,arg):
		arg = eval(arg)
		sql("delete from `tabUserRole` where parenttype='Profile' and parent ='%s'" % (cstr(arg['usr'])))
		role_list = arg['role_list'].split(',')
		for r in role_list:
			pr=Document('UserRole')
			pr.parent = arg['usr']
			pr.parenttype = 'Profile'
			pr.role = r
			pr.parentfield = 'userroles'
			pr.save(1)

	# Save profile
	def save_profile(self,arg):
		arg = eval(arg)
		p = Document('Profile', session['user'])
		for k in arg:
			p.fields[k] = arg[k]
		p.save()

	def update_profile_image(self, fid, fname):
		sql("update tabProfile set file_list = '%s,%s' where name='%s'" % (fname, fid, session['user']))
		
	def update_profile_property(self, arg):
		arg = eval(arg)
		sql("update tabProfile set `%s`=%s where name=%s" % (arg['fieldname'], '%s', '%s'), (arg['value'], arg['name']))
		return arg['value']
		
	# update gateway picture
	def update_gateway_picture(self):
		# get file list
		p = Document('Profile',session['user'])
		
		arg = {}
		arg['file_list'] = p.file_list
		arg['name'] = session['user']
		
		# login to gateway
		from webnotes.utils.webservice import FrameworkServer
		fw = FrameworkServer('www.erpnext.com','/','__system@webnotestech.com','password',https=1)

		# call add profile
		ret = fw.runserverobj('Profile Control','Profile Control','update_gateway_picture',str(arg))

		if ret.get('exc'):
			msgprint(ret['exc'])
			raise Exception
	
	# add user
	def add_user(self,arg):
		arg = eval(arg)
	
		if(sql("select name from tabProfile where name=%s", arg['email_id'])):
			msgprint('User with this email id already exist.')
			raise Exception
		else:
			p = Document('Profile')
			p.first_name = arg['first_name']
			p.last_name = arg['last_name']
			p.email = arg['email_id']
			p.name = arg['email_id']
			p.user_type = arg['user_type']
			p.enabled = 0	
			p.save(1)
			
			p_obj = get_obj('Profile', p.name)
			p_obj.on_update()
			
			
		# get account id
		cp = Document('Control Panel','Control Panel')
		
		if cint(cp.sync_with_gateway):
			
			arg['account_id'] = cp.account_id
			# add user to gateway
			from webnotes.utils.webservice import FrameworkServer
			fw = FrameworkServer('www.erpnext.com','/','__system@webnotestech.com','password',https=1)
	
			# call remove profile
			ret = fw.runserverobj('Profile Control','Profile Control','add_user',str(arg))

	# reset password
	def update_password(self,pwd):
		sql("update tabProfile set password=password(%s), password_last_updated=%s where name=%s",(pwd,nowdate(),session['user']))
		pwd = sql("select password from tabProfile where name=%s", session['user'])
		pwd = pwd and pwd[0][0] or ''
		
		if pwd:
			# login to gateway
			from webnotes.utils.webservice import FrameworkServer
			fw = FrameworkServer('www.erpnext.com','/','__system@webnotestech.com','password',https=1)

			arg = {}
			arg['password'] = pwd
			arg['name'] = session['user']
			
			# call add profile
			ret = fw.runserverobj('Profile Control','Profile Control','update_gateway_password',str(arg))

			if ret.get('exc'):
				msgprint(ret['exc'])
				raise Exception

	def get_login_url(self):
		return session['data']['login_from']
		
	def get_user_info(self):
		
		usr = sql("select count(name) from tabProfile where docstatus != 2 and name not in ('Guest','Administrator')")
		usr = usr and usr[0][0] or 0
	
		ol = sql("select count(distinct t1.name) from tabProfile t1, tabSessions t2 where t1.name = t2.user and t1.name not in('Guest','Administrator') and TIMESTAMPDIFF(HOUR,t2.lastupdate,NOW()) <= 1 and t1.docstatus != 2 and t1.enabled=1")
		ol = ol and ol[0][0] or 0
		
		ac = sql("select count(name) from tabProfile where enabled=1 and docstatus != 2 and name not in ('Guest', 'Administrator')")
		ac = ac and ac[0][0] or 0
		
		inac = sql("select count(name) from tabProfile where (enabled=0 or enabled is null or enabled = '') and docstatus != 2 and name not in ('Guest','Administrator')")
		inac = inac and inac[0][0] or 0
		
		return usr, ol, ac, inac
			
	def get_social_badge(self,usr):
		out = convert_to_lists(sql("select ifnull(t1.social_badge,''), ifnull(t1.social_points,0), ifnull(t2.badge_image,'') from tabProfile t1, `tabSocial Badge` t2 where t2.name = t1.social_badge and t1.name = %s", usr))
		return out and out[0] or ''
		
	def get_sm_count(self)	:
		return sql("select count(t1.parent) from tabUserRole t1, tabProfile t2 where t1.role='System Manager' and t1.parent = t2.name and t2.enabled=1")[0][0] or 0