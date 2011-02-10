class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    
    # Notification objects    
    self.badge_obj = get_obj('Badge Settings','Badge Settings','','',1)
  
  #autoname function
  def autoname(self):
    self.doc.name = make_autoname(self.doc.naming_series+'.#####')
  
  #get employee name based on employee id selected 
  def get_emp_name(self):
    emp_nm = sql("select employee_name from `tabEmployee` where name=%s", self.doc.employee)
    ret = { 'employee_name' : emp_nm and emp_nm[0][0] or ''}
    set(self.doc, 'employee_name', emp_nm and emp_nm[0][0] or '')
    return str(ret)
  
  #validation for duplicate record
  def validate_duplicate_record(self):   
    res = sql("select name from `tabAttendance` where employee = '%s' and att_date = '%s' and not name = '%s'"%(self.doc.employee,self.doc.att_date, self.doc.name))
    if res:
      msgprint("Employee's attendance already marked.")
      raise Exception
      
  #validation - leave_type is mandatory for status absent/ half day else not required to entered.
  def validate_status(self):
    if self.doc.status == 'Present' and self.doc.leave_type:
      msgprint("You can not enter leave type for attendance status 'Present'")
      raise Exception

    elif (self.doc.status == 'Absent' or self.doc.status == 'Half Day') and not self.doc.leave_type:
      msgprint("Please enter leave type for attendance status 'Absent'")
      raise Exception
  
  #check for already record present in leave transaction for same date
  def check_leave_record(self):
    if self.doc.status == 'Present':
      chk = sql("select name from `tabLeave Transaction` where employee=%s and (from_date <= %s and to_date >= %s) and status = 'Submitted' and leave_transaction_type = 'Deduction' and docstatus!=2", (self.doc.employee, self.doc.att_date, self.doc.att_date))
      if chk:
        msgprint("Leave Application created for employee "+self.doc.employee+" whom you are trying to mark as 'Present' ")
        raise Exception
  
  #For absent/ half day record - check for leave balances of the employees 
  def validate_leave_type(self):
    if not self.doc.status =='Present' and self.doc.leave_type not in ('Leave Without Pay','Compensatory Off'):
      #check for leave allocated to employee from leave transaction
      ret = sql("select name from `tabLeave Transaction` where employee = '%s' and leave_type = '%s' and leave_transaction_type = 'Allocation' and fiscal_year = '%s'"%(self.doc.employee,self.doc.leave_type,self.doc.fiscal_year))   
      
      #if leave allocation is present then calculate leave balance i.e. sum(allocation) - sum(deduction) 
      if ret:
        q1 = 'SUM(CASE WHEN leave_transaction_type = "Allocation" THEN total_leave ELSE 0 END)-SUM(CASE WHEN leave_transaction_type = "Deduction" THEN total_leave ELSE 0 END)'
        q2 = "select %s from `tabLeave Transaction` where employee = '%s' and leave_type = '%s' and fiscal_year = '%s' and docstatus = 1"
        
        res = sql(q2%(q1,self.doc.employee,self.doc.leave_type,self.doc.fiscal_year))
       
        if res:
          if self.doc.status == 'Absent' and flt(res[0][0]) < 1:
            msgprint("%s balances are insufficient to cover a day absence, please select other leave type."%self.doc.leave_type)
            raise Exception
          if self.doc.status == 'Half Day' and flt(res[0][0]) < 0.5:
            msgprint("%s balances are insufficient to cover a half day absence, please select other leave type."%self.doc.leave_type)
            raise Exception

      else:
        msgprint("Leave Allocation for employee %s not done.\n You can allocate leaves from HR -> Leave Transaction OR HR -> Leave Control Panel."%self.doc.employee)
        raise Exception
  
  def validate_fiscal_year(self):
    fy=sql("select year_start_date from `tabFiscal Year` where name='%s'"% self.doc.fiscal_year)
    ysd=fy and fy[0][0] or ""
    yed=add_days(str(ysd),365)
    if str(self.doc.att_date) < str(ysd) or str(self.doc.att_date) > str(yed):
      msgprint("'%s' Not Within The Fiscal Year selected"%(att_date))
      raise Exception
  
  def validate_att_date(self):
    import datetime
    if getdate(self.doc.att_date)>getdate(datetime.datetime.now().date().strftime('%Y-%m-%d')):
      msgprint("Attendance can not be marked for future dates")
      raise Exception
  
  # validate...
  def validate(self):
    self.validate_fiscal_year()
    self.validate_att_date()
    #self.validate_leave_type()
    self.validate_duplicate_record()
    #self.validate_status()
    self.check_leave_record()
    
  def on_update(self):
    #self.validate()
    if not self.doc.employee_name:
      x=self.get_emp_name()
      
    # add badge points
    if sql("select name from `tab%s` where creation = modified and name='%s'" % (self.doc.doctype, self.doc.name)):
        self.badge_obj.add_badge_points(self.doc.doctype,0)