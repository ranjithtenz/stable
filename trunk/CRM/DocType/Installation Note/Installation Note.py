class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    self.tname = 'Installed Item Details'
    self.fname = 'installed_item_details'

  # Autoname
  # ---------
  def autoname(self):
    self.doc.name = make_autoname(self.doc.naming_series+'.#####')
  
  #fetch customer details
  #=================================
  def get_customer_details(self):
    det = sql("select t1.customer_name, t1.address,t1.territory,t2.contact_name from `tabCustomer` t1, `tabContact` t2 where t1.name = '%s' and t1.name=t2.customer and t2.is_primary_contact = 'Yes'"%self.doc.customer, as_dict=1)
    
    ret = {
      'customer_name':  det and det[0]['customer_name'] or '',
      'address'  :  det and det[0]['address'] or '',
      'territory':  det and det[0]['territory'] or '',
      'contact_person' : det and det[0]['contact_name'] or ''
    }

    return str(ret)
  
  #fetch delivery note details
  #====================================
  def pull_delivery_note_details(self):
    self.validate_prev_docname()
    self.doclist = get_obj('DocType Mapper', 'Delivery Note-Installation Note').dt_map('Delivery Note', 'Installation Note', self.doc.delivery_note_no, self.doc, self.doclist, "[['Delivery Note', 'Installation Note'],['Delivery Note Detail', 'Installed Item Details']]")
  
  # Validates that Delivery Note is not pulled twice 
  #============================================
  def validate_prev_docname(self):
    for d in getlist(self.doclist, 'installed_item_details'): 
      if self.doc.delivery_note_no == d.prevdoc_docname:
        msgprint(cstr(self.doc.delivery_note_no) + " delivery note details have already been pulled. ")
        raise Exception, "Validation Error. "
  
  #Fiscal Year Validation
  #================================
  def validate_fiscal_year(self):
    get_obj('Sales Common').validate_fiscal_year(self.doc.fiscal_year,self.doc.inst_date,'Installation Date')
  
  #  Validate Mandatory 
  #===============================
  def validate_mandatory(self):
    # Amendment Date
    if self.doc.amended_from and not self.doc.amendment_date:
      msgprint("Please Enter Amendment Date")
      raise Exception, "Validation Error. "
  
  # Validate values with reference document
  #----------------------------------------
  def validate_reference_value(self):
    get_obj('DocType Mapper', 'Delivery Note-Installation Note', with_children = 1).validate_reference_value(self, self.doc.name)
  
  #check if serial no added
  #-----------------------------
  def is_serial_no_added(self,item_code,serial_no):
    ar_required = sql("select has_serial_no from tabItem where name = '%s'" % item_code)
    ar_required = ar_required and ar_required[0][0] or ''
    if ar_required == 'Yes' and not serial_no:
      msgprint("Serial No is mandatory for item: "+ item_code)
      raise Exception
    elif ar_required != 'Yes' and cstr(serial_no).strip():
      msgprint("If serial no required, please select 'Yes' in 'Has Serial No' in Item :"+item_code)
      raise Exception
  
  #check if serial no exist in system
  #-------------------------------------
  def is_serial_no_exist(self, item_code, serial_no):
    for x in serial_no:
      chk = sql("select name from `tabSerial No` where name =%s", x)
      if not chk:
        msgprint("Serial No "+x+" does not exist in the system")
        raise Exception
  
  #check if serial no already installed
  #------------------------------------------
  def is_serial_no_installed(self,cur_s_no,item_code):
    for x in cur_s_no:
      status = sql("select status from `tabSerial No` where name = %s", x)
      status = status and status[0][0] or ''
      
      if status == 'Installed':
        msgprint("Item "+item_code+" with serial no. "+x+" already installed")
        raise Exception, "Validation Error."
  
  #get list of serial no from previous_doc
  #----------------------------------------------
  def get_prevdoc_serial_no(self, prevdoc_detail_docname, prevdoc_docname):
    prevdoc_s_no1 =[]
    prevdoc_serial_no = sql("select serial_no from `tabDelivery Note Detail` where name = '%s' and parent ='%s'" % (d.prevdoc_detail_docname, d.prevdoc_docname))
    prevdoc_serial_no = prevdoc_serial_no and prevdoc_serial_no[0][0] or ''
    if prevdoc_serial_no:
      prevdoc_serial_no = prevdoc_serial_no.replace(' ', '')
      prevdoc_s_no1 = prevdoc_serial_no.split(',')
    return prevdoc_s_no1
  
  #check if serial no added for all items
  #------------------------------------------------
  def is_serial_no_added_for_all(self, cur_s_no, qty, item_code):
    if not flt(len(cur_s_no)) == flt(qty):
      msgprint("Please enter serial nos for all "+ cstr(qty) + " quantity of item "+cstr(item_code))
      raise Exception
  
  #check if all serial nos from current record exist in resp delivery note
  #---------------------------------------------------------------------------------
  def is_serial_no_match(self, cur_s_no, prevdoc_s_no, prevdoc_docname):
    for x in cur_s_no:
      if not(x in prevdoc_s_no):
        msgprint("Serial No. "+x+" not present in respective Delivery Note "+prevdoc_docname)
        raise Exception, "Validation Error."
  
  #validate serial number
  #----------------------------------------
  def validate_serial_no(self):
    cur_s_no, prevdoc_s_no = [], []
    
    for d in getlist(self.doclist, 'installed_item_details'):
      self.is_serial_no_added(d.item_code, d.serial_no)
      
      if d.serial_no:
        cur_serial_no = d.serial_no.replace(' ', '')
        cur_s_no = cur_serial_no.split(',')
        
        self.is_serial_no_exist(d.item_code, cur_s_no)
        self.is_serial_no_added_for_all(cur_s_no, d.qty, d.item_code)
        
        prevdoc_s_no = self.get_prevdoc_serial_no(d.prevdoc_detail_docname, d.prevdoc_docname)
        if prevdoc_s_no:
          self.is_serial_no_match(cur_s_no, prevdoc_s_no, d.prevdoc_docname)
        
        self.is_serial_no_installed(cur_s_no, d.item_code)
    return cur_s_no
  
  #validate installation date
  #-------------------------------
  def validate_installation_date(self):
    for d in getlist(self.doclist, 'installed_item_details'):
      if d.prevdoc_docname:
        d_date = sql("select posting_date from `tabDelivery Note` where name=%s", d.prevdoc_docname)
        d_date = d_date and d_date[0][0] or ''
        
        if d_date > getdate(self.doc.inst_date):
          msgprint("Installation Date can not be before Delivery Date "+cstr(d_date)+" for item "+d.item_code)
          raise Exception
  
  def validate(self):
    self.validate_fiscal_year()
    self.validate_installation_date()
    self.check_item_table()
    sales_com_obj = get_obj(dt = 'Sales Common')
    sales_com_obj.check_active_sales_items(self)
    sales_com_obj.get_prevdoc_date(self)
    self.validate_mandatory()
    self.validate_reference_value()
  
  def check_item_table(self):
    if not(getlist(self.doclist, 'installed_item_details')):
      msgprint("Please fetch items from Delivery Note selected")
      raise Exception
  
  def on_update(self):
    set(self.doc, 'status', 'Draft')

    # make feed
    obj = get_obj('Feed Control','Feed Control')
    
    if not self.doc.creation:
      obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      obj.make_feed('modified', self.doc.doctype, self.doc.name)

    self.doc.save()
  
  def on_submit(self):
    valid_lst = []
    valid_lst = self.validate_serial_no()
    
    get_obj("Sales Common").update_prevdoc_detail(1,self)
    
    for x in valid_lst:
      wp = sql("select warranty_period from `tabSerial No` where name = '%s'"% x)
      wp = wp and wp[0][0] or 0
      if wp:
        sql("update `tabSerial No` set maintenance_status = 'Under Warranty' where name = '%s'" % x)
      
      sql("update `tabSerial No` set status = 'Installed' where name = '%s'" % x)
    
    set(self.doc, 'status', 'Submitted')

    # make feed
    get_obj('Feed Control').make_feed('submitted', self.doc.doctype, self.doc.name)
  
  def on_cancel(self):
    cur_s_no = []
    sales_com_obj = get_obj(dt = 'Sales Common')
    sales_com_obj.update_prevdoc_detail(0,self)
    
    for d in getlist(self.doclist, 'installed_item_details'):
      if d.serial_no:
        #get current list of serial no
        cur_serial_no = d.serial_no.replace(' ', '')
        cur_s_no = cur_serial_no.split(',')
    
    for x in cur_s_no:
      sql("update `tabSerial No` set status = 'Delivered' where name = '%s'" % x)
      
    set(self.doc, 'status', 'Cancelled')

    # make feed
    get_obj('Feed Control').make_feed('cancelled', self.doc.doctype, self.doc.name)