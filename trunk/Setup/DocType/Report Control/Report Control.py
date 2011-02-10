class DocType:
  def __init__(self,d,dl):
    self.doc, self.doclist = d,dl

  def get_reports(self,mod):
    ret = {}
    rep = sql('select doc_type, doc_name, display_name, icon, description, fields from `tabModule Def Item` where parent=%s and doc_type = "Reports" order by idx asc', mod)
    ret[mod] = [[i or '' for i in r] for r in rep]
    if mod == 'Accounts':
      cnty = sql("select value from `tabSingles` where field = 'country' and doctype = 'Control Panel'")
      ret['Country']= cnty and cnty[0][0] or ''
    return ret

  def get_setup_details(self,mod):
    ret = {}

    pg = sql("select doc_type,doc_name,display_name, icon, description, fields from `tabModule Def Item` where parent=%s and doc_type='Setup Pages' order by idx asc", mod)
    ret['Pages'] = [[i or '' for i in p] for p in pg]

    frm = sql("select doc_type,doc_name,display_name, icon, description, fields from `tabModule Def Item` where parent=%s and doc_type='Setup Forms' order by idx asc", mod)
    ret['Forms'] = [[i or '' for i in f] for f in frm]

    return ret