class DocType:
	def __init__(self,doc,doclist=[]):
		self.doc = doc
		self.doclist = doclist
	
	# ----- enable login -------
	def enable_login(self,arg):
		arg = eval(arg)
		sql("update tabContact set disable_login = 'No' where name=%s",arg['contact'])
		sql("update tabProfile set enabled=1 where name=%s",arg['email'])
		
	# ----- disable login -------
	def disable_login(self,arg):
		arg = eval(arg)
		sql("update tabContact set disable_login = 'Yes' where name=%s",arg['contact'])
		sql("update tabProfile set enabled=0 where name=%s",arg['email'])
		
	# ------- invite contact -------
	def invite_contact(self,arg):
		arg = eval(arg)
		
		cont_det = sql("select * from tabContact where name=%s",(arg['contact']),as_dict=1)
			
		if sql("select name from tabProfile where name=%s",cont_det[0]['email_id']):
			msgprint('You have already invited this contact.')
			raise Exception
		else:
			p = Document('Profile')
			p.name = cont_det[0]['email_id']
			p.first_name = cont_det[0]['first_name']
			p.last_name = cont_det[0]['last_name']
			p.email = cont_det[0]['email_id']
			p.cell_no = cont_det[0]['contact_no']
			p.password = 'password'
			p.enabled = 1
			p.user_type = 'Partner';
			p.save(1)
			
			get_obj(doc=p).on_update()
			
			role = []
			if cont_det[0]['contact_type'] == 'Individual':
				role = ['Customer']
			else:
				if cont_det[0]['is_customer']:	role.append('Customer')
				if cont_det[0]['is_supplier']:	role.append('Supplier')
				if cont_det[0]['is_sales_partner']:	role.append('Partner')

			if role:
				prof_nm = p.name
				for i in role:
					r = Document('UserRole')
					r.parent = p.name
					r.role = i
					r.parenttype = 'Profile'
					r.parentfield = 'userroles'
					r.save(1)
				
					if i == 'Customer':
						def_keys = ['from_company','customer_name','customer']
						def_val = cont_det[0]['customer_name']
						self.set_default_val(def_keys,def_val,prof_nm)

					if i == 'Supplier':
						def_keys = ['supplier_name','supplier']
						def_val = cont_det[0]['supplier_name']
						self.set_default_val(def_keys,def_val,prof_nm)

			sql("update tabContact set has_login = 'Yes' where name=%s",cont_det[0]['name'])
			sql("update tabContact set disable_login = 'No' where name=%s",cont_det[0]['name'])
			msgprint('User login is created.')
			
			arg = {'name':p.name, 'email_id':p.email, 'first_name':p.first_name, 'last_name':p.last_name, 'user_type':p.user_type}
			
			# get account id
			arg['account_id'] = Document('Control Panel','Control Panel').account_id
			
			# add user to gateway
			from webnotes.utils.webservice import FrameworkServer
			fw = FrameworkServer('www.erpnext.com','/','__system@webnotestech.com','password',https=1)

			# call add_user
			ret = fw.runserverobj('Profile Control','Profile Control','add_user',str(arg))

			
 #------set default values---------
	def set_default_val(self,def_keys,def_val,prof_nm):
		for d in def_keys:
			kv = Document('DefaultValue')
			kv.defkey = d
			kv.defvalue = def_val
			kv.parent = prof_nm
			kv.parenttype = 'Profile'
			kv.parentfield = 'defaults'
			kv.save(1)