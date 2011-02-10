columns = [['DN No','Data','250px','']]

for c in columns:
  colnames.append(c[0])
  coltypes.append(c[1])
  colwidths.append(c[2])
  coloptions.append(c[3])
  col_idx[c[0]] = len(colnames)-1


for r in res:
  det = sql("select parent from `tabDelivery Note Detail` where item_code = %s and prevdoc_docname = %s" , (r[col_idx['Item Code']], r[col_idx['ID']]))
  dn = ''
  for d in det:
    dn += cstr(d[0])+NEWLINE
  r.append(cstr(dn))