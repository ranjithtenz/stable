class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    self.tname = 'Service Order Detail'
    self.fname = 'service_order_details'
  
  def get_customer_details(self, name):
    return get_obj('Sales Common').get_customer_details(name)
  
  def get_serial_details(self, serial_no):
    return get_obj('Sales Common').get_serial_details(serial_no, self)


#---------------- get tax rate if account type is tax  (Trigger written in other charges master)----------------------------#
   
  def get_rate(self,arg):
    get_obj('Other Charges').get_rate(arg)

#--------------------- pull details from other charges master (Get Other Charges) ---------------------------------#

  def get_other_charges(self):
    return get_obj('Sales Common').get_other_charges(self)

# GET TERMS & CONDITIONS
# =====================================================================================
  def get_tc_details(self):
    return get_obj('Sales Common').get_tc_details(self)

    
#------------------------------Get inquiry date-----------------------------------------------------------------#

  def get_inquiry_date(self, arg =''):
    lead = sql("select date from tabLead where name = %s", arg, as_dict = 1)
    ret = {
      'inquiry_date'  :  lead and lead[0]['date'].strftime('%Y-%m-%d') or ''
    }
    return str(ret)
 
  # Get Commission rate of Sales Partner
  # -------------------------------------
  def get_comm_rate(self, sales_partner):
    return get_obj('Sales Common').get_comm_rate(sales_partner, self)
 
  #------------------------------------------------------------------------------------------
  #trigger functions
  def pull_service_quotation_details(self):
    self.validate_doc()
    self.doc.clear_table(self.doclist, 'other_charges')
    self.doc.clear_table(self.doclist, 'service_order_details')
    self.doc.clear_table(self.doclist, 'sales_team')
    get_obj('DocType Mapper', 'Service Quotation-Service Order').dt_map('Service Quotation', 'Service Order', self.doc.service_quotation_no, self.doc, self.doclist, "[['Service Quotation', 'Service Order'],['Service Quotation Detail', 'Service Order Detail'], ['Other Charges', 'Other Charges'],['TC Detail','TC Detail'],['Sales Team','Sales Team']]")

  def clear_service_order_details(self):
    self.doc.clear_table(self.doclist, 'service_order_details')

  #-------------------------------------------------------------------------------------------
  #Validation
  def validate_doc(self):
    if self.doc.service_quotation_no:
      dt = sql("select name,company, docstatus from `tabService Quotation` where name = '%s'" % self.doc.service_quotation_no)
      if dt:  #check for incorrect docname
        name = dt and dt[0][0] or ''
        company = dt and dt[0][1] or ''
        docstatus = dt and dt[0][2] or 0
        if (company != self.doc.company):
          msgprint("Service Quotation: " + cstr(self.doc.service_quotation_no) + " does not belong to the Company: " + cstr(self.doc.company))
          raise Exception, "Validation Error."
        if (docstatus != 1):
          msgprint("Service Quotation: " + cstr(self.doc.service_quotation_no) + " is not Submitted Document.")
          raise Exception, "Validation Error."
      else:
        msgprint("Service Quotation: " + cstr(self.doc.service_quotation_no) + " does not exist in the system")
        raise Exception, "Validation Error."
  
  def validate_mandatory(self):
    for d in getlist(self.doclist, 'service_order_details'):
      if d.prevdoc_docname and self.doc.service_quotation_date:
        if getdate(self.doc.service_quotation_date) > getdate(self.doc.transaction_date):
          msgprint("Service Order Date cannot be before Quotation Date")
          raise Exception
   
    if self.doc.amended_from and not self.doc.amendment_date:
      msgprint("Please Enter Amendment Date")
      raise Exception

    
