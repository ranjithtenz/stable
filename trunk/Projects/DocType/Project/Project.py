class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist  
  
  # Get Customer Details along with its primary contact details
  # ==============================================================
  def get_customer_details(self):
    details =sql("select address, territory, customer_group,customer_name from `tabCustomer` where name=%s and docstatus!=2",(self.doc.customer),as_dict=1)
    if details:
      ret = {
        'customer_address'  :  details and details[0]['address'] or '',
        'territory'       :  details and details[0]['territory'] or '',
        'customer_group'    :  details and details[0]['customer_group'] or '',
	'customer_name'     :  details and details[0]['customer_name'] or ''
      }
      #get primary contact details(this is done separately coz. , if join query used & no primary contact thn it would not be able to fetch customer details)
      contact_det = sql("select contact_name, contact_no, email_id from `tabContact` where customer_name='%s' and is_customer=1 and is_primary_contact='Yes' and docstatus!=2" %(self.doc.customer), as_dict = 1)
      ret['contact_person'] = contact_det and contact_det[0]['contact_name'] or ''
      ret['contact_no'] = contact_det and contact_det[0]['contact_no'] or ''
      ret['email_id'] = contact_det and contact_det[0]['email_id'] or ''    
      return cstr(ret)
    else:
      msgprint("Customer : %s does not exist in system." % (self.doc.customer))
      raise Exception  
  
  # Get customer's contact person details
  # ==============================================================
  def get_contact_details(self):
    contact = sql("select contact_no, email_id from `tabContact` where contact_name = '%s' and customer_name = '%s' and docstatus != 2" %(self.doc,contact_person,self.doc.customer), as_dict=1)
    if contact:
      ret = {
        'contact_no' : contact and contact[0]['contact_no'] or '',
        'email_id' : contact and contact[0]['email_id'] or ''
      }
      return str(ret)
    else:
      msgprint("Contact Person : %s does not exist in the system." % (self.doc,contact_person))
      raise Exception
  
  #calculate gross profit
  #=============================================
  def get_gross_profit(self):
    pft, per_pft =0, 0
    pft = flt(self.doc.project_value) - flt(self.doc.est_material_cost)
    #if pft > 0:
    per_pft = (flt(pft) / flt(self.doc.project_value)) * 100
    ret = {'gross_margin_value': pft, 'per_gross_margin': per_pft}
    return cstr(ret)
    
  # validate
  #================================================
  def validate(self):
    if self.doc.project_start_date and self.doc.completion_date:
      if getdate(self.doc.completion_date) < getdate(self.doc.project_start_date):
        msgprint("Expected Completion Date can not be less than Project Start Date")
        raise Exception
