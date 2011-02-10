class DocType:
  def __init__(self,d,dl):
    self.doc, self.doclist = d,dl
    self.nsm_parent_field = 'parent_cost_center'
        
  def autoname(self):
    #company_abbr = sql("select abbr from tabCompany where name=%s", self.doc.company)[0][0]
    self.doc.name = self.doc.cost_center_name + ' - ' + self.doc.company_abbr   
 
      
  def get_abbr(self):
    abbr = sql("select abbr from tabCompany where company_name='%s'"%(self.doc.company_name))[0][0] or ''
    ret = {
      'company_abbr'  : abbr
    }
    return cstr(ret)

  def validate(self): 

    # Cost Center name must be unique
    # ---------------------------

    if (self.doc.__islocal or (not self.doc.name)) and sql("select name from `tabCost Center` where cost_center_name = %s and company_name=%s", (self.doc.cost_center_name, self.doc.company_name)):
      msgprint("Cost Center Name already exists, please rename")
      raise Exception
      
    check_acc_list = []
    for d in getlist(self.doclist, 'budget_details'):
      if d.account in check_acc_list:
        msgprint("Account " + cstr(d.account) + "has been entered more than once.")
        raise Exception
      if d.account not in check_acc_list: check_acc_list.append(d.account)
      
  def on_update(self):
    # update Node Set Model
    if globals().has_key('version') and globals()['version'] == 'v170':
      import webnotes
      import webnotes.utils.nestedset
      # update Node Set Model
      webnotes.utils.nestedset.update_nsm(self)
    else:
      update_nsm(self)