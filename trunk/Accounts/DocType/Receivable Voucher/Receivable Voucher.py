class DocType:
  def __init__(self,d,dl):
    self.doc, self.doclist = d, dl
    self.log = []
    self.tname = 'RV Detail'
    self.fname = 'entries'


  # Autoname
  # ---------
  def autoname(self):
    self.doc.name = make_autoname(self.doc.naming_series+ '.#####')



# ********************************* Trigger Functions ******************************

  #Set retail related fields from pos settings
  #-------------------------------------------------------------------------
  def set_pos_fields(self):
    pos = sql("select * from `tabPOS Setting` where user = '%s'"%session['user'], as_dict=1)
    if not pos:
      pos = sql("select * from `tabPOS Setting` where user = ''", as_dict=1)
    if pos:  
      val=pos and pos[0]['customer_account'] or ''
      if not self.doc.debit_to:
        set(self.doc,'debit_to',val)
      
      lst = ['territory','naming_series','currency','charge','letter_head','tc_name','price_list_name','company','select_print_heading','cash_bank_account']
        
      for i in lst:
        val = pos and pos[0][i] or ''
        set(self.doc,i,val)
        
      val = pos and flt(pos[0]['conversion_rate']) or 0  
      set(self.doc,'conversion_rate',val)

      #fetch terms  
      if self.doc.tc_name:   self.get_tc_details()
      
      #fetch charges
      if self.doc.charge:    self.get_other_charges()

      
  # Get Account Head to which amount needs to be Debited based on Customer
  # ----------------------------------------------------------------------
  def get_debit_to(self):
    acc_head = sql("select name from `tabAccount` where name = %s and docstatus != 2", (cstr(self.doc.customer) + " - " + self.get_company_abbr()))
    if acc_head and acc_head[0][0]:
      ret = { 'debit_to' : acc_head[0][0] }
      return cstr(ret)
    else:
      msgprint("%s does not have an Account Head in %s. You must first create it from the Customer Master" % (self.doc.customer, self.doc.company))


  # Set Due Date = Posting Date + Credit Days
  # -----------------------------------------
  def get_cust_and_due_date(self):

    if self.doc.debit_to:

      credit_days_cust=sql("select t1.credit_days, t1.master_name, t2.customer_name,t2.address, t2.territory, t2.default_sales_partner, t2.default_commission_rate from `tabAccount` t1, `tabCustomer` t2 where t1.name='%s' and t1.master_name = t2.name and t1.docstatus != 2" %self.doc.debit_to)

    if self.doc.company:
      credit_days_comp=sql("select credit_days from `tabCompany` where name='%s'" %self.doc.company)

    ret = {}
    # Customer has higher priority than company
    # i.e.if not entered in customer will take credit days from company
    
    if credit_days_cust and cint(credit_days_cust[0][0])>0:
      ret = { 'due_date' : add_days(self.doc.posting_date,cint(credit_days_cust[0][0])) }
      
    elif credit_days_comp and cint(credit_days_comp[0][0])>0:
      ret = { 'due_date' : add_days(self.doc.posting_date,cint(credit_days_comp[0][0])) }
      
    ret['customer'] = credit_days_cust and credit_days_cust[0][1] or ''
    ret['customer_name'] = credit_days_cust and credit_days_cust[0][2] or ''   
    ret['customer_address'] = credit_days_cust and credit_days_cust[0][3] or ''
    ret['territory'] = credit_days_cust and credit_days_cust[0][4] or ''
    ret['sales_partner'] = credit_days_cust and credit_days_cust[0][5] or ''
    ret['commission_rate'] = credit_days_cust and flt(credit_days_cust[0][6]) or 0
    self.doc.clear_table(self.doclist,'sales_team')
    get_obj('Sales Common').get_sales_person_details(self)

    return cstr(ret)


  # Get Customer Address & territory
  # ---------------------
  def pull_cust_details(self):
    e = sql("select customer_name, address,territory, default_sales_partner, default_commission_rate from `tabCustomer` where name = '%s'" % self.doc.customer)

    ret = {
      'customer_name': e and e[0][0] or '',
      'customer_address': e and e[0][1] or '',
      'territory': e and e[0][2] or '',
      'sales_partner' : e and e[0][3] or '',
      'commission_rate' : e and flt(e[0][4]) or 0
    }
    self.doc.clear_table(self.doclist,'sales_team')
    get_obj('Sales Common').get_sales_person_details(self)
    acc_head = sql("select name from `tabAccount` where name = %s and docstatus != 2", (cstr(self.doc.customer) + " - " + self.get_company_abbr()))
    ret['debit_to']=acc_head and acc_head[0][0] or ''
    return str(ret)


  # Pull Details of Delivery Note or Sales Order Selected
  # ------------------------------------------------------
  def pull_details(self):
    # Delivery Note
    if self.doc.delivery_note_main:
      self.validate_prev_docname('delivery note')
      self.doc.clear_table(self.doclist,'other_charges')
      self.doclist = get_obj('DocType Mapper', 'Delivery Note-Receivable Voucher').dt_map('Delivery Note', 'Receivable Voucher', self.doc.delivery_note_main, self.doc, self.doclist, "[['Delivery Note', 'Receivable Voucher'],['Delivery Note Detail', 'RV Detail'],['RV Tax Detail','RV Tax Detail'],['Sales Team','Sales Team']]")
    # Sales Order
    elif self.doc.sales_order_main:
      self.validate_prev_docname('sales order')
      self.doc.clear_table(self.doclist,'other_charges')
      get_obj('DocType Mapper', 'Sales Order-Receivable Voucher').dt_map('Sales Order', 'Receivable Voucher', self.doc.sales_order_main, self.doc, self.doclist, "[['Sales Order', 'Receivable Voucher'],['Sales Order Detail', 'RV Detail'],['RV Tax Detail','RV Tax Detail']]")


  # Item Details
  # -------------
  def get_item_details(self, item_code):
    return get_obj('Sales Common').get_item_details(item_code, self)
 
 
  # Get tax rate if account type is tax
  # ------------------------------------
  def get_rate(self,arg):
    get_obj('Sales Common').get_rate(arg)
    
    
  # Get Commission rate of Sales Partner
  # -------------------------------------
  def get_comm_rate(self, sales_partner):
    return get_obj('Sales Common').get_comm_rate(sales_partner, self)  
  
 
  # GET TERMS & CONDITIONS
  # -------------------------------------
  def get_tc_details(self):
    return get_obj('Sales Common').get_tc_details(self)

  # Get Other Charges Details
  # --------------------------
  def get_other_charges(self):
    return get_obj('Sales Common').get_other_charges(self)
    

  # Get Advances
  # -------------
  def get_advances(self):
    get_obj('GL Control').get_advances(self, self.doc.debit_to, 'Advance Adjustment Detail', 'advance_adjustment_details', 'credit')

  #pull project customer
  #-------------------------
  def pull_project_customer(self):
    res = sql("select customer from `tabProject` where name = '%s'"%self.doc.project_name)
    if res:
      get_obj('DocType Mapper', 'Project-Receivable Voucher').dt_map('Project', 'Receivable Voucher', self.doc.project_name, self.doc, self.doclist, "[['Project', 'Receivable Voucher']]")

