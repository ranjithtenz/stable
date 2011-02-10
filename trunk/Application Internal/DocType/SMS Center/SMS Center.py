class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
      
  def create_receiver_table(self):
    if self.doc.send_to:
      self.doc.clear_table(self.doclist, 'receiver_details')
      rec = ''
      if self.doc.send_to == 'All Customer':
        rec = sql("select customer_name, CONCAT(ifnull(first_name,''),'',ifnull(last_name,'')), mobile_no from `tabContact` where ifnull(customer_name,'') !='' and ifnull(mobile_no,'')!=''")

      elif self.doc.send_to == 'Customer Group' and self.doc.customer_group_name:
       
        rec = sql("select t2.customer_name, CONCAT(ifnull(first_name,''),'',ifnull(last_name,'')), t1.mobile_no from `tabContact` t1, `tabCustomer` t2 where t2.name = t1.customer_name and ifnull(t1.mobile_no,'')!='' and t2.customer_group = '%s'"%self.doc.customer_group_name)
      if not rec:
        msgprint("Either customer having no contact or customer's contact does not have mobile no")
        raise Exception 

      for d in rec:
        ch = addchild(self.doc, 'receiver_details', 'Receiver Detail', 1, self.doclist)
        ch.customer_name = d[0]
        ch.receiver_name = d[1]
        ch.mobile_no = d[2]
    else:
      msgprint("Please select 'Send To' field")
        
        
  def send_sms(self):
    if not self.doc.message:
      msgprint("Please type the message before sending")
    elif not getlist(self.doclist, 'receiver_details'):
      msgprint("Receiver Table is blank.")
    else:
      receiver_list = []
      for d in getlist(self.doclist, 'receiver_details'):
        if d.mobile_no:
          receiver_list.append(d.mobile_no)
      if receiver_list:
        msgprint(get_obj('SMS Control', 'SMS Control').send_sms(receiver_list, self.doc.message))