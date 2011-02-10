class DocType:
  #init function
  def __init__(self,doc,doclist=[]):
    self.doc = doc
    self.doclist = doclist
    self.ear_ded_lst = [] #earning & deduction list eg. ['basic', 'hra', 'pf' , 'esic']
    self.expressions = [] #list of expression eg. ['basic=1000','hra = basic*0.1']
    self.rule_name = [] #list of rule name
    self.rule_exp_lst = []
    self.cap_ed_lst=[] #original name of earning & deduction type
  
  #---------------------------------------------------------
  #autoname function
  
  def autoname(self):
    self.doc.name = make_autoname(self.doc.employee + '/.SST' + '/.#####')
  
  def set_ss_values(self):
    basic_info = sql("select bank_name, bank_ac_no, esic_card_no, pf_number from `tabEmployee` where name ='%s'" %self.doc.employee) 

    return {'bank_name':basic_info[0][0],'bank_ac_no':basic_info[0][1],'esic_no':basic_info[0][2],'pf_no':basic_info[0][3]}
   
  #--------------------------------------------------------- 
  #called from make_earning_deduction_table to identify rules & calculate values 
  
  def apply_rule(self):
    #get list of rule_name & expression whose condition hold is true
    str = ''
    exp = ''
    
    rule_list = sql("select rule_name, expression from `tabPayroll Rule` where docstatus !=2 order by rule_priority asc")
        
    for rl in rule_list:
      payroll_obj=get_obj("Payroll Rule",rl[0],with_children=1)   
      cond_hold = payroll_obj.evalute_rule(self)
      
      if cond_hold =='Yes':

        self.rule_name.append(rl[0]) 
        self.expressions.append(rl[1].lower())
        self.rule_exp_lst.append("<b>Rule - " +rl[0] + "</b> : " +rl[1])     
    
    
    
  #---------------------------------------------------------
  #called from apply_rule to execute expressions of rules whose condition hold is true
  def apply_action(self):
     
    for e in self.ear_ded_lst:
      locals()[e.lower().replace(' ','_')] = 0.0  #set all locals value to 0.0
         
    
    for e in self.expressions:
      exec e in locals() #execute the expression from self.expression list & set values in locals
      
    #=============================================================#
    self.doc.expression_list = cstr(self.expressions)
    self.doc.earnded_list = cstr(self.ear_ded_lst)
    
    
    #=============================================================#
    tot1 = 0
    
    for d in getlist(self.doclist, 'earning_details'):  #eg. ['Basic','HRA', 'Dearness Allowance']
      for r in self.cap_ed_lst:
        if d.e_type == r:
          val =locals()[r.lower().replace(' ','_')] 
          d.e_value = val
          d.modified_value = val
          tot1 +=val
          d.save() 
          
                   
     
    
    #===================================================================#
    tot2 = 0
    for d in getlist(self.doclist, 'deduction_details'):  #eg. ['Employees state insurance', 'Professional Fund']
      for r in self.cap_ed_lst:
        if d.d_type == r:
          val = locals()[r.lower().replace(' ','_')]
          d.d_value  =  val
          d.d_modified_amt =val
          tot2 += val
          d.save()  
          
  
    self.doc.total_earning = round(flt(tot1))
    self.doc.total_deduction = round(flt(tot2))
    self.doc.total = round(flt(tot1-tot2))
  
  
  def re_apply_action(self):
  
    for e in getlist(self.doclist, 'earning_details'):
      self.ear_ded_lst.append(cstr(e.e_type).lower().replace(' ','_'))
      self.cap_ed_lst.append(cstr(e.e_type)) 
      
    for d in getlist(self.doclist, 'deduction_details'):
      self.ear_ded_lst.append(cstr(d.d_type).lower().replace(' ','_')) 
      self.cap_ed_lst.append(cstr(d.d_type))
      
    
    for e in self.ear_ded_lst:
      locals()[e] = 0.0  #set all locals value to 0.0
            
    #=============================================================#
    
    for e in getlist(self.doclist, 'earning_details'):
      if e.modified_value :
        r = e.e_type
        locals()[r.lower().replace(' ','_')] = flt(e.modified_value)
      
      
    for d in getlist(self.doclist, 'deduction_details'):
      if d.d_modified_amt:
        r = d.d_type
        locals()[r.lower().replace(' ','_')] = flt(d.d_modified_amt)
 
    
    
    for e in self.expressions:
      exec e in locals() #execute the expression from self.expression list & set values in locals
      
    #=============================================================#
    self.doc.expression_list = cstr(self.expressions)
    self.doc.earnded_list = cstr(self.ear_ded_lst)
    
    
    #=============================================================#
    tot1 = 0

    for d in getlist(self.doclist, 'earning_details'):  #eg. ['Basic','HRA', 'Dearness Allowance']
      for r in self.cap_ed_lst:
       
        if d.e_type == r:
        
          val =locals()[r.lower().replace(' ','_')] 
          if flt(d.e_value) == flt(d.modified_value):
            d.e_value = val
            d.modified_value = val
          tot1 +=val
          d.save() 
       
     
    
    #===================================================================#
    tot2 = 0
    for d in getlist(self.doclist, 'deduction_details'):  #eg. ['Employees state insurance', 'Professional Fund']
      for r in self.cap_ed_lst:
        if d.d_type == r:
 
          val = locals()[r.lower().replace(' ','_')]
          if flt(d.d_value) == flt(d.d_modified_amt):
            d.d_value  =  val
            d.d_modified_amt =val
          tot2 += val
          d.save()  
          
  
    set(self.doc,'total_earning',round(flt(tot1)))
    set(self.doc,'total_deduction', round(flt(tot2)))
    set(self.doc,'total',round(flt(tot1-tot2)))
    
  #----------------------------------------------------------------------
  #make_table function add earning & deduction types to table called from make_earning_deduction_table
  def make_table(self, doct_name, tab_fname, tab_name):
   
    list1 = sql("select name from `tab%s` where docstatus != 2"%doct_name)
    list1 = [x[0] for x in list1]

    for li in list1:
      child = addchild(self.doc, tab_fname, tab_name, 0, self.doclist)
      if(tab_fname == 'earning_details'):
        child.e_type = cstr(li)
      elif(tab_fname == 'deduction_details'):
        child.d_type = cstr(li)
      child.save()
     
      self.cap_ed_lst.append(cstr(li)) #eg. self.cap_ed_lst = ['Basic','HRA']
      self.ear_ded_lst.append(cstr(li).lower().replace(' ','_'))
	
  def reapply_rules(self):
 
    self.apply_rule()
    self.re_apply_action()

  
  #---------------------------------------------------------   
  # add earning & deduction types to table 
  def make_earning_deduction_table(self):
    
    #ret = sql("select name from `tabEarning Detail` where parent = '%s'" %self.doc.name)
    self.doc.clear_table(self.doclist, 'earning_details',1)
    self.doc.clear_table(self.doclist, 'deduction_details',1)
           
    #Earning List
    self.make_table('Earning Type','earning_details','Earning Detail')
    
    #Deduction List
    self.make_table('Deduction Type','deduction_details', 'Deduction Detail')
    self.apply_rule()
    self.apply_action()
    return self.rule_exp_lst
    
  #---------------------------------------------------------
  #get basic values of employee from employee table 
  def set_values(self):
    
    self.doc.clear_table(self.doclist, 'earning_details',1)
    self.doc.clear_table(self.doclist, 'deduction_details',1)
    set(self.doc,'log_info' ,'')
    set(self.doc,'total',0)
    ret = sql("select employee_name, branch, designation, department, grade from `tabEmployee` where name = '%s'" %self.doc.employee) 
    if ret:
      set(self.doc,'employee_name',ret[0][0])
      set(self.doc,'branch',ret[0][1])
      set(self.doc,'designation',ret[0][2])
      set(self.doc,'department',ret[0][3])
      set(self.doc,'grade',ret[0][4])
      set(self.doc,'backup_employee',self.doc.employee)
    
  #---------------------------------------------------
  def calculate_total(self):
    tot = 0.0
    tot1 = 0.0
    tot2 = 0.0
    
    
    for e in getlist(self.doclist, 'earning_details'):
      msgprint(e.modified_value)
      tot1 += flt(e.modified_value)
      
    set(self.doc,'total_earning', round(flt(tot1)))
        
        
    for d in getlist(self.doclist, 'deduction_details'):
      tot2 += flt(d.d_modified_amt)
    
    set(self.doc,'total_deduction',round(flt(tot2)))
       
            
    tot = tot1-tot2
    set(self.doc,'total',flt(tot))

    
  def check_current(self):
    
    ret = sql("select name from `tabSalary Structure` where is_active = 'Yes' and employee = '%s' and name!='%s'" %(self.doc.employee,self.doc.name)) 
    ret = ret and ret[0][0] or ''
    if ret!='' and self.doc.is_active=='Yes':
      msgprint("'%s' Salary Structure is active for employee '%s'. Please make its status Is Active No to create current active salary structure."%(cstr(ret), self.doc.employee))
      raise Exception
  

  def validate(self):   
    self.check_current()
    
  def on_update(self):
    ret_earn, ret_ded ='',''
    for e in getlist(self.doclist, 'earning_details'):
      ret_earn = e.e_type 
    for d in getlist(self.doclist, 'deduction_details'): 
      ret_ded = d.d_type
      
    if not ret_earn and not ret_ded:
      #Earning List
      self.make_table('Earning Type','earning_details','Earning Detail')
    
      #Deduction List
      self.make_table('Deduction Type','deduction_details', 'Deduction Detail')
      self.apply_rule()
      self.apply_action()
      msg1 = ''
      for i in self.rule_exp_lst:
        msg1 +='<br>' +'<pre>' + i +'</pre>' 
      set(self.doc,'log_info',msg1)

    # make feed
    obj = get_obj('Feed Control', 'Feed Control')
    
    if not self.doc.creation:
      obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      obj.make_feed('modified', self.doc.doctype, self.doc.name)