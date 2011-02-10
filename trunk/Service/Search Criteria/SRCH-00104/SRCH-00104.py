out=[]
amt,fc_amt,qty=0,0,0

for r in res:
  amt += flt(r[col_idx['Amount']])
  qty += flt(r[col_idx['No of Visit']])
  fc_amt += flt(r[col_idx['FC Amount']])
  out.append(r)


#Add the totals row
l_row = ['' for i in range(len(colnames))]
l_row[col_idx['Brand']] = '<b>TOTAL</b>' 
l_row[col_idx['No of Visit']] = qty
l_row[col_idx['Amount']] = amt
l_row[col_idx['FC Amount']] = fc_amt
out.append(l_row)