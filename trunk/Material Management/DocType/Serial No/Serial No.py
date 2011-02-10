class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
  
  def get_item_details(self):
    item = sql("select item_group,brand,description,warranty_period from `tabItem` where name = '%s' and (ifnull(end_of_life,'')='' or end_of_life = '0000-00-00' or end_of_life >  now()) " %(self.doc.item_code), as_dict=1)
    ret = {
      'item_group' : item and item[0]['item_group'] or '',
      'brand' : item and item[0]['brand'] or '',
      'description' : item and item[0]['description'] or '',
      'warranty_period' : item and item[0]['warranty_period'] or 0
    }
    return str(ret)
  
  def get_customer_details(self):
    det = sql("select customer_name,address,territory from `tabCustomer` where name = %s ", self.doc.customer, as_dict=1)
    
    ret = {
      'customer_name':  det and det[0]['customer_name'] or '',
      'customer_address'  :  det and det[0]['address'] or '',
      'territory':  det and det[0]['territory'] or ''
    }
    return str(ret)
  
  def get_delivery_details(self):
    det = sql("select posting_date, customer, customer_name, customer_address, territory from `tabDelivery Note` where name=%s", self.doc.delivery_note_no, as_dict=1)
    if det:
      ret = {
        'delivery_date' : det and (det[0]['posting_date']).strftime('%Y-%m-%d') or '',
        'customer' : det and det[0]['customer'] or '',  
        'customer_name' : det and det[0]['customer_name'] or '',
        'customer_address'  :  det and det[0]['customer_address'] or '',
        'territory':  det and det[0]['territory'] or ''
      }
      return str(ret)
  
  def get_purchase_details(self):
    det = sql("select posting_date from `tabPurchase Receipt` where name=%s", self.doc.pr_no)
    if det:
      ret = {
        'purchase_date' : det and det[0][0].strftime('%Y-%m-%d') or ''
      }
      return str(ret)
  
  def validate(self):
    import datetime
    if self.doc.warranty_expiry_date and getdate(self.doc.warranty_expiry_date) >= datetime.date.today() and self.doc.maintenance_status == 'Out of Warranty':
      msgprint("Warranty expiry date and maintenance status mismatch. Please verify")
      raise Exception
    elif (not self.doc.warranty_expiry_date or getdate(self.doc.warranty_expiry_date) < datetime.date.today()) and self.doc.maintenance_status == 'Under Warranty':
      msgprint("Warranty expiry date and maintenance status mismatch. Please verify")
      raise Exception
    
    if self.doc.amc_expiry_date and getdate(self.doc.amc_expiry_date) >= datetime.date.today() and self.doc.maintenance_status == 'Out of AMC':
      msgprint("AMC expiry date and maintenance status mismatch. Please verify")
      raise Exception
    elif (not self.doc.amc_expiry_date or getdate(self.doc.amc_expiry_date) < datetime.date.today()) and self.doc.maintenance_status == 'Under AMC':
      msgprint("Warranty expiry date and maintenance status mismatch. Please verify")
      raise Exception

  def on_update(self):
    obj = get_obj('Feed Control', 'Feed Control')

    if not self.doc.creation:
      obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      obj.make_feed('modified', self.doc.doctype, self.doc.name)