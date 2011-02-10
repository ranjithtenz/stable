
# Columns
cl = [['Account','Data', '200px'],['Debit/Credit', 'Data', '100px'], ['Group/Ledger', 'Data', '100px'], ['Is PL Account', 'Data', '100px'], ['Opening','Data', '100px'],['Debit', 'Data', '100px'],['Credit', 'Data', '100px'],['Closing', 'Data', '100px']]
for c in cl:
  colnames.append(c[0])
  coltypes.append(c[1])
  colwidths.append(c[2])
  coloptions.append('')
  col_idx[c[0]] = len(colnames)-1
  

# transaction date
if not filter_values.get('transaction_date') or not filter_values.get('transaction_date1'):
  msgprint("Please enter From Date and To Date")
  raise Exception
else:
  from_date = filter_values['transaction_date']
  to_date = filter_values['transaction_date1']

#check for from date and to date within same year.
#try except used for tuple index out of range error.
 
if not sql("select name from `tabFiscal Year` where %s between year_start_date and date_add(year_start_date,interval 1 year) and %s between year_start_date and date_add(year_start_date,interval 1 year)",(from_date, to_date)):
  msgprint("From Date and To Date must be within same year")
  raise Exception
 
from_date_year = sql("select name from `tabFiscal Year` where %s between year_start_date and date_add(year_start_date,interval 1 year)",add_days(from_date, -1))[0][0]
to_date_year = sql("select name from `tabFiscal Year` where %s between year_start_date and date_add(year_start_date,interval 1 year)",to_date)[0][0]

# if output is more than 300 lines then it will ask to export
if len(res) > 300  and from_export == 0:
  msgprint("This is a very large report and cannot be shown in the browser as it is likely to make your browser very slow.Please click on 'Export' to open in a spreadsheet")
  raise Exception

total_debit, total_credit = 0,0
glc = get_obj('GL Control')

for r in res:
  acc = r[col_idx['Account']].strip()
  acc_det = sql("select debit_or_credit, is_pl_account, lft, rgt, group_or_ledger from tabAccount where name = '%s'" % acc)
  r.append(acc_det[0][0])
  r.append(acc_det[0][4])
  r.append(acc_det[0][1])
  
  if acc_det[0][4] == 'Group' and filter_values.get('show_group_balance') == 'No':
    for i in range(4):
      r.append('')
    continue

  debit_on_fromdate, credit_on_fromdate, opening = glc.get_as_on_balance(acc, from_date_year, add_days(from_date, -1), acc_det[0][0], acc_det[0][2], acc_det[0][3])
  debit_on_todate, credit_on_todate, closing = glc.get_as_on_balance(acc, to_date_year, to_date, acc_det[0][0], acc_det[0][2], acc_det[0][3])

  if from_date_year == to_date_year:
    debit = flt(debit_on_todate) - flt(debit_on_fromdate)
    credit = flt(credit_on_todate) - flt(credit_on_fromdate)
  else:
    debit = flt(debit_on_todate)
    credit = flt(credit_on_todate)
    
  total_debit += debit
  total_credit += credit

  if acc_det[0][1] == 'Yes' and from_date_year != to_date_year:
    opening = 0

  if acc_det[0][0] == 'Credit':
    opening, closing = -1*opening, -1*closing
  
  r.append(flt(opening))
  r.append(flt(debit))
  r.append(flt(credit))
  r.append(flt(closing))

if filter_values.get('show_group_balance') == 'No':
  t_row = ['' for i in range(len(colnames))]
  t_row[col_idx['Account']] = 'Total'
  t_row[col_idx['Debit']] = total_debit
  t_row[col_idx['Credit']] = total_credit
  res.append(t_row)