$import(Production Tips Common)

cur_frm.cscript.onload = function(doc, cdt, cdn) {

  cur_frm.cscript.get_tips(doc, cdt, cdn);

  cfn_set_fields(doc, cdt, cdn);

  callback = function(r,rt) { 
    var doc = locals[cdt][cdn];
    if(r.message) { set_field_options('naming_series', NEWLINE+r.message); }
  }
  $c_obj('Naming Series','get_series_options',cdt,callback);
  m_lst = [];
  if(inList(user_roles, 'Material User') || inList(user_roles, 'Material Manager')) 
    m_lst = ['Material Issue', 'Material Receipt', 'Material Transfer', 'Sales Return', 'Purchase Return', 'Subcontracting'];
  if(inList(user_roles, 'Production User') || inList(user_roles, 'Production Manager')) 
    m_lst.push('Production Order')
  if(inList(user_roles, 'Purchase User') || inList(user_roles, 'Purchase Manager'))
    m_lst.concat(['Purchase Return','Subcontracting']);
  set_field_options('purpose', NEWLINE+m_lst.join(NEWLINE));
}
cur_frm.cscript.refresh = function(doc, cdt, cdn) {

  cur_frm.cscript.get_tips(doc, cdt, cdn);

}
var cfn_set_fields = function(doc, cdt, cdn) {
  lst = ['supplier','supplier_name','supplier_address','customer','customer_name','customer_address']; 
  if (doc.purpose == 'Production Order'){
    unhide_field(['production_order', 'process', 'Get Items']);
    hide_field(['from_warehouse', 'to_warehouse','purchase_receipt_no','delivery_note_no','Warehouse HTML']);
    doc.from_warehouse = '';
    doc.to_warehosue = '';
    if (doc.process == 'Backflush'){
      unhide_field('fg_completed_qty');
    }
    else{
      hide_field('fg_completed_qty');
      doc.fg_completed_qty = 0;
    }
  }
  else{
    unhide_field(['from_warehouse', 'to_warehouse']);
    hide_field(['production_order', 'process', 'Get Items', 'fg_completed_qty','purchase_receipt_no','delivery_note_no']);
    hide_field(lst);
    doc.production_order = '';
    doc.process = '';
    doc.fg_completed_qty = 0;
  }
  
 
  if(doc.purpose == 'Purchase Return'){
    doc.customer=doc.customer_name = doc.customer_address=doc.delivery_note_no='';
    hide_field(lst);
    unhide_field(['supplier','supplier_name','supplier_address','purchase_receipt_no']);
  }
  if(doc.purpose == 'Sales Return'){
    doc.supplier=doc.supplier_name = doc.supplier_address=doc.purchase_receipt_no='';
    hide_field(lst);
    unhide_field(['customer','customer_name','customer_address','delivery_note_no']);
  }
  else{
      doc.customer=doc.customer_name=doc.customer_address=doc.delivery_note_no=doc.supplier=doc.supplier_name = doc.supplier_address=doc.purchase_receipt_no='';
  }
  refresh_many(lst);
}

cur_frm.cscript.delivery_note_no = function(doc,cdt,cdn){
  if(doc.delivery_note_no) get_server_fields('get_cust_values','','',doc,cdt,cdn,1);
}

cur_frm.cscript.customer = function(doc,cdt,cdn){
  if(doc.customer)  get_server_fields('get_cust_addr','','',doc,cdt,cdn,1);
}

cur_frm.cscript.purchase_receipt_no = function(doc,cdt,cdn){
  if(doc.purchase_receipt_no)  get_server_fields('get_supp_values','','',doc,cdt,cdn,1);
}

cur_frm.cscript.supplier = function(doc,cdt,cdn){
  if(doc.supplier)  get_server_fields('get_supp_addr','','',doc,cdt,cdn,1);

}

cur_frm.fields_dict['production_order'].get_query = function(doc) {
   return 'SELECT DISTINCT `tabProduction Order`.`name` FROM `tabProduction Order` WHERE `tabProduction Order`.`docstatus` = 1 AND `tabProduction Order`.`qty` > ifnull(`tabProduction Order`.`produced_qty`,0) AND `tabProduction Order`.`name` like "%s" ORDER BY `tabProduction Order`.`name` DESC LIMIT 50';
}

cur_frm.cscript.purpose = function(doc, cdt, cdn) {
  cfn_set_fields(doc, cdt, cdn);
}


cur_frm.cscript.process = function(doc, cdt, cdn) {
  cfn_set_fields(doc, cdt, cdn);
}


//========================= Overloaded query for link batch_no =============================================================
cur_frm.fields_dict['mtn_details'].grid.get_field('batch_no').get_query= function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  if(d.item_code){
    return "SELECT tabBatch.name FROM tabBatch WHERE tabBatch.is_active='Yes' AND tabBatch.item = '"+ d.item_code +"' AND `tabBatch`.`name` like '%s' ORDER BY `tabBatch`.`name` DESC LIMIT 50"
  }
  else{
    alert("Please enter Item Code.");
  }
}

//==================================================================================================================

cur_frm.cscript.item_code = function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  cal_back = function(doc){ /*cur_frm.cscript.calc_amount(doc)*/}
  // get values
  str_arg = "{'item_code': '" + d.item_code + "', 'warehouse': '" + (cstr(doc.purpose) != 'Production Order' ? cstr(doc.from_warehouse): cstr(d.s_warehouse)) + "'}";
  get_server_fields('get_item_details',str_arg,'mtn_details',doc,cdt,cdn,1,cal_back);
}

//==================================================================================================================

cur_frm.cscript.transfer_qty = function(doc,cdt,cdn) {
  var d = locals[cdt][cdn];
  if (doc.from_warehouse && (flt(d.transfer_qty) > flt(d.actual_qty))) {
    alert("Transfer Quantity is more than Available Qty");
  }
}


//==================================================================================================================

cur_frm.cscript.qty = function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  set_multiple('Stock Entry Detail', d.name, {'transfer_qty': flt(d.qty) * flt(d.conversion_factor)}, 'mtn_details');
  refresh_field('mtn_details');
}

//==================================================================================================================

cur_frm.cscript.uom = function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  if(d.uom && d.item_code){
    var arg = {'item_code':d.item_code, 'uom':d.uom, 'qty':d.qty}
    get_server_fields('get_uom_details',JSON.stringify(arg),'mtn_details', doc, cdt, cdn, 1);
  }
}