class DocType:
  def __init__(self, doc, doclist):
    self.doc = doc
    self.doclist = doclist   
  
  # Get Employees
  # ********************************************************************** 
  def get_employee(self):    

    e1 = self.emp_fr_memp()  #get employee list from employee where employee is active
    e2 = self.emp_fr_salstr(e1)  #get employee list from salary structure whose salary structure is created and is active 
    e3 = self.emp_fr_salslip(e2)  #get employee list from salary slip whose salary slip not yet created for this month and year
    return e3

  # ********************************************************************** 
  def emp_fr_memp(self):
    lst1 = [[self.doc.employee_type,"employment_type"],[self.doc.branch,"branch"],[self.doc.designation,"designation"],[self.doc.department, "department"],[self.doc.grade,"grade"]]
    
    condition = ""
    flag = 0
    for l in lst1:
      
      if(l[0]):
        if flag == 0:
          condition += l[1] + "= '" + l[0] +"'"
        else:
          condition += " and " + l[1]+ "= '" +l[0] +"'"
        flag = 1

    emp_query = "select name from `tabEmployee` where status = 'Active' and "
    if flag == 1:
      emp_query += condition
            
    e = sql(emp_query)
    return e

  # ********************************************************************** 
  def emp_fr_salstr(self,e1):
    lst = []
    for r in e1:
      lst.append(r[0])
    
    
    e_lst = "%s"%lst
    e_lst=e_lst.replace("[","(")
    e_lst=e_lst.replace("]",")")
    cond = ''

    if e1:
      cond = " and employee in %s"%e_lst
    
    el=sql("select employee from `tabSalary Structure` where is_active = 'Yes'"+cond)
    return el

  # ********************************************************************** 
  def emp_fr_salslip(self,e2):
    e3 = []
    for i in e2:
      ret = sql("select name from `tabSalary Slip` where month = '%s' and year = '%s' and employee = '%s' and docstatus !=2 "%(self.doc.month,self.doc.year,i[0]))

      if not ret:
        e3.append(i[0])
    return e3
    
  # ********************************************************************** 
  def process_payroll(self):
    
    sal_slip_str = ''
    if self.doc.month and self.doc.fiscal_year and self.doc.year:
      
      e = self.get_employee()

      if e:
        self.doc.emp_lst=e
        sal_slip_str += 'Sucessfully created following salary slips:'
      for i in e:
      	ss = Document('Salary Slip')
        ss.fiscal_year = self.doc.fiscal_year
        ss.employee = i
        ss.month = self.doc.month
        ss.year= self.doc.year
        ss.arrear_amount = self.doc.arrear_amount
              
        ss.email_check = self.doc.email_check
        ss.save(1)
        salary_obj=get_obj("Salary Slip",ss.name,with_children=1)   
        salary_obj.process_payroll_all()
        sal_slip_str += "<br/>"+ss.name 
        
    else:
    
      msgprint("For Process Payroll Fiscal Year, Month, Year fields are mandatory.")
    if not sal_slip_str: 
     
      sal_slip_str = "No record found."
    return cstr(sal_slip_str)

  # ********************************************************************** 
  def submit_sal_slip(self):
  
    sal_slip_str = ''
    r = sql("select name from `tabSalary Slip` where month='%s' and year = '%s' and fiscal_year = '%s' and docstatus = 0"%(self.doc.month,self.doc.year,self.doc.fiscal_year))

  
    ret = sql("update `tabSalary Slip` set docstatus = 1 where month='%s' and year = '%s' and fiscal_year = '%s' and docstatus = 0"%(self.doc.month,self.doc.year,self.doc.fiscal_year))
    if r:
      sal_slip_str += 'Sucessfully updated following salary slips:'
    for i in r:
      
      salary_obj=get_obj("Salary Slip",i[0],with_children=1)   
      salary_obj.on_submit()
      sal_slip_str += "<br/>"+cstr(i[0]) 
    if not sal_slip_str: 
     
      sal_slip_str = "No record found."
    return cstr(sal_slip_str)
  
  # ********************************************************************** 
  #get default bank account,default salary acount from company.
  def get_acct_dtl(self):
    res = sql("select default_bank_account,default_salary_acount from `tabCompany` where name = '%s'"%get_defaults()['company'], as_dict=1)
    return res[0]