class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    self.prefix = is_testing and 'test' or 'tab'

  def validate(self):
    import string
  
    if not (self.doc.address_line1)  and not (self.doc.address_line2) and not (self.doc.city) and not (self.doc.state) and not (self.doc.country) and not (self.doc.pincode):
      return "Please enter address"
      
    else:
      address =["address_line1", "address_line2", "city", "state", "country", "pincode"]
      comp_address=''
      for d in address:
        if self.doc.fields[d]:
          comp_address += self.doc.fields[d] + NEWLINE
      self.doc.address = comp_address

  def check_state(self):
    return NEWLINE + NEWLINE.join([i[0] for i in sql("select state_name from `tabState` where `tabState`.country='%s' " % self.doc.country)])
    
  def get_contacts(self,nm):
    if nm:
      contact_details =convert_to_lists(sql("select name, CONCAT(IFNULL(first_name,''),' ',IFNULL(last_name,'')),contact_no,email_id from `tabContact` where sales_partner = '%s'"%nm))
      return contact_details
    else:
      return ''