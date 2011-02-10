class DocType:
  def __init__(self, d,dl):
    self.doc, self.doclist = d,dl

  def set_module(self):
    sql("update tabDocType set module=%s where name=%s", (self.doc.module, self.doc.doc_type))