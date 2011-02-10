class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
    self.msg = []

  def get_count_for_reposting(self, args):
    args = eval(args)
    if args['check'] == 'Bin':
      return [d[0] for d in sql("select name from `tabBin` where item_code = 'Repost Item' " )]

    if args['check'] == 'Account Balance':
      # message
      if not self.doc.past_year:
        msgprint('<div style="color: ORANGE"> Warning: Opening balances were not imported </div>')

      # do not repost from same year
      if self.doc.past_year == self.doc.name:
        msgprint("Cannot import from the current year")
 
      return [d[0] for d in sql("select name from `tabAccount` ")]

  def get_bin_qty(self, wh, item):
    msgprint(wh)
    msgprint(item)
    # get actual_qty
    act_qty = sql("select ifnull(actual_qty, 0) from `tabBin` where warehouse = '%s' and item_code = '%s'" % (wh, item))
    act_qty = act_qty and flt(act_qty[0][0]) or 0

    # get indented_qty 
    ind_qty = sql("select sum(if( ifnull(t2.qty, 0) > ifnull(t2.ordered_qty, 0), ifnull(t2.qty, 0) - ifnull(t2.ordered_qty, 0), 0) ) from `tabIndent` t1, `tabIndent Detail`t2 where t1.name = t2.parent and t1.docstatus = 1 and t2.warehouse = '%s' and t2.item_code = '%s'" % (wh, item))
    ind_qty = ind_qty and flt(ind_qty[0][0]) or 0
    
    # get ordered_qty
    ord_qty = sql("select sum(if ( ifnull(t2.qty, 0) > ifnull(t2.received_qty, 0), (ifnull(t2.qty, 0) - ifnull(t2.received_qty, 0)) * ifnull(t2.conversion_factor, 0) , 0) ) from `tabPurchase Order` t1, `tabPO Detail` t2 where t1.name = t2.parent and t1.docstatus = 1 and t2.warehouse = '%s' and t2.item_code = '%s'" % (wh, item))
    ord_qty = ord_qty and flt(ord_qty[0][0]) or 0
    msgprint(ord_qty)

    # get reserved_qty
    res_qty =sql("select sum(if ( ifnull(t2.qty, 0) > ifnull(t2.delivered_qty, 0), ifnull(t2.qty, 0) - ifnull(t2.delivered_qty, 0) , 0) ) from `tabSales Order` t1, `tabSales Order Detail` t2 where  t1.name = t2.parent and t1.docstatus = 1 and t2.reserved_warehouse = '%s' and t2.item_code = '%s' " % (wh, item))
    res_qty = res_qty and flt(res_qty[0][0]) or 0

    # get planned_qty 
    plan_qty = sql("select sum(if ( ifnull(qty, 0) > ifnull(produced_qty,0), ifnull(qty, 0) - ifnull(produced_qty, 0), 0) ) from `tabProduction Order` where fg_warehouse = '%s' and production_item = '%s' and docstatus = 1" % (wh, item))
    plan_qty = plan_qty and flt(plan_qty[0][0]) or 0
    msgprint({'actual_qty': act_qty, 'indented_qty': ind_qty, 'ordered_qty': ord_qty, 'reserved_qty': res_qty, 'planned_qty': plan_qty })

    return {'actual_qty': act_qty, 'indented_qty': ind_qty, 'ordered_qty': ord_qty, 'reserved_qty': res_qty, 'planned_qty': plan_qty }

  def check_bin_qty(self, bin_obj, qty_dict):
    label_dict = {'actual_qty': 'Actual Qty', 'indented_qty': 'Indent Qty', 'ordered_qty': 'Ordered Qty', 'reserved_qty': 'Reserved Qty', 'planned_qty': 'Planned Qty'}
    for f in qty_dict:
      if flt(bin_obj.doc.fields[f]) != qty_dict[f]:
        msgprint('<div style="color: RED"> Difference found in %s for Item:= %s and Warehouse:= %s (Before : %s; After : %s)</div>' % (label_dict[f], bin_obj.doc.item_code, bin_obj.doc.warehouse, cstr(bin_obj.doc.fields[f]), cstr(qty_dict[f])))
        self.msg.append('<div style="color: RED"> Difference found in %s for Item:= %s and Warehouse:= %s (Before : %s; After : %s)</div>' % (label_dict[f], bin_obj.doc.item_code, bin_obj.doc.warehouse, cstr(bin_obj.doc.fields[f]), cstr(qty_dict[f])))
    
    # Check projected qty
    projected_qty = flt(qty_dict['actual_qty']) + flt(qty_dict['indented_qty']) + flt(qty_dict['ordered_qty']) + flt(qty_dict['planned_qty']) - flt(qty_dict['reserved_qty'])
    if flt(projected_qty) != flt(bin_obj.doc.projected_qty):
      msgprint('<div style="color: RED">Difference found in Projected Qty for Item:= %s and Warehouse:= %s (Before : %s; After : %s)</div>' % (bin_obj.doc.item_code, bin_obj.doc.warehouse, bin_obj.doc.projected_qty, cstr(projected_qty))) 
      self.msg.append('<div style="color: RED">Difference found in Projected Qty for Item:= %s and Warehouse:= %s (Before : %s; After : %s)</div>' % (bin_obj.doc.item_code, bin_obj.doc.warehouse, bin_obj.doc.projected_qty, cstr(projected_qty)))

  def repair_bin(self, bin):
    import webnotes
    bin_obj = get_obj('Bin',bin)
    bin_act_qty =  flt(bin_obj.doc.actual_qty)
    try:
      # udpate actual qty and item valuation
      bin_obj.update_item_valuation('', '2000-01-01', '00:00')
      msgprint(bin_obj.doc.name)
      msgprint(bin_obj.doc.warehouse)
      msgprint(bin_obj.doc.item_code)
      # get bin qty
      qty_dict = self.get_bin_qty(bin_obj.doc.warehouse, bin_obj.doc.item_code)
      
      # check bin qty
      self.check_bin_qty(bin_obj, qty_dict)

      # update indented_qty, ordered_qty, reserved_qty, planned_qty
      sql("update `tabBin` set indented_qty = '%s', ordered_qty = '%s', reserved_qty = '%s', planned_qty = '%s' where warehouse = '%s' and item_code = '%s'" % ( flt(qty_dict['indented_qty']), flt(qty_dict['ordered_qty']), flt(qty_dict['reserved_qty']), flt(qty_dict['planned_qty']),  bin_obj.doc.warehouse, bin_obj.doc.item_code))
 
      # update projected_qty
      sql("update `tabBin` set projected_qty = ifnull(indented_qty, 0) + ifnull(ordered_qty,0) + ifnull(actual_qty, 0) + ifnull(planned_qty, 0) - ifnull(reserved_qty,0) where warehouse = '%s' and item_code = '%s' " % (bin_obj.doc.warehouse, bin_obj.doc.item_code))
      if not self.msg:
        msgprint('<div style="color: GREEN"> Reposting of Stock for Item %s and Warehouse %s completed Successfully. </div>' % (bin_obj.doc.item_code, bin_obj.doc.warehouse))
    except Exception:
      msgprint('<div style="color: RED"> Handle Item %s and Warehouse %s seprately. </div> <div style="color: RED"> ERROR: %s</div>' % (bin_obj.doc.item_code, bin_obj.doc.warehouse, str(webnotes.utils.getTraceback())))
      self.msg.append('<div style="color: RED"> ERROR: %s</div>' % (str(webnotes.utils.getTraceback())))

  def repair_opening_bal(self, d, acc_obj, past_yr, fiscal_yr):
    # check opening balance
    opbal = sql("select balance from `tabAccount Balance` where parent=%s and period = %s", (acc_obj.doc.name, past_yr))
    if flt(d.opening) != flt(opbal and flt(opbal[0][0]) or 0):
      msgprint('<div style="color: RED"> Difference found in Opening of Account %s for Period %s in Fiscal Year %s (Before : %s; After : %s) </div>' % (acc_obj.doc.name, d.period, fiscal_yr, flt(d.opening), opbal and flt(opbal[0][0]) or 0)) 
      self.msg.append('<div style="color: RED"> Difference found in Opening of Account %s for Period %s in Fiscal Year %s (Before : %s; After : %s) </div>'  % (acc_obj.doc.name, d.period, fiscal_yr, flt(d.opening), opbal and flt(opbal[0][0]) or 0))
      sql("update `tabAccount Balance` set opening = '%s' where period = '%s' and parent = '%s' " % (opbal and flt(opbal[0][0]) or 0, fiscal_yr, acc_obj.doc.name))

  def repair_bal(self, d, acc_obj, fiscal_yr):
    # check balances 
    ysd = get_value('Fiscal Year', fiscal_yr, 'year_start_date')
    bal = get_obj('GL Control').get_as_on_balance(acc_obj.doc.name, fiscal_yr, d.end_date, acc_obj.doc.debit_or_credit, acc_obj.doc.is_pl_account, acc_obj.doc.lft, acc_obj.doc.rgt, ysd)
    if flt(d.balance) != flt(bal):
      msgprint('<div style="color: RED"> Difference found in Balance of Account %s for Period %s in Fiscal Year %s (Before : %s; After : %s) </div>' % (acc_obj.doc.name, d.period, fiscal_yr, flt(d.balance), flt(bal))) 
      self.msg.append('<div style="color: RED"> Difference found in Balance of Account %s for Period %s in Fiscal Year %s (Before : %s; After : %s) </div>'  % (acc_obj.doc.name, d.period, fiscal_yr, flt(d.balance), flt(bal)))
      sql("update `tabAccount Balance` set balance = '%s' where period = '%s' and parent = '%s' " % (bal, d.period, acc_obj.doc.name))
          
  def repair_acc_bal(self, acc, past_yr = '' , fiscal_yr = ''):
    # get account obj
    acc_obj = get_obj('Account', acc, with_children = 1)
  
    # get fiscal yr & past yr
    if not fiscal_yr:
      import webnotes.utils
      fiscal_yr = webnotes.utils.get_defaults()['fiscal_year']
    if not past_yr: past_yr = get_value('Fiscal Year', fiscal_yr, 'past_year')

    # Repair Opening and Balance For Account Balances
    for d in getlist(acc_obj.doclist, 'account_balances'):
      if d.fiscal_year == fiscal_yr:
        if past_yr and (past_yr != fiscal_yr) and d.period == fiscal_yr:
          self.repair_opening_bal(d, acc_obj, past_yr, fiscal_yr)
        else:
          self.repair_bal(d, acc_obj, fiscal_yr)

    # Acknowledge USer
    if not self.msg:
      msgprint('<div style="color: GREEN"> Openings & Balances of Account %s for Fiscal Year %s updated successfully. </div>' % ( acc_obj.doc.name, fiscal_yr))

    return self.msg
  
  def send_mail(self, args):
    args = eval(args)
    self.msg, subject = args['msg'], args['subject']
    msgprint(self.msg)
    if self.msg:
      email_msg = """ Dear Administrator,

In Account := %s User := %s has Reposted %s and following was found:-

%s

""" % (get_value('Control Panel', None,'account_id'), session['user'], subject, '\n'.join(self.msg))

      sendmail(['saumil@iwebnotes.com','nabin@iwebnotes.com'], subject='Repair of ' + cstr(subject), parts = [('text/plain', email_msg)])