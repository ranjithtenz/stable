class DocType:
  def __init__(self,d,dl):
    self.doc, self.doclist = d,dl
  
  def get_projects(self, arg):
    # project list
    pl=[]
    status={}
    if arg == 'Open':
      pl = [p[0] for p in sql("select name from `tabProject` where status = 'Open' order by creation desc limit 20")]
      for p1 in pl:
        status[p1] = 'Open'
    elif arg == 'Completed':
      pl = [p[0] for p in sql("select name from `tabProject` where status = 'Completed' order by creation desc limit 20")]
      for p2 in pl:
        status[p2] = 'Completed'
    elif arg == 'Cancelled':
      pl = [p[0] for p in sql("select name from `tabProject` where status = 'Cancelled' order by creation desc limit 20")]
      for p3 in pl:
        status[p3] = 'Cancelled'
    else:
      #pl = [p[0] for p in sql("select name from `tabProject` order by creation desc limit 20")]
      pl1 = sql("select name, status from `tabProject` order by creation desc limit 20", as_dict=1)
      for p4 in pl1:
        status[p4['name']] = p4['status']
        pl.append(p4['name'])
    
    # milestones in the next 7 days for active projects
    ml = convert_to_lists(sql("select t1.milestone_date, t1.milestone, t1.parent from `tabProject Milestone` t1, tabProject t2 where t1.parent = t2.name and t2.status='Open' and DATEDIFF(t1.milestone_date, CURDATE()) BETWEEN 0 AND 7 ORDER BY t1.milestone_date ASC"))

    # percent of activity completed per project
    comp = {}
    n_tasks = {}
    
    for p in pl:
      t1 = sql('select count(*) from tabTicket where project=%s and docstatus!=2', p)[0][0]
      n_tasks[p] = t1 or 0
      if t1:
        t2 = sql('select count(*) from tabTicket where project=%s and docstatus!=2 and status="Closed"', p)[0][0]
        comp[p] = cint(flt(t2)*100/t1)
    
    return {'pl':pl, 'ml':ml, 'comp':comp, 'n_tasks':n_tasks, 'status':status}
    
  def get_resources(self):
    ret = {}

    # resource list
    rl = sql("select distinct allocated_to, assignee_email from tabTicket")

    # get open & closed tickets
    for r in rl:
      if r[0]:
        ret[r[1]] = {}
        ret[r[1]]['id'] = r[0]
        ret[r[1]]['Total'] = sql("select count(*) from tabTicket where allocated_to=%s and docstatus!=2", r[0])[0][0]
        ret[r[1]]['Closed'] = sql("select count(*) from tabTicket where allocated_to=%s and status='Closed' and docstatus!=2", r[0])[0][0]
        ret[r[1]]['percent'] = cint(flt(ret[r[1]]['Closed']) * 100 / ret[r[1]]['Total'])

    return ret

  # --------------------------------------------------------------
  # for Gantt Chart

  def get_init_data(self, arg=''):
    pl = [p[0] for p in sql('select name from tabProject where docstatus != 2')]
    rl = [p[0] for p in sql('select distinct allocated_to from tabTicket where docstatus != 2 and ifnull(allocated_to,"") != ""')]
    return {'pl':pl, 'rl':rl}

  def get_tasks(self, arg):
    start_date, end_date, project, resource = arg.split('~~~')

    cl = ''
    if project and project != 'All':
      cl = " and ifnull(project,'') = '%s'" % project

    if resource and resource != 'All':
      cl = " and ifnull(allocated_to,'') = '%s'" % resource

    tl = sql("""
      select subject, allocated_to, project, start_date, scheduled_date, priority, status, name
      from tabTicket 
      where 
        ((start_date between '%(st)s' and '%(end)s') or 
        (scheduled_date between '%(st)s' and '%(end)s') or 
        (start_date < '%(st)s' and scheduled_date > '%(end)s')) %(cond)s order by start_date limit 100""" % {'st': start_date, 'end': end_date, 'cond':cl})

    return convert_to_lists(tl)
  
  def declare_proj_completed(self, arg):
    chk = sql("select name from `tabTicket` where project=%s and status='Open'", arg)
    if chk:
      chk_lst = [x[0] for x in chk]
      msgprint("Task(s) "+','.join(chk_lst)+" has staus 'Open'. Please submit all tasks against this project before closing the project.")
      return cstr('false')
    else:
      sql("update `tabProject` set status = 'Completed' where name = %s", arg)
      return cstr('true')