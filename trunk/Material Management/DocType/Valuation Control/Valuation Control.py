class DocType:
  def __init__(self, d, dl):
    self.doc, self.doclist = d, dl

  # Get FIFO Rate from Stack
  # -------------------------
  def get_fifo_rate(self, fcfs_bal, qty):
    if qty:
      fcfs_val = 0
      withdraw = flt(qty)
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
      fcfs_rate = flt(fcfs_val) / flt(qty)
      return fcfs_rate
    else:
      return fcfs_bal and fcfs_bal[0][1] or 0


  # Get Incoming Rate based on valuation method
  # --------------------------------------------
  def get_incoming_rate(self, posting_date, posting_time, item, warehouse, qty = 0):
    in_rate = 0
    val_method = sql("select valuation_method from tabItem where name = %s", item)
    val_method = val_method and val_method[0][0] or ''
    if not val_method: val_method = get_defaults().has_key('valuation_method') and get_defaults()['valuation_method'] or 'FIFO'
    if val_method == 'FIFO':
      bin_obj = get_obj('Warehouse',warehouse).get_bin(item)
      prev_sle = bin_obj.get_prev_sle('',posting_date, posting_time)
      fcfs_stack = prev_sle and (prev_sle[0][3] and eval(prev_sle[0][3]) or []) or []
      in_rate = fcfs_stack and self.get_fifo_rate(fcfs_stack, qty) or 0
    elif val_method == 'Moving Average':
      bin_obj = get_obj('Warehouse',warehouse).get_bin(item)
      prev_sle = bin_obj.get_prev_sle('',posting_date, posting_time)
      in_rate = prev_sle and prev_sle[0][1] or 0
    return in_rate 