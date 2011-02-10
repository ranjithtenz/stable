class DocType:
  #init function
  def __init__(self,doc,doclist=[]):
    self.doc = doc
    self.doclist = doclist

  def set_content(self):
    ret_content = sql("select content from `tabBusiness Letter Template` where name ='%s'"%self.doc.template)
    if ret_content: self.doc.content = ret_content[0][0]
    return ''