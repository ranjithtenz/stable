class DocType:
  def __init__(self, doc, doclist):
    self.doc = doc
    self.doclist = doclist

  def validate(self):
     self.disable_users()
    
  
  # Function to Disallow disabling of users from client account
  # -----------------------------------------------------------
  def disable_users(self):
    if self.doc.enabled==0:
      msgprint('Please go to Setup --> Manage User Page to disable users from this account')
      raise Exception
  
  
  # Autoname is Email id
  # --------------------

  def autoname(self):
    import re

    self.doc.email = self.doc.email.strip()
    if self.doc.name!='Guest' and not re.match("^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$", self.doc.email):
      msgprint("%s is not a valid email id" % self.doc.email)
      raise Exception

    self.doc.name = self.doc.email
  
  def on_update(self):
    # owner is always name
    if not self.doc.password:
      set(self.doc, 'password' ,'password')
    set(self.doc, 'owner' ,self.doc.name)


  def update_password(self):
    sql("UPDATE `tabProfile` SET password=PASSWORD(%s) where name=%s", (self.doc.new_password, self.doc.name))
    email_text = '''%s,
    
Your password has been changed.
    
- Administrator
''' % self.doc.name
    sendmail([self.doc.email], subject='Change of Password Notification', parts = [('text/plain', email_text)])
    msgprint("Your password has been changed")