class DocType:
  def __init__(self, d, dl):
    self.doc, self.doclist = d, dl

  
  # Get Masters
  # -----------
  def get_masters(self):
    mlist = []
    res = sql("select distinct t1.name from tabDocType t1, tabDocPerm t2 where ifnull(t1.allow_trash, 0) = 1 and (ifnull(t2.write, 0) = 1 or ifnull(t2.create, 0) = 1) and t2.role in %s and t2.parent = t1.name and t1.module not in ('DocType','Application Internal','Recycle Bin','Development','Testing','Testing System','Test') ORDER BY t1.name" % cstr(tuple(webnotes.user.get_roles())))
    for r in res:
      mlist.append(r[0])
    return mlist


  # Get Trash Records
  # -----------------
  def get_trash_records(self, mast_name):
    mlist = []
    rec_dict = {}
    if mast_name == 'All':
      mlist = self.get_masters()
    else:
      mlist.append(mast_name)
    for i in mlist:
      rec = [r[0] for r in sql("select name from `tab%s` where docstatus = 2" % i)]
      if rec:
        rec_dict[i] = rec
    return rec_dict


  # Restore Records
  # ---------------
  def restore_records(self, arg):
    arg = eval(arg)
    for k in arg:
      for r in arg[k]:
        sql("update `tab%s` set docstatus = 0, modified = '%s', trash_reason = '' where name = '%s'" % (k, now(), r))
        dt_obj = get_obj(k,r)
        if hasattr(dt_obj, 'on_restore'): dt_obj.on_restore()