class DocType:
  def __init__(self, doc, doclist):
    self.doc = doc
    self.doclist = doclist   
  
# Get Employees
  # ********************************************************************** 
  def get_employee(self):    

    lst1 = [[self.doc.employee_type,"employment_type"],[self.doc.branch,"branch"],[self.doc.designation,"designation"],[self.doc.department, "department"],[self.doc.grade,"grade"]]
    
    condition = "where "
    flag = 0
    for l in lst1:
      
      if(l[0]):
        if flag == 0:
          condition += l[1] + "= '" + l[0] +"'"
        else:
          condition += " and " + l[1]+ "= '" +l[0] +"'"
        flag = 1

    emp_query = "select name from `tabEmployee` "
    if flag == 1:
      emp_query += condition 
    e = sql(emp_query)
    
    return e

# Query
  # **********************************************************************          
  def get_leave_query(self):
    query = ''
    query += 'SUM(CASE WHEN leave_transaction_type = "Allocation" THEN total_leave ELSE 0 END)-SUM(CASE WHEN leave_transaction_type = "Deduction" THEN total_leave ELSE 0 END)';
    return query

# Allocation
  # ********************************************************************** 
  def add_leave_transaction(self):
    if self.doc.allocation_type != 'Carry Forward':
      if self.doc.to_date:
        e = self.get_employee()
        
        query = self.get_leave_query()
        
        for i in e:
          actual = sql("select %s from `tabLeave Transaction` where employee = '%s' and leave_type = '%s' and fiscal_year = '%s' and docstatus = 1" %(query,i[0],self.doc.leave_type,self.doc.fiscal_year))      
          lt = Document('Leave Transaction')
          lt.fiscal_year = self.doc.fiscal_year
          lt.employee = i[0]
          lt.leave_type = self.doc.leave_type
          lt.pre_balance= actual[0][0]
          lt.leave_transaction_type = self.doc.leave_transaction_type
          lt.allocation_type = self.doc.allocation_type
          lt.from_date = self.doc.from_date
          lt.to_date = self.doc.to_date
          lt.total_leave = self.doc.no_of_days
          lt.status = 'Submitted'
          lt.date = self.doc.date
          lt.save(1)
          sql("update `tabLeave Transaction` set docstatus = 1 where name = '%s'" %lt.name)
        msgprint("Allocation Successful")
      else:
        msgprint("Please select to date")
    else:
      self.carry_fwd_days()
  
# Validation For To Date
  # **********************************************************************
  def to_date_validation(self):
    if (getdate(self.doc.to_date) < getdate(self.doc.from_date)):
      return 1
  #***********************************************************************
    
# Getting Previous Year
  # **********************************************************************
  def get_previous_year(self):
      yr = self.doc.fiscal_year
      yr1 = yr.split('-')
      y1=(yr1[0])
      y2 = int(y1)-1
      year = str(y2) + '-' + str(y1)
      return year
  # **********************************************************************
  
# Getting Days Which Will Be Carry Forwarded
  # **********************************************************************       
  def carry_fwd_days(self):
    year=self.get_previous_year()
    query=self.get_leave_query()
    if self.doc.to_date:
      e = self.get_employee()
      for i in e:
        carry = sql("select %s from `tabLeave Transaction` where employee = '%s' and leave_type = '%s' and fiscal_year = '%s' and docstatus = 1" %(query,i[0],self.doc.leave_type,year))[0][0]
        if carry:
          if(flt(carry[0][0])>flt(self.doc.no_of_days)):
            crbal = flt(self.doc.no_of_days)
          else:
            crbal = flt(carry[0][0])
          lt = Document('Leave Transaction')
          lt.fiscal_year = self.doc.fiscal_year
          lt.employee = i[0]
          lt.leave_type = self.doc.leave_type
          lt.pre_balance= crbal
          lt.leave_transaction_type = self.doc.leave_transaction_type
          lt.allocation_type = self.doc.allocation_type
          lt.from_date = self.doc.from_date
          lt.to_date = self.doc.to_date
          lt.total_leave = crbal
          lt.status = 'Submitted'
          lt.date = self.doc.date
          lt.save(1)
          sql("update `tabLeave Transaction` set docstatus = 1 where name = '%s'" %lt.name)
        
        msgprint("Carry Forwarded")
    else:
      msgprint("Please select to date")