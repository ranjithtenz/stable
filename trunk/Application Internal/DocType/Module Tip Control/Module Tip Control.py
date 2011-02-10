class DocType:
  def __init__(self, d, dl):
    self.doc, self.doclist = d, dl

  # get update on recent activities of module
  # -----------------------------------------
  def get_module_activity(self, args):
    args = eval(args)
    ret = {}
    for tr in args['tr_list']:
      cnt = sql("select ifnull(count(name),0) from `tab%s` where datediff(now(),creation) between 0 and 7"%(tr))
      if cnt[0][0]:
        ret[tr] = cnt
    if ret:        
      return ret