#---------------------------------- server side functions ----------------------------------------------------#
  
  def validate_for_items(self):
    check_list=[]
    for d in getlist(self.doclist,'service_order_details'):
      if cstr(d.serial_no) in check_list:
        msgprint("Serial %s has been entered twice." % d.serial_no)
        raise Exception
      else:
        check_list.append(cstr(d.serial_no))

  def validate_amc_date(self):
    for d in getlist(self.doclist,'service_order_details'):
      if d.start_date and d.end_date:      # in AMC we don't require start_date and end_date
        if getdate(d.start_date) >= getdate(d.end_date):
          msgprint("End Date must be after Start Date in Item .")
          raise Exception
        if flt(d.no_of_visit) <= 0:
          msgprint("No of visit must be a positive value")
          raise Exception

  def validate(self):
    #self.doc.status = get_obj('Sales Common').set_status('Open',self.doc.doctype,self.doc.name)
    set(self.doc,'status','Draft')
    self.validate_mandatory()
    self.validate_for_items()
    self.validate_amc_date()
    #****************************** get total in words **************************************************#
    self.doc.in_words = get_obj('Sales Common').get_total_in_words('Rs', flt(self.doc.rounded_total))
    self.doc.in_words_export = get_obj('Sales Common').get_total_in_words(self.doc.currency, flt(self.doc.rounded_total_export))
    
  def send_sms(self):
    if not self.doc.customer_mobile_no:
      msgprint("Please enter customer mobile no")
    elif not self.doc.message:
      msgprint("Please enter the message you want to send")
    else:
      msgprint(get_obj("SMS Control", "SMS Control").send_sms([self.doc.customer_mobile_no,], self.doc.message))
        
  def on_submit(self):
    if not self.doc.amended_from:
      set(self.doc, 'message', 'Service Order: '+self.doc.name+' has been sent')
    else:
      set(self.doc, 'message', 'Service Order has been amended. New Service Order no:'+self.doc.name)
    
    #self.doc.status = get_obj('Sales Common').set_status('Submitted',self.doc.doctype,self.doc.name)    
    set(self.doc,'status','Submitted')
    
    self.update_serial_master()
    msgprint("Schedule added to calender")
    
  def on_cancel(self):
    set(self.doc, 'message', 'Service Order: '+self.doc.name+' has been cancelled')
    #self.doc.status = get_obj('Sales Common').set_status('Cancelled',self.doc.doctype,self.doc.name)
    set(self.doc,'status','Cancelled')
    
    # remove from calendar and serial master
    self.remove_from_serial_table()
    self.remove_calendar_event()

  def print_other_charges(self,docname):
    print_lst = []
    for d in getlist(self.doclist,'other_charges'):
      lst1 = []
      lst1.append(d.description)
      lst1.append(d.total)
      print_lst.append(lst1)
    return print_lst
  
  # ----------------------Add service schedule in serial Master---------------------------------
  
  def update_serial_master(self):
    import datetime
    for d in getlist(self.doclist,'service_order_details'):
      if d.no_of_visit == 1:
        self.add_to_serial_table(d.serial_no,d.start_date)
      else :
        st_dt = getdate(d.start_date)
        end_dt = getdate(d.end_date)
        if d.no_of_visit > 0:
          days = cint(((end_dt - st_dt).days)/d.no_of_visit)  # this gives the period between two visits
        schedule_list = []
        for no in range(cint(d.no_of_visit)):
          if (getdate(str(st_dt)) < getdate(str(end_dt))):
            sch_dt = add_days(str(st_dt), days)
            schedule_list.append(sch_dt)
            st_dt = sch_dt
        for sl in range (len(schedule_list)):
          self.add_to_serial_table(d.serial_no,schedule_list[sl])
      sql("update `tabSerial No` set amc_expiry_date = '%s' where name = '%s'"%(d.end_date,d.serial_no))
    
  def add_to_serial_table(self,ser_no,sch_dt):
    serial_list = Document('Serial No',ser_no)
    child = addchild(serial_list, 'service_schedule', 'Service Schedule', 0)
    child.schedule_date = sch_dt
    child.customer_name = self.doc.customer_name
    child.cost_center = self.doc.cost_center
    child.service_type = "AMC"
    child.against_docname = self.doc.name
    child.save()
    self.add_calendar_event(ser_no,sch_dt,self.doc.order_type)
    
     
  def add_calendar_event(self,ser_no,sch_dt,service):
    ev = Document('Event')
    ev.description = cstr(ser_no) + '/' + cstr(service)
    ev.event_date = sch_dt
    ev.event_hour = '10:00'
    ev.event_type = 'Private'
    ev.ref_type = 'Service Order'
    ev.ref_name = self.doc.name
    ev.save(1)
      
    user_list=['Sales Manager', 'Sales User']
    for d in user_list:
      ch = addchild(ev, 'event_roles', 'Event Role', 0)
      ch.role = d
      ch.save()

  def remove_from_serial_table(self):
    sql("delete from `tabService Schedule` where against_docname = %s",self.doc.name)

  def remove_calendar_event(self):
    sql("update tabEvent set event_type = 'Cancel' where ref_type = 'Service Order' and ref_name = '%s'" % self.doc.name)
    msgprint("Schedule Cancelled from calendar")