# ********************************** Server Utility Functions ******************************
  
  # Get Company Abbr.
  # ------------------
  def get_company_abbr(self):
    return sql("select abbr from tabCompany where name=%s", self.doc.company)[0][0]
    
  
  # Check whether sales order / delivery note items already pulled
  #----------------------------------------------------------------
  def validate_prev_docname(self,doctype):
    for d in getlist(self.doclist, 'entries'): 
      if doctype == 'delivery note' and self.doc.delivery_note_main == d.delivery_note:
        msgprint(cstr(self.doc.delivery_note_main) + " delivery note details have already been pulled.")
        raise Exception , "Validation Error. Delivery note details have already been pulled."
      elif doctype == 'sales order' and self.doc.sales_order_main == d.sales_order and not d.delivery_note:
        msgprint(cstr(self.doc.sales_order_main) + " sales order details have already been pulled.")
        raise Exception , "Validation Error. Sales order details have already been pulled."


  #-----------------------------------------------------------------
  # ADVANCE ALLOCATION
  #-----------------------------------------------------------------
  def update_against_document_in_jv(self,against_document_no, against_document_doctype):
    get_obj('GL Control').update_against_document_in_jv( self, 'advance_adjustment_details', against_document_no, against_document_doctype, self.doc.debit_to, 'credit', self.doc.doctype)
  


