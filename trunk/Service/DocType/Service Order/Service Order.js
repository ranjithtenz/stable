cur_frm.cscript.tname = "Service Order Detail";
cur_frm.cscript.fname = "service_order_details";
cur_frm.cscript.other_fname = "other_charges";
cur_frm.cscript.sales_team_fname = "sales_team";

$import(Sales Common)
$import(Other Charges)

cur_frm.cscript.onload = function(doc, cdt, cdn) {
  if (!doc.note) doc.note = 'ACCEPTED AND CONFIRMED' + NEWLINE + NEWLINE + NEWLINE + NEWLINE + 'Signed and Date';
  if(!doc.transaction_date) set_multiple(cdt,cdn,{transaction_date:get_today()}); 
}

cur_frm.cscript.refresh = function(doc, cdt, cdn) {
  if(!doc.status)
    doc.status = 'Draft'

  if(doc.quotation_type == 'Others')
    unhide_field('others_detail');
  else
    hide_field('others_detail');

  if (!doc.docstatus){
    hide_field(['Send SMS', 'message', 'customer_mobile_no']);
  } else {
    unhide_field(['Send SMS', 'message', 'customer_mobile_no']);
  }
}

cur_frm.fields_dict['contact_person'].get_query = function(doc, cdt, cdn) {
  return 'SELECT `tabContact`.contact_name FROM `tabContact` WHERE `tabContact`.is_customer = 1 AND `tabContact`.customer_name = "'+ doc.customer_name+'" AND `tabContact`.contact_name LIKE "%s" ORDER BY `tabContact`.name ASC LIMIT 50';
}

cur_frm.fields_dict['service_quotation_no'].get_query = function(doc) {
  return 'SELECT DISTINCT `tabService Quotation`.`name` FROM `tabService Quotation` WHERE `tabService Quotation`.company = "' + doc.company + '" and `tabService Quotation`.`docstatus` = 1 and `tabService Quotation`.`status` != "Closed" and `tabService Quotation`.`name` like "%s" ORDER BY `tabService Quotation`.`name` DESC LIMIT 50';
}

// ----------------------pull inquiry date------------------------

cur_frm.cscript.inquiry_no = function(doc, cdt, cdn) {
  get_server_fields('get_inquiry_date', doc.inquiry_no,'',doc, cdt, cdn, 1);
}

//------------------------pull serial details-----------------------------

cur_frm.cscript.serial_no = function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  get_server_fields('get_serial_details', d.serial_no,'service_order_details',doc, cdt, cdn, 1);
}
// -------------------------------set qty and rate ----------------------------

cur_frm.cscript.amount = function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  ret = {'qty':1, 'basic_rate':d.amount};
  set_multiple('Service Order Detail', d.name, ret, 'service_order_details');
  cur_frm.cscript.recalc(doc, 4);
}
// -------------------------------display others detail----------------------------

cur_frm.cscript.order_type = function(doc,cdt,cdn) {
  if (doc.order_type == 'Others') {
    unhide_field('others_detail');
  } else {
    hide_field('others_detail');
  }
}
//----------------------------Validate-------------------------------------------------

cur_frm.cscript.validate = function(doc,cdt,cdn) {
  if (doc.order_type == 'Others' && ! doc.others_detail) {
    validated = false;
    alert("Please enter 'Others Detail'");
  }
}