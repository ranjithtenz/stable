class DocType:
  #init function
  def __init__(self,doc,doclist=[]):
    self.doc = doc
    self.doclist = doclist
    
  #=======================================================
  #autoname
  def autoname(self):
    self.doc.name = make_autoname('Sal Slip/' +self.doc.employee + '/.#####')  
  
  def validate(self):
    ret_exist = sql("select name from `tabSalary Slip` where month = '%s' and year = '%s' and docstatus = 1 and employee = '%s' and name !='%s'"%(self.doc.month,self.doc.year,self.doc.employee,self.doc.name))
    if ret_exist:
      msgprint("Salary Slip already created for '%s' month"%self.doc.month)
      self.doc.employee = ''
      raise Exception
      
    
  #=======================================================
  #when employee set basic values changeed like emp name, dept, branch etc. and also earning & deduction table values 
  def set_values(self):
    ret_sal_stru = sql("select name from `tabSalary Structure` where employee ='%s' and is_active = 'Yes' "%self.doc.employee)
    if not ret_sal_stru:
      msgprint("Please create Salary Structure for employee '%s'"%self.doc.employee)
      self.doc.employee = ''
    else:
      self.set_basic_values() #set basic values   
    self.leave_details()
    
    return ''
  
  def leave_details(self):
    import calendar
    self.doc.total_days_in_month= flt(calendar.monthrange(cint(self.doc.year) ,cint(self.doc.month))[1])  
    if self.doc.employee:    
      self.leave_values()      #set leave related values
   
      self.cal_payment_days()  #calculate payment days based on total days in month, leave without pay days 
  
  #-------------------------------------------------------
  def set_basic_values(self):
    basic_info = sql("select employee_name, branch, department, designation, grade, bank_name, bank_ac_no, esic_card_no, pf_number from `tabEmployee` where name ='%s'" %self.doc.employee)
    
    if basic_info:
      self.doc.employee_name =basic_info[0][0]
      self.doc.branch= basic_info[0][1]     
      self.doc.department =basic_info[0][2]
      self.doc.designation=basic_info[0][3]
      self.doc.grade=basic_info[0][4]
      self.doc.bank_name=basic_info[0][5]
      self.doc.bank_account_no=basic_info[0][6]
      self.doc.esic_no=basic_info[0][7]
      self.doc.pf_no=basic_info[0][8]
  
  
  #------------------------------------------------------
  def set_ed_tables(self):
  
    self.doc.clear_table(self.doclist, 'earning_details',1)
    self.doc.clear_table(self.doclist, 'deduction_details',1)

    ret = sql("Select name from `tabSalary Structure` where employee = '%s' and is_active = 'Yes'"%self.doc.employee)
    if ret:
      salstruct = get_obj('Salary Structure',ret[0][0],with_children = 1)
      
      for e in getlist(salstruct.doclist,'earning_details'):
        if (e.e_type != 'Earning Total'):
          ch1 = addchild(self.doc,'earning_details','SS Earning Detail',0, self.doclist)
          ch1.e_type = e.e_type
          if(e.depend_on_lwp == 1):
            ch1.e_amount = round(flt(e.modified_value)*(flt(self.doc.payment_days)/cint(self.doc.total_days_in_month)))
          else:
            ch1.e_amount = round(flt(e.modified_value))
          ch1.save()
          

      for d in getlist(salstruct.doclist,'deduction_details'):
        if (d.d_type != 'Deduction Total'):
          ch2 = addchild(self.doc,'deduction_details','SS Deduction Detail',0, self.doclist)
          ch2.d_type = d.d_type
          
          if (d.d_type =='Income Tax'):#add income tax 
            ret_tax = sql("select tax_per_month from `tabIT Checklist` where employee = '%s' and is_cheklist_active = 'Yes'" %self.doc.employee)
            if ret_tax:
              ch2.d_amount = flt(ret_tax[0][0])
          elif(d.depend_on_lwp == 1):
            ch2.d_amount = round(flt(d.d_modified_amt)*(flt(self.doc.payment_days)/cint(self.doc.total_days_in_month)))
          else:
            ch2.d_amount = round(flt(d.d_modified_amt))
          ch2.save()
      

  #=========================================================
  #Payroll Process Button click   
  def process_payroll(self):
    
    #self.leave_values()      #set leave related values
    if(self.doc.flag ==1):
      #self.cal_payment_days()  #calculate payment days based on total days in month, leave without pay days 
     
      self.set_ed_tables() 
      self.cal_gp_td_np()      #calculate gross pay, total deduction & net pay
      if(self.doc.email_check == 1):
        msgprint("Please submit salary slip to send mail")
        #self.send_mail_funct()
    else:
      msgprint("Please save salary slip before process payroll")
  #------------------------------------------------------
  def leave_values(self):
    
    lwp_sum = sql("select sum(total_leave) from `tabLeave Transaction` where leave_type = 'Leave Without Pay' and docstatus = 1 and employee = '%s' and from_date like '%%-%s-%%' and to_date like '%%-%s-%%'"%(self.doc.employee,cstr(self.doc.month),cstr(self.doc.month)))
    self.doc.leave_without_pay = flt(lwp_sum[0][0]) or 0.00

    
    #import calendar
    
    #self.doc.total_days_in_month= flt(calendar.monthrange(cint(self.doc.year) ,cint(self.doc.month))[1])
  
 
  #------------------------------------------------------
  #calculate payment days based on total days in month, leave without pay days 
  def cal_payment_days(self): 
    self.doc.payment_days = cint(self.doc.total_days_in_month) - flt(self.doc.leave_without_pay)
  
  #-----------------------------------------------------  
  #calculate gross pay, total deduction & net pay  
  def cal_gp_td_np(self):
    
    sum_e = 0.0
    sum_d = 0.0
    for e in getlist(self.doclist,'earning_details'):
      sum_e += flt(e.e_amount) or 0
    
    for d in getlist(self.doclist,'deduction_details'):
      sum_d +=flt(d.d_amount) or 0
    
    self.doc.gross_pay = round(flt(sum_e))
    self.doc.total_deduction = round(flt(sum_d))
    if not self.doc.encashment_amount:
      self.doc.encashment_amount = 0.00
    amount= round(flt(sum_e) + round(flt(self.doc.arrear_amount))+round(flt(self.doc.encashment_amount))-flt(sum_d))
    self.doc.net_pay = amount
    
    in_words = self.get_total_in_words('Rs',amount)
    self.doc.net_pay_in_words  = in_words 

  
  def process_payroll_all(self):
    self.doc.save()
    self.set_values()
    self.set_ed_tables() 
    self.cal_gp_td_np()
    self.doc.save()
    
   
    
    
  # Get total in words
  # ==================================================================
  def get_total_in_words(self, currency, amount):
    in_words = self.in_words(amount)
    if in_words:
      in_words = currency + ". " + in_words + " only."
    return in_words

  
  def in_words(self,n):
    l = str(n).split('.')
    out = ''
    for n in l:
      n=int(n)
      if n > 0:
        known = {0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5:
'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten',
          11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', 15:
'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen',
          19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty', 50:
'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty', 90: 'Ninety'}

        def psn(n, known, xpsn):
          import sys;
          #print >>sys.stderr, n
          #n=cint(n)
          if n in known:
            return known[n]
          bestguess = str(n)
          remainder = 0
          if n<=20:
            print >>sys.stderr, n, "How did this happen?"
            assert 0
          elif n < 100:
            bestguess= xpsn((n//10)*10, known, xpsn) + '-' + xpsn(n%10,
known, xpsn)
            return bestguess
          elif n < 1000:
            bestguess= xpsn(n//100, known, xpsn) + ' ' + 'Hundred'
            remainder = n%100
          elif n < 100000:
            bestguess= xpsn(n//1000, known, xpsn) + ' ' + 'Thousand'
            remainder = n%1000
          elif n < 10000000:
            bestguess= xpsn(n//100000, known, xpsn) + ' ' + 'Lakh'
            remainder = n%100000
          else:
            bestguess= xpsn(n//10000000, known, xpsn) + ' ' + 'Crore'
            remainder = n%10000000
          if remainder:
            if remainder >= 100:
              comma = ','
            else:
              comma = ''
            return bestguess + comma + ' ' + xpsn(remainder, known, xpsn)
          else:
            return bestguess

        if not out and len(l) > 1  and int(l[1]) > 0:
          out += psn(n, known, psn) + " and "
        elif out and len(l) > 1:
          out += psn(n, known, psn) + " Paise"
        else:
          out += psn(n, known, psn)
    return out


  def send_mail_funct(self):
   
    emailid_ret=sql("select company_email from `tabEmployee` where name = '%s'"%self.doc.employee)
    if emailid_ret:
      receiver = cstr(emailid_ret[0][0]) 
      subj = 'Salary Slip ' + cstr(self.doc.month) +' '+cstr(self.doc.year)
      earn_ret=sql("select e_type,e_amount from `tabSS Earning Detail` where parent = '%s'"%self.doc.name)
      ded_ret=sql("select d_type,d_amount from `tabSS Deduction Detail` where parent = '%s'"%self.doc.name)
     
      earn_table = ''
      ded_table = ''
      if earn_ret:
      
        earn_table += "<table cellspacing= '5' cellpadding='5' >"
        
        for e in earn_ret:
          if not e[1]:
            earn_table +='<tr><td>%s</td><td>0.00</td></tr>'%(cstr(e[0]))
          else:
            earn_table +='<tr><td>%s</td><td>%s</td></tr>'%(cstr(e[0]),cstr(e[1]))
        earn_table += '</table>'
      
      if ded_ret:
      
        ded_table += "<table cellspacing= '5' cellpadding='5' >"
        
        for d in ded_ret:
          if not d[1]:
            ded_table +='<tr><td>%s</td><td>0.00</td></tr>'%(cstr(d[0]))
          else:
            ded_table +='<tr><td>%s</td><td>%s</td></tr>'%(cstr(d[0]),cstr(d[1]))
        ded_table += '</table>'
      
      letter_head = sql("select value from `tabSingles` where field = 'letter_head' and doctype = 'Control Panel'")
      
      if not letter_head:
        letter_head = ''
      
      msg = ''' %s <br>
      <table cellspacing= "5" cellpadding="5" >
      <tr>
        <td colspan = 4><h4>Salary Slip</h4></td>
      </tr>
      <tr>
        <td colspan = 2><b>Employee Code : %s</b></td>
        <td colspan = 2><b>Employee Name : %s</b></td>
      </tr>
      <tr>
        <td>Month : %s</td>
        <td>Year : %s</td>
        <td colspan = 2>Fiscal Year : %s</td>
      </tr>
      <tr>
        <td>Department : %s</td>
        <td>Branch : %s</td>
        <td colspan = 2>Designation : %s</td>
        
      </tr>
      <tr>
        <td>Grade : %s</td>
        <td>Bank Account No. : %s</td>
        <td colspan = 2>Bank Name : %s</td>
        
      </tr>
      <tr>
        <td>PF No. : %s</td>
        <td>ESIC No. : %s</td>
        <td colspan = 2>Arrear Amount : <b>%s</b></td>
      </tr>
      <tr>
        <td>Total days in month : %s</td>
        <td>Leave Without Pay : %s</td>
        <td colspan = 2>Payment days : %s</td>
        
      </tr>
      <br><br>
      <tr>
        <td colspan = 2><b>Earning</b></td>
        <td colspan = 2><b>Deduction</b></td>
      </tr>
      <tr>
        <td colspan = 2>%s</td>
        <td colspan = 2>%s</td>
      </tr>
      <br>
      <tr>
        <td colspan = 2><b>Gross Pay :</b> %s</td>
        <td colspan = 2><b>Total Deduction :</b> %s</td>
      </tr>
      <tr>
        <td><b>Net Pay : %s</b></td>
        <td colspan = 3><b>Net Pay (in words) : %s</b></td>
      </tr>
      </table>'''%(cstr(letter_head[0][0]),cstr(self.doc.employee),self.doc.employee_name,cstr(self.doc.month),cstr(self.doc.year),cstr(self.doc.fiscal_year),self.doc.department,self.doc.branch,self.doc.designation,self.doc.grade,cstr(self.doc.bank_account_no),self.doc.bank_name,cstr(self.doc.pf_no),cstr(self.doc.esic_no),cstr(self.doc.arrear_amount),cstr(self.doc.total_days_in_month),cstr(self.doc.leave_without_pay),cstr(self.doc.payment_days),earn_table,ded_table,cstr(self.doc.gross_pay),cstr(self.doc.total_deduction),cstr(self.doc.net_pay),cstr(self.doc.net_pay_in_words))
      sendmail([receiver], sender='automail@webnotestech.com', subject=subj, parts=[['text/plain', msg]])
    else:
      msgprint("Company Email ID not found.")

  
  # ON SUBMIT
  # **********************************************************************
  def on_submit(self):
    
    ret_earn = sql("select name from `tabSS Earning Detail` where parent = '%s'"%self.doc.name)
    ret_ded =  sql("select name from `tabSS Deduction Detail` where parent = '%s'"%self.doc.name)
    if not ret_earn and not ret_ded:
      msgprint("Please Make Salary Structure Earn/Ded Table")
      raise Exception
    elif(self.doc.email_check == 1):
      
      self.send_mail_funct()

    # make feed
    obj = get_obj('Feed Control', 'Feed Control')
    obj.make_feed('submitted', self.doc.doctype, self.doc.name)

  # on update
  def on_update(self):
    obj = get_obj('Feed Control', 'Feed Control')
    
    if not self.doc.creation:
      obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      obj.make_feed('modified', self.doc.doctype, self.doc.name)