# ************************************* VALIDATE **********************************************
  # Get Customer Name and address based on Debit To Account selected
  # This case arises in case of direct RV where user doesn't enter customer name.
  # Hence it should be fetched from Account Head.
  # -----------------------------------------------------------------------------
  def get_customer_details(self):
    e = sql("select t1.master_name , t1.address, t2.customer_name, t2.default_sales_partner, t2.default_commission_rate from `tabAccount` t1, `tabCustomer` t2 where t1.name = '%s' and t1.master_name = t2.name" % self.doc.debit_to)

    self.doc.customer = e and e[0][0] or ''
    self.doc.customer_address = e and e[0][1] or ''
    self.doc.customer_name = e and e[0][2] or ''
    self.doc.sales_partner = e and e[0][3] or ''
    self.doc.commission_rate = e and flt(e[0][4]) or 0
    self.doc.clear_table(self.doclist,'sales_team')
    get_obj('Sales Common').get_sales_person_details(self)



  # Validate Customer Name with SO or DN if items are fetched from SO or DN
  # ------------------------------------------------------------------------
  def validate_customer(self):
    for d in getlist(self.doclist,'entries'):
      customer = ''
      if d.sales_order:
        customer = sql("select customer from `tabSales Order` where name = '%s'" % d.sales_order)[0][0]
        doctype = 'sales order'
        doctype_no = cstr(d.sales_order)
      if d.delivery_note:
        customer = sql("select customer from `tabDelivery Note` where name = '%s'" % d.delivery_note)[0][0]
        doctype = 'delivery note'
        doctype_no = cstr(d.delivery_note)
      if customer and not cstr(self.doc.customer) == cstr(customer):
        msgprint("Customer %s do not match with customer  of %s %s." %(self.doc.customer,doctype,doctype_no))
        raise Exception , " Validation Error "
    

  # Validates Debit To Account and Customer Matches
  # ------------------------------------------------
  def validate_debit_to_acc(self):
    if self.doc.customer and not self.doc.is_pos:
      acc_head = sql("select name from `tabAccount` where name = %s and docstatus != 2", (cstr(self.doc.customer) + " - " + self.get_company_abbr()))
      if acc_head and acc_head[0][0]:
        if not cstr(acc_head[0][0]) == cstr(self.doc.debit_to):
          msgprint("Debit To %s do not match with Customer %s for Company %s i.e. %s" %(self.doc.debit_to,self.doc.customer,self.doc.company,cstr(acc_head[0][0])))
          raise Exception, "Validation Error "
      if not acc_head:
         msgprint("%s does not have an Account Head in %s. You must first create it from the Customer Master" % (self.doc.customer, self.doc.company))
         raise Exception, "Validation Error "


  # Validate Debit To Account
  # 1. Account Exists
  # 2. Is a Debit Account
  # 3. Is a PL Account
  # ---------------------------
  def validate_debit_acc(self):
    acc = sql("select debit_or_credit, is_pl_account from tabAccount where name = '%s' and docstatus != 2" % self.doc.debit_to)
    if not acc:
      msgprint("Account: "+ self.doc.debit_to + "does not exist")
      raise Exception
    elif acc[0][0] and acc[0][0] != 'Debit':
      msgprint("Account: "+ self.doc.debit_to + "is not a debit account")
      raise Exception
    elif acc[0][1] and acc[0][1] != 'No':
      msgprint("Account: "+ self.doc.debit_to + "is a pl account")
      raise Exception


  # Validate Fixed Asset Account and whether Income Account Entered Exists
  # -----------------------------------------------------------------------
  def validate_fixed_asset_account(self):
    for d in getlist(self.doclist,'entries'):
      item = sql("select name,is_asset_item,is_sales_item from `tabItem` where name = '%s' and (ifnull(end_of_life,'')='' or end_of_life = '0000-00-00' or end_of_life >  now())"% d.item_code)
      acc =  sql("select account_type from `tabAccount` where name = '%s' and docstatus != 2" % d.income_account)
      if not acc:
        msgprint("Account: "+d.income_account+" does not exist in the system")
        raise Exception
      elif item and item[0][1] == 'Yes' and not acc[0][0] == 'Fixed Asset Account':
        msgprint("Please select income head with account type 'Fixed Asset Account' as Item %s is an asset item" % d.item_code)
        raise Exception



  # Set totals in words
  #--------------------
  def set_in_words(self):
    self.doc.in_words = get_obj('Sales Common').get_total_in_words(get_defaults()['currency'], self.doc.rounded_total)
    self.doc.in_words_export = get_obj('Sales Common').get_total_in_words(self.doc.currency, self.doc.rounded_total_export)

  # Clear Advances
  # --------------
  def clear_advances(self):
    get_obj('GL Control').clear_advances(self, 'Advance Adjustment Detail','advance_adjustment_details')


  # set aging date
  #-------------------
  def set_aging_date(self):
    if self.doc.is_opening != 'Yes':
      self.doc.aging_date = self.doc.posting_date
    elif not self.doc.aging_date:
      msgprint("Aging Date is mandatory for opening entry")
      raise Exception
      

  # Set against account for debit to account
  #------------------------------------------
  def set_against_income_account(self):
    against_acc = []
    for d in getlist(self.doclist, 'entries'):
      if d.income_account not in against_acc:
        against_acc.append(d.income_account)
    self.doc.against_income_account = ','.join(against_acc)

  def add_remarks(self):
    if not self.doc.remarks: self.doc.remarks = 'No Remarks'

  #check in manage account if sales order / delivery note required or not.
  def so_dn_required(self):
    dict = {'Sales Order':'so_required','Delivery Note':'dn_required'}
    for i in dict:  
      res = sql("select value from `tabSingles` where doctype = 'Manage Account' and field = '%s'"%dict[i])
      if res and res[0][0] == 'Yes':
        for d in getlist(self.doclist,'entries'):
          if not d.fields[i.lower().replace(' ','_')]:
            msgprint("%s No. required against item %s"%(i,d.item_code))
            raise Exception

  #check for does customer belong to same project as entered..
  #-------------------------------------------------------------------------------------------------
  def validate_proj_cust(self):
    if self.doc.project_name and self.doc.customer:
      res = sql("select name from `tabProject` where name = '%s' and (customer = '%s' or ifnull(customer,'')='')"%(self.doc.project_name, self.doc.customer))
      if not res:
        msgprint("Customer - %s does not belong to project - %s. \n\nIf you want to use project for multiple customers then please make customer details blank in that project."%(self.doc.customer,self.doc.project_name))
        raise Exception       

  def validate_pos(self):
    if not self.doc.cash_bank_account:
      msgprint("Cash/Bank Account is mandatory for POS entry")
      raise Exception
    if flt(self.doc.paid_amount) > flt(self.doc.grand_total):
      msgprint("Paid amount can not be greater than grand total")
      raise Exception

  
  # ******* CHECKS WHETHER SERIAL NO IS REQUIRED IS NOT ********
  def validate_serial_no(self):
    for d in getlist(self.doclist, 'entries'):
      ar_required = sql("select has_serial_no from tabItem where name = '%s'" % d.item_code)
      ar_required = ar_required and ar_required[0][0] or ''
      if ar_required == 'Yes' and not d.serial_no:
        msgprint("Serial No is mandatory for item: "+ d.item_code)
        raise Exception
      elif ar_required != 'Yes' and cstr(d.serial_no).strip():
        msgprint("If serial no required, please select 'Yes' in 'Has Serial No' in Item :"+d.item_code)
        raise Exception


    
  # VALIDATE
  # ====================================================================================
  def validate(self):
    self.so_dn_required()
    #self.dn_required()
    self.validate_proj_cust()
    sales_com_obj = get_obj(dt = 'Sales Common')
    sales_com_obj.check_stop_sales_order(self)
    sales_com_obj.check_active_sales_items(self)
    sales_com_obj.check_conversion_rate(self)
    sales_com_obj.validate_max_discount(self, 'entries')   #verify whether rate is not greater than tolerance
    sales_com_obj.get_allocated_sum(self)  # this is to verify that the allocated % of sales persons is 100%
    if not self.doc.customer:
      self.get_customer_details()
    self.validate_customer()
    self.validate_debit_to_acc()
    self.validate_debit_acc()
    self.validate_fixed_asset_account()
    self.add_remarks()
    if self.doc.is_pos:
      self.validate_pos()
      self.validate_serial_no()
    self.set_in_words()
    if not self.doc.is_opening:
      self.doc.is_opening = 'No'
    self.set_aging_date()
    self.clear_advances()
    #get_obj('Workflow Engine','RV Test').apply_rule(self)
    # Set against account
    self.set_against_income_account()
    
  

