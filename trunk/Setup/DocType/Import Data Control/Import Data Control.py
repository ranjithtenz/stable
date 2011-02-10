class DocType:
  def __init__(self,d,dl):
    self.doc, self.doclist = d,dl

  def get_master_lst(self):
    
    return [r[0] for r in sql("select name from `tabDocType` where document_type = 'Master'")]

  def get_child_lst(self,nm):
    res = [nm]
    
    ret=sql("select options from `tabDocField` where parent='%s' and fieldtype = 'Table'"%nm)
    for r in ret:
      res.append(r[0])
    return res