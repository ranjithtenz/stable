# Check mandatory filters
#------------------------------

if not filter_values.get('posting_date') or not filter_values.get('posting_date1'):
  msgprint("Please select From Posting Date and To Posting Date ")
  raise Exception
else:
  from_date = filter_values.get('posting_date')
  to_date = filter_values.get('posting_date1')

if not filter_values['range_1'] or not filter_values['range_2'] or not filter_values['range_3'] or not filter_values['range_4']:
  msgprint("Please select aging ranges in no of days in 'More Filters' ")
  raise Exception

# validate Range
range_list = ['range_1','range_2','range_3','range_4']
for r in range(len(range_list)-1):
  if not cint(filter_values[range_list[r]]) < cint(filter_values[range_list[r + 1]]):
    msgprint("Range %s should be less than Range %s." % (cstr(r+1),cstr(r+2)))
    raise Exception

  
# Add columns
# -----------
data = [['Aging Date','Date','80px',''],
        ['Transaction Date','Date','80px',''],
        ['Account','Data','120px',''],
        ['Against Voucher','Data','120px',''],
        ['Voucher No','Data','120px',''],
        ['Remarks','Data','160px',''],
        ['Supplier Type', 'Data', '80px', ''],
        ['Due Date', 'Date', '80px', ''],
        ['Bill No','Data','80px',''],
        ['Bill Date','Date','80px',''],
        ['Opening Amt','Currency','120px',''],
        ['Outstanding Amt','Currency','120px',''],
        ['Break up','Data','150px',''],
        ['Age (Days)', 'Currency', '150px', ''],
        ['0-'+cstr(filter_values['range_1']),'Currency','100px',''],
        [cstr(cint(filter_values['range_1']) + 1)+ '-' +cstr(filter_values['range_2']),'Currency','100px',''],
        [cstr(cint(filter_values['range_2']) + 1)+ '-' +cstr(filter_values['range_3']),'Currency','100px',''],
        [cstr(cint(filter_values['range_3']) + 1)+ '-' +cstr(filter_values['range_4']),'Currency','100px',''],
        [cstr(filter_values['range_4']) + '-Above','Currency','100px','']]
        
for d in data:
  colnames.append(d[0])
  coltypes.append(d[1])
  colwidths.append(d[2])
  coloptions.append(d[3])
  col_idx[d[0]] = len(colnames)-1
  
# ageing based on
aging_based_on = 'Aging Date'
if filter_values.has_key('aging_based_on') and filter_values['aging_based_on']:
  aging_based_on = filter_values['aging_based_on'].split(NEWLINE)[-1]


out = []
total_opening_amt,total_outstanding_amt = 0,0
for r in res:
  supplier_type = sql("select t1.supplier_type from tabSupplier t1, tabAccount t2 where t1.name = t2.account_name and t2.name = '%s'" % r[col_idx['Account']])
  r.append(supplier_type and cstr(supplier_type[0][0]) or '')
  due_date = sql("select due_date,bill_no,bill_date from `tabPayable Voucher` where name = '%s'" % r[col_idx['Against Voucher']])
  r.append(due_date and cstr(due_date[0][0]) or '')
  r.append(due_date and due_date[0][1] or '')
  r.append(due_date and cstr(due_date[0][2]) or '')

  
  
  if r[col_idx['Against Voucher']]:    
    # get opening and outstanding amt
    opening_amt = sql("select credit from `tabGL Entry` where account = '%s' and voucher_no = '%s' and is_cancelled = 'No'" % (r[col_idx['Account']], r[col_idx['Voucher No']]))
    outstanding_amt = sql("select sum(ifnull(credit, 0))-sum(ifnull(debit, 0)) from `tabGL Entry` where account = %s and against_voucher = %s and against_voucher is not null and posting_date <= %s and is_cancelled = 'No'",(r[col_idx['Account']],r[col_idx['Against Voucher']],to_date))
    opening_amt = opening_amt and flt(opening_amt[0][0]) or 0
    outstanding_amt = outstanding_amt and flt(outstanding_amt[0][0]) or 0
    if outstanding_amt:
      total_opening_amt += flt(opening_amt)
  else:
    # get opening and outstanding amt
    outstanding_amt = sql("select sum(ifnull(credit, 0))-sum(ifnull(debit, 0)) from `tabGL Entry` where account = '%s' and ((voucher_no = '%s' and against_voucher = '') or (against_voucher = '%s' and against_voucher_type = 'Journal Voucher')) and ifnull(against_voucher,'') = '' and is_cancelled = 'No'" % (r[col_idx['Account']], r[col_idx['Voucher No']], r[col_idx['Voucher No']]))
    outstanding_amt = outstanding_amt and -1*flt(outstanding_amt[0][0]) or 0
    opening_amt = ''
    
  total_outstanding_amt += flt(outstanding_amt)
  r.append(opening_amt)
  r.append(outstanding_amt)
  
  # get break up (in case JV is adjusted against two or more RV's. This will get break up of the amt adjusted)
  #------------------------------------------------------------
  if r[col_idx['Against Voucher']]:
    r.append('')
  else:
    det = ""
    break_up = sql("select debit from `tabJournal Voucher Detail` where parent = %s and account = %s and ifnull(against_invoice,'') = ''",(r[col_idx['Voucher No']],r[col_idx['Account']]))
    for i in break_up:
      det += cstr(i[0])+" + "
    det = det and det[:-3] or ''
    r.append(cstr(det))
  

  #Ageing Outstanding
  diff = val_l1 = val_l2 = val_l3 = val_l4 = val_l5_above = 0

  if r[col_idx[aging_based_on]]:
    diff = (getdate(to_date) - getdate(r[col_idx[aging_based_on]])).days
    if diff < cint(filter_values['range_1']):
      val_l1 = outstanding_amt
    if diff >= cint(filter_values['range_1']) and diff < cint(filter_values['range_2']):
      val_l2 = outstanding_amt
    if diff >= cint(filter_values['range_2']) and diff < cint(filter_values['range_3']):
      val_l3 = outstanding_amt
    if diff >= cint(filter_values['range_3']) and diff < cint(filter_values['range_4']):
      val_l4 = outstanding_amt
    if diff >= cint(filter_values['range_4']):
      val_l5_above = outstanding_amt

  r.append(diff)
  r.append(val_l1)
  r.append(val_l2)
  r.append(val_l3)
  r.append(val_l4)
  r.append(val_l5_above)
    
  if (r[col_idx['Against Voucher']] and flt(outstanding_amt) > 0) or (not r[col_idx['Against Voucher']] and flt(outstanding_amt) != 0):
    out.append(r)
    
if  len(out) > 300 and from_export == 0:
  msgprint("This is a very large report and cannot be shown in the browser as it is likely to make your browser very slow.Please select Account or click on 'Export' to open in excel")
  raise Exception


# Append Extra rows to RES
t_row = ['' for i in range(len(colnames))]
t_row[col_idx['Voucher No']] = 'Total'
t_row[col_idx['Opening Amt']] = total_opening_amt
t_row[col_idx['Outstanding Amt']] = total_outstanding_amt
out.append(t_row)