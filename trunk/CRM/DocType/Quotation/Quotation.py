class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    self.tname = 'Quotation Detail'
    self.fname = 'quotation_details'
    
    # Notification objects
    self.feed_obj = get_obj('Feed Control')
    self.notify_obj = get_obj('Notification Control')

  # Autoname
  # ---------
  def autoname(self):
    self.doc.name = make_autoname(self.doc.naming_series+'.#####')


# DOCTYPE TRIGGER FUNCTIONS
# ==============================================================================    
 
  # Pull Enquiry Details
  # --------------------
  def pull_enq_details(self):
    self.doc.clear_table(self.doclist, 'quotation_details')
    get_obj('DocType Mapper', 'Enquiry-Quotation').dt_map('Enquiry', 'Quotation', self.doc.enq_no, self.doc, self.doclist, "[['Enquiry', 'Quotation'],['Enquiry Detail', 'Quotation Detail']]")

    self.get_adj_percent()

    return cstr(self.doc.quotation_to)
  # Get Customer Details
  # --------------------
  def get_customer_details(self):
    return cstr(get_obj('Sales Common').get_customer_details(self))

  # Get contact person details based on customer selected
  # ------------------------------------------------------
  def get_contact_details(self, arg):
    return cstr(get_obj('Sales Common').get_contact_details(arg))
  
  # Clear Quotation Details
  # -----------------------
  def clear_quotation_details(self):
    self.doc.clear_table(self.doclist, 'quotation_details')

    
# QUOTATION DETAILS TRIGGER FUNCTIONS
# ================================================================================    

  # Get Item Details
  # -----------------
  def get_item_details(self, item_code):
    return get_obj('Sales Common').get_item_details(item_code, self)
  
  # Re-calculates Basic Rate & amount based on Price List Selected
  # --------------------------------------------------------------
  def get_adj_percent(self, arg=''):
    get_obj('Sales Common').get_adj_percent(self)
    

# OTHER CHARGES TRIGGER FUNCTIONS
# ====================================================================================
  
  # Get Tax rate if account type is TAX
  # -----------------------------------
  def get_rate(self,arg):
    return get_obj('Sales Common').get_rate(arg)

  # Pull details from other charges master (Get Other Charges)
  # ----------------------------------------------------------
  def get_other_charges(self):
    return get_obj('Sales Common').get_other_charges(self)
  
  # Get Lead Details along with its details
  # ==============================================================
  def get_lead_details(self, name):
    details = sql("select lead_name, address, territory, email_id, contact_no from `tabLead` where name = '%s'" %(name), as_dict = 1)
    ret = {
      'lead_name'         :  details and details[0]['lead_name'] or '',
      'customer_address'  :  details and details[0]['address'] or '',
      'territory'         :  details and details[0]['territory'] or '',
      'email_id'          :  details and details[0]['email_id'] or '',
      'contact_no'        :  details and details[0]['contact_no'] or ''
    }
    return cstr(ret)

  
     
# GET TERMS AND CONDITIONS
# ====================================================================================
  def get_tc_details(self):
    return get_obj('Sales Common').get_tc_details(self)

    
