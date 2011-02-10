//--------------------------------------------------------------------------------------------------------
// Permissions
// Trigger on table fields to check value change 

cur_frm.cscript.level = function(doc, cdt, cdn){
  var d = locals[cdt][cdn];
  if(d.level){
    d.changed = 1;
  }
}



cur_frm.cscript.TreePage = function(nm){
  var call_back = function(){
    var sb_obj = new SalesBrowser();        
    sb_obj.set_val(nm);

  }
  loadpage('Sales Browser',call_back);

}

//get query select Territory
cur_frm.fields_dict['default_territory'].get_query = function(doc,cdt,cdn) {
  return 'SELECT `tabTerritory`.`name`, `tabTerritory`.`parent_territory` FROM `tabTerritory` WHERE `tabTerritory`.`is_group` = "No" AND `tabTerritory`.`docstatus`!= 2 AND `tabTerritory`.%(key)s LIKE "%s" ORDER BY  `tabTerritory`.`name` ASC LIMIT 50';
}

//get query select Customer Group
cur_frm.fields_dict['default_customer_group'].get_query = function(doc,cdt,cdn) {
  return 'SELECT `tabCustomer Group`.`name`, `tabCustomer Group`.`parent_customer_group` FROM `tabCustomer Group` WHERE `tabCustomer Group`.`is_group` = "No" AND `tabCustomer Group`.`docstatus`!= 2 AND `tabCustomer Group`.%(key)s LIKE "%s" ORDER BY  `tabCustomer Group`.`name` ASC LIMIT 50';
}

//get query select item group
cur_frm.fields_dict['default_item_group'].get_query = function(doc,cdt,cdn) {
  return 'SELECT `tabItem Group`.`name`,`tabItem Group`.`parent_item_group` FROM `tabItem Group` WHERE `tabItem Group`.`is_group` = "No" AND `tabItem Group`.`docstatus`!= 2 AND `tabItem Group`.%(key)s LIKE "%s"  ORDER BY  `tabItem Group`.`name` ASC LIMIT 50';
}

cur_frm.cscript.read = function(doc, cdt, cdn){
  var d = locals[cdt][cdn];
  d.changed = 1;
}

cur_frm.cscript.write = function(doc, cdt, cdn){
  var d = locals[cdt][cdn];
  d.changed = 1;
}

cur_frm.cscript.create = function(doc, cdt, cdn){
  var d = locals[cdt][cdn];
  d.changed = 1;
}

cur_frm.cscript.submit = function(doc, cdt, cdn){
  var d = locals[cdt][cdn];
  d.changed = 1;
}

cur_frm.cscript.cancel = function(doc, cdt, cdn){
  var d = locals[cdt][cdn];
  d.changed = 1;
}

cur_frm.cscript.amend = function(doc, cdt, cdn){
  var d = locals[cdt][cdn];
  d.changed = 1;
}

cur_frm.cscript.match = function(doc, cdt, cdn){
  var d = locals[cdt][cdn];
  d.changed = 1;
}

cur_frm.cscript.remove_permission = function(doc, cdt, cdn){
  var d = locals[cdt][cdn];
  d.changed = 1;
}

cur_frm.cscript.select_permission_role = function(doc, cdt, cdn){
  doc.select_doc_for_perm = '';
  doc.for_level = '';
  hide_field('select_doc_for_perm');
  hide_field('for_level');
  hide_field('Add Permission');
  hide_field('Update Permissions');
}

// get doctype list
cur_frm.cscript['Get Doctypes'] = function(doc, cdt, cdn){
  $c('runserverobj', args={'method':'get_doctypes', 'docs':compress_doclist (make_doclist (doc.doctype,doc.name))},
    function(r, rt) {
      refresh_field('role_permissions');
      unhide_field('select_doc_for_perm');
      unhide_field('for_level');
      unhide_field('Add Permission');
      unhide_field('Update Permissions');
    }
  );
}

// Validate
cur_frm.cscript.validate = function(doc, cdt, cdn) {
  $c_obj(make_doclist(cdt, cdn), 'update_cp', '', function(r, rt){
    sys_defaults = r.message;
  });
}