class DocType:
  def __init__(self, doc, doclist):
    self.doc = doc
    self.doclist = doclist
    
  def validate(self):
    self.doc.module = 'Accounts'