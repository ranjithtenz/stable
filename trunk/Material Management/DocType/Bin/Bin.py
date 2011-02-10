class DocType:  
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
      
  # stock update
  # ------------
  def update_stock(self, actual_qty=0, reserved_qty=0, ordered_qty=0, indented_qty=0, planned_qty=0, dt=None, sle_id='', posting_time=''):
    if not dt: dt = nowdate()
    
    self.doc.actual_qty = flt(self.doc.actual_qty) + flt(actual_qty)
    self.doc.ordered_qty = flt(self.doc.ordered_qty) + flt(ordered_qty)            
    self.doc.reserved_qty = flt(self.doc.reserved_qty) + flt(reserved_qty)
    self.doc.indented_qty = flt(self.doc.indented_qty) + flt(indented_qty)
    self.doc.planned_qty = flt(self.doc.planned_qty) + flt(planned_qty)
    
    #self.doc.available_qty = flt(self.doc.actual_qty) + flt(self.doc.ordered_qty) + flt(self.doc.indented_qty) - flt(self.doc.reserved_qty)
    self.doc.projected_qty = flt(self.doc.actual_qty) + flt(self.doc.ordered_qty) + flt(self.doc.indented_qty) + flt(self.doc.planned_qty) - flt(self.doc.reserved_qty)
    

    self.doc.save()

    # if actual qty update valuation
    if actual_qty:
      prev_sle = self.get_prev_sle(sle_id, dt,posting_time)
      cqty = prev_sle and flt(prev_sle[0][0]) or 0
      
      # Block if actual qty becomes negative
      if (flt(cqty) + flt(actual_qty)) < 0 and flt(actual_qty) < 0:
        msgprint('Negative Stock Not Allowed: Item %s, Warehouse %s' % (self.doc.item_code, self.doc.warehouse))
        raise Exception

      self.update_item_valuation(sle_id,dt,posting_time)

  def get_prev_sle(self, sle_id, posting_date,posting_time):
    import datetime
    hrs, mins = [ int(t) for t in str(posting_time).split(':')]
    prev_sle = sql("select bin_aqat, valuation_rate, name, fcfs_stack, posting_date, posting_time from `tabStock Ledger Entry` where item_code = '%s' and warehouse = '%s' and posting_date <= '%s' and name != '%s' order by posting_date DESC,  posting_time DESC, name DESC limit 1" % (self.doc.item_code, self.doc.warehouse, posting_date, sle_id))
    if prev_sle:
      check = 0
      if prev_sle[0][4] == getdate(str(posting_date)):
        if prev_sle[0][5] == datetime.timedelta(minutes = mins, hours = hrs):
          check = sql("select name from `tabStock Ledger Entry` where item_code = '%s' and warehouse = '%s' and posting_date ='%s' and name != '%s'" % (self.doc.item_code, self.doc.warehouse, prev_sle[0][4], prev_sle[0][2]))
        elif prev_sle[0][5] > datetime.timedelta(minutes = mins, hours = hrs):
          ret1 = sql("select bin_aqat, valuation_rate, name, fcfs_stack from `tabStock Ledger Entry` where item_code = '%s' and warehouse = '%s' and posting_date ='%s' and posting_time = '%s' and name < '%s' order by posting_date DESC, posting_time DESC, name DESC limit 1" % (self.doc.item_code, self.doc.warehouse, posting_date, posting_time, sle_id))
          if ret1:
            prev_sle = ret1
          else:
            ret2 = sql("select bin_aqat, valuation_rate, name, fcfs_stack from `tabStock Ledger Entry` where item_code = '%s' and warehouse = '%s' and posting_date ='%s' and posting_time < '%s' order by posting_date DESC, posting_time DESC, name DESC limit 1" % (self.doc.item_code, self.doc.warehouse, posting_date,posting_time))
            if ret2:
              prev_sle = ret2
            else:
              prev_sle = sql("select bin_aqat, valuation_rate, name, fcfs_stack from `tabStock Ledger Entry` where item_code = '%s' and warehouse = '%s' and posting_date < '%s' order by posting_date DESC, posting_time DESC, name DESC limit 1" % (self.doc.item_code, self.doc.warehouse, prev_sle[0][4]))

      if check:
        prev_sle = sql("select bin_aqat, valuation_rate, name, fcfs_stack from `tabStock Ledger Entry` where item_code = '%s' and warehouse = '%s' and posting_date <= '%s' and name < '%s' order by posting_date DESC, posting_time DESC, name DESC limit 1" % (self.doc.item_code, self.doc.warehouse, prev_sle[0][4], sle_id))
    return prev_sle
    
  # item valuation
  # -------------- 
  def update_item_valuation(self, sle_id, posting_date, posting_time):
    # get last SLEs for this bin.... this is required as there could be new back-dated entries

    # get sle where posting date is after this posting date
    prev_sle = sql("select bin_aqat, valuation_rate, name, posting_date, posting_time, actual_qty, fcfs_stack from `tabStock Ledger Entry` where item_code = '%s' and warehouse = '%s' and posting_date < '%s' and name != '%s' order by posting_date DESC,  posting_time DESC, name DESC limit 1" % (self.doc.item_code, self.doc.warehouse, posting_date, sle_id))
    
    # opening quantity at the beginning of this day
    cqty = prev_sle and prev_sle[0][0] or 0

    # moving average rate at the beginning of this day
    val_rate = prev_sle and prev_sle[0][1] or 0

    # FIFO stack at the beginning of this day
    fcfs_bal = prev_sle and (prev_sle[0][6] and eval(prev_sle[0][6]) or []) or []

    val_method = sql("select valuation_method from tabItem where name = %s", self.doc.item_code)
    val_method = val_method and val_method[0][0] or ''
    if not val_method: val_method = get_defaults().has_key('valuation_method') and get_defaults()['valuation_method'] or 'FIFO'

    bin_stock_value = 0

    sll = sql("select actual_qty, incoming_rate, name, voucher_type, voucher_no, voucher_detail_no, is_cancelled, posting_date from `tabStock Ledger Entry` where item_code=%s and warehouse=%s and posting_date >= %s order by posting_date asc, posting_time asc, name asc", (self.doc.item_code, self.doc.warehouse, posting_date))
    for s in sll:
      stock_val = 0
      # IN
      in_rate = s[1]
      # validate if stock is going -ve in between for back dated entries will consider only is_cancel = 'No' entries
      if cqty + s[0] < 0 and s[6] != 'Yes':
        msgprint('Stock is getting Negative for Item %s, Warehouse %s on posting date %s' % (self.doc.item_code, self.doc.warehouse, s[7]))
        raise Exception
      if val_method == 'Moving Average':
        if flt(in_rate) <= 0:
          in_rate = val_rate
        # moving average
        if in_rate and val_rate == 0:
          val_rate = in_rate
        elif s[0] > 0 and (cqty + s[0])>0 and s[6] == 'No' and ((cqty*val_rate) + (s[0]*in_rate))> 0:
          val_rate = ((cqty*val_rate) + (s[0]*in_rate)) / (cqty + s[0])
        stock_val = val_rate

      elif val_method == 'FIFO':
        if s[0] > 0:          
          fcfs_bal.append([flt(s[0]), flt(in_rate)]) # add batch to fcfs balance
          val_rate = s[1]
        else:
          # remove from fcfs balance
          fcfs_val = 0
          withdraw = flt(abs(s[0]))
          while withdraw:
            if not fcfs_bal:
              break # nothing in store
            
            batch = fcfs_bal[0]
           
            if batch[0] < withdraw:
              # not enough in current batch, clear batch
              withdraw -= batch[0]
              fcfs_val += (flt(batch[0]) * flt(batch[1]))
              fcfs_bal.pop(0)
            else:
              # all from current batch
              fcfs_val += (flt(withdraw) * flt(batch[1]))
              batch[0] -= withdraw
              withdraw = 0
          val_rate = flt(fcfs_val) / flt(abs(s[0]))
      cqty += s[0]
      # Get Stock Value
      if val_method == 'Moving Average': stock_val = flt(stock_val) * flt(cqty)
      elif val_method == 'FIFO':
        for d in fcfs_bal:
          stock_val += (flt(d[0]) * flt(d[1]))
      # Update SLE
      sql("update `tabStock Ledger Entry` set bin_aqat=%s, valuation_rate=%s, fcfs_stack=%s, stock_value=%s where name=%s", (cqty, flt(val_rate), cstr(fcfs_bal), stock_val, s[2]))
      bin_stock_value = flt(stock_val)
    # update in BIN
    sql("update `tabBin` set valuation_rate=%s, actual_qty=%s, stock_value = %s where name=%s", (flt(val_rate), cqty, flt(bin_stock_value), self.doc.name))

 
  # item re-order
  # -------------
  def reorder_item(self):
    #check if re-order is required
    projected_qty = flt(self.doc.actual_qty)  + flt(self.doc.indented_qty) + flt(self.doc.ordered_qty)
    item_reorder_level = sql("select reorder_level from `%sItem` where name = '%s'" % (self.prefix, self.doc.item_code))[0][0] or 0
    if flt(item_reorder_level) > flt(projected_qty):
      msgprint("Item: " + self.doc.item_code + " is to be re-ordered. Indent raised (Not Implemented).")
  
  # validate bin  

  def validate(self):
    self.validate_mandatory()

  
  # set defaults in bin
  def validate_mandatory(self):
    qf = ['actual_qty', 'reserved_qty', 'ordered_qty', 'indented_qty']
    for f in qf:
      if (not self.doc.fields.has_key(f)) or (not self.doc.fields[f]): 
        self.doc.fields[f] = 0.0
