class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    
  def get_bin(self, item_code):
    bin = sql("select name from tabBin where item_code = '%s' and warehouse = '%s'" % (item_code, self.doc.name))
    bin = bin and bin[0][0] or ''
    if not bin:
      if not self.doc.warehouse_type :
        msgprint("[Warehouse Type is Mandatory] Please Enter warehouse type in Warehouse " + self.doc.name)
        raise Exception
      item = sql("select * from `tabItem` where name = %s", (item_code), as_dict = 1)
      bin = Document('Bin')
      bin.item_code = item_code
      bin.stock_uom = item and item[0]['stock_uom'] or ''
      bin.warehouse = self.doc.name
      bin.warehouse_type = self.doc.warehouse_type
      bin_obj = get_obj(doc=bin)
      bin_obj.validate()
      bin.save(1)
      bin = bin.name
    else:
      bin_obj = get_obj('Bin',bin)

    return bin_obj
  
  '''def auto_indent_mail(self,item, it_det):
    msgprint(it_det[0][0])
    msgprint("will send mail soon...")'''
  

  def validate_asset(self, item_code):
    if sql("select is_asset_item from tabItem where name=%s", item_code)[0][0] == 'Yes' and self.doc.warehouse_type != 'Fixed Asset':
      msgprint("Fixed Asset Item %s can only be transacted in a Fixed Asset type Warehouse" % item_code)
      raise Exception

  # update bin
  # ----------
  def update_bin(self, actual_qty, reserved_qty, ordered_qty, indented_qty, planned_qty, item_code, dt,sle_id = '',posting_time = ''):
    self.validate_asset(item_code)
    it_det = sql("select is_stock_item, re_order_level, item_name, description from tabItem where name=%s", item_code)
    if it_det[0][0]=='Yes':
      bin = self.get_bin(item_code)
      bin.update_stock(actual_qty, reserved_qty, ordered_qty, indented_qty, planned_qty, dt, sle_id, posting_time)
  
      #if it_det[0][1]:
      #msgprint(bin.doc.fields['actual_qty'])
      #msgprint(it_det[0][1])
      #if bin.doc.fields['actual_qty'] < flt(it_det[0][1]):
      #self.auto_indent_mail(item_code,it_det)
      return bin
    else:
      msgprint("[Stock Update] Ignored %s since it is not a stock item" % item_code)

  # repost stock
  # ------------
  def repost_stock(self):
    bl = sql("select name from tabBin where warehouse=%s", self.doc.name)
    for b in bl:
      bobj = get_obj('Bin',b[0])
      bobj.update_item_valuation()

      sql("COMMIT")
      sql("START TRANSACTION")

  def check_state(self):
    return NEWLINE + NEWLINE.join([i[0] for i in sql("select state_name from `tabState` where `tabState`.country='%s' " % self.doc.country)])

  def validate(self):
    if self.doc.email_id:
      if not validate_email_add(self.doc.email_id):
        msgprint("Please enter valid Email Id.")
        raise Exception
    if not self.doc.warehouse_type:
      msgprint("[Warehouse Type is Mandatory] Please Enter  Please Entry warehouse type in Warehouse " + self.doc.name)
      raise Exception
    wt = sql("select warehouse_type from `tabWarehouse` where name ='%s'" % self.doc.name)
    if cstr(self.doc.warehouse_type) != cstr(wt and wt[0][0] or ''):
      sql("update `tabStock Ledger Entry` set warehouse_type = '%s' where warehouse = '%s'" % (self.doc.warehouse_type, self.doc.name))
      msgprint("All Stock Ledger Entries Updated.")