cur_frm.cscript.tname = "Service Quotation Detail";
cur_frm.cscript.fname = "service_quotation_details";
cur_frm.cscript.other_fname = "other_charges";
cur_frm.cscript.sales_team_fname = "sales_team";

$import(Sales Common)
$import(Other Charges)

// ONLOAD
// ===================================================================================
cur_frm.cscript.onload = function(doc, cdt, cdn) {

  if(!doc.price_list_name) set_multiple(cdt,cdn,{price_list_name:sys_defaults.price_list_name});
  if(!doc.status) set_multiple(cdt,cdn,{status:'Draft'});
  if(!doc.transaction_date) set_multiple(cdt,cdn,{transaction_date:get_today()});
  if(!doc.conversion_rate) set_multiple(cdt,cdn,{conversion_rate:'1.00'});
  if(!doc.currency && sys_defaults.currency) set_multiple(cdt,cdn,{currency:sys_defaults.currency});
  //if(!doc.price_list_name && sys_defaults.price_list_name) set_multiple(cdt,cdn,{price_list_name:sys_defaults.price_list_name});
  if(!doc.company && sys_defaults.company) set_multiple(cdt,cdn,{company:sys_defaults.company});
  if(!doc.fiscal_year && sys_defaults.fiscal_year) set_multiple(cdt,cdn,{fiscal_year:sys_defaults.fiscal_year});  

  // set naming series
  callback = function(r,rt) {
    if(r.message) 
    { 
      set_field_options('naming_series', NEWLINE+r.message);
      
    } 
    if(doc.__islocal==1){  cur_frm.cscript.price_list_name(doc, cdt, cdn);}
  }
  $c_obj('Naming Series','get_series_options',cdt,callback);
}

cur_frm.cscript.refresh = function(doc, cdt, cdn) {
  if(!doc.status)
    doc.status = 'Draft';
  if(doc.quotation_type == 'Others')
    unhide_field('others_detail');
  
  if(doc.docstatus == 1 && doc.status != 'Closed')
    unhide_field(['Make Service Order','Send SMS', 'message', 'customer_mobile_no']);
  else
    hide_field(['Make Service Order','Send SMS', 'message', 'customer_mobile_no']);
    
  if(inList(user_roles, 'CRM Manager')) {
    hide_field('Send For Approval');
    unhide_field('Send Feedback');
  }
  else {
    unhide_field('Send For Approval');
    hide_field('Send Feedback');
  }
}

cur_frm.fields_dict['contact_person'].get_query = function(doc, cdt, cdn) {
  return 'SELECT `tabContact`.contact_name FROM `tabContact` WHERE `tabContact`.is_customer = 1 AND `tabContact`.customer_name = "'+ doc.customer_name+'" AND `tabContact`.contact_name LIKE "%s" ORDER BY `tabContact`.name ASC LIMIT 50';
}

cur_frm.fields_dict['enq_no'].get_query = function(doc,cdt,cdn){
  return 'SELECT `tabEnquiry`.`name` FROM `tabEnquiry` WHERE `tabEnquiry`.`enquiry_type` = "Service" AND `tabEnquiry`.`name` LIKE "%s" ORDER BY `tabEnquiry`.`name` ASC LIMIT 50';
}

/*----------------Make Service Order Mapper-------------------------------------------------------------------------*/

cur_frm.cscript['Make Service Order'] = function(doc, cdt, cdn) {
  if (doc.docstatus == 1) { 
  n = createLocal("Service Order");
  $c('dt_map', args={
	  'docs':compress_doclist([locals["Service Order"][n]]),
	  'from_doctype':'Service Quotation',
	  'to_doctype':'Service Order',
	  'from_docname':doc.name,
    'from_to_list':"[['Service Quotation', 'Service Order'], ['Service Quotation Detail', 'Service Order Detail'],['RV Tax Detail','RV Tax Detail'], ['Sales Team', 'Sales Team'],['TC Detail','TC Detail']]"
  }
  , function(r,rt) {
    loaddoc("Service Order", n);
    }
    );
  }
}

//------------------------pull serial details-----------------------------

cur_frm.cscript.serial_no = function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  get_server_fields('get_serial_details', d.serial_no,'service_quotation_details',doc, cdt, cdn, 1);
}


// -------------------------------set qty and rate ----------------------------

cur_frm.cscript.amount = function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  ret = {'qty':1, 'basic_rate':d.amount};
  set_multiple('Service Quotation Detail', d.name, ret, 'service_quotation_details');
  cur_frm.cscript.recalc(doc, 4);
}

// -------------------------------display others detail----------------------------

cur_frm.cscript.quotation_type = function(doc,cdt,cdn) {
  if (doc.quotation_type == 'Others') {
    unhide_field('others_detail');
  } else {
    hide_field('others_detail');
  }
}
//----------------------------Validate-------------------------------------------------

cur_frm.cscript.validate = function(doc,cdt,cdn) {
  if (doc.quotation_type == 'Others' && ! doc.others_detail) {
    msgprint("Please enter 'Others Detail' in 'Quotation'");
    validated = false;
  }
}