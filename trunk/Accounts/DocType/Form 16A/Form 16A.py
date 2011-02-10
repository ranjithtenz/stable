class DocType:
  def __init__(self,d,dl):
    self.doc, self.doclist = d, dl
  
  def autoname(self):   
    self.doc.name = make_autoname('Form 16A' + '/.#####') 

  # Get pan no and tan no from company
  #-------------------------------------
  def get_registration_details(self):
    comp_det=sql("Select address,registration_details from `tabCompany` where name = '%s'"%(self.doc.company))
    if not comp_det:
      msgprint("Registration Details is not mentioned in comapny")
      ret = {
      'company_address':'',
      'registration_details':  ''
    }
    else:
      ret = {
        'company_address': cstr(comp_det[0][0]),
        'registration_details': cstr(comp_det[0][1])
      }   
    return cstr(ret)

  # Get party details
  #------------------
  def get_party_det(self):
    party_det=sql("Select pan_number, address from `tabAccount` where name = '%s'" % self.doc.party_name)
    ret = {
      'pan_number': cstr(party_det[0][0]) ,
      'party_address': cstr(party_det[0][1])
    }    
    return cstr(ret)

  # Get TDS Return acknowledgement
  #-------------------------------
  def get_return_ack_details(self):
    self.doc.clear_table(self.doclist, 'form_16A_ack_details')
    if not (self.doc.from_date and self.doc.to_date):
      msgprint("Please enter From Date, To Date")
    else:
      ack = sql("select quarter, acknowledgement_no from `tabTDS Return Acknowledgement` where date_of_receipt>='%s' and date_of_receipt<='%s' and tds_category = '%s' order by date_of_receipt ASC" % (self.doc.from_date, self.doc.to_date, self.doc.tds_category))
      for d in ack:
        ch = addchild(self.doc, 'form_16A_ack_details', 'Form 16A Ack Detail', 1, self.doclist)
        ch.quarter = d[0]
        ch.ack_no = d[1]

  # Get tds payment details
  #-------------------------------
  def get_tds(self):
    self.doc.clear_table(self.doclist,'form_16A_tax_details')
    import datetime
    if self.doc.from_date and self.doc.to_date and self.doc.tds_category:      
      party_tds_list=sql("select t2.amount_paid,t2.date_of_payment,t2.tds_amount,t2.cess_on_tds, t2.total_tax_amount,t1.cheque_no,t1.bsr_code,t1.date_of_receipt,t1.challan_no from `tabTDS Payment` t1, `tabTDS Payment Detail` t2 where t1.tds_category='%s' and t1.party_name='%s' and t1.from_date >= '%s' and t1.to_date <= '%s' and t2.total_tax_amount>0 and t2.parent=t1.name and t1.docstatus=1" % (self.doc.tds_category,self.doc.party_name,self.doc.from_date,self.doc.to_date))
      for s in party_tds_list:
        child = addchild(self.doc, 'form_16A_tax_details', 'Form 16A Tax Detail', 1, self.doclist)
        child.amount_paid = s and flt(s[0]) or ''
        child.date_of_payment =s and s[1].strftime('%Y-%m-%d') or ''
        child.tds_amount = s and flt(s[2]) or ''
        child.surcharge = 0
        child.cess_on_tds = s and flt(s[3]) or ''
        child.total_tax_deposited = s and flt(s[4]) or ''
        child.cheque_no = s and s[5] or ''
        child.bsr_code = s and s[6] or ''
        child.tax_deposited_date = s and s[7].strftime('%Y-%m-%d') or ''
        child.challan_no = s and s[8] or ''
    else:
      msgprint("Plaese enter from date, to date and TDS category")
  
  # validate
  #----------------
  def validate(self):
    tot=0.0
    for d in getlist(self.doclist,'form_16A_tax_details'):
      tot=flt(tot)+flt(d.total_tax_deposited)
    
    self.doc.total_amount = flt(tot)

  # on update
  def on_update(self):
    obj = get_obj('Feed Control', 'Feed Control')
    
    if not self.doc.creation:
      obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      obj.make_feed('modified', self.doc.doctype, self.doc.name)