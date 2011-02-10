class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    self.tname = ' Service Quotation Detail'
    self.fname = 'service_quotation_details'
    
  def get_customer_details(self, name = ''):
    return cstr(get_obj('Sales Common').get_customer_details(name))

  def get_contact_details(self):
    return cstr(get_obj('Sales Common').get_contact_details(self))
  
  def get_serial_details(self, serial_no):
    return get_obj('Sales Common').get_serial_details(serial_no, self)

# ----------------------------------------- get tax rate if account type is tax  (Trigger written in other charges master)----------------------------#
   
  def get_rate(self,arg):
    get_obj('Other Charges').get_rate(arg)

  #--------------------- pull details from other charges master (Get Other Charges) ---------------------------------#

  def get_other_charges(self):
    return get_obj('Sales Common').get_other_charges(self)
     
# GET TERMS & CONDITIONS
# =====================================================================================
  def get_tc_details(self):
    return get_obj('Sales Common').get_tc_details(self)

    
#-------------------------------------------- clear table ------------------------------------------------------# 
  def clear_service_quotation_details(self):
    self.doc.clear_table(self.doclist, 'service_quotation_details')

  # Pull Enquiry Details
  # --------------------
  def pull_enq_details(self):
    get_obj('DocType Mapper', 'Enquiry-Service Quotation').dt_map('Enquiry', 'Service Quotation', self.doc.enq_no, self.doc, self.doclist, "[['Enquiry', 'Service Quotation']]")
 
#------------------------------------------- utility functions -------------------------------------------------#

  def check_nextdoc_docstatus(self): 
    submit_so = sql("select t1.name from `tabService Order` t1,`tabService Order Detail` t2 where t1.name = t2.parent and t2.prevdoc_docname = '%s' and t1.docstatus = 1" % (self.doc.name))
    if submit_so:
      msgprint("Service Order : " + cstr(submit_so[0][0]) + " has been created against " + cstr(self.doc.doctype) + ". So " + cstr(self.doc.doctype) + " cannot be Cancelled.")
      raise Exception, "Validation Error."
    
#---------------------------------- server side functions ----------------------------------------------------#
  
  def validate_for_items(self):
    check_list=[]
    for d in getlist(self.doclist,'service_quotation_details'):
      if cstr(d.serial_no) in check_list:
        msgprint("Serial %s has been entered twice." % d.serial_no)
        raise Exception
      else:
        check_list.append(cstr(d.serial_no))

  def validate_amc_date(self):
    for d in getlist(self.doclist,'service_quotation_details'):
      if d.amc_start_date and d.amc_end_date:         # this is done coz in case type is not AMC no need to enter amc_start_date and amc_end_date
        if getdate(d.amc_start_date) >= getdate(d.amc_end_date):
          msgprint("AMC End Date must be after AMC Start Date")
          raise Exception

  def validate(self):
    #self.doc.status = get_obj('Sales Common').set_status('Open',self.doc.doctype,self.doc.name)
    set(self.doc,'status','Draft')
    self.validate_for_items()
    self.validate_amc_date()
    #****************************** get total in words **************************************************#
    self.doc.in_words = get_obj('Sales Common').get_total_in_words('Rs', flt(self.doc.rounded_total))
    self.doc.in_words_export = get_obj('Sales Common').get_total_in_words(self.doc.currency, flt(self.doc.rounded_total_export))
    
  def on_update(self):
    sql("update `tabCustomer` set cost_center = '%s', customer_ref = '%s', customer_group = '%s' where name='%s'" % (self.doc.cost_center, self.doc.customer_ref, self.doc.customer_name, self.doc.customer_group))

  def send_sms(self):
    if not self.doc.customer_mobile_no:
      msgprint("Please enter customer mobile no")
    elif not self.doc.message:
      msgprint("Please enter the message you want to send")
    else:
      msgprint(get_obj("SMS Control", "SMS Control").send_sms([self.doc.customer_mobile_no,], self.doc.message))
      
  def send_for_approval(self):
    self.doc.save()
    send_to = []
    send = sql("select t1.email from `tabProfile` t1,`tabUserRole` t2 where t2.role = 'Sales Manager' and t2.parent = t1.name")
    for d in send:
      send_to.append(d[0])
    msg = '''
Approval of Service Quotation for
Customer: %s,

''' % (self.doc.customer_name)
    sendmail(send_to, sender='automail@webnotestech.com', subject='Approval of Service Quotation', parts=[['text/plain', msg]])
    msgprint("Service Quotation has been sent for approval")

  def send_feedback(self):
    self.doc.save()
    send_to = []
    send = sql("select t1.email from `tabProfile` t1 where t1.name = %s",self.doc.owner) 
    for d in send:
      send_to.append(d[0])
    msg = '''
Service Quotation for
Customer: %s
has been Submitted
by %s

''' % (self.doc.customer_name, self.doc.approved_by)

    sendmail(send_to, sender='automail@webnotestech.com', subject='Service Quotation status', parts=[['text/plain', msg]])
    msgprint("Feedback has been sent to %s"%(self.doc.owner))
        
  def on_submit(self):
    if not self.doc.amended_from:
      set(self.doc, 'message', 'Quotation: '+self.doc.name+' has been sent')
    else:
      set(self.doc, 'message', 'Quotation has been amended. New Quotation no:'+self.doc.name)
    #self.doc.status = get_obj('Sales Common').set_status('Submitted',self.doc.doctype,self.doc.name)
    set(self.doc,'status','Submitted')

    #check whether user has permission to submit the document
    #approved_by = cstr(get_obj('Manage Account',with_children = 1).get_permissions(self.doc.doctype,self.doc.grand_total,session['user']))
    #set(self.doc,'approved_by',approved_by)

  def on_cancel(self):
    set(self.doc, 'message', 'Quotation: '+self.doc.name+' has been cancelled')
    #self.doc.status = get_obj('Sales Common').set_status('Cancelled',self.doc.doctype,self.doc.name)
    set(self.doc,'status','Cancelled')
    self.check_nextdoc_docstatus()
    
  def print_other_charges(self,docname):
    print_lst = []
    for d in getlist(self.doclist,'other_charges'):
      lst1 = []
      lst1.append(d.description)
      lst1.append(d.total)
      print_lst.append(lst1)
    return print_lst