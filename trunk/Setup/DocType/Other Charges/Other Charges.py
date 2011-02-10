class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist

  # Get Tax Rate if account type is Tax
  # ===================================================================
  def get_rate(self, arg):
    get_obj('Sales Common').get_rate(arg, self)