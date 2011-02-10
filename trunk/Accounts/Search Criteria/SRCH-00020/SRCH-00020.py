# add additional columns

cl = [c[0] for c in sql("select distinct add_tax_code from `tabPV Add Tax Detail` where parenttype='Payable Voucher' and docstatus=1 order by idx asc")]
expense_acc = [c[0] for c in sql("select distinct expense_head from `tabPV Detail` where parenttype='Payable Voucher' and docstatus=1 order by idx asc")]

expense_acc.append('Net Total')

for i in expense_acc:
  colnames.append(i)
  coltypes.append('Currency')
  colwidths.append('100px')
  coloptions.append('')

cl.append('Total Tax')
cl.append('GrandTotal')
for c in cl:
  if c:
    colnames.append(c)
    coltypes.append('Currency')
    colwidths.append('100px')
    coloptions.append('')
expense_acc = expense_acc[:-1]
cl = cl[:-2]
# add the values
for r in res:
  net_total = 0
  for i in expense_acc:
    val = sql("select sum(amount) from `tabPV Detail` where parent = %s and parenttype='Payable Voucher' and expense_head = %s", (r[col_idx['ID']], i))
    val = flt(val and val[0][0] or 0)
    net_total += val
    r.append(val)
  r.append(net_total)

  total_tax = 0
  grand_total = 0
  for c in cl:
    if c:
      val = sql("select add_amount from `tabPV Add Tax Detail` where parent = %s and parenttype='Payable Voucher' and add_tax_code = %s", (r[col_idx['ID']], c))
      val = flt(val and val[0][0] or 0)
      total_tax += val
      r.append(val)
  r.append(total_tax)
  r.append(total_tax+net_total)