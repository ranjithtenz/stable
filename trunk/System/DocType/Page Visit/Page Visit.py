class DocType:
  def __init__(self, doc, doclist):
    self.doc = doc
    self.doclist = doclist
  
  def autoname(self):
    self.doc.name = make_autoname(self.doc.page_name+'/.####')