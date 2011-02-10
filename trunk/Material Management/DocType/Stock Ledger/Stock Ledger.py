class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist


  # update stock
  # ------------
    
  def update_stock(self, values):
    
    for v in values:
      sle_id = ''
      # reverse quantities for cancel
      if v['is_cancelled']=='Yes':
        v['actual_qty'] = -flt(v['actual_qty'])

        # cancel matching entry:
        sql("update `tabStock Ledger Entry` set is_cancelled='Yes' where voucher_no=%s and voucher_type=%s", (v['voucher_no'], v['voucher_type']))

      
      # make ledger entry
      if v["actual_qty"]:
        sle_id = self.make_entry(v)
      # update bin qty
      get_obj('Warehouse', v["warehouse"]).update_bin(flt(v["actual_qty"]), 0, 0, 0, 0, v["item_code"], v["posting_date"],sle_id,v["posting_time"])
      # get_obj("Item",v["item_code"]).check_min_inventory_level()       # to check minimum inventory level in item

  # make entry
  # ----------
  
  def make_entry(self, args):
    sle = Document(doctype = 'Stock Ledger Entry')
    for k in args.keys():
      # adds warehouse_type
      if k == 'warehouse': 
        sle.fields['warehouse_type'] = get_value('Warehouse' , args[k], 'warehouse_type')
      
      sle.fields[k] = args[k]

    sle_obj = get_obj(doc=sle)

    # validate
    sle_obj.validate()
    
    sle.save(new = 1)
    return sle.name