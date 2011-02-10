class DocType:
  def __init__(self, doc, doclist):
    self.doc = doc
    self.doclist = doclist
  
  def get_date_diff(self):
    if session['user'] != 'Administrator' and session['user'] != 'Demo':
      last_pwd_date = sql("select password_last_updated from tabProfile where name=%s",session['user'])[0][0] or ''
      if cstr(last_pwd_date) == '':
        sql("update tabProfile set password_last_updated = '%s' where name='%s'"% (nowdate(),session['user']))
      else:
        date_diff = (getdate(nowdate()) -last_pwd_date).days
        return date_diff
        
  def get_cur_pwd(self):
    if session['user'] != 'Administrator' and session['user'] != 'Demo':
      cur_pwd = sql("select password from tabProfile where name=%s",session['user'])[0][0] or ''
      return cur_pwd
      
  def reset_password(self,pwd):
    sql("update tabProfile set password= '%s',password_last_updated='%s' where name = '%s'" % (pwd,nowdate(),session['user']))