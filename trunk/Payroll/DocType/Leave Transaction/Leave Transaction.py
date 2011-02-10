import datetime
class DocType:
  def __init__(self, doc, doclist):
    self.doc = doc
    self.doclist = doclist 
    
  def holiday_validation(self):
  #****************No. Of Holidays in Between**************************
    r = (getdate(self.doc.to_date)+datetime.timedelta(days=1)-getdate(self.doc.from_date)).days
    dateList = [getdate(self.doc.from_date)+datetime.timedelta(days=i) for i in range(r)]
    hol=([str(date) for date in dateList])
   
    #retrive all holiday date from child table data of holiday list
    ret_hd =convert_to_lists(sql("select h1.holiday_date from `tabHoliday List Detail` h1, `tabHoliday List` h2, `tabEmployee` e1 where e1.name = '%s' and h1.parent = h2.name and e1.holiday_list = h2.name"%self.doc.employee))
    temp = 0
    
    if ret_hd:
      #retrive all holiday date from child table data of holiday list
    
      for hd in ret_hd:  

        if hol.__contains__(hd[0]):
          
    	  temp = temp + 1   #count total number of holidays
        
    return temp
  #*******************************************************************

  def date_difference(self):
  #****************Getting Date Difference****************************
    str1 = str(self.doc.to_date)
    str2 = str(self.doc.from_date)
    y1, m1, d1 = (int(x) for x in str1.split('-'))
    y2, m2, d2 = (int(x) for x in str2.split('-'))
    date1 = datetime.date(y1, m1, d1)
    date2 = datetime.date(y2, m2, d2)
    dateDiff = date1 - date2
    dd = dateDiff.days
    days= dd + 1
    return days
  #********************************************************************

  def get_days(self):
  #********************************************************************
    
    days=self.date_difference()
    
    temp =self.holiday_validation()
    
    tl = days - temp
    self.doc.total_leave = tl
    if temp:
      msgprint("Total Days: %s \n Total in-between Holiday: %s \n So Total Leave Days: %s "%(cstr(days),cstr(temp),cstr(tl)))
    #set(self.doc, 'total_leave',tl) 
    return tl
  #********************************************************************  
  
# Getting Total Leave Days
  # **********************************************************************   
  def get_leave_days(self):
    if self.doc.from_date and self.doc.to_date:
      self.get_days()
      self.to_date_validation()      
    else:
      msgprint("Please select both from date and to date")
  #********************************************************************
  
# Getting Total Leave Days For LWP/Comp Off
  # **********************************************************************   
  def leave_days(self):
    if self.doc.from_date and self.doc.to_date:
      if (self.doc.leave_type == 'Leave Without Pay' or self.doc.leave_type == 'Compensatory Off'):
        self.get_days()
        self.to_date_validation()
  #********************************************************************  
  
# Validation For Total Leave
  # **********************************************************************   
  def validation_total_leave(self):
    prbal = self.get_prv_bal()
    if self.doc.leave_type != 'Leave Without Pay':
      if self.doc.leave_transaction_type == 'Deduction':
        if (flt(self.doc.total_leave) >= 0.0):
          if (flt(self.doc.total_leave) > prbal):
            msgprint("Total leave days greater than  previous balance")
            raise Exception
        else:
          msgprint("Invalid days")
          raise Exception
      else:
        if (flt(self.doc.total_leave) < 0.0):
          msgprint("Invalid days")
          raise Exception        
  #********************************************************************
      
# Getting Previous Year
  # **********************************************************************       
  def get_previous_year(self):
      yr = self.doc.fiscal_year
      yr1 = yr.split('-')
      y1=(yr1[0])
      y2 = int(y1)-1
      year = str(y2) + '-' + str(y1)
      return year
      
# Common Queries
  # **********************************************************************       
  def get_leave_query(self):
    query = ''
    query += 'SUM(CASE WHEN leave_transaction_type = "Allocation" THEN total_leave ELSE 0 END)-SUM(CASE WHEN leave_transaction_type = "Deduction" THEN total_leave ELSE 0 END)';
    return query      
  
  def get_balance_query(self):
    query1 = "select %s from `tabLeave Transaction` where employee = '%s' and leave_type = '%s' and fiscal_year = '%s' and docstatus = 1"
    return query1
  
  #***********************************************************************
        
# Getting Days Which Will Be Carry Forwarded
  # **********************************************************************       
  def get_carry_fwd_days(self):
    year=self.get_previous_year()
    query=self.get_leave_query()
    query1=self.get_balance_query()
    carry = sql(query1 %(query,self.doc.employee,self.doc.leave_type,year))  
    crbal = carry[0][0] or 0
    return flt(crbal)
    
