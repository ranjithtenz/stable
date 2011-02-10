class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist

  def update_bom_operation(self):
      bom_list = sql(" select DISTINCT parent from `tabBOM Operation` where workstation = '%s'" % self.doc.name)
      for bom_no in bom_list:
        sql("update `tabBOM Operation` set hour_rate = '%s' where parent = '%s' and workstation = '%s'"%( self.doc.hour_rate, bom_no, self.doc.name))
  
  def on_update(self):
    set(self.doc, 'overhead', flt(self.doc.hour_rate_electricity) + flt(self.doc.hour_rate_consumable) + flt(self.doc.hour_rate_rent))
    set(self.doc, 'hour_rate', flt(self.doc.hour_rate_labour) + flt(self.doc.overhead))
    self.update_bom_operation()