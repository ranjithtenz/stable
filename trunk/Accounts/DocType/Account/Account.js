
cur_frm.cscript.parent_account = function(doc,dt,dn) {
  $c_obj([doc],'get_parent_details','',function(r,rt) {refresh_many(['debit_or_credit','is_pl_account'])} );
}

cur_frm.cscript.account_type = function(doc, cdt, cdn) {
  if(doc.account_type == 'Tax'){
    unhide_field(['tax_rate']);
  }
  else
    hide_field(['tax_rate']);
}

cur_frm.cscript.onload = function(doc, cdt, cdn) {
  cur_frm.cscript.account_type(doc, cdt, cdn)
  myArray = ['Application of Funds','Expenses','Income','Source of Funds']
  if(myArray.indexOf(doc.account_name) != -1){
    if(!doc.__islocal && doc.docstatus == 0){
      set_field_permlevel('parent_account',1);
      refresh_field('parent_account');
      set_field_permlevel('account_type',1);
      refresh_field('account_type');
    }
  }
  
}

cur_frm.fields_dict['master_name'].get_query=function(doc){
 if (doc.master_type){
    return 'SELECT `tab'+doc.master_type+'`.name FROM `tab'+doc.master_type+'` WHERE `tab'+doc.master_type+'`.name LIKE "%s" and `tab'+doc.master_type+'`.docstatus != 2 ORDER BY `tab'+doc.master_type+'`.name LIMIT 50';
  }
  else alert("Please select master type")
}

cur_frm.cscript.master_name = function(doc,cdt,cdn){
  if(doc.master_name){
    get_server_fields('get_address','','',doc,cdt,cdn);
  }
}

cur_frm.fields_dict['parent_account'].get_query = function(doc){
  return 'SELECT DISTINCT `tabAccount`.name FROM `tabAccount` WHERE `tabAccount`.group_or_ledger="Group" AND `tabAccount`.docstatus != 2 AND `tabAccount`.company="'+ doc.company+'" AND `tabAccount`.company is not NULL AND `tabAccount`.name LIKE "%s" ORDER BY `tabAccount`.name LIMIT 50';
}