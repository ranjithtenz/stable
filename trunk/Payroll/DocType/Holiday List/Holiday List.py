class DocType:
  def __init__(self,doc,doclist=[]):
    self.doc = doc
    self.doclist = doclist
   


  def autoname(self):
    fy = cstr(self.doc.fiscal_year).split('-')
    self.doc.name = make_autoname(self.doc.holiday_list_name +"/"+ cstr(fy[0]))