# VALIDATE
# ==============================================================================================
  
  # Amendment date is necessary if document is amended
  # --------------------------------------------------
  def validate_mandatory(self):
    if self.doc.amended_from and not self.doc.amendment_date:
      msgprint("Please Enter Amendment Date")
      raise Exception

  # Fiscal Year Validation
  # ----------------------
  def validate_fiscal_year(self):
    get_obj('Sales Common').validate_fiscal_year(self.doc.fiscal_year,self.doc.transaction_date,'Quotation Date')
  
  # Does not allow same item code to be entered twice
  # -------------------------------------------------
  def validate_for_items(self):
    check_list=[]
    chk_dupl_itm = []
    for d in getlist(self.doclist,'quotation_details'):
      ch = sql("select is_stock_item from `tabItem` where name = '%s'"%d.item_code)
      if ch and ch[0][0]=='Yes':
        if cstr(d.item_code) in check_list:
	  msgprint("Item %s has been entered twice." % d.item_code)
	  raise Exception
	else:
	  check_list.append(cstr(d.item_code))
      
      if ch and ch[0][0]=='No':
        f = [cstr(d.item_code),cstr(d.description)]
	if f in chk_dupl_itm:
	  msgprint("Item %s has been entered twice." % d.item_code)
	  raise Exception
	else:
	  chk_dupl_itm.append(f)


  #do not allow sales item in maintenance quotation and service item in sales quotation
  #-----------------------------------------------------------------------------------------------
  def validate_order_type(self):
    if self.doc.order_type == 'Maintenance':
      for d in getlist(self.doclist, 'quotation_details'):
        is_service_item = sql("select is_service_item from `tabItem` where name=%s", d.item_code)
        is_service_item = is_service_item and is_service_item[0][0] or 'No'
        
        if is_service_item == 'No':
          msgprint("You can not select non service item "+d.item_code+" in Maintenance Quotation")
          raise Exception
    else:
      for d in getlist(self.doclist, 'quotation_details'):
        is_sales_item = sql("select is_sales_item from `tabItem` where name=%s", d.item_code)
        is_sales_item = is_sales_item and is_sales_item[0][0] or 'No'
        
        if is_sales_item == 'No':
          msgprint("You can not select non sales item "+d.item_code+" in Sales Quotation")
          raise Exception
  
  #--------------Validation For Last Contact Date-----------------
  # ====================================================================================================================
  def set_last_contact_date(self):
    #if not self.doc.contact_date_ref:
      #self.doc.contact_date_ref=self.doc.contact_date
      #self.doc.last_contact_date=self.doc.contact_date_ref
    if self.doc.contact_date_ref and self.doc.contact_date_ref != self.doc.contact_date:
      if getdate(self.doc.contact_date_ref) < getdate(self.doc.contact_date):
        self.doc.last_contact_date=self.doc.contact_date_ref
      else:
        msgprint("Contact Date Cannot be before Last Contact Date")
        raise Exception
      #set(self.doc, 'contact_date_ref',self.doc.contact_date)
  

  # Validate
  # --------
  def validate(self):
    self.validate_fiscal_year()
    self.validate_mandatory()
    self.set_last_contact_date()
    self.validate_order_type()
    self.validate_for_items()
    sales_com_obj = get_obj('Sales Common')
    sales_com_obj.check_active_sales_items(self)
    sales_com_obj.validate_max_discount(self,'quotation_details') #verify whether rate is not greater than max_discount
    sales_com_obj.check_conversion_rate(self)
    
    # Get total in words
    self.doc.in_words = sales_com_obj.get_total_in_words(get_defaults()['currency'], self.doc.rounded_total)
    self.doc.in_words_export = sales_com_obj.get_total_in_words(self.doc.currency, self.doc.rounded_total_export)

  def on_update(self):
    # Add to calendar
    #if self.doc.contact_date and self.doc.last_contact_date != self.doc.contact_date:
    if self.doc.contact_date and self.doc.contact_date_ref != self.doc.contact_date:
      if self.doc.contact_by:
        self.add_calendar_event()
      set(self.doc, 'contact_date_ref',self.doc.contact_date)
    
    # Set Quotation Status
    set(self.doc, 'status', 'Draft')

    # Set feed
    if not self.doc.creation:
      self.feed_obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      self.feed_obj.make_feed('modified', self.doc.doctype, self.doc.name)
  
  # Add to Calendar
  # ====================================================================================================================
  def add_calendar_event(self):
    desc=''
    user_lst =[]
    if self.doc.customer:
      if self.doc.contact_person:
        desc = 'Contact '+cstr(self.doc.contact_person)
      else:
        desc = 'Contact customer '+cstr(self.doc.customer)
    elif self.doc.lead:
      if self.doc.lead_name:
        desc = 'Contact '+cstr(self.doc.lead_name)
      else:
        desc = 'Contact lead '+cstr(self.doc.lead)
    desc = desc+ '.By : ' + cstr(self.doc.contact_by)
    
    if self.doc.to_discuss:
      desc = desc+' To Discuss : ' + cstr(self.doc.to_discuss)
    
    ev = Document('Event')
    ev.description = desc
    ev.event_date = self.doc.contact_date
    ev.event_hour = '10:00'
    ev.event_type = 'Private'
    ev.ref_type = 'Enquiry'
    ev.ref_name = self.doc.name
    ev.save(1)
    
    user_lst.append(self.doc.owner)
    
    chk = sql("select t1.name from `tabProfile` t1, `tabSales Person` t2 where t2.email_id = t1.name and t2.name=%s",self.doc.contact_by)
    if chk:
      user_lst.append(chk[0][0])
    
    for d in user_lst:
      ch = addchild(ev, 'event_individuals', 'Event User', 0)
      ch.person = d
      ch.save(1)
  
  #update enquiry
  #------------------
  def update_enquiry(self, flag):
    prevdoc=''
    for d in getlist(self.doclist, 'quotation_details'):
      if d.prevdoc_docname:
        prevdoc = d.prevdoc_docname
    
    if prevdoc:
      if flag == 'submit': #on submit
        sql("update `tabEnquiry` set status = 'Quotation Sent' where name = %s", prevdoc)
      elif flag == 'cancel': #on cancel
        sql("update `tabEnquiry` set status = 'Open' where name = %s", prevdoc)
      elif flag == 'order lost': #order lost
        sql("update `tabEnquiry` set status = 'Enquiry Lost' where name=%s", prevdoc)
      elif flag == 'order confirm': #order confirm
        sql("update `tabEnquiry` set status='Order Confirmed' where name=%s", prevdoc)
  
  # declare as order lost
  #-------------------------
  def declare_order_lost(self,arg):
    chk = sql("select t1.name from `tabSales Order` t1, `tabSales Order Detail` t2 where t2.parent = t1.name and t1.docstatus=1 and t2.prevdoc_docname = %s",self.doc.name)
    if chk:
      msgprint("Sales Order No. "+cstr(chk[0][0])+" is submitted against this Quotation. Thus 'Order Lost' can not be declared against it.")
      raise Exception
    else:
      set(self.doc, 'status', 'Order Lost')
      set(self.doc, 'order_lost_reason', arg)
      self.update_enquiry('order lost')
      return cstr('true')
  
  #check if value entered in item table
  #--------------------------------------
  def check_item_table(self):
    if not getlist(self.doclist, 'quotation_details'):
      msgprint("Please enter item details")
      raise Exception
    
  # ON SUBMIT
  # =========================================================================
  def on_submit(self):
    self.check_item_table()
    if not self.doc.amended_from:
      set(self.doc, 'message', 'Quotation: '+self.doc.name+' has been sent')
    else:
      set(self.doc, 'message', 'Quotation has been amended. New Quotation no:'+self.doc.name)
    
    # Check for Approving Authority
    get_obj('Authorization Control').validate_approving_authority(self.doc.doctype, self.doc.company, self.doc.grand_total, self)

    # Set Quotation Status
    set(self.doc, 'status', 'Submitted')
    
    #update enquiry status
    self.update_enquiry('submit')
    
    # on submit notification
    self.notify_obj.notify_contact('Quotation', self.doc.doctype, self.doc.name, self.doc.email_id, self.doc.contact_person)

    # make feed
    self.feed_obj.make_feed('submitted', self.doc.doctype, self.doc.name)
    
# ON CANCEL
# ==========================================================================
  def on_cancel(self):
    set(self.doc, 'message', 'Quotation: '+self.doc.name+' has been cancelled')
    
    #update enquiry status
    self.update_enquiry('cancel')
    
    set(self.doc,'status','Cancelled')
    
    # make feed
    self.feed_obj.make_feed('cancelled', self.doc.doctype, self.doc.name)
  
# SEND SMS
# =============================================================================
  def send_sms(self):
    if not self.doc.customer_mobile_no:
      msgprint("Please enter customer mobile no")
    elif not self.doc.message:
      msgprint("Please enter the message you want to send")
    else:
      msgprint(get_obj("SMS Control", "SMS Control").send_sms([self.doc.customer_mobile_no,], self.doc.message))
  
# Print other charges
# ===========================================================================
  def print_other_charges(self,docname):
    print_lst = []
    for d in getlist(self.doclist,'other_charges'):
      lst1 = []
      lst1.append(d.description)
      lst1.append(d.total)
      print_lst.append(lst1)
    return print_lst
  
  def update_followup_details(self):
    sql("delete from `tabFollow up` where parent = '%s'"%self.doc.name)
    for d in getlist(self.doclist, 'follow_up'):
      d.save()