class DocType:

  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
  #=======================================================================================================
  def get_master_lists(self):
    ret = convert_to_lists(sql("select name from `tabWarehouse Type`"))
    ret = ret and ret or []
    return ret
      
  #=======================================================================================================
  def create_record(self,dict_val):
    obj_dict = eval(dict_val)
    
    for d in obj_dict:
      if not obj_dict[d] == '' and not d =='Doctype':
        
        ret =sql("select name from `tab%s` where name = '%s'" %(obj_dict['Doctype'],obj_dict[d]))
        if ret:
          return "Record already exist."
          raise Exception
        rec = Document(obj_dict['Doctype'])
    for i in obj_dict:
      if not obj_dict[i] == '' and not i == 'Doctype':
        rec.fields[i] = obj_dict[i]
      
    rec.save(1)
    return "Record created."

  #=======================================================================================================
  def get_page_lst(self,nm):
    
    r1 = cstr(webnotes.user.get_roles()).replace('[','').replace(']','')

    ret = sql("select parent from `tabPage Role` where role in (%s) and parent = '%s'"%(r1,nm))

    return ret and True or False
    
  #=======================================================================================================
  #------------------------get contry--------------------------------
  def get_country(self):
    cty = sql("select value from `tabSingles` where field = 'country' and doctype = 'Control Panel'")

    return cty and cty[0][0] or ''