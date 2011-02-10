class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
  
  #check for item quantity available in stock
  def actual_amt_check(self):
    if self.doc.batch_no:
      ret_sum = sql("select sum(actual_qty) from `tabStock Ledger Entry` where warehouse = '%s' and item_code = '%s' and batch_no = '%s'"%(self.doc.warehouse,self.doc.item_code,self.doc.batch_no))
      ret_sum = ret_sum and flt(ret_sum[0][0]) or 0
  
      if (ret_sum + self.doc.actual_qty) < 0:
        msgprint("For item: '%s', Warehouse: '%s', Actual Quantity: '%s', Required Quantity: '%s'. Available Stock is less for this item."%(self.doc.item_code,self.doc.warehouse,cstr(ret_sum) or 0,self.doc.actual_qty))
        raise Exception
       

  # mandatory
  # ---------
  
  def validate_mandatory(self):
    
    mandatory = ['item_code','warehouse','transaction_date','posting_date','voucher_type','voucher_no','actual_qty','company','fiscal_year']
    for k in mandatory:
      if self.doc.fields.get(k)==None:
        msgprint("Stock Ledger Entry: %s is mandatory" % k)
        raise Exception
      elif k == 'item_code':
        if not sql("select name from tabItem where name = '%s'" % self.doc.fields.get(k)):
          msgprint("Item Code: %s does not exist in the system. Please check." % self.doc.fields.get(k))
          raise Exception
        check = sql("Select name from `tabItem` where has_batch_no = 'Yes' and name = '%s'"%self.doc.fields.get(k))
        check = check and check[0][0] or []
        if check :
          if not self.doc.batch_no:
            msgprint("Please enter batch number")
            raise Exception
          else:
            ret_batch = sql("select name from `tabBatch` where item='%s' and name ='%s' and docstatus != 2"%(self.doc.item_code,self.doc.batch_no))
            if not ret_batch:
              msgprint("Please select proper batch no. Item '%s' is not in Batch '%s'" %(self.doc.item_code,self.doc.batch_no))
              raise Exception
      elif k == 'warehouse':

        if not sql("select name from tabWarehouse where name = '%s'" % self.doc.fields.get(k)):
          msgprint("Warehouse: %s does not exist in the system. Please check." % self.doc.fields.get(k))
          raise Exception

        
  def validate(self):

    self.validate_mandatory()
    self.actual_amt_check()