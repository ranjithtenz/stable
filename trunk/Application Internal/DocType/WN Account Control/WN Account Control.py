class DocType:
  def __init__(self,doc,doclist):
    self.doc = doc
    self.doclist = doclist

  def get_users(self):
    ret = sql("select name from tabProfile where name!='Administrator' and name!='Guest' and enabled=1")
    return ret

  def remove_users(self,args):
    args = eval(args)
    #for user in args['app_user_list']:
      #sql("update tabProfile set enabled=0 where email=%s",(user))

  def create_users_profile(self,args):
    args = eval(args)
    for email_id in args['user_email_ids']:
      if sql("select email from tabProfile where email=%s",(email_id)):
        p = Document('Profile',email_id)
        p.enabled = 1
        p.save()
      else:  
        p = Document('Profile')
        p.email = email_id
        p.save(1)