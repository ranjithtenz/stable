$import(Tips Common)

//--------- ONLOAD -------------
cur_frm.cscript.onload = function(doc, cdt, cdn) {
  cur_frm.cscript.get_tips(doc, cdt, cdn);
}

cur_frm.cscript.refresh = function(doc, cdt, cdn) {
  cur_frm.cscript.get_tips(doc, cdt, cdn);
  if(doc.abbr && !doc.__islocal) set_field_permlevel('abbr',1);
}

cur_frm.fields_dict.default_bank_account.get_query = function(doc) {
  if(!doc.__islocal) return 'SELECT `tabAccount`.name FROM `tabAccount` WHERE `tabAccount`.name = "Cheating Query just to make it work"';
  else return 'SELECT `tabAccount`.name FROM `tabAccount` WHERE `tabAccount`.company = "'+doc.name+'" AND `tabAccount`.docstatus != 2 AND `tabAccount`.%(key)s LIKE "%s" ORDER BY `tabAccount`.name LIMIT 50';
}

cur_frm.fields_dict.default_receivables_group.get_query = function(doc) {
  if(!doc.__islocal) return 'SELECT `tabAccount`.name FROM `tabAccount` WHERE `tabAccount`.name = "Cheating Query just to make it work"';
  else return 'SELECT `tabAccount`.name FROM `tabAccount` WHERE `tabAccount`.company = "'+doc.name+'" AND `tabAccount`.docstatus != 2 AND `tabAccount`.%(key)s LIKE "%s" ORDER BY `tabAccount`.name LIMIT 50';
}

cur_frm.fields_dict.default_payables_group.get_query = function(doc) {
  if(!doc.__islocal) return 'SELECT `tabAccount`.name FROM `tabAccount` WHERE `tabAccount`.name = "Cheating Query just to make it work"';
  else return 'SELECT `tabAccount`.name FROM `tabAccount` WHERE `tabAccount`.company = "'+doc.name+'" AND `tabAccount`.docstatus != 2 AND `tabAccount`.%(key)s LIKE "%s" ORDER BY `tabAccount`.name LIMIT 50';
}
cur_frm.fields_dict.default_salary_account.get_query = function(doc) {
  if(!doc.__islocal) return 'SELECT `tabAccount`.name FROM `tabAccount` WHERE `tabAccount`.name = "Cheating Query just to make it work"';
  else return 'SELECT `tabAccount`.name FROM `tabAccount` WHERE `tabAccount`.group_or_ledger = 'Ledger' AND `tabAccount`.is_pl_account = 'Yes' AND `tabAccount`.debit_or_credit = 'Debit' AND `tabAccount`.company = "'+doc.name+'" AND `tabAccount`.docstatus != 2 AND `tabAccount`.%(key)s LIKE "%s" ORDER BY `tabAccount`.name LIMIT 50';
}