class DocType:
  def __init__(self, d, dl):
    self.doc, self.doclist = d, dl

  def logout_sso(self):
    import webnotes
    import webnotes.utils.webservice

    if session['data'].get('login_from'):
      sso = webnotes.utils.webservice.FrameworkServer(session['data'].get('login_from'), '/', '__system@webnotestech.com', 'password')
      sso.runserverobj('SSO Control', 'SSO Control', 'logout_user', session['user'])