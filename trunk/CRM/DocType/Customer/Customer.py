class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    self.prefix = is_testing and 'test' or 'tab'

  def autoname(self):
    cust_master_name = get_defaults()['cust_master_name']

    if cust_master_name == 'Customer Name':
    
      supp = sql("select name from `tabSupplier` where name = '%s'" % (self.doc.customer_name))
      supp = supp and supp[0][0] or ''
      if supp:
        msgprint("Supplier by this name already exist")
        raise Exception
      else:
        self.doc.name = self.doc.customer_name
    else:
      self.doc.name = make_autoname(self.doc.naming_series+'.#####')       

  # get parent account
  # ------------------
  def get_receivables_group(self):
    g = sql("select receivables_group from tabCompany where name=%s", self.doc.company)
    
    g = g and g[0][0] or '' 
    if not g:
      msgprint("Update Company master, assign a default group for Receivables")
      raise Exception
    return g

  '''def add_account(self, ac, par, is_territory, abbr):

    # if not group created for zone, create it
    if is_territory and (not sql("select name from tabAccount where name=%s", par)):
      g = self.get_receivables_group()
      self.add_account(self.doc.zone, g, 0, abbr)
    
    arg = {'account_name':ac,'parent_account':par, 'group_or_ledger':'Group', 'company':self.doc.company,'account_type':'','tax_rate':'0'}
   
    t = get_obj('GL Control').add_ac(cstr(arg))
    msgprint("Created Group " + t)'''
  
  def get_company_abbr(self):
    return sql("select abbr from tabCompany where name=%s", self.doc.company)[0][0]
  
  '''def get_parent_account(self, abbr):
    
    if not self.doc.territory:
      msgprint("Territory is mandatory")
      raise Exception

    if not sql("select name from tabAccount where name=%s", (self.doc.territory + " - " + abbr)):

      # if not group created for territory, create it
      self.add_account(self.doc.territory, self.doc.zone + ' - ' + abbr, 1, abbr)
    
    return self.doc.territory + " - " + abbr'''  
  
  # create accont head - in tree under receivables_group of selected company
  # ------------------
  def create_account_head(self):
    if self.doc.company :
      abbr = self.get_company_abbr()  
      if not sql("select name from tabAccount where name=%s", (self.doc.name + " - " + abbr)):
        parent_account = self.get_receivables_group()
        arg = {'account_name':self.doc.name,'parent_account': parent_account, 'group_or_ledger':'Ledger', 'company':self.doc.company,'account_type':'','tax_rate':'0','master_type':'Customer','master_name':self.doc.name,'address':self.doc.address}
        # create
        ac = get_obj('GL Control').add_ac(cstr(arg))
        msgprint("Account Head created for "+ac)
    else :
      msgprint("Please Select Company under which you want to create account head")

  def check_state(self):
    return NEWLINE + NEWLINE.join([i[0] for i in sql("select state_name from `tabState` where `tabState`.country='%s' " % self.doc.country)])

  def validate(self):
    import string
    #validation for individual customers phone number field...
    if self.doc.customer_type == 'Individual' and not self.doc.phone_1:
      msgprint("As this customer is Individual, you need to enter phone number.")
      raise Exception
      
             
    #validation for Naming Series mandatory field...
    if get_defaults()['cust_master_name'] == 'Naming Series':

      if not self.doc.naming_series:
        msgprint("Series is Mandatory.")
        raise Exception
    
    # check if first creation
    self.first_creation = (not self.doc.name) and 1 or 0
  
    # make address
    if not (self.doc.address_line1)  and not (self.doc.city) and not (self.doc.state) and not (self.doc.country) and not (self.doc.pincode):
      return "Please enter address"

    if not (self.doc.phone_1) and not (self.doc.phone_2) and not (self.doc.fax_1):
      return "Please enter contact number"

  def get_customer(self, customer_name):
    customer = sql("select * from `tabCustomer` where name = %s", (customer_name), as_dict = 1)
    return customer
  
  #create primary contact for customer
  #------------------------------------------
  def create_p_contact(self,nm,phn_no,email_id,mob_no,fax,cont_addr):

      c1 = Document('Contact')
      c1.first_name = nm
      c1.contact_name = nm
      c1.contact_no = phn_no
      c1.email_id = email_id
      c1.mobile_no = mob_no
      c1.fax = fax
      c1.contact_address = cont_addr
      c1.is_primary_contact = 'Yes'
      c1.is_customer =1
      c1.customer = self.doc.name
      c1.customer_name = self.doc.customer_name
      c1.customer_address = self.doc.address
      c1.customer_group = self.doc.customer_group
      c1.save(1)
      msgprint("Primary Contact for customer %s created successfully."%nm)
  
  def on_update(self):
    if not self.doc.naming_series:
      self.doc.naming_series = ''
    

    if self.doc.first_creation:
      msgprint("")
    
    # build address
    # -------------
    addr_flds = [self.doc.address_line1, self.doc.address_line2, self.doc.city, self.doc.state, self.doc.country, self.doc.pincode]
    address_line = NEWLINE.join(filter(lambda x : (x!='' and x!=None),addr_flds))

    if self.doc.phone_1:
      address_line = address_line + NEWLINE + "Phone: " + cstr(self.doc.phone_1)
    if self.doc.email_1:
      address_line = address_line + NEWLINE + "E-mail: " + cstr(self.doc.email_1)

    set(self.doc,'address', address_line)
    
    telephone = "(O): " + cstr(self.doc.phone_1) +NEWLINE+ cstr(self.doc.phone_2) + NEWLINE + "(M): " +  NEWLINE + "(fax): " + cstr(self.doc.fax_1)
    set(self.doc,'telephone',telephone)


    contact = sql("select distinct name from `tabContact` where customer_name=%s", (self.doc.customer_name))
    contact = contact and contact[0][0] or ''
    
    if self.doc.lead_name:
      sql("update `tabLead` set status='Converted' where name = %s", self.doc.lead_name)

    #create contact
    if not contact:
    
      #create primary contact for individual customer 
      if self.doc.customer_type == 'Individual':
        self.create_p_contact(self.doc.customer_name,self.doc.phone_1,'','',self.doc.fax_1,self.doc.address)
    
      #update lead status and create primary contact
      #---------------------
      elif self.doc.lead_name:
        c_detail = sql("select lead_name, company_name, contact_no, mobile_no, email_id, fax, address from `tabLead` where name =%s", self.doc.lead_name, as_dict=1)
        self.create_p_contact(c_detail and c_detail[0]['lead_name'] or '', c_detail and c_detail[0]['contact_no'] or '', c_detail and c_detail[0]['email_id'] or '', c_detail and c_detail[0]['mobile_no'] or '', c_detail and c_detail[0]['fax'] or '', c_detail and c_detail[0]['address'] or '')

    # create account head
    # -------------------
    self.create_account_head()

    # update feed
    # -----------
    obj = get_obj('Feed Control', 'Feed Control')
    if not self.doc.creation:
      obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      obj.make_feed('modified', self.doc.doctype, self.doc.name)

  def get_contacts(self,nm):
    if nm:
      contact_details =convert_to_lists(sql("select name, CONCAT(IFNULL(first_name,''),' ',IFNULL(last_name,'')),contact_no,email_id from `tabContact` where customer = '%s'"%nm))
      return contact_details
    else:
      return ''
  
  def on_trash(self):
    if self.doc.lead_name:
      sql("update `tabLead` set status='Interested' where name=%s",self.doc.lead_name)
