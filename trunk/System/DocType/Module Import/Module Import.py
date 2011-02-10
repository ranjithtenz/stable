class DocType:
  def __init__(self, d, dl):
    self.doc, self.doclist = d, dl

  def login_remote(self):
    import webnotes.utils.webservice
    self.fw = webnotes.utils.webservice.FrameworkServer(self.doc.host, self.doc.path, self.doc.login_id, self.doc.pwd, self.doc.account or '')

  def get_remote_modules(self, arg=''):
    self.login_remote()
    self.module_list = self.fw.runserverobj('Module Import', 'Module Import', 'get_modules', '')
    return self.module_list['message']

  def get_modules(self):
    return [m[0] for m in sql("select name from `tabModule Def`")]

  def import_module(self, arg):
    self.login_remote()
    r = self.fw.http_get_response('webnotes.utils.transfer.get_module', {'module':arg} )
    try:
      import json
    except:
      import simplejson as json # python 2.4

    r = json.loads(r.read())

    if r.get('exc'): msgprint(r['exc'])
    if r.get('server_messages'): msgprint(r['server_messages'])

    import webnotes.utils.transfer
    return webnotes.utils.transfer.accept_module(r['super_doclist'])
