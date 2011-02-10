cur_frm.cscript.tname = "Installed Item Details";
cur_frm.cscript.fname = "installed_item_details";

cur_frm.cscript.onload = function(doc, dt, dn) {
  if(!doc.status) set_multiple(dt,dn,{status:'Draft'});

  if(doc.__islocal==1){  cur_frm.cscript.price_list_name(doc, cdt, cdn);}
}

//================ create new contact ============================================================================
cur_frm.cscript.new_contact = function(){
  tn = createLocal('Contact');
  locals['Contact'][tn].is_customer = 1;
  if(doc.customer) locals['Contact'][tn].customer = doc.customer;
  loaddoc('Contact', tn);
}

cur_frm.fields_dict['delivery_note_no'].get_query = function(doc) {
  doc = locals[this.doctype][this.docname];
  var cond = '';
  if(doc.customer) {
    cond = '`tabDelivery Note`.customer = "'+doc.customer+'" AND';
  }
  return repl('SELECT DISTINCT `tabDelivery Note`.name FROM `tabDelivery Note`, `tabDelivery Note Detail` WHERE `tabDelivery Note`.company = "%(company)s" AND `tabDelivery Note`.docstatus = 1 AND ifnull(`tabDelivery Note`.per_installed,0) < 100 AND %(cond)s `tabDelivery Note`.name LIKE "%s" ORDER BY `tabDelivery Note`.name DESC LIMIT 50', {company:doc.company, cond:cond});
}

cur_frm.fields_dict['contact_person'].get_query = function(doc, cdt, cdn) {
  return 'SELECT `tabContact`.contact_name FROM `tabContact` WHERE `tabContact`.is_customer = 1 AND `tabContact`.customer = "'+ doc.customer+'" AND `tabContact`.contact_name LIKE "%s" ORDER BY `tabContact`.contact_name ASC LIMIT 50';
}

cur_frm.cscript.customer = function(doc, cdt, cdn) {
  get_server_fields('get_customer_details','','',doc, cdt, cdn, 1);
}

//get query select Territory
//=======================================================================================================================
cur_frm.fields_dict['territory'].get_query = function(doc,cdt,cdn) {
  return 'SELECT `tabTerritory`.`name`,`tabTerritory`.`parent_territory` FROM `tabTerritory` WHERE `tabTerritory`.`is_group` = "No" AND `tabTerritory`.`docstatus`!= 2 AND `tabTerritory`.%(key)s LIKE "%s"  ORDER BY  `tabTerritory`.`name` ASC LIMIT 50';
}