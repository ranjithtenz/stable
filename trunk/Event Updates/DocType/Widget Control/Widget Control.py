class DocType:
  def __init__(self,d,dl):
    self.doc, self.doclist = d, dl
      
  def add_comment(self,args):
    import time
    args = eval(args)
    if(args['comment']):
      cmt = Document('Comment Widget Record')
      for arg in args:
        cmt.fields[arg] = args[arg]
      cmt.comment_date = nowdate()
      cmt.comment_time = time.strftime('%H:%M')
      cmt.save(1)
    else:
      raise Exception
        
  def remove_comment(self,cmt_id):
    sql("delete from `tabComment Widget Record` where name=%s",cmt_id)
    
  def get_topics(self):
    dt = {}
    main_topic = {}
    sub_topic = {}
    topics = []
    mt = sql("select distinct(t1.parent_topic) from `tabForum Topic`t1 left join `tabForum Topic`t2 on t2.topic!=t1.parent_topic")
    '''st = sql("select distinct(topic) from `tabForum Topic`")
    for m in mt:
      for s in st:
        if m==s:
          sub_topic[m] = ''
        else:
          main_topic[m] = ''
    msgprint(main_topic)
    msgprint(sub_topic)'''
    msgprint(mt)