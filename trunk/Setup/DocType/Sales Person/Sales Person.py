class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    self.nsm_parent_field = 'parent_sales_person';

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

    for d in getlist(self.doclist, 'target_details'):
      if not flt(d.target_qty) and not flt(d.target_amount):
        msgprint("Either target qty or target amount is mandatory.")
        raise Exception