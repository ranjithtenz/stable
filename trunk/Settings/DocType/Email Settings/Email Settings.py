class DocType:
  def __init__(self,doc,doclist):
    self.doc,self.doclist = doc,doclist

  def set_vals(self):
    res = sql("select field, value from `tabSingles` where doctype = 'Control Panel' and field IN ('outgoing_mail_server','mail_login','mail_password','auto_email_id','mail_port','use_ssl')")
    ret = {}
    for r in res:
      ret[cstr(r[0])]=r[1] and cstr(r[1]) or ''
        
    return str(ret)

  def on_update(self):
    if self.doc.outgoing_mail_server:
      sql("update `tabSingles` set value ='%s' where doctype = 'Control Panel' and field = 'outgoing_mail_server'"%self.doc.outgoing_mail_server)
    if self.doc.mail_login:
      sql("update `tabSingles` set value ='%s' where doctype = 'Control Panel' and field = 'mail_login'"%self.doc.mail_login)
    if self.doc.mail_password:
      sql("update `tabSingles` set value ='%s' where doctype = 'Control Panel' and field = 'mail_password'"%self.doc.mail_password)
    if self.doc.auto_email_id:
      sql("update `tabSingles` set value ='%s' where doctype = 'Control Panel' and field = 'auto_email_id'"%self.doc.auto_email_id)
    if self.doc.mail_port:
      sql("update `tabSingles` set value ='%s' where doctype = 'Control Panel' and field = 'mail_port'"%self.doc.mail_port)
    if self.doc.use_ssl:
      sql("update `tabSingles` set value ='%s' where doctype = 'Control Panel' and field = 'use_ssl'"%self.doc.use_ssl)