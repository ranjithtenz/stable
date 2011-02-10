class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    self.item_dict = {}

  # Autoname
  # ---------
  def autoname(self):
    self.doc.name = make_autoname(self.doc.naming_series+'.#####')


  # get item details
  # ----------------
  def get_item_details(self, arg):
    arg, bin, in_rate = eval(arg), None, 0
    item = sql("select stock_uom, description from `tabItem` where name = %s and (ifnull(end_of_life,'')='' or end_of_life ='0000-00-00' or end_of_life >  now())", (arg['item_code']), as_dict = 1)
    if not item:
      msgprint("Item is not active. You can restore it from Trash")
      raise Exception
      
    if arg['warehouse']:
      bin = sql("select actual_qty from `tabBin` where item_code = %s and warehouse = %s", (arg['item_code'], arg['warehouse']), as_dict = 1)
      in_rate = get_obj('Valuation Control').get_incoming_rate(self.doc.posting_date, self.doc.posting_time, arg['item_code'],arg['warehouse'])
    ret = {
      'uom'               : item and item[0]['stock_uom'] or '',
      'stock_uom'         : item and item[0]['stock_uom'] or '',
      'description'       : item and item[0]['description'] or '',
      'actual_qty'        : bin and flt(bin[0]['actual_qty']) or 0, 
      'transfer_qty'      : 0,
      'incoming_rate'     : flt(in_rate),
      'conversion_factor' : 1
    }
    return str(ret)


  # Get UOM Details
  def get_uom_details(self, arg = ''):
    arg, ret = eval(arg), {}
    uom = sql("select conversion_factor from `tabUOM Conversion Detail` where parent = %s and uom = %s", (arg['item_code'],arg['uom']), as_dict = 1)
    if not uom:
      msgprint("There is no Conversion Factor for UOM '%s' in Item '%s'" % (arg['uom'], arg['item_code']))
      ret = {'uom' : ''}
    else:
      ret = {
        'conversion_factor'          : flt(uom[0]['conversion_factor']),
        'transfer_qty'               : flt(arg['qty']) * flt(uom[0]['conversion_factor']),
      }
    return str(ret)

    
  # get rate of FG item 
  #---------------------------
  def get_in_rate(self, pro_obj):
    # calculate_cost for production item
    get_obj('BOM Control').calculate_cost(pro_obj.doc.bom_no)
    # return cost
    return flt(get_obj('Bill Of Materials', pro_obj.doc.bom_no).doc.cost_as_per_mar)

  # get current_stock
  # ----------------
  def get_current_stock(self, pro_obj = ''):
    for d in getlist(self.doclist, 'mtn_details'):
      d.s_warehouse = (self.doc.purpose != 'Production Order') and  self.doc.from_warehouse or cstr(d.s_warehouse)
      d.t_warehouse = (self.doc.purpose != 'Production Order') and  self.doc.to_warehouse or cstr(d.t_warehouse)
      
      if d.s_warehouse:
        bin = sql("select actual_qty from `tabBin` where item_code = %s and warehouse = %s", (d.item_code, d.s_warehouse), as_dict = 1)
        d.actual_qty = bin and flt(bin[0]['actual_qty']) or 0
      else: d.actual_qty = 0
      if d.fg_item:
        d.incoming_rate = pro_obj and self.get_in_rate(pro_obj) or ''
      else:
        if not (self.doc.purpose == 'Material Receipt' and d.incoming_rate):
          d.incoming_rate = flt(get_obj('Valuation Control').get_incoming_rate(self.doc.posting_date, self.doc.posting_time, d.item_code, d.s_warehouse, d.transfer_qty))
      d.save()

  # makes dict of unique items with it's qty
  #-----------------------------------------
  def make_items_dict(self, items_list):
    # items_list = [[item_name, qty]]
    for i in items_list:
      if self.item_dict.has_key(i[0]):
        self.item_dict[i[0]][0] = flt(self.item_dict[i[0]][0]) + flt(i[1])
      else:
        self.item_dict[i[0]] = [flt(i[1]), cstr(i[2]), cstr(i[3])]
        
  def get_raw_materials(self,pro_obj):
    # get all items from flat bom except, child items of sub-contracted and sub assembly items and sub assembly items itself.
    flat_bom_items = sql("select item_code, ifnull(sum(qty_consumed_per_unit), 0) * '%s', description, stock_uom  from `tabFlat BOM Detail` where parent = '%s' and parent_bom = '%s' and is_pro_applicable = 'No' and docstatus < 2 group by item_code" % ((self.doc.process == 'Backflush') and flt(self.doc.fg_completed_qty) or flt(pro_obj.doc.qty), cstr(pro_obj.doc.bom_no), cstr(pro_obj.doc.bom_no)))
    self.make_items_dict(flat_bom_items)
    if pro_obj.doc.consider_sa_items == 'Yes':
      # get all Sub Assembly items only from flat bom
      fl_bom_sa_items = sql("select item_code, ifnull(sum(qty_consumed_per_unit), 0) * '%s', description, stock_uom from `tabFlat BOM Detail` where parent = '%s' and parent_bom != '%s' and is_pro_applicable = 'Yes' and docstatus < 2 group by item_code" % ((self.doc.process == 'Backflush') and flt(self.doc.fg_completed_qty) or flt(pro_obj.doc.qty), cstr(pro_obj.doc.bom_no), cstr(pro_obj.doc.bom_no)))
      self.make_items_dict(fl_bom_sa_items)
    
    if pro_obj.doc.consider_sa_items == 'No':
      # get all sub assembly childs only from flat bom
      fl_bom_sa_child_item = sql("select item_code, ifnull(sum(qty_consumed_per_unit), 0) * '%s', description, stock_uom from `tabFlat BOM Detail` where parent = '%s' and parent_bom in (select distinct parent_bom from `tabFlat BOM Detail` where parent = '%s' and parent_bom != '%s' and is_pro_applicable = 'Yes' and docstatus < 2 ) and is_pro_applicable = 'No' and docstatus < 2 group by item_code" % ((self.doc.process == 'Backflush') and flt(self.doc.fg_completed_qty) or flt(pro_obj.doc.qty), cstr(pro_obj.doc.bom_no), cstr(pro_obj.doc.bom_no), cstr(pro_obj.doc.bom_no)))
      self.make_items_dict(fl_bom_sa_child_item)

  def add_to_stock_entry_detail(self, pro_obj, item_dict, fg_item = 0):
    sw, tw = '', ''
    if self.doc.process == 'Material Transfer':
      tw = cstr(pro_obj.doc.wip_warehouse)
    if self.doc.process == 'Backflush':
      tw = fg_item and cstr(pro_obj.doc.fg_warehouse) or ''
      if not fg_item: sw = cstr(pro_obj.doc.wip_warehouse)
    for d in item_dict:
      se_child = addchild( self.doc, 'mtn_details', 'Stock Entry Detail', 0, self.doclist)
      se_child.s_warehouse = sw
      se_child.t_warehouse = tw
      se_child.fg_item  = fg_item
      se_child.item_code = cstr(d)
      se_child.description = item_dict[d][1]
      se_child.stock_uom = item_dict[d][2]
      se_child.reqd_qty = flt(item_dict[d][0])
      se_child.transfer_qty = flt(item_dict[d][0])

  
  # get items 
  #------------------
  def get_items(self):
    pro_obj = self.doc.production_order and get_obj('Production Order', self.doc.production_order) or ''
    
    self.validate_for_production_order(pro_obj)
    self.get_raw_materials(pro_obj)
    
    self.doc.clear_table(self.doclist, 'mtn_details', 1)
    
    self.add_to_stock_entry_detail(pro_obj, self.item_dict)
    if self.doc.process == 'Backflush':
      item_dict = {cstr(pro_obj.doc.production_item) : [self.doc.fg_completed_qty, pro_obj.doc.description, pro_obj.doc.stock_uom]}
      self.add_to_stock_entry_detail(pro_obj, item_dict, fg_item = 1)

  def validate_transfer_qty(self):
    for d in getlist(self.doclist, 'mtn_details'):
      if flt(d.transfer_qty) <= 0:
        msgprint("Transfer Quantity can not be less than or equal to zero at Row No " + cstr(d.idx))
        raise Exception
      if d.s_warehouse:
        if flt(d.transfer_qty) > flt(d.actual_qty):
          msgprint("Transfer Quantity is more than Available Qty at Row No " + cstr(d.idx))
          raise Exception
  
  def calc_amount(self):
    total_amount = 0
    for d in getlist(self.doclist, 'mtn_details'):
      d.amount = flt(d.transfer_qty) * flt(d.incoming_rate)
      total_amount += flt(d.amount)
    self.doc.total_amount = flt(total_amount)

  def add_to_values(self, d, wh, qty, is_cancelled):
    self.values.append({
        'item_code'          : d.item_code,
        'warehouse'          : wh,
        'transaction_date'   : self.doc.transfer_date,
        'posting_date'       : self.doc.posting_date,
        'posting_time'       : self.doc.posting_time,
        'voucher_type'       : 'Stock Entry',
        'voucher_no'         : self.doc.name, 
        'voucher_detail_no'  : d.name,
        'actual_qty'         : qty,
        'incoming_rate'      : flt(d.incoming_rate) or 0,
        'stock_uom'          : d.stock_uom,
        'company'            : self.doc.company,
        'fiscal_year'        : self.doc.fiscal_year,
        'is_cancelled'       : (is_cancelled ==1) and 'Yes' or 'No',
        'batch_no'           : d.batch_no
    })
  
  def update_stock_ledger(self, is_cancelled=0):
    self.values = []      
    for d in getlist(self.doclist, 'mtn_details'):
      if cstr(d.s_warehouse):
        self.add_to_values(d, cstr(d.s_warehouse), -flt(d.transfer_qty), is_cancelled)
      
      if cstr(d.t_warehouse):
        self.add_to_values(d, cstr(d.t_warehouse), flt(d.transfer_qty), is_cancelled)
    
    get_obj('Stock Ledger', 'Stock Ledger').update_stock(self.values)

  
  def validate_for_production_order(self, pro_obj):
    if self.doc.purpose == 'Production Order' or self.doc.process or self.doc.production_order or flt(self.doc.fg_completed_qty):
      if self.doc.purpose != 'Production Order':
        msgprint("Purpose should be 'Production Order'.")
        raise Exception
      if not self.doc.process:
        msgprint("Process Field is mandatory.")
        raise Exception
      if self.doc.process == 'Backflush' and not flt(self.doc.fg_completed_qty):
        msgprint("FG Completed Qty is mandatory as the process selected is 'Backflush'")
        raise Exception
      if self.doc.process == 'Material Transfer' and flt(self.doc.fg_completed_qty):
        msgprint("FG Completed Qty should be zero. As the Process selected is 'Material Transfer'.")
        raise Exception
      if not self.doc.production_order:
        msgprint("Production Order field is mandatory")
        raise Exception
      if flt(pro_obj.doc.qty) < flt(pro_obj.doc.produced_qty) + flt(self.doc.fg_completed_qty) :
        msgprint("error:Already Produced Qty for %s is %s and maximum allowed Qty is %s" % (pro_obj.doc.production_item, cstr(pro_obj.doc.produced_qty) or 0.00 , cstr(pro_obj.doc.qty)))
        raise Exception
  

  def validate_serial_no_count(self,item_code,serial_no,qty):
    serial_no = serial_no.replace(' ','')
    serial_nos = cstr(serial_no).split(',')
    if not flt(len(serial_nos)) == flt(qty):
      msgprint("Please enter serial nos for all "+ cstr(qty) + " quantity")
      raise Exception
    for a in serial_nos:
      if a:
        exists = sql("select name from `tabSerial No` where name = '%s' and item_code = '%s'" % (a, item_code))
        if not exists:
          msgprint("Item "+ item_code +" of Serial No: "+ a + " does not exists in the system")
          raise Exception
  
  def validate_serial_no(self):
    for d in getlist(self.doclist, 'mtn_details'):
      ar_required = sql("select has_serial_no from tabItem where name = '%s'" % d.item_code)
      ar_required = ar_required and ar_required[0][0] or ''
      if ar_required == 'Yes' and not d.serial_no:
        msgprint("Serial No is mandatory for item: "+ d.item_code)
        raise Exception
      elif ar_required != 'Yes' and cstr(d.serial_no).strip():
        msgprint("If serial no required, please select 'Yes' in 'Has Serial No' in Item :"+d.item_code)
        raise Exception
      
      #check serial no count
      if d.serial_no:
        self.validate_serial_no_count(d.item_code, d.serial_no, d.transfer_qty)
  
  def validate(self):
    self.validate_serial_no()
    pro_obj = ''
    if self.doc.production_order:
      pro_obj = get_obj('Production Order', self.doc.production_order)
    self.validate_for_production_order(pro_obj)
    self.validate_warehouse(pro_obj)
    self.get_current_stock(pro_obj)
    self.calc_amount()
        
  def validate_warehouse(self, pro_obj):
    fg_qty = 0
    for d in getlist(self.doclist, 'mtn_details'):
      d.s_warehouse = (self.doc.purpose != 'Production Order') and  self.doc.from_warehouse or cstr(d.s_warehouse)
      d.t_warehouse = (self.doc.purpose != 'Production Order') and  self.doc.to_warehouse or cstr(d.t_warehouse)

      if not (d.s_warehouse or d.t_warehouse):
        msgprint("Atleast one warehouse is mandatory for Stock Entry ")
        raise Exception
      if d.s_warehouse and not sql("select name from tabWarehouse where name = '%s'" % d.s_warehouse):
        msgprint("Invalid Warehouse: %s" % self.doc.s_warehouse)
        raise Exception
      if d.t_warehouse and not sql("select name from tabWarehouse where name = '%s'" % d.t_warehouse):
        msgprint("Invalid Warehouse: %s" % self.doc.t_warehouse)
        raise Exception
      if d.s_warehouse == d.t_warehouse:
        msgprint("Source and Target Warehouse Cannot be Same.")
        raise Exception
      if self.doc.purpose == 'Material Issue':
        if not cstr(d.s_warehouse):
          msgprint("Source Warehouse is Mandatory for Purpose => 'Material Issue'")
          raise Exception
        if cstr(d.t_warehouse):
          msgprint("Target Warehouse is not Required for Purpose => 'Material Issue'")
          raise Exception
      if self.doc.purpose == 'Material Transfer':
        if not cstr(d.s_warehouse) or not cstr(d.t_warehouse):
          msgprint("Source Warehouse and Target Warehouse both are Mandatory for Purpose => 'Material Transfer'")
          raise Exception
      if self.doc.purpose == 'Material Receipt':
        if not cstr(d.t_warehouse):
          msgprint("Target Warehouse is Mandatory for Purpose => 'Material Receipt'")
          raise Exception
        if not flt(d.incoming_rate):
          msgprint("Rate is mandatory for Item " + cstr(d.item_code) + " at row " + cstr(d.idx))
          raise Exception
        if cstr(d.s_warehouse):
          msgprint("Source Warehouse is not Required for Purpose => 'Material Receipt'")
          raise Exception
      if self.doc.process == 'Material Transfer':
        if cstr(d.t_warehouse) != (pro_obj.doc.wip_warehouse):
          msgprint(" Target Warehouse should be same as WIP Warehouse %s in Production Order %s at Row No %s" % (cstr(pro_obj.doc.wip_warehouse), cstr(pro_obj.doc.name), cstr(d.idx)) )
          raise Exception
        if not cstr(d.s_warehouse):
          msgprint("Please Enter Source Warehouse at Row No %s is mandatory." % (cstr(d.idx)))
          raise Exception
      if self.doc.process == 'Backflush':
        if flt(d.fg_item):
          if cstr(pro_obj.doc.production_item) != cstr(d.item_code):
            msgprint("Item %s in Stock Entry Detail as Row No %s do not match with Item %s in Production Order %s" % (cstr(d.item_code), cstr(d.idx), cstr(pro_obj.doc.production_item), cstr(pro_obj.doc.name)))
            raise Exception
          fg_qty = flt(fg_qty) + flt(d.transfer_qty)
          if cstr(d.t_warehouse) != cstr(pro_obj.doc.fg_warehouse):
            msgprint("As Item %s is FG Item. Target Warehouse should be same as FG Warehouse %s in Production Order %s, at Row No %s. " % ( cstr(d.item_code), cstr(pro_obj.doc.fg_warehouse), cstr(pro_obj.doc.name), cstr(d.idx)))
            raise Exception
          if cstr(d.s_warehouse):
            msgprint("As Item %s is a FG Item. There should be no Source Warehouse at Row No %s" % (cstr(d.item_code), cstr(d.idx)))
            raise Exception
        if not flt(d.fg_item):
          if cstr(d.t_warehouse):
            msgprint("As Item %s is not a FG Item. There should no Tareget Warehouse at Row No %s" % (cstr(d.item_code), cstr(d.idx)))
            raise Exception
          if cstr(d.s_warehouse) != cstr(pro_obj.doc.wip_warehouse):
            msgprint("As Item %s is Raw Material. Source Warehouse should be same as WIP Warehouse %s in Production Order %s, at Row No %s. " % ( cstr(d.item_code), cstr(pro_obj.doc.wip_warehouse), cstr(pro_obj.doc.name), cstr(d.idx)))
            raise Exception
      d.save()
    if self.doc.fg_completed_qty and flt(self.doc.fg_completed_qty) != flt(fg_qty):
      msgprint("The Total of FG Qty %s in Stock Entry Detail do not match with FG Completed Qty %s" % (flt(fg_qty), flt(self.doc.fg_completed_qty)))
      raise Exception

  def update_production_order(self, is_submit):
    if self.doc.production_order:
      pro_obj = get_obj("Production Order", self.doc.production_order)
      if flt(pro_obj.doc.docstatus) != 1:
        msgprint("One cannot do any transaction against Production Order : %s, as it's not submitted" % (pro_obj.doc.name))
        raise Exception
      if pro_obj.doc.status == 'Stopped':
        msgprint("One cannot do any transaction against Production Order : %s, as it's status is 'Stopped'" % (pro_obj.doc.name))
        raise Exception
      if getdate(pro_obj.doc.posting_date) > getdate(self.doc.posting_date):
        msgprint("Posting Date of Stock Entry cannot be before Posting Date of Production Order "+ cstr(self.doc.production_order))
        raise Exception
      if self.doc.process == 'Backflush':
        pro_obj.doc.produced_qty = flt(pro_obj.doc.produced_qty) + (is_submit and 1 or -1 ) * flt(self.doc.fg_completed_qty)
        get_obj('Warehouse',  pro_obj.doc.fg_warehouse).update_bin(0, 0, 0, 0, (is_submit and 1 or -1 ) *  flt(self.doc.fg_completed_qty), pro_obj.doc.production_item, now())
      pro_obj.doc.status = (flt(pro_obj.doc.qty) == flt(pro_obj.doc.produced_qty)) and  'Completed' or 'In Process'
      pro_obj.doc.save()
  
  def update_serial_no(self, is_submit):
    for d in getlist(self.doclist, 'mtn_details'):
      serial_nos = []
      if d.serial_no:
        serial_nos = cstr(d.serial_no).split(',')
      
        for x in serial_nos:
          if d.s_warehouse:
            if is_submit == 1:
              sql("update `tabSerial No` set status = 'Issued' where name = %s", x)
            elif is_submit == 0:
              sql("update `tabSerial No` set status = 'In Store' where name = %s", x)
          if d.t_warehouse:
            if is_submit == 1:
              sql("update `tabSerial No` set warehouse = %s, status = 'In Store' where name = %s", (d.t_warehouse, x))
            elif is_submit == 0:
              sql("update `tabSerial No` set warehouse = %s, status = 'In Store' where name = %s", (d.s_warehouse, x))
          
          if self.doc.purpose == 'Purchase Return':
            sql("delete from `tabSerial No` where name = %s", x)
  
  def on_submit(self):
    self.validate_transfer_qty()
    # Check for Approving Authority
    get_obj('Authorization Control').validate_approving_authority(self.doc.doctype, self.doc.company, self.doc.total_amount)
    self.update_stock_ledger(0)
    self.update_serial_no(1)
    # update Production Order
    self.update_production_order(1)

    # make feed
    get_obj('Feed Control').make_feed('submitted', self.doc.doctype, self.doc.name)
    
  def on_cancel(self):
    self.update_stock_ledger(1)
    self.update_serial_no(0)
    # update Production Order
    self.update_production_order(0)

    # make feed
    get_obj('Feed Control').make_feed('cancelled', self.doc.doctype, self.doc.name)
    
  def get_cust_values(self):
    res = sql("select customer,customer_name, customer_address from `tabDelivery Note` where name = '%s'"%self.doc.delivery_note_no)
    ret = {
      'customer'         : res and res[0][0] or '',
      'customer_name'    : res and res[0][1] or '',
      'customer_address' : ret and ret[0][2] or ''}

    return str(ret)


  def get_cust_addr(self):
    res = sql("select customer_name,address from `tabCustomer` where name = '%s'"%self.doc.customer)
    ret = { 
      'customer_name'    : res and res[0][0] or '',
      'customer_address' : res and res[0][1] or ''}

    return str(ret)


    
  def get_supp_values(self):
    res = sql("select supplier,supplier_name,supplier_address from `tabPurchase Receipt` where name = '%s'"%self.doc.purchase_receipt_no)
    ret = {
      'supplier' : res and res[0][0] or '',
      'supplier_name' :res and res[0][1] or '',
      'supplier_address' : res and res[0][2] or ''}
    return str(ret)
    

  def get_supp_addr(self):
    res = sql("select supplier_name,address from `tabSupplier` where name = '%s'"%self.doc.supplier)
    ret = {
      'supplier_name' : res and res[0][0] or '',
      'supplier_address' : res and res[0][1] or ''}
    return str(ret)

  # on update
  def on_update(self):
    obj = get_obj('Feed Control', 'Feed Control')
    
    if not self.doc.creation:
      obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      obj.make_feed('modified', self.doc.doctype, self.doc.name)
