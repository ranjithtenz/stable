# add additional columns

colnames.append('Expense Head')
coltypes.append('Text')
colwidths.append('200px')
coloptions.append('')

#cl = [c[0] for c in sql("select distinct add_tax_code from `tabPV Add Tax Detail` where parenttype='Payable Voucher' and docstatus=1 order by idx asc")]
cl = [c[0] for c in sql("select distinct account_head from `tabPurchase Tax Detail` where parenttype = 'Payable Voucher' and add_deduct_tax = 'Add' and category != 'For Valuation' order by idx asc")]

cl.append('Total Tax')
cl.append('Grand Total')

for c in cl:
  if c:
    colnames.append(c)
    coltypes.append('Currency')
    colwidths.append('100px')
    coloptions.append('')

cl = cl[:-2]
# add the values
for r in res:
  exp_head_list = [c[0] for c in sql("select distinct expense_head from `tabPV Detail` where parenttype='Payable Voucher' and docstatus=1 and parent = %s order by idx asc", r[col_idx['ID']])]
  r.append(cstr(exp_head_list))

  total_tax = 0

  for c in cl:
    if c:
      val = sql("select tax_amount from `tabPurchase Tax Detail` where parent = '%s' and parenttype = 'Payable Voucher' and account_head = '%s' and add_deduct_tax = 'Add' and category != 'For Valuation'"%(r[col_idx['ID']], c))
      val = flt(val and val[0][0] or 0)
      total_tax += val
      r.append(val)

  r.append(total_tax)
  r.append(flt(total_tax)+ flt(r[col_idx['Net Total']]))