# *************************************************** ON SUBMIT **********************************************
  # Check Ref Document's docstatus
  # -------------------------------
  def check_prev_docstatus(self):
    for d in getlist(self.doclist,'entries'):
      if d.sales_order:
        submitted = sql("select name from `tabSales Order` where docstatus = 1 and name = '%s'" % d.sales_order)
        if not submitted:
          msgprint("Sales Order : "+ cstr(d.sales_order) +" is not submitted")
          raise Exception , "Validation Error."

      if d.delivery_note:
        submitted = sql("select name from `tabDelivery Note` where docstatus = 1 and name = '%s'" % d.delivery_note)
        if not submitted:
          msgprint("Delivery Note : "+ cstr(d.delivery_note) +" is not submitted")
          raise Exception , "Validation Error."

  # Check qty in stock depends on item code and warehouse
  #-------------------------------------------------------
  def check_qty_in_stock(self):
    for d in getlist(self.doclist, 'entries'):
      is_stock_item = sql("select is_stock_item from `tabItem` where name = '%s'" % d.item_code)[0][0]
      actual_qty = 0
      if d.item_code and d.warehouse:
        actual_qty = sql("select actual_qty from `tabBin` where item_code = '%s' and warehouse = '%s'" % (d.item_code, d.warehouse))
        actual_qty = actual_qty and flt(actual_qty[0][0]) or 0

      if is_stock_item == 'Yes' and flt(d.qty) > flt(actual_qty):
        msgprint("For Item: " + cstr(d.item_code) + " at Warehouse: " + cstr(d.warehouse) + " Quantity: " + cstr(d.qty) +" is not Available. (Must be less than or equal to " + cstr(actual_qty) + " )")
        raise Exception, "Validation Error"

  

  # ********** Update Serial No. Details *************
  def check_serial_no(self):

    import datetime
    for d in getlist(self.doclist, 'entries'):
      if d.serial_no:
        s_no = d.serial_no.strip()
        serial_nos = cstr(s_no).split(',')
        if not flt(len(serial_nos)) == flt(d.qty):
          msgprint("Please enter serial nos for all "+ cstr(d.qty) + " quantity of item "+cstr(d.item_code))
          raise Exception
        for a in serial_nos:
          if a:

            chk = sql("select customer, delivery_note_no, delivery_date from `tabSerial No` where name = %s and item_code = %s and status = 'In Store'", (a.strip(), d.item_code), as_dict=1)
            if not chk:
              msgprint("Serial No: "+ a +" of Item "+ d.item_code + " does not exists in the system")
              raise Exception
            elif chk[0]['customer'] or chk[0]['delivery_note_no'] or chk[0]['delivery_date']:
              msgprint("Serial No: "+ a +" of Item "+ d.item_code + " is already delivered to customer")
              raise Exception
            else:
              wp = sql("select warranty_period from `tabSerial No` where name = %s", a)
              warranty_p = wp and wp[0][0] or 0
              
              if warranty_p:
                warranty_exp_date = add_days(self.doc.posting_date,warranty_p)
              else:
                warranty_exp_date = ''
              self.update_serial_record(a,self.doc.posting_date,self.doc.name,'Delivered',warranty_exp_date)

  # UPDATE SERIAL RECORD
  # ------------------------------------------------------------------------
  def update_serial_record(self,serial_no,date,name,status,warranty_exp):
    sql("update `tabSerial No` set delivery_date = %s, delivery_note_no = %s, status = %s, modified = %s, modified_by = %s, customer = %s, customer_name = %s, customer_address = %s,territory = %s,warranty_expiry_date=%s where name = %s",(date,name,status,self.doc.modified,self.doc.modified_by,self.doc.customer,self.doc.customer_name,self.doc.customer_address,self.doc.territory,warranty_exp,serial_no))


  # ********************** Make Stock Entry ************************************
  def make_sl_entry(self, d, wh, qty, in_value, update_stock):
    st_uom = sql("select stock_uom from `tabItem` where name = '%s'"%d.item_code)
    self.values.append({
      'item_code'           : d.item_code,
      'warehouse'           : wh,
      'transaction_date'    : self.doc.voucher_date,
      'posting_date'        : self.doc.posting_date,
      'posting_time'        : self.doc.posting_time,
      'voucher_type'        : 'Receivable Voucher',
      'voucher_no'          : cstr(self.doc.name),
      'voucher_detail_no'   : cstr(d.name), 
      'actual_qty'          : qty, 
      'stock_uom'           : st_uom and st_uom[0][0] or '',
      'incoming_rate'       : in_value,
      'company'             : self.doc.company,
      'fiscal_year'         : self.doc.fiscal_year,
      'is_cancelled'        : (update_stock==1) and 'No' or 'Yes',
      'batch_no'            : ''      
    })    
      

  # UPDATE STOCK LEDGER
  # ---------------------------------------------------------------------------
  def update_stock_ledger(self, update_stock, clear = 0):
    
    self.values = []
    for d in getlist(self.doclist, 'entries'):
      stock_item = sql("SELECT is_stock_item, is_sample_item FROM tabItem where name = '%s'"%(d.item_code), as_dict = 1) # stock ledger will be updated only if it is a stock item
      if stock_item[0]['is_stock_item'] == "Yes":
          
        # Reduce actual qty from warehouse
        self.make_sl_entry( d, d.warehouse, - flt(d.qty) , 0, update_stock)

    get_obj('Stock Ledger', 'Stock Ledger').update_stock(self.values)

  #------------ check credit limit of items in DN Detail which are not fetched from sales order----------
  def credit_limit(self):
    amount, total = 0, 0
    for d in getlist(self.doclist, 'entries'):
      amount += d.amount
    if amount != 0:
      total = (amount/self.doc.net_total)*self.doc.grand_total
      get_obj('Sales Common').check_credit(self, total)

  #-------------------POS Stock Updatation Part----------------------------------------------
  def pos_update_stock(self): 
    self.check_qty_in_stock()  
    self.check_serial_no()
    self.update_stock_ledger(update_stock = 1)
    self.credit_limit()


  # On Submit
  # ---------
  def on_submit(self):
    if self.doc.is_pos == 1:
      if self.doc.update_stock == 1:
        self.pos_update_stock()

    else:
      self.check_prev_docstatus()
      get_obj("Sales Common").update_prevdoc_detail(1,self)

      # Check for Approving Authority
      get_obj('Authorization Control').validate_approving_authority(self.doc.doctype, self.doc.company, self.doc.grand_total, self)

    # this sequence because outstanding may get -ve
    get_obj(dt='GL Control').make_gl_entries(self.doc, self.doclist,use_mapper = self.doc.is_pos and 'POS' or '')
    
    if not self.doc.is_pos == 1:
      self.update_against_document_in_jv(self.doc.name, self.doc.doctype)   

   
    
    # on submit notification
    get_obj('Notification Control').notify_contact('Sales Invoice', self.doc.doctype,self.doc.name, self.doc.email_id, self.doc.contact_person)

    # make feed
    get_obj('Feed Control').make_feed('submitted', self.doc.doctype, self.doc.name)

      
