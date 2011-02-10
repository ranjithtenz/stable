class DocType:
  def __init__(self,d,dl):
    self.doc, self.doclist = d,dl

  def autoname(self):
    account_id = sql("select UPPER(value) from tabSingles where doctype='Control Panel' and field='account_id'")[0][0]
    if account_id == 'BROWNIE':
      self.doc.standard = 'Yes'
      self.doc.name = make_autoname('SRCH/.#####')
    elif account_id != 'BROWNIE' and (not self.doc.standard or self.doc.standard == 'No'):
      self.doc.standard = 'No'
      self.doc.name = make_autoname('SRCH/C/.#####')

  def validate(self):
    if not self.doc.module:
      msgprint("Please don't forget to enter MODULE after Search Criteria is Saved.")