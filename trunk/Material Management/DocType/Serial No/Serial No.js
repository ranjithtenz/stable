$import(Tips Common)

//--------- ONLOAD -------------
cur_frm.cscript.onload = function(doc, cdt, cdn) {
  cur_frm.cscript.get_tips(doc, cdt, cdn);
}

cur_frm.cscript.refresh = function(doc, cdt, cdn) {
  cur_frm.cscript.get_tips(doc, cdt, cdn);
}

cur_frm.cscript.item_code = function(doc, cdt, cdn) {
  get_server_fields('get_item_details','', '',doc,cdt,cdn,1);
}

cur_frm.cscript.customer = function(doc, cdt, cdn) {
  get_server_fields('get_customer_details','','',doc, cdt, cdn, 1);
}

cur_frm.cscript.delivery_note_no = function(doc,cdt,cdn){
  get_server_fields('get_delivery_details','','',doc,cdt,cdn,1);
}

cur_frm.cscript.pr_no = function(doc,cdt,cdn){
  get_server_fields('get_purchase_details','','',doc,cdt,cdn,1);
}

cur_frm.fields_dict['delivery_note_no'].get_query = function(doc) {
  var cond = '';
  if(doc.customer) {
    cond = '`tabDelivery Note`.customer = "'+doc.customer+'" AND';
  }
  return repl('SELECT DISTINCT `tabDelivery Note`.name FROM `tabDelivery Note` WHERE `tabDelivery Note`.docstatus = 1 AND %(cond)s `tabDelivery Note`.name LIKE "%s" ORDER BY `tabDelivery Note`.name DESC LIMIT 50', {cond:cond});
}

cur_frm.fields_dict['pr_no'].get_query = function(doc) {
  return repl('SELECT DISTINCT `tabPurchase Receipt`.name FROM `tabPurchase Receipt` WHERE `tabPurchase Receipt`.docstatus = 1 AND `tabPurchase Receipt`.name LIKE "%s" ORDER BY `tabPurchase Receipt`.name DESC LIMIT 50');
}

//get query select Territory
//=======================================================================================================================
cur_frm.fields_dict['territory'].get_query = function(doc,cdt,cdn) {
  return 'SELECT `tabTerritory`.`name`,`tabTerritory`.`parent_territory` FROM `tabTerritory` WHERE `tabTerritory`.`is_group` = "No" AND `tabTerritory`.`docstatus`!= 2 AND `tabTerritory`.%(key)s LIKE "%s"  ORDER BY  `tabTerritory`.`name` ASC LIMIT 50';
}