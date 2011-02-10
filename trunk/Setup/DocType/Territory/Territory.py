class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    self.nsm_parent_field = 'parent_territory'

  def check_state(self):
    return NEWLINE + NEWLINE.join([i[0] for i in sql("select state_name from `tabState` where `tabState`.country='%s' " % self.doc.country)])

       

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
    if self.doc.lft and self.doc.rgt:
      res = sql("select name from `tabTerritory` where is_group = 'Yes' and docstatus!= 2 and (rgt > %s or lft < %s) and name ='%s' and name !='%s'"%(self.doc.rgt,self.doc.lft,self.doc.parent_territory,self.doc.territory_name))
      if not res:
        msgprint("Please enter proper parent territory.") 
        raise Exception

    r = sql("select name from `tabTerritory` where name = '%s' and docstatus = 2"%(self.doc.territory_name))
    if r:
      msgprint("%s record is trashed. To untrash please go to Setup & click on Trash."%(self.doc.territory_name))
      raise Exception

    for d in getlist(self.doclist, 'target_details'):
      if not flt(d.target_qty) and not flt(d.target_amount):
        msgprint("Either target qty or target amount is mandatory.")
        raise Exception