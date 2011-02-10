class DocType:
  def __init__(self,doc,doclist=[]):
    self.doc = doc
    self.doclist = doclist

  #========================================================================================================
  def autoname(self):
    ret = sql("select value from `tabSingles` where doctype = 'Manage Account' and field = 'emp_created_by'")
    if not ret:
      msgprint("To Save Employee, please go to Setup -->Global Defaults. Click on HR and select 'Employee Records to be created by'.")
      raise Exception 
    else:
      if ret[0][0]=='Naming Series':
        self.doc.name = make_autoname(self.doc.naming_series + '.####')
      elif ret[0][0]=='Employee Number':
        self.doc.name = make_autoname(self.doc.employee_number)
        
  #========================================================================================================
  def retirement_date(self):
    month_dict = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}
    get_month = cstr(self.doc.date_of_birth).split('-')
    
    import datetime
    ret = ''
    last_day={1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    if self.doc.date_of_birth:
      dob = getdate(self.doc.date_of_birth)
      doc1 = dob + datetime.timedelta(21915)
      month = cint(doc1.strftime("%m"))
      d = last_day[month]
      y = cint(doc1.strftime("%Y"))
      if month==2: 
        if (y % 4 == 0) or ((y % 400 == 0) and (y % 4 == 0)):
          d = 29
        else:
          d = 28
      if month < 10 :
        abc = datetime.date(y, month, d)
      elif month >= 10:
        abc = datetime.date(y, month, d)
        #abc = str(d) + "-" + str(month) + "-" + str(y)
      self.doc.date_of_retirement = abc.strftime('%Y-%m-%d')

      ret = {'date_of_retirement':abc.strftime('%Y-%m-%d'),'month_of_birth':cstr(month_dict[get_month[1]])}
    return str(ret)
    
  #========================================================================================================
  def set_values(self):
    
    ret= ''
    lst1 = []
    lst = []
    ret = convert_to_lists(sql("select distinct name, ctc,is_active FROM `tabSalary Structure` where employee = '%s'"%self.doc.name))
  
    return ret

  #========================================================================================================

  def emp_prof_exist(self):
    
    ret_emp_prof=sql("select name from `tabEmployee Profile` where employee='%s'"%self.doc.name)
    
    return ret_emp_prof and ret_emp_prof[0][0] or ''
  
  #========================================================================================================
  def sal_struct_exist(self):
    ret_sal_struct=sql("select name from `tabSalary Structure` where employee='%s' and is_active = 'Yes'"%self.doc.name)

    return ret_sal_struct and ret_sal_struct[0][0] or ''

  #========================================================================================================
  def validate(self):
    self.date_validate()
    self.email_validate()
    self.name_validate()
    self.left_status_validate()
  
  #-------------------------------------------------------------------------------------------------------
  def date_validate(self):  
    import datetime
    if self.doc.date_of_birth and self.doc.date_of_joining and (getdate(self.doc.date_of_birth) >= getdate(self.doc.date_of_joining)):
      msgprint('Date of Joining must be greater than Date of Birth')
      raise Exception

    elif self.doc.scheduled_confirmation_date and self.doc.date_of_joining and (getdate(self.doc.scheduled_confirmation_date) < getdate(self.doc.date_of_joining)):
      msgprint('Scheduled Confirmation Date must be greater than Date of Joining')
      raise Exception
    
    elif self.doc.final_confirmation_date and self.doc.date_of_joining and (getdate(self.doc.final_confirmation_date) < getdate(self.doc.date_of_joining)):
      msgprint('Final Confirmation Date must be greater than Date of Joining')
      raise Exception
    
    elif self.doc.date_of_retirement and self.doc.date_of_joining and (getdate(self.doc.date_of_retirement) <= getdate(self.doc.date_of_joining)):
      msgprint('Date Of Retirement must be greater than Date of Joining')
      raise Exception
    
    elif self.doc.relieving_date and self.doc.date_of_joining and (getdate(self.doc.relieving_date) <= getdate(self.doc.date_of_joining)):
      msgprint('Relieving Date must be greater than Date of Joining')
      raise Exception
    
    elif self.doc.contract_end_date and self.doc.date_of_joining and (getdate(self.doc.contract_end_date)<=getdate(self.doc.date_of_joining)):
      msgprint('Contract End Date must be greater than Date of Joining')
      raise Exception
      
  #-------------------------------------------------------------------------------------------------------
  def email_validate(self):
    if self.doc.company_email:
      if not validate_email_add(self.doc.company_email):
        msgprint("Please enter valid Company Email")
        raise Exception
 
  #-------------------------------------------------------------------------------------------------------
  def name_validate(self):
  
    ret = sql("select value from `tabSingles` where doctype = 'Manage Account' and field = 'emp_created_by'")

    if not ret:
      msgprint("To Save Employee, please go to Setup -->Global Defaults. Click on HR and select 'Employee Records to be created by'.")
      raise Exception 
    else:
      if ret[0][0]=='Naming Series' and not self.doc.naming_series:
        msgprint("Please select Naming Series.")
        raise Exception 
      elif ret[0][0]=='Employee Number' and not self.doc.employee_number:
        msgprint("Please enter Employee Number.")
        raise Exception 
        
  #-------------------------------------------------------------------------------------------------------  
  def left_status_validate(self):
    if self.doc.status == 'Left' and not self.doc.relieving_date:
      msgprint("Please enter relieving date.")
      raise Exception
    if self.doc.status == 'Left' and self.doc.relieving_date > now():
      msgprint("You cannot set employee's status as Left, since relieving date is future date.")
      raise Exception
    
  # on update
  #========================================================================================================
  def on_update(self):
    obj = get_obj('Feed Control', 'Feed Control')
  
    if not self.doc.creation:
      obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      obj.make_feed('modified', self.doc.doctype, self.doc.name)