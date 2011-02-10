class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist


  def get_purchase_receipts(self):
    self.doc.clear_table(self.doclist,'lc_pr_details',1)
    if not self.doc.from_pr_date or not self.doc.to_pr_date:
      msgprint("Please enter From and To PR Date")
      raise Exception
    if not self.doc.currency:
      msgprint("Please enter Currency.")
      raise Exception
    pr = sql("select name from `tabPurchase Receipt` where docstatus = 1 and posting_date >= '%s' and posting_date <= '%s' and currency = '%s' order by name "%(self.doc.from_pr_date,self.doc.to_pr_date,self.doc.currency), as_dict = 1)
    if len(pr)>200:
      msgprint("Please enter date of shorter duration as there are too many purchase receipt, hence it cannot be loaded.")
      raise Exception
    for i in pr:
      if i and i['name']:
        pr_no = addchild(self.doc, 'lc_pr_details', 'LC PR Detail', 1, self.doclist)
        pr_no.purchase_receipt_no = i and i['name'] or ''
        pr_no.save()
        
        
  def update_pr_lc_se(self):
    lst = []
    condition = ' name in('
    
    amt = 0
    for d in getlist(self.doclist, 'lc_pr_details'):
      
      if cint(d.include_in_landed_cost) == 1:
        condition += '"'+d.purchase_receipt_no+'",'
        lst.append(d.purchase_receipt_no) 
    condition += '"")'
    
    amount = sql("SELECT SUM(net_total) FROM `tabPurchase Receipt` WHERE docstatus = 1 AND %s"%condition)
    amt = amount and flt(amount[0][0]) or 0
    for lc in getlist(self.doclist, 'landed_cost_details'):
      for name in lst:
        pr_oc_det = sql("select name from `tabPurchase Tax Detail` where parent = %s and category = 'For Valuation' and add_deduct_tax = 'Add' and charge_type = 'Actual' and account_head = %s ",(name, lc.account_head))
        #obj = get_obj('Purchase Receipt', name, with_children = 1)
        if not pr_oc_det:
          obj = get_obj('Purchase Receipt', name, with_children = 1)
          lgth = cint(sql("select count(name) from `tabPurchase Tax Detail` where parent = '%s' "%(name))[0][0])
          pr_oc = addchild(obj.doc, 'purchase_tax_details', 'Purchase Tax Detail', 1)
          pr_oc.category = 'For Valuation'
          pr_oc.add_deduct_tax = 'Add'
          pr_oc.charge_type = 'Actual'
          pr_oc.description = lc.description
          pr_oc.account_head = lc.account_head
          pr_oc.rate = flt(flt(lc.amount) * flt(obj.doc.net_total/ amt))
          pr_oc.tax_amount = flt(flt(lc.amount) * flt(obj.doc.net_total/ amt))
          pr_oc.total = obj.doc.grand_total
          pr_oc.docstatus = 1
          pr_oc.idx = cint(lgth)
          pr_oc.save()
        else:
          obj = get_obj('Purchase Receipt', name)
          sql("update `tabPurchase Tax Detail` set rate = %s, tax_amount = %s where name = %s and parent = %s",(flt(flt(lc.amount) * flt(obj.doc.net_total/ amt)),flt(flt(lc.amount) * flt(obj.doc.net_total/ amt)),pr_oc_det[0][0],name))
        self.calc_pr_other_charges(name)
        obj = get_obj('Purchase Receipt', name, with_children = 1)
        for d in getlist(obj.doclist, 'purchase_receipt_details'):
          if flt(d.qty):
            d.valuation_rate = (flt(d.purchase_rate) + (flt(d.rm_supp_cost) / flt(d.qty)) + (flt(d.item_tax_amount)/flt(d.qty))) / flt(d.conversion_factor)
            d.save()
          sql("update `tabStock Ledger Entry` set incoming_rate = '%s' where voucher_detail_no = '%s'"%(flt(d.valuation_rate), d.name))
          bin_name = sql("select t1.name, t2.name, t2.posting_date, t2.posting_time from `tabBin` t1, `tabStock Ledger Entry` t2 where t2.voucher_detail_no = '%s' and t2.item_code = t1.item_code and t2.warehouse = t1.warehouse LIMIT 1"%(d.name))
          if bin_name and bin_name[0][0]:
            obj = get_obj('Bin', bin_name[0][0]).update_item_valuation(bin_name[0][1], bin_name[0][2], bin_name[0][3])

              
  def calc_pr_other_charges(self, name):
    obj = get_obj('Purchase Receipt', name, with_children = 1)
    total = 0
    net_total = obj.doc.net_total
    for prd in getlist(obj.doclist, 'purchase_receipt_details'):
      prev_total, item_tax = flt(prd.amount), 0
      total += flt(flt(prd.qty) * flt(prd.purchase_rate))
      check_tax = prd.item_tax_rate and eval(prd.item_tax_rate) or {}
      ocd = getlist(obj.doclist, 'purchase_tax_details')
      for oc in range(len(ocd)):
        if check_tax.get(ocd[oc].account_head) and ocd[oc].charge_type != 'Actual':
          rate  = check_tax[ocd[oc].account_head]
        else:
          rate = flt(ocd[oc].rate)
        
        tax_amount = self.cal_tax(ocd, prd, rate, net_total, oc)
        if ocd[oc].add_deduct_tax == 'Add':
          
          ocd[oc].total_amount = flt(tax_amount)    
           
          ocd[oc].total_tax_amount = flt(prev_total)
          ocd[oc].tax_amount += flt(tax_amount)   
          total_amount = flt(ocd[oc].tax_amount)
          total_tax_amount = flt(ocd[oc].total_tax_amount) + flt(total_amount)
          if ocd[oc].category != "For Valuation":  
            prev_total += flt(ocd[oc].total_amount)
            total += flt(ocd[oc].tax_amount)
            ocd[oc].total = flt(total) + flt(tax[t].tax_amount)
          else:
            prev_total = prev_total        
            ocd[oc].total = flt(total)
          if ocd[oc].category != "For Total":
            item_tax += ocd[oc].total_amount
            
        elif ocd[oc].add_deduct_tax == 'Deduct':
          
          ocd[oc].total_amount = flt(tax_amount.toFixed(2))     
          ocd[oc].total_tax_amount = flt(prev_total.toFixed(2))
          ocd[oc].tax_amount += flt(tax_amount.toFixed(2))   
          total_amount = flt(ocd[oc].tax_amount)
          total_tax_amount = flt(ocd[oc].total_tax_amount) - flt(total_amount)
          if ocd[oc].category != "For Valuation":  
            prev_total -= flt(ocd[oc].total_amount)
            total -= flt(ocd[oc].tax_amount)
            ocd[oc].total = flt(total) - flt(tax[t].tax_amount)
          else:
            prev_total = prev_total        
            ocd[oc].total = flt(total)
          if ocd[oc].category != "For Total":
            item_tax -= ocd[oc].total_amount
          ocd[oc].save()

      prd.item_tax_amount = flt(item_tax)
      prd.save()
    obj.doc.save()
          
  def cal_tax(self, ocd, prd, rate, net_total, oc):
    tax_amount = 0
    if ocd[oc].charge_type == 'Actual':
      value = flt(flt(rate) / flt(net_total))
      return flt(flt(value) * flt(prd.amount))
      
    elif ocd[oc].charge_type == 'On Net Total':
      return flt(flt(rate) * flt(prd.amount) / 100)
      
    elif ocd[oc].charge_type == 'On Previous Row Amount':
      
      row_no = cstr(ocd[oc].row_id)
      row = (row_no).split("+")
      for r in range(0, len(row.length)):
        id = cint(row[r])
        tax_amount += flt((flt(rate) * flt(ocd[id-1].total_amount) / 100))
      row_id = row_no.find("/")
      if row_id != -1:
        rate = ''
        row = (row_no).split("/")
        
        id1 = cint(row[0])
        id2 = cint(row[1])
        tax_amount = flt(flt(ocd[id1-1].total_amount) / flt(ocd[id2-1].total_amount))
        
      return tax_amount

    elif ocd[oc].charge_type == 'On Previous Row Total':

      row = cint(ocd[oc].row_id)    

      if ocd[row-1].add_deduct_tax == 'Add':
        tax_amount = flt(rate) * (flt(ocd[row-1].total_tax_amount)+flt(ocd[row-1].total_amount)) / 100
         
      elif ocd[row-1].add_deduct_tax == 'Deduct':
        tax_amount = flt(rate) * (flt(ocd[row-1].total_tax_amount)-flt(ocd[row-1].total_amount)) / 100
      return tax_amount


  # get details for landed cost table from master
  # ---------------------------------------------
  def get_landed_cost_master_details(self):
    msgprint('fetching details.....' + self.doc.landed_cost)
    self.doc.clear_table(self.doclist, 'landed_cost_details')
    idx = 0
    landed_cost = sql("select account_head, description from `tabLanded Cost Master Detail` where parent=%s", (self.doc.landed_cost), as_dict = 1)
    msgprint(landed_cost)
    for cost in landed_cost:
      lct = addchild(self.doc, 'landed_cost_details', 'Landed Cost Detail', 1, self.doclist)
      lct.account_head = cost['account_head']
      lct.description = cost['description']