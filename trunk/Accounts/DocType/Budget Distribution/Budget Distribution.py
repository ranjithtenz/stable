class DocType:
  def __init__(self,doc,doclist=[]):
    self.doc,self.doclist = doc,doclist
    
  def get_months(self):
    month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
    idx =1
    for m in month_list:
      mnth = addchild(self.doc,'budget_distribution_details','Budget Distribution Detail',1,self.doclist)
      mnth.month = m or ''
      mnth.idx = idx
      idx += 1
      
  def validate(self):
    total = 0
    for d in getlist(self.doclist,'budget_distribution_details'):
      total = flt(total) + flt(d.percentage_allocation)
    if total > 100:
      msgprint("Percentage Allocation should not exceed 100%.")
      raise Exception
    elif total < 100:
      msgprint("Percentage Allocation should not recede 100%.")
      raise Exception