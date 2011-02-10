class DocType:
  def __init__(self,doc,doclist=[]):
    self.doc, self.doclist = doc,doclist

  #--------------------get naming series from sales invoice-----------------
  def get_series(self):
    res = sql("select options from `tabDocField` where parent='Receivable Voucher' and fieldname = 'naming_series'")
    return res and cstr(res[0][0]) or ''
