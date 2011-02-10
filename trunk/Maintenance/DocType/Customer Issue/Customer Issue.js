cur_frm.cscript.onload = function(doc,cdt,cdn){
  if(user == 'Guest'){
    hide_field(['status', 'fiscal_year', 'customer', 'customer_name', 'customer_group', 'customer_address', 'contact_person',  'territory', 'company', 'item_code', 'item_name', 'description', 'allocated_on', 'allocated_to', 'resolution_details', 'resolution_date', 'resolved_by', 'Resolution Detail', 'Make Maintenance Visit', 'Next Steps', 'complaint_date', 'service_address']);
  }
  if(!doc.status) set_multiple(dt,dn,{status:'Open'});  
}

cur_frm.cscript.refresh = function(doc,ct,cdn){
  if(!doc.docstatus) hide_field('Make Maintenance Visit');
  else if(doc.docstatus && (doc.status == 'Open' || doc.status == 'Work In Progress')) unhide_field('Make Maintenance Visit');
}

cur_frm.cscript['Make Maintenance Visit'] = function(doc, cdt, cdn) {
  if (doc.docstatus == 1) { 
    $c_obj(make_doclist(doc.doctype, doc.name),'check_maintenance_visit','',
      function(r,rt){
        if(r.message == 'No'){
          n = createLocal("Maintenance Visit");
          $c('dt_map', args={
                  'docs':compress_doclist([locals["Maintenance Visit"][n]]),
                  'from_doctype':'Customer Issue',
                  'to_doctype':'Maintenance Visit',
                  'from_docname':doc.name,
            'from_to_list':"[['Customer Issue', 'Maintenance Visit'], ['Customer Issue', 'Maintenance Visit Detail']]"
          }
          , function(r,rt) {
            loaddoc("Maintenance Visit", n);
          }
          );
        }
        else{
          msgprint("You have already completed maintenance against this Customer Issue");
        }
      }
    );
  }
}
 
cur_frm.cscript.customer = function(doc, cdt, cdn) {
  if (doc.customer)
    get_server_fields('get_customer_details','','',doc,cdt,cdn,1);
}

cur_frm.cscript.contact_person = function(doc, cdt, cdn) {
  if(doc.contact_person) {
    var arg = {'customer':doc.customer,'contact_person':doc.contact_person};
    get_server_fields('get_contact_details',docstring(arg),'',doc, cdt, cdn, 1);
  }
}

cur_frm.fields_dict['contact_person'].get_query = function(doc, cdt, cdn) {
  return 'SELECT `tabContact`.contact_name, `tabContact`.email_id FROM `tabContact` WHERE `tabContact`.is_customer = 1 AND `tabContact`.docstatus != 2 AND `tabContact`.customer = "'+ doc.customer +'" AND `tabContact`.docstatus != 2 AND `tabContact`.contact_name LIKE "%s" ORDER BY `tabContact`.contact_name ASC LIMIT 50';
}

cur_frm.cscript.item_code = function(doc,cdt,cdn){
  get_server_fields('get_item_name','','',doc,cdt,cdn,1);  
}

//get query select Territory
//=======================================================================================================================
cur_frm.fields_dict['territory'].get_query = function(doc,cdt,cdn) {
  return 'SELECT `tabTerritory`.`name`,`tabTerritory`.`parent_territory` FROM `tabTerritory` WHERE `tabTerritory`.`is_group` = "No" AND `tabTerritory`.`docstatus`!= 2 AND `tabTerritory`.%(key)s LIKE "%s"  ORDER BY  `tabTerritory`.`name` ASC LIMIT 50';
}