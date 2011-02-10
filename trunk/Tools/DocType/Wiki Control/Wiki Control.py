class DocType:
  def __init__(self,d,dl):
    self.doc = d
    self.doclist = dl
  
  def get_wiki_detail(self,arg):
    arg = eval(arg)
    ret = {}
    latest_revision = sql("select max(revision) from `tabWiki History` where reference=%s", arg['dn'])[0][0]
    
    ret['detail'] = convert_to_lists(sql("select revision, modified_by,creation from `tabWiki History` where reference=%s and revision=%s", (arg['dn'],latest_revision)))
    ret['contributors'] = convert_to_lists(sql("select distinct modified_by from `tabWiki History` where reference=%s", arg['dn']))
    return ret