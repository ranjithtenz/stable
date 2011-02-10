class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    self.defaults = get_defaults()
    self.tname = 'Indent Detail'
    self.fname = 'indent_details'

  # Autoname
  # ---------
  def autoname(self):
    self.doc.name = make_autoname(self.doc.naming_series+'.#####')


  def get_default_schedule_date(self):
    get_obj(dt = 'Purchase Common').get_default_schedule_date(self)
    
  def validate_fiscal_year(self):
    get_obj(dt = 'Purchase Common').validate_fiscal_year(self.doc.fiscal_year,self.doc.transaction_date,'Indent Date')

  # get item details
  def get_item_details(self, arg =''):
    return cstr( get_obj(dt='Purchase Common').get_item_details(self,arg) )

  # Get UOM Details
  def get_uom_details(self, arg = ''):
    return cstr(get_obj(dt='Purchase Common').get_uom_details(arg))

  # GET TERMS & CONDITIONS
  def get_tc_details(self):
    return get_obj('Purchase Common').get_tc_details(self)
    
  # ******************** Validate Schedule Date *********************
  def validate_schedule_date(self):
     #:::::::: validate schedule date v/s indent date ::::::::::::
    for d in getlist(self.doclist, 'indent_details'):
      if d.schedule_date < self.doc.transaction_date:
        msgprint("Expected Schedule Date cannot be before Indent Date")
        raise Exception
        
  # validate
  def validate(self):
    self.validate_schedule_date()
    self.validate_fiscal_year()
    
    # Step 1:=> set status as "Draft"
    set(self.doc, 'status', 'Draft')

    # Step 2:=> Get Purchase Common Obj
    pc_obj = get_obj(dt='Purchase Common')

    # Step 3:=> Validate Mandatory
    pc_obj.validate_mandatory(self)

    # Step 4:=> Validate for items
    pc_obj.validate_for_items(self)
    
  # On Submit Functions
  #----------------------------------------------------------------------------
  
  # Update Indented Qty in Bin
  def update_bin(self, is_submit, is_stopped):
    for d in getlist(self.doclist, 'indent_details'):
      # Step 1:=> Check if is_stock_item == 'Yes'
      if cstr(sql("select is_stock_item from `tabItem` where name = '%s'" % cstr(d.item_code))[0][0]) == 'Yes':
        if not d.warehouse:
          msgprint('Please Enter Warehouse for Item %s as it is stock item.' % cstr(d.item_code))
          raise Exception
        # Step 2:=> Set Qty 
        qty =flt(d.qty)
        if is_stopped:
          qty = (d.qty > d.ordered_qty) and flt(flt(d.qty) - flt(d.ordered_qty)) or 0 
        # Step 3 :=> Update Bin's Indent Qty by +- qty 
        get_obj('Warehouse', d.warehouse).update_bin(0, 0, 0, (is_submit and 1 or -1) * flt(qty), 0, d.item_code, self.doc.transaction_date)    
    
  # On Submit      
  #---------------------------------------------------------------------------
  def on_submit(self):
    # Step 1:=> Set Status
    set(self.doc,'status','Submitted')

    # Step 2:=> Update Bin
    self.update_bin(is_submit = 1, is_stopped = 0)

    # make feed
    obj = get_obj('Feed Control','Feed Control')
    obj.make_feed('submitted', self.doc.doctype, self.doc.name)
  
  def check_modified_date(self):
    mod_db = sql("select modified from `tabIndent` where name = '%s'" % self.doc.name)
    date_diff = sql("select TIMEDIFF('%s', '%s')" % ( mod_db[0][0],cstr(self.doc.modified)))
    
    if date_diff and date_diff[0][0]:
      msgprint(cstr(self.doc.doctype) +" => "+ cstr(self.doc.name) +" has been modified. Please Refresh. ")
      raise Exception
  
  # On Stop / unstop
  #------------------------------------------------------------------------------
  def update_status(self, status):
    self.check_modified_date()
    # Step 1:=> Update Bin
    self.update_bin(is_submit = (status == 'Submitted') and 1 or 0, is_stopped = 1)

    # Step 2:=> Set status 
    set(self.doc,'status',cstr(status))
    
    # Step 3:=> Acknowledge User
    msgprint(self.doc.doctype + ": " + self.doc.name + " has been %s." % ((status == 'Submitted') and 'Unstopped' or cstr(status)) )
 
  # On Cancel
  #-----------------------------------------------------------------------------
  def on_cancel(self):
    # Step 1:=> Get Purchase Common Obj
    pc_obj = get_obj(dt='Purchase Common')
    
    # Step 2:=> Check for stopped status
    pc_obj.check_for_stopped_status( self.doc.doctype, self.doc.name)
    
    # Step 3:=> Check if Purchase Order has been submitted against current Indent
    pc_obj.check_docstatus(check = 'Next', doctype = 'Purchase Order', docname = self.doc.name, detail_doctype = 'PO Detail')

    # Step 4:=> Check if RFQ has been submitted against current Indent
    #pc_obj.check_docstatus(check = 'Next', doctype = 'RFQ', docname = self.doc.name, detail_doctype = 'RFQ Detail')
    
    # Step 5:=> Update Bin
    self.update_bin(is_submit = 0, is_stopped = (cstr(self.doc.status) == 'Stopped') and 1 or 0)
    
    # Step 6:=> Set Status
    set(self.doc,'status','Cancelled')

    # make feed
    obj = get_obj('Feed Control', 'Feed Control')
    obj.make_feed('cancelled', self.doc.doctype, self.doc.name)

  # on update
  def on_update(self):
    obj = get_obj('Feed Control','Feed Control')
    if not self.doc.creation:
      obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      obj.make_feed('modified', self.doc.doctype, self.doc.name)

  # Repair Indent
  # ===========================================
  def repair_indent(self):
    get_obj('Purchase Common', 'Purchase Common').repair_curr_doctype_details(self)