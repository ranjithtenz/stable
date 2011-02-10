cur_frm.cscript.onload = function(doc, dt, dn) {
  if(!doc.status) set_multiple(dt,dn,{status:'Draft'});
}

cur_frm.fields_dict['item_maintenance_detail'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
  return 'SELECT tabItem.name,tabItem.item_name,tabItem.description FROM tabItem WHERE tabItem.is_service_item="Yes" AND tabItem.docstatus != 2 AND tabItem.%(key)s LIKE "%s" LIMIT 50';
}

cur_frm.cscript.item_code = function(doc, cdt, cdn) {
  var fname = cur_frm.cscript.fname;
  var d = locals[cdt][cdn];
  if (d.item_code) {
    get_server_fields('get_item_details',d.item_code, 'item_maintenance_detail',doc,cdt,cdn,1);
  }
}

cur_frm.fields_dict['contact_person'].get_query = function(doc, cdt, cdn) {
  return 'SELECT `tabContact`.contact_name FROM `tabContact` WHERE `tabContact`.is_customer = 1 AND `tabContact`.customer = "'+ doc.customer+'" AND `tabContact`.contact_name LIKE "%s" ORDER BY `tabContact`.contact_name ASC LIMIT 50';
}

cur_frm.cscript.customer = function(doc, cdt, cdn) {
  get_server_fields('get_customer_details','','',doc, cdt, cdn, 1);
}

cur_frm.fields_dict['sales_order_no'].get_query = function(doc) {
  doc = locals[this.doctype][this.docname];
  var cond = '';
  if(doc.customer) {
    cond = '`tabSales Order`.customer = "'+doc.customer+'" AND';
  }
  //return repl('SELECT DISTINCT `tabSales Order`.name FROM `tabSales Order`, `tabSales Order Detail` WHERE `tabSales Order`.company = "%(company)s" AND `tabSales Order`.docstatus = 1 AND %(cond)s `tabSales Order`.name LIKE "%s" ORDER BY `tabSales Order`.name DESC LIMIT 50', {company:doc.company, cond:cond});
  return repl('SELECT DISTINCT `tabSales Order`.name FROM `tabSales Order`, `tabSales Order Detail`, `tabItem` WHERE `tabSales Order`.company = "%(company)s" AND `tabSales Order`.docstatus = 1 AND `tabSales Order Detail`.parent = `tabSales Order`.name AND `tabSales Order Detail`.item_code = `tabItem`.name AND `tabItem`.is_service_item = "Yes" AND %(cond)s `tabSales Order`.name LIKE "%s" ORDER BY `tabSales Order`.name DESC LIMIT 50', {company:doc.company, cond:cond});
}

cur_frm.cscript.periodicity = function(doc, cdt, cdn){
  var d = locals[cdt][cdn];
  if(d.start_date && d.end_date){
    arg = {}
    arg.start_date = d.start_date;
    arg.end_date = d.end_date;
    arg.periodicity = d.periodicity;
    get_server_fields('get_no_of_visits',docstring(arg),'item_maintenance_detail',doc, cdt, cdn, 1);
  }
  else{
    msgprint("Please enter Start Date and End Date");
  }
}

cur_frm.cscript['Generate Schedule'] = function(doc, cdt, cdn) {
  if (!doc.__islocal) {
    $c('runserverobj', args={'method':'generate_schedule', 'docs':compress_doclist(make_doclist(cdt,cdn))},
      function(r,rt){
        refresh_field('maintenance_schedule_detail');
      }
    );
  } else {
    alert("Please save the document before generating maintenance schedule");
  }  
}

//get query select Territory
//=======================================================================================================================
cur_frm.fields_dict['territory'].get_query = function(doc,cdt,cdn) {
  return 'SELECT `tabTerritory`.`name`,`tabTerritory`.`parent_territory` FROM `tabTerritory` WHERE `tabTerritory`.`is_group` = "No" AND `tabTerritory`.`docstatus`!= 2 AND `tabTerritory`.%(key)s LIKE "%s"  ORDER BY  `tabTerritory`.`name` ASC LIMIT 50';
}