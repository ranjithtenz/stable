class DocType:
  def __init__(self,d,dl):
    self.doc, self.doclist = d, dl
    
#posting response in table
  def post_response(self,arg):
    arg = eval(arg)
    res = Document('Ticket Response Detail')
    res.response =  arg['response']
    res.response_by = arg['response_by']
    res.response_date = nowdate();
    res.parent = arg['parent']
    res.parenttype = 'Ticket'
    res.parentfield = 'ticket_response_details'
    res.save(1)

  def get_status(self):
    # all
    all = sql('select count(*) from tabTicket where docstatus!=2')[0][0]

    # open
    open = sql('select count(*) from tabTicket where docstatus!=2 and status="Open"')[0][0]
    review = sql('select count(*) from tabTicket where docstatus!=2 and status="Pending Review"')[0][0]
    if not open:
      return {'open':0}

    # urgent
    urgent = sql('select count(*) from tabTicket where docstatus!=2 and status="Open" and priority="Urgent"')[0][0]

    # urgent
    high = sql('select count(*) from tabTicket where docstatus!=2 and status="Open" and priority="High"')[0][0]

    # urgent
    medium = sql('select count(*) from tabTicket where docstatus!=2 and status="Open" and priority="Medium"')[0][0]

    return {'open':cint(flt(open)*100/all),'review':cint(flt(review)*100/open), 'urgent':cint(flt(urgent)*100/open), 'high':cint(flt(high)*100/open), 'medium':cint(flt(medium)*100/open)}
    
  def get_activity(self,days):
    import datetime
    from datetime import timedelta
    
    ret = {}
    for d in range(eval(days)):
      cd = getdate(nowdate()) - timedelta(d)
      
      if(d == 0):
        cd_nm = 'Today'
      elif d == 1:
        cd_nm = 'Yesterday'
      else:
        cd_nm = formatdate(str(cd))

      ret[6-d] = {
        'Day' : cd_nm,
        'Open' : (sql("select count(name) from tabTicket where opening_date=%s",cd)[0][0] or 0),
        'Closed' : (sql("select count(name) from tabTicket where status='Closed' and closing_date=%s",cd)[0][0] or 0)
      }
    return ret

  # for Help - return the domain for helpdesk
  # -------------------------------------------------------------
  def get_domain(self):
    if session['data'].get('login_from'):
      return session['data'].get('login_from')
    else:
      return 'https://www.erpnext.com'