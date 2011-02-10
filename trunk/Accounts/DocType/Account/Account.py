class DocType:
  def __init__(self,d,dl):
    self.doc, self.doclist = d,dl
    self.nsm_parent_field = 'parent_account'

    # Notification objects
    self.feed_obj = get_obj('Feed Control')

  def autoname(self):
    company_abbr = sql("select abbr from tabCompany where name=%s", self.doc.company)[0][0]
    self.doc.name = self.doc.account_name.strip() + ' - ' + company_abbr

  # Get customer/supplier address
  #-----------------------------------------
  def get_address(self):    
    add=sql("Select address from `tab%s` where name='%s'"%(self.doc.master_type,self.doc.master_name))
    ret={'address':add[0][0]}
    return cstr(ret)

  # check whether master name entered for supplier/customer
  #----------------------------------------------------------
  def validate_master_name(self):
    if (self.doc.master_type == 'Customer' or self.doc.master_type == 'Supplier') and not self.doc.master_name:
      msgprint("Message: Please enter Master Name once the account is created.")

      
  # Rate is mandatory for tax account   
  #-------------------------------------  
  def validate_rate_for_tax(self):
    if self.doc.account_type == 'Tax' and not self.doc.tax_rate:
      msgprint("Please Enter Rate")    
      raise Exception

  # Fetch Parent Details and validation for account to be not created under ledger
  #----------------------------------------------------------------------------------
  def validate_parent(self):
    if self.doc.parent_account:
      par = sql("select name, group_or_ledger, is_pl_account, debit_or_credit from tabAccount where name =%s",self.doc.parent_account)
      if not par:
        msgprint("Parent account does not exists")
        raise Exception
      elif par and par[0][0] == self.doc.name:
        msgprint("You can not assign itself as parent account")
        raise Exception
      elif par and par[0][1] != 'Group':
        msgprint("Parent account can not be a ledger")
        raise Exception
      elif par and self.doc.debit_or_credit and par[0][3] != self.doc.debit_or_credit:
        msgprint("You can not move a %s account under %s account" % (self.doc.debit_or_credit, par[0][3]))
        raise Exception
      elif par and not self.doc.is_pl_account:
        self.doc.is_pl_account = par[0][2]
        self.doc.debit_or_credit = par[0][3]
  
  # Account name must be unique
  # ------------------------------------
  def validate_duplicate_account(self):
    if (self.doc.__islocal or (not self.doc.name)) and sql("select name from tabAccount where account_name=%s and company=%s", (self.doc.account_name, self.doc.company)):
      msgprint("Account Name already exists, please rename")
      raise Exception
        
  # validate root details
  # -----------------------------------------
  def validate_root_details(self):
    #does not exists parent
    if self.doc.account_name in ['Income','Source of Funds', 'Expenses','Application of Funds'] and self.doc.parent_account:
      msgprint("You can not assign parent for root account")
      raise Exception

    # Debit / Credit
    if self.doc.account_name in ['Income','Source of Funds']:
      self.doc.debit_or_credit = 'Credit'
    elif self.doc.account_name in ['Expenses','Application of Funds']:
      self.doc.debit_or_credit = 'Debit'
        
    # Is PL Account 
    if self.doc.account_name in ['Income','Expenses']:
      self.doc.is_pl_account = 'Yes'
    elif self.doc.account_name in ['Source of Funds','Application of Funds']:
      self.doc.is_pl_account = 'No'
  
  # Update balance
  #--------------------------------------------------
  def update_balance(self, fy, period_det, flag = 1):
    # update in all parents
    for p in period_det:
      sql("update `tabAccount Balance` t1, `tabAccount` t2 set t1.balance = t1.balance + (%s), t1.opening = t1.opening + (%s), t1.debit = t1.debit + (%s), t1.credit = t1.credit + (%s) where t1.period = %s and t1.parent = t2.name and t2.lft<=%s and t2.rgt>=%s", (flt(flag)*flt(p[1]), flt(flag)*flt(p[2]), flt(flag)*flt(p[3]), flt(flag)*flt(p[4]), p[0], self.doc.lft, self.doc.rgt))


  # change parent balance
  # ---------------------
  def change_parent_bal(self):
    period_det = []
    fy = sql("select name from `tabFiscal Year` where is_fiscal_year_closed = 'No'")
    for f in fy:
      # get my opening, balance
      per = sql("select period, balance, opening, debit, credit from `tabAccount Balance` where parent = %s and fiscal_year = %s", (self.doc.name, f[0]))
      for p in per:
        period_det.append([p[0], p[1], p[2], p[3], p[4]])

    # deduct balance from old_parent
    op = get_obj('Account',self.doc.old_parent)
    op.update_balance(fy, period_det, -1)
      
    # add to new parent_account
    flag = 1
    if op.doc.debit_or_credit != self.doc.debit_or_credit:
      flag = -1
    get_obj('Account', self.doc.parent_account).update_balance(fy, period_det, flag)
    get_obj('Account', self.doc.parent_account).update_balance(fy, period_det, flag)

    msgprint('Balances updated for Current Fiscal Year')
  
  # VALIDATE
  # --------------------------
  def validate(self): 
    self.validate_master_name()
    self.validate_rate_for_tax()
    self.validate_parent()
    self.validate_duplicate_account()
    self.validate_root_details()
  
    if not (self.doc.is_pl_account and self.doc.debit_or_credit):
      msgprint("Account must have a parent or must be one of root accounts: 'Income','Expenses','Source of Funds','Application of Funds'")
      raise Exception

    # Defaults
    if not self.doc.parent_account:
      self.doc.parent_account = ''
    
    # parent changed   
    if self.doc.old_parent and self.doc.parent_account and (self.doc.parent_account != self.doc.old_parent):
      self.change_parent_bal()
             
  # Add current fiscal year balance
  # -------------------------------
  def set_year_balance(self):
    p = sql("select name, start_date, end_date, fiscal_year from `tabPeriod` where docstatus != 2 and period_type in ('Month', 'Year')")
    for d in p:
      if not sql("select name from `tabAccount Balance` where parent=%s and period=%s", (self.doc.name, d[0])):
        ac = addchild(self.doc, 'account_balances', 'Account Balance', 1, self.doclist)
        ac.period = d[0]
        ac.start_date = d[1].strftime('%Y-%m-%d')
        ac.end_date = d[2].strftime('%Y-%m-%d')
        ac.fiscal_year = d[3]
        ac.opening = 0
        ac.debit = 0
        ac.credit = 0
        ac.balance = 0
        ac.save()

  # update Node Set Model
  def update_nsm_model(self):
    if globals().has_key('version') and globals()['version'] == 'v170':
      import webnotes
      import webnotes.utils.nestedset
      webnotes.utils.nestedset.update_nsm(self)
    else:
      update_nsm(self)
      
  # ON UPDATE
  #--------------------------------------
  def on_update(self):
    # update nsm
    self.update_nsm_model()   
 
    # Add curret year balance
    self.set_year_balance()
    
    # Set feed
    if not self.doc.creation:
      self.feed_obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      self.feed_obj.make_feed('modified', self.doc.doctype, self.doc.name)


  # Check user role for approval process
  #----------------------------------------
  def get_authorized_user(self):
    # Fetch credit controller role
    approving_authority = sql("select value from `tabSingles` where field='credit_controller' and doctype='Manage Account'")
    approving_authority = approving_authority and approving_authority[0][0] or ''
    
    # Check logged-in user is authorized
    if approving_authority in session['data']['roles']:
      return 1
      
  # Check Credit limit for customer
  #--------------------------------
  def check_credit_limit(self, account, company, tot_outstanding):
    # Get credit limit
    cr_limit_cust = sql("select credit_limit from `tabAccount` where name='%s'" %account)
    cr_limit_comp = sql("select credit_limit from `tabCompany` where name='%s'" %company)
    credit_limit = cr_limit_cust and flt(cr_limit_cust[0][0]) or cr_limit_comp and flt(cr_limit_comp[0][0]) or 0
    
    # If outstanding greater than credit limit and not authorized person raise exception
    if credit_limit > 0 and not self.get_authorized_user and flt(tot_outstanding) > credit_limit:
      msgprint("Total Outstanding amount can not be greater than credit limit. Please contact Credit Controller.")
      raise Exception

      
  # Account with balance cannot be inactive
  # ---------------------------------------
  def check_balance_before_trash(self):
    bal = sql("select balance from `tabAccount Balance` where period = '%s' and parent = '%s'" % (get_defaults()['fiscal_year'], self.doc.name))
    bal = bal and bal[0][0] or 0
    if flt(bal) != 0:
      msgprint("Account with existing balance can not be trashed")
      raise Exception

  def on_trash(self): 
    # Check balance before trash
    self.check_balance_before_trash()
    # rebuild tree
    set(self.doc,'old_parent', '')
    self.update_nsm_model()

  def on_restore(self):
    # rebuild tree
    self.update_nsm_model()