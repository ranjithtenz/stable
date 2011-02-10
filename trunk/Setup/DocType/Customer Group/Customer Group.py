class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    self.nsm_parent_field = 'parent_customer_group';


  # update Node Set Model
  def update_nsm_model(self):
    if globals().has_key('version') and globals()['version'] == 'v170':
      import webnotes
      import webnotes.utils.nestedset
      webnotes.utils.nestedset.update_nsm(self)
      #webnotes.utils.nestedset.rebuild_tree(self.doc.doctype, self.nsm_parent_field)
    else:
      update_nsm(self)
      #rebuild_tree(self.doc.doctype, self.nsm_parent_field)
  # ON UPDATE
  #--------------------------------------
  def on_update(self):
    # update nsm
    self.update_nsm_model()   


  def validate(self): 

    r = sql("select name from `tabCustomer Group` where name = '%s' and docstatus = 2"%(self.doc.customer_group_name))
    if r:
      msgprint("%s record is trashed. To untrash please go to Setup & click on Trash."%(self.doc.customer_group_name))
      raise Exception