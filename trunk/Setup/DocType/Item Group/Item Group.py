class DocType:
  def __init__(self,d,dl):
    self.doc, self.doclist = d,dl
    self.nsm_parent_field = 'parent_item_group';

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
      res = sql("select name from `tabItem Group` where is_group = 'Yes' and docstatus!= 2 and (rgt > %s or lft < %s) and name ='%s' and name !='%s'"%(self.doc.rgt,self.doc.lft,self.doc.parent_item_group,self.doc.item_group_name))
      if not res:
        msgprint("Please enter proper parent item group.") 
        raise Exception
    
    r = sql("select name from `tabItem Group` where name = '%s' and docstatus = 2"%(self.doc.item_group_name))
    if r:
      msgprint("'%s' record is trashed. To untrash please go to Setup & click on Trash."%(self.doc.item_group_name))
      raise Exception