class DocType :
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
      
  def validate(self):
    if not self.doc.return_type:
      msgprint("Please Enter Return Type")
      raise Exception
      
  def get_rate(self, det):
    ret = []
    for d in det:
      d = list(d)
      # check item is equal to parent item 
      if cstr(d[1]) == cstr(d[4]):
        d[5] = flt(sql("select basic_rate from `tabDelivery Note Detail` where name = '%s'" % d[5])[0][0])
      ret.append(d)
    return ret
        
  def pull_details(self):
    flg, ret_type  = 0, self.doc.return_type
    if ret_type == 'Sales Return' and self.doc.delivery_note_no:
      det = sql("select name, item_code, description, qty, uom, parent_item, parent_detail_docname from `tabDelivery Note Packing Detail` where parent = '%s' and docstatus = 1"%(self.doc.delivery_note_no))
      cust_supp = sql("select company from `tabDelivery Note` where name = '%s'"%(self.doc.delivery_note_no))
      det = self.get_rate(det)
      flg = 1
    if ret_type == 'Purchase Return' and self.doc.purchase_receipt_no:
      det = sql("select name, item_code, description, received_qty, uom from `tabPurchase Receipt Detail` where parent = '%s' and docstatus = 1"%(self.doc.purchase_receipt_no))
      cust_supp = sql("select company from `tabPurchase Receipt` where name = '%s'"%(self.doc.purchase_receipt_no))
      flg = 1
    if ret_type == 'Sales Return' and flg == 0:
      msgprint("Please Enter Delivery Note No")    
      raise Exception
    if ret_type == 'Purchase Return' and flg == 0:
      msgprint("Please Enter Purchase Receipt No")
      raise Exception
      
    if flg == 1:
      self.add_details(det)
      ret = []
      ret.append(cust_supp[0][0])
      self.doc.save()
      return ret

    
    
  def add_details(self, det):
    r = []
    ret = 0
    self.doc.clear_table(self.doclist, 'return_details', 1)
    for i in det:
      ret_child = addchild(self.doc, 'return_details', 'Return Detail', 1, self.doclist)
      
      ret_child.detail_name = i and i[0] or ''
      ret_child.item_code = i and i[1] or ''
      ret_child.description = i and i[2] or ''
      ret_child.qty = i and flt(i[3]) or 0
      ret_child.uom = i and i[4] or ''
      ret_child.rate = (len(i) > 5) and i[5] or 0
      ret_child.save()

    self.doc.save()
    
  def get_voucher_det(self):
    fg = 0
    det_list = []
    if self.doc.return_type == 'Sales Return':
      if self.doc.delivery_note_no:
        det = sql("select customer_name, company from `tabDelivery Note` where name = '%s'"%(self.doc.delivery_note_no))
        det_list.append(det[0][1])
        acc_head = sql("select name from `tabAccount` where account_name = '%s'"%(det[0][0]))
        if acc_head:
          det_list.append(acc_head[0][0])
        else:
          msgprint("Account Head of customer "+det[0][0]+" does not exists. Please create account head before making Credit Note")
          raise Exception
        fg = 1
      else:
        msgprint("Please Enter Delivery Note No to make Credit Note")
        raise Exception
    elif self.doc.return_type == 'Purchase Return':
      if self.doc.purchase_receipt_no:
        det = sql("select supplier, company from `tabPurchase Receipt` where name = '%s'"%(self.doc.purchase_receipt_no))
        det_list.append(det[0][1])        
        acc_head = sql("select name from `tabAccount` where account_name = '%s'"%(det[0][0]))
        if acc_head:
          det_list.append(acc_head[0][0])
        else:
          msgprint("Account Head of supplier "+det[0][0]+" does not exists. Please create account head before making Debit Note")
          raise Exception
        fg = 1 
      else:
        msgprint("Please Enter Purchase Receipt No to make debit note")
        raise Exception
    if fg == 1:
      return det_list
      
  def clear_return_table(self):
    self.doc.clear_table(self.doclist, 'return_details', 1)
    self.doc.save()
    return ''