class DocType:
  def __init__(self,doc,doclist=[]):
    self.doc = doc
    self.doclist = doclist
  
  def autoname(self):
    if self.doc.batch_id:
      self.doc.name = self.doc.batch_id
    else:
      self.doc.name = make_autoname('Batch/' + '/.#####')