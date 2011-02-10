class DocType:
	def __init__(self,doc,doclist=[]):
		self.doc = doc
		self.doclist = doclist

#-------call to validate email id and company name---------		
	def validate(self):
		self.validate_company_name()

		if not self.doc.contact_name:
			if self.doc.last_name:
				self.doc.contact_name = self.doc.first_name + ' ' + self.doc.last_name
			else:
				self.doc.contact_name = self.doc.first_name
				
		self.validate_primary_contact()

#-------validate email -------------------------------------		
	def validate_email(self):
		if not validate_email_add(self.doc.email_id):
			msgprint('Please enter valid email id.')
			raise Exception
 
#--------Get customer, supplier or sales partner address-------
	def get_address(self,arg):
		arg = eval(arg)
		add = sql("select `%s`, address,`%s` from `tab%s` where name='%s'"%(arg['nm'],arg['type'],arg['dt'],arg['dn']))
		if arg['dt'] == 'Customer':
			add1 = {
				'customer_name'	: add and add[0][0] or '',
				'customer_address'	: add and add[0][1] or '',
				'customer_group' : add and add[0][2] or ''
			}
		elif arg['dt'] == 'Supplier':
			add1 = {
				'supplier_name' : add and add[0][0] or '',
				'supplier_address'	: add and add[0][1] or '',
				'supplier_type' : add and add[0][2] or ''
			}			
		else:
			add1 = {
				'sales_partner_address' : add and add[0][1] or '',
				'partner_type' : add and add[0][2] or ''
			}
		return cstr(add1)

#--------- on update ------------------------------------------		
	def on_update(self):
		if self.doc.email_id:
			self.validate_email()
	 
		if self.doc.has_login == 'Yes':
			en = sql("select enabled from tabProfile where name=%s",self.doc.email_id)
			en = en and en[0][0] or 0
			if en == 1 and self.doc.disable_login == 'Yes':
				sql("update tabProfile set enabled=0 where name=%s",self.doc.email_id)
			elif en != 1 and self.doc.disable_login == 'No':
				sql("update tabProfile set enabled=1 where name=%s",self.doc.email_id)
			else:
				pass
				
			self.set_roles()

#--------- Validate company name ----------------------------				
	def validate_company_name(self):

		if self.doc.is_customer ==1 and not self.doc.customer:
			msgprint("Please enter Customer")
			raise Exception
		if self.doc.is_supplier == 1 and not self.doc.supplier:
			msgprint("Please enter Supplier")
			raise Exception
		if self.doc.is_sales_partner == 1 and not self.doc.sales_partner:
			msgprint("Please enter Sales Partner Name")
			raise Exception
				
	# Validate that there can only be one primary contact for particular customer, supplier or sales partner
	# --------------------------------------------------------------------------------------------------------
	def validate_primary_contact(self):
		if self.doc.is_primary_contact == 'Yes':
			if self.doc.customer:
				primary_contact = sql("SELECT contact_name from tabContact where customer = %s and is_customer = 1 and is_primary_contact = 'Yes' and contact_name != %s",(self.doc.customer,self.doc.contact_name))
				primary_contact = primary_contact and primary_contact[0][0] or ''
				if primary_contact:
					msgprint("You have already selected '%s' as primary contact for '%s'"%(primary_contact,self.doc.customer))
					raise Exception
			elif self.doc.supplier_name:
				primary_contact = sql("SELECT contact_name from tabContact where supplier_name = %s and is_supplier = 1 and is_primary_contact = 'Yes'	and contact_name != %s",(self.doc.supplier_name,self.doc.contact_name))
				primary_contact = primary_contact and primary_contact[0][0] or ''
				if primary_contact:
					msgprint("You have already selected '%s' as primary contact for '%s'"%(primary_contact,self.doc.supplier_name))
					raise Exception
			elif self.doc.sales_partner:
				primary_contact = sql("SELECT contact_name from tabContact where sales_partner = %s and is_sales_partner = 1 and is_primary_contact = 'Yes' and contact_name != %s",(self.doc.sales_partner,self.doc.contact_name))
				primary_contact = primary_contact and primary_contact[0][0] or ''
				if primary_contact:
					msgprint("You have already selected '%s' as primary contact for '%s'" %(primary_contact,self.doc.sales_partner))
					raise Exception
				
#--------- set profile roles-----------
	def set_roles(self):
			roles = []

			if self.doc.is_customer == 1:
				roles.append('Customer')
			if self.doc.is_supplier == 1:
				roles.append('Supplier')
			if self.doc.is_sales_partner == 1:
				roles.append('Partner')
				
			sql("delete from tabUserRole where parenttype='Profile' and parent=%s",self.doc.email_id)
			sql("delete from tabDefaultValue where parenttype='Profile' and parent=%s",self.doc.email_id)
			if roles:
				for i in roles:
					match_defaults = []
					
					r = Document('UserRole')
					r.parent = self.doc.email_id
					r.role = i
					r.parenttype = 'Profile'
					r.parentfield = 'userroles'
					r.save(1)
					
					if i == 'Customer':
						def_keys = ['from_company','customer_name','customer']
						def_val = self.doc.customer
						self.set_default_val(def_keys,def_val)

					if i == 'Supplier':
						def_keys = ['supplier']
						def_val = self.doc.supplier_name
						self.set_default_val(def_keys,def_val)
						# Following fields are required for RFQ
						self.set_default_val(['send_to'], 'All Suppliers')
						supplier_type = sql("select supplier_type from `tabSupplier` where name = '%s'" % self.doc.supplier_name)
						self.set_default_val(['supplier_type'], supplier_type and supplier_type[0][0] or '')

							
#------set default values---------
	def set_default_val(self,def_keys,def_val):
		
		for d in def_keys:
			
			kv = Document('DefaultValue')
			kv.defkey = d
			kv.defvalue = def_val
			kv.parent = self.doc.email_id
			kv.parenttype = 'Profile'
			kv.parentfield = 'defaults'
			kv.save(1)