# *************************************************** ON CANCEL **********************************************
  # Check Next Document's docstatus
  # --------------------------------
  def check_next_docstatus(self):
    submit_jv = sql("select t1.name from `tabJournal Voucher` t1,`tabJournal Voucher Detail` t2 where t1.name = t2.parent and t2.against_invoice = '%s' and t1.docstatus = 1" % (self.doc.name))
    if submit_jv:
      msgprint("Journal Voucher : " + cstr(submit_jv[0][0]) + " has been created against " + cstr(self.doc.doctype) + ". So " + cstr(self.doc.doctype) + " cannot be Cancelled.")
      raise Exception, "Validation Error."

  # ******************** Check Serial No ******************************
  def back_update_serial_no(self):
    import datetime
    for d in getlist(self.doclist, 'entries'):
      if d.serial_no:
        serial_nos = cstr(d.serial_no).split(',')
        for a in serial_nos:
          self.update_serial_record(a,'','','In Store','')

  # On Cancel
  # ----------
  def on_cancel(self):
    if self.doc.is_pos == 1:
      self.back_update_serial_no()
      if self.doc.update_stock == 1:
        self.update_stock_ledger(update_stock = -1)
    else:
      sales_com_obj = get_obj(dt = 'Sales Common')
      sales_com_obj.check_stop_sales_order(self)
      self.check_next_docstatus()
      sales_com_obj.update_prevdoc_detail(0,self)
    
    get_obj(dt='GL Control').make_gl_entries(self.doc, self.doclist, cancel=1, use_mapper=self.doc.is_pos and 'POS' or '')

    # make feed
    obj = get_obj('Feed Control', 'Feed Control')
    obj.make_feed('cancelled', self.doc.doctype, self.doc.name)

  # Get Warehouse
  def get_warehouse(self):
    w = sql("select warehouse from `tabPOS Setting` where user = '%s'"%session['user'])
    if not w:
      ps = sql("select name, warehouse from `tabPOS Setting` where user = ''")
      if not ps:
        msgprint("To make POS entry, please create POS Setting from Setup --> Accounts --> POS Setting and refresh the system.")
        raise Exception
      elif not ps[0][1]:
        msgprint("Please enter warehouse in POS Setting")
      else: w = ps[0][1]
    return w

  # on update
  def on_update(self):
    # Set default warehouse from pos setting
    #---------------------------------------------
    if self.doc.is_pos == 1:
      w = self.get_warehouse()
      if w:
        for d in getlist(self.doclist, 'entries'):
          if not d.warehouse:
            d.warehouse = w and w[0][0] or ''

      if flt(self.doc.paid_amount) == 0: 
        set(self.doc,'paid_amount',flt(doc.grand_total))
    else:
      set(self.doc,'paid_amount',0)

    set(self.doc,'outstanding_amount',flt(doc.grand_total) - flt(self.doc.total_advance) - flt(self.doc.paid_amount))
      
             
    #--------------------------------------------   
    obj = get_obj('Feed Control','Feed Control')
    
    if not self.doc.creation:
      obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      obj.make_feed('modified', self.doc.doctype, self.doc.name)

########################################################################
# Repair Outstanding
#######################################################################
  def repair_rv_outstanding(self):
    get_obj(dt = 'GL Control').repair_voucher_outstanding(self)
