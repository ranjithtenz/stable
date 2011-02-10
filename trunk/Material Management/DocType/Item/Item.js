
// ONLOAD
// ===================================================================================
cur_frm.cscript.onload = function(doc, cdt, cdn) {
  //
}

cur_frm.fields_dict['default_bom'].get_query = function(doc) {
   //var d = locals[this.doctype][this.docname];
   return 'SELECT DISTINCT `tabBill Of Materials`.`name` FROM `tabBill Of Materials` WHERE `tabBill Of Materials`.`item` = "' + doc.item_code + '"  AND `tabBill Of Materials`.`is_active` = "No" and `tabBill Of Materials`.docstatus != 2 AND `tabBill Of Materials`.%(key)s LIKE "%s" ORDER BY `tabBill Of Materials`.`name` LIMIT 50';
}

cur_frm.fields_dict['purchase_account'].get_query = function(doc){ 
  if (doc.is_purchase_item == 'Yes') account_type = "Expense Account";
  if (doc.is_asset_item == 'Yes') account_type = "Asset Account";
  return 'SELECT DISTINCT `tabAccount`.`name` FROM `tabAccount` WHERE `tabAccount`.docstatus != 2 AND `tabAccount`.`group_or_ledger` = "Ledger" AND `tabAccount`.`account_type` = account_type AND `tabAccount`.`account_name` like "%s" ORDER BY `tabAccount`.`account_name` LIMIT 50';
}

cur_frm.cscript['Get Report'] = function(doc,cdt,cdn) {
  var query = 
   'SELECT '+
   ' `tabBin`.`warehouse`,'+
   ' `tabBin`.`valuation_rate`,'+
   ' `tabBin`.`actual_qty`,'+
   ' `tabBin`.`ordered_qty`,'+
   ' `tabBin`.`reserved_qty`,'+
   ' `tabBin`.`indented_qty`'+
   ' FROM '+
   ' `tabBin`'+
   ' WHERE '+
   ' `tabBin`.`item_code` = "' + doc.name + '"'+
   'GROUP BY ' + 
   ' `tabBin`.`warehouse`'
   ' ORDER BY '+
   ' `tabBin`.`warehouse`';

  show_data_table('Output HTML', query, '500px');
}

cur_frm.fields_dict['item_tax'].grid.get_field("tax_type").get_query = function(doc, cdt, cdn) {
  return 'SELECT tabAccount.name FROM tabAccount WHERE tabAccount.account_type="Tax" and tabAccount.docstatus != 2 and tabAccount.%(key)s LIKE "%s" ORDER BY tabAccount.name DESC LIMIT 50'
}

cur_frm.cscript.tax_type = function(doc, cdt, cdn){
  var d = locals[cdt][cdn];
  get_server_fields('get_tax_rate',d.tax_type,'item_tax',doc, cdt, cdn, 1);
}

cur_frm.cscript.file_name = function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  // get values
  str_arg = "{'file_name': '" + d.file_name + "'}";
  get_server_fields('get_file_details',str_arg,'item_attachments_details',doc,cdt,cdn,1);
}

cur_frm.cscript.create_new_file = function(){
  newdoc('File');
}

//get query select item group
cur_frm.fields_dict['item_group'].get_query = function(doc,cdt,cdn) {
  return 'SELECT `tabItem Group`.`name`,`tabItem Group`.`parent_item_group` FROM `tabItem Group` WHERE `tabItem Group`.`is_group` = "No" AND `tabItem Group`.`docstatus`!= 2 AND `tabItem Group`.%(key)s LIKE "%s"  ORDER BY  `tabItem Group`.`name` ASC LIMIT 50';
}


cur_frm.cscript.IGHelp = function(doc,dt,dn){
  var call_back = function(){
    var sb_obj = new SalesBrowser();        
    sb_obj.set_val('Item Group');

  }
  loadpage('Sales Browser',call_back);
  
}