# Getting Previous Leave Balance
  # **********************************************************************      
  def get_prv_bal(self):
  
    if (self.doc.employee == ''):
      msgprint("Please select fiscal year & employee")
      raise Exception
    else:
      prbal = self.get_balance()
      return flt(prbal)
    
# Getting Previous Leave Balance
  # **********************************************************************      
  def get_balance(self):
      query=self.get_leave_query()
      query1=self.get_balance_query()
      prbal = 0.0
      if (self.doc.leave_type == ''):
        msgprint("Please select leave type")
      else:      
        actual = sql(query1 %(query,self.doc.employee,self.doc.leave_type,self.doc.fiscal_year))
        prbal = actual[0][0]
      return flt(prbal)
  #*********************************************************************
  
# Validation For Half Day
  # **********************************************************************  
  def half_day_validation(self):
    if self.doc.half_day == 1:
      if flt(self.doc.total_leave) <> 0.5:
        msgprint("For half days,total leave should be equal to 0.5")
        raise Exception
  #********************************************************************* 
  
# Duplicate Date Validation
  # ********************************************************************** 
  def duplicate_date_validation(self):
    dt1 = sql("select name from `tabLeave Transaction` where employee = '%s' and leave_transaction_type = 'Deduction' and (('%s' between from_date and to_date) or ('%s' between from_date and to_date)) and docstatus = 1" %(self.doc.employee,self.doc.from_date,self.doc.to_date))
    if dt1:
      msgprint("Record Exists")
      raise Exception  
  #**********************************************************************  
    
# Joining Date Validation
  # **********************************************************************            
  def joining_date_validation(self):
    #******** Validate (from_date/to_date) v/s joining date **********
    join = sql("select date_of_joining from `tabEmployee` where name = '%s'" %self.doc.employee)
    join_date = join[0][0]
    if self.doc.from_date:
      if getdate(self.doc.from_date) <= join_date:
        return 1
    if self.doc.to_date:
      if getdate(self.doc.to_date) <= join_date:
        return 1
    #*******************************************************************

# Date Range Validation
  # **********************************************************************    
  def date_range_validation(self):
  #******************************************************************
    if self.doc.leave_transaction_type == 'Deduction':
      r=(getdate(self.doc.to_date)+datetime.timedelta(days=1)-getdate(self.doc.from_date)).days
      dateList = [getdate(self.doc.from_date)+datetime.timedelta(days=i) for i in range(r)]
    
      ddt=([str(date) for date in dateList])
      dt3 = convert_to_lists(sql("select from_date,to_date from `tabLeave Transaction` where employee = '%s' and fiscal_year = '%s' and leave_transaction_type = 'Deduction' and docstatus = 1" %(self.doc.employee,self.doc.fiscal_year)))
      for dt in dt3:
        if ddt.__contains__(dt[0]):
          msgprint("Record exists in this date range")
          raise Exception
  #********************************************************************         
    
# Validation For To Date
  # **********************************************************************
  def to_date_validation(self):
    if (getdate(self.doc.to_date) < getdate(self.doc.from_date)):
      msgprint("To date cannot be before from date")
      raise Exception        
#***********************************************************************  

# Updating Leave Balance
  # **********************************************************************
  def update_balance(self):
    if self.doc.leave_type != 'Leave Without Pay':
      if self.doc.leave_type != 'Compensatory Off': 
        if self.doc.leave_transaction_type == 'Deduction':
          prbal = self.get_prv_bal()
          set(self.doc, 'pre_balance',prbal)
#***********************************************************************
 
# Updating Compensatory Off Details
  # **********************************************************************
  def update_compoff_details(self):
    if self.doc.leave_type == 'Compensatory Off':
      set(self.doc, 'leave_transaction_type','Deduction')
      set(self.doc, 'deduction_type','Leave')      
      set(self.doc, 'total_leave',0.0)
#***********************************************************************

# Updating LWP Details
  # **********************************************************************
  def update_lwp_details(self):
    if self.doc.leave_type == 'Leave Without Pay':
      set(self.doc, 'leave_transaction_type','Deduction')
      set(self.doc, 'deduction_type','Leave')
      set(self.doc, 'pre_balance',0.0)
#***********************************************************************

# Max Days Allowed
  # **********************************************************************
  def max_allowed(self):
    max_all = sql("select max_days_allowed from `tabLeave Type` where leave_type_name = '%s'" %self.doc.leave_type)
    if max_all:
      max_allowed1 = max_all[0][0]
      if self.doc.leave_type == 'Sick Leave' or self.doc.leave_type == 'Casual Leave':
        if self.doc.leave_transaction_type == 'Deduction':
          if self.doc.status == 'Unsaved':
            msgprint(('Max allowed '+self.doc.leave_type+' is' + ' %d') %int(max_allowed1))
#***********************************************************************
  
# Validation For Expired Days
  # **********************************************************************
  def validate_expired_days(self):
    if self.doc.leave_transaction_type == 'Expired':
      ex = sql("select name from `tabLeave Transaction` where fiscal_year = '%s' and employee = '%s' and leave_type = '%s' and leave_transaction_type = 'Allocation'" %(self.doc.fiscal_year,self.doc.employee,self.doc.leave_type))
      if not(ex):
        msgprint(("Allocation for employee: " + '%s' + " not done") %self.doc.employee)
        raise Exception
      
  #***********************************************************************  
  
  def duplicate_allocation(self):
    if (self.doc.leave_transaction_type == 'Allocation' and self.doc.allocation_type != 'Carry Forward'):
      dt1 = sql("select name from `tabLeave Transaction` where employee = '%s' and leave_transaction_type = 'Allocation' and ((('%s' between from_date and to_date) or ('%s' between from_date and to_date)) or ((from_date between '%s' and '%s') or (to_date between '%s' and '%s'))) and docstatus = 1 and allocation_type != 'Carry Forward' and leave_type = '%s'  " %(self.doc.employee,self.doc.from_date,self.doc.to_date,self.doc.from_date,self.doc.to_date,self.doc.from_date,self.doc.to_date, self.doc.leave_type))
      if dt1:
        msgprint("Allocation already done. Please check Leave Transaction '%s'"%cstr(dt1[0][0]))
        raise Exception
  
  
# VALIDATE
# **********************************************************************  
  def validate(self):
#*********************************************************************************  
    self.duplicate_allocation()
    if self.doc.status == 'Unsaved':
      
      if (self.doc.leave_type != 'Leave Without Pay' and self.doc.leave_type != 'Compensatory Off') and self.doc.leave_transaction_type == 'Deduction':
        e = sql("select name from `tabLeave Transaction` where fiscal_year = '%s' and employee = '%s' and leave_type = '%s' and leave_transaction_type = 'Allocation'" %(self.doc.fiscal_year,self.doc.employee,self.doc.leave_type))
        if not(e):
          msgprint(("Allocation for employee: " + '%s' + " not done") %self.doc.employee)
          raise Exception
#*********************************************************************************
    if (self.doc.to_date == ''):
      set(self.doc, 'to_date',self.doc.from_date)
    if (self.doc.half_day == 1):
      set(self.doc, 'to_date',self.doc.from_date)
    self.half_day_validation()
    self.to_date_validation()
    self.validation_total_leave()
    self.validate_expired_days()
    #self.max_allowed()
    self.duplicate_date_validation()
    self.date_range_validation()

    days=self.date_difference()
    if flt(self.doc.total_leave)>flt(days):
      msgprint("To Date & From Date Difference : '%s' \n Total Leave Days : '%s' \n Total Leave days cannot be greater than date difference."%(days,self.doc.total_leave))
      raise Exception
#*********************************************************************************    
  
  def cal_tot_leave(self):
    if(self.doc.from_date and self.doc.to_date and flt(self.doc.total_leave) == 0.00 and self.doc.leave_transaction_type == "Deduction"):
      
      self.get_leave_days()
  
  
# ON UPDATE
# **********************************************************************
  def on_update(self):
    
    set(self.doc, 'status', 'Draft')
    self.cal_tot_leave()
    self.update_compoff_details()
    self.update_lwp_details()
    self.update_balance()

    obj = get_obj('Feed Control', 'Feed Control')
  
    if not self.doc.creation:
      obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      obj.make_feed('modified', self.doc.doctype, self.doc.name)

    
# ON SUBMIT
# **********************************************************************
  def on_submit(self):
    set(self.doc, 'status', 'Submitted')

    obj = get_obj('Feed Control', 'Feed Control')
    obj.make_feed('submitted', self.doc.doctype, self.doc.name)
    
# ON CANCEL
# **********************************************************************
  def on_cancel(self):
    msgprint('Leave Transaction: '+self.doc.name+' has been cancelled')
    set(self.doc,'status','Cancelled')

    obj = get_obj('Feed Control', 'Feed Control')
    obj.make_feed('cancelled', self.doc.doctype, self.doc.name)