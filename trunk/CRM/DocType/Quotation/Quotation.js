// Module CRM
cur_frm.cscript.tname = "Quotation Detail";
cur_frm.cscript.fname = "quotation_details";
cur_frm.cscript.other_fname = "other_charges";
cur_frm.cscript.sales_team_fname = "sales_team";

// =====================================================================================
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
      //locals[cdt][cdn].naming_series = r.message.split(NEWLINE)[0]; 
      set_field_options('naming_series', NEWLINE+r.message);
    } 
    if(doc.__islocal==1){  cur_frm.cscript.price_list_name(doc, cdt, cdn);}
  }
  $c_obj('Naming Series','get_series_options',cdt,callback);
}


// hide - unhide fields based on lead or customer..
//=======================================================================================================================
cur_frm.cscript.lead_cust_show = function(doc,cdt,cdn){

  if(doc.quotation_to == 'Lead'){
    unhide_field(['lead','customer_address','lead_name','territory','Territory Help']);
    hide_field(['customer','customer_name','contact_person','customer_group', 'Contact Help']);

    doc.customer = doc.customer_name = doc.contact_person = doc.customer_group = "";
  }
  else if(doc.quotation_to == 'Customer'){
    hide_field(['lead','lead_name']);
    unhide_field(['customer','customer_name','customer_address','contact_person', 'Contact Help','territory','Territory Help', 'customer_group']);
    doc.lead =  doc.lead_name = "";
  }
  else{ 
    hide_field(['lead','lead_name','customer','customer_name','customer_address','contact_person', 'Contact Help','territory','customer_group','Territory Help']);
    doc.lead = doc.lead_name = doc.customer = doc.customer_name = doc.contact_person = "";
  }
  refresh_many(['lead','lead_name','customer','customer_name','contact_person','customer_group']);

}

//================ hide - unhide fields on basis of quotation to either lead or customer =============================== 
cur_frm.cscript.quotation_to = function(doc,cdt,cdn){

  cur_frm.cscript.lead_cust_show(doc,cdt,cdn);
  doc.customer_address = doc.territory = doc.contact_no = doc.email_id = "";
  refresh_many(['territory','customer_address','contact_no','email_id']);
}

// REFRESH
// ===================================================================================
cur_frm.cscript.refresh = function(doc, cdt, cdn) {

  cur_frm.clear_custom_buttons();

  if(doc.docstatus == 1 && doc.status!='Order Lost') {
    cur_frm.add_custom_button('Make Sales Order', cur_frm.cscript['Make Sales Order'])
    cur_frm.add_custom_button('Set as Lost', cur_frm.cscript['Declare Order Lost'])
  }
  
  if (!doc.docstatus) hide_field(['Send SMS', 'message', 'customer_mobile_no', 'Update Follow up']);
  else unhide_field(['Send SMS', 'message', 'customer_mobile_no', 'Update Follow up']);
  cur_frm.cscript.lead_cust_show(doc,cdt,cdn);
}

// ============== Lead and its Details ============================
cur_frm.cscript.lead = function(doc, cdt, cdn) {
  if(doc.lead) get_server_fields('get_lead_details', doc.lead,'', doc, cdt, cdn, 1);
}

//================ create new contact ============================================================================
cur_frm.cscript.new_contact = function(){
  tn = createLocal('Contact');
  locals['Contact'][tn].is_customer = 1;
  if(doc.customer) locals['Contact'][tn].customer = doc.customer;
  loaddoc('Contact', tn);
}


// DOCTYPE TRIGGERS
// ====================================================================================


// ***************** Get Contact Person based on customer selected *****************
cur_frm.fields_dict['contact_person'].get_query = function(doc, cdt, cdn) {
  return 'SELECT `tabContact`.contact_name, `tabContact`.email_id FROM `tabContact` WHERE `tabContact`.is_customer = 1 AND `tabContact`.docstatus != 2 AND `tabContact`.customer = "'+ doc.customer +'" AND `tabContact`.docstatus != 2 AND `tabContact`.contact_name LIKE "%s" ORDER BY `tabContact`.contact_name ASC LIMIT 50';
}

// =====================================================================================
cur_frm.fields_dict['enq_no'].get_query = function(doc,cdt,cdn){
  var cond='';
  var cond1='';
  if(doc.order_type) cond = 'ifnull(`tabEnquiry`.enquiry_type, "") = "'+doc.order_type+'" AND';
  if(doc.customer) cond1 = '`tabEnquiry`.customer = "'+doc.customer+'" AND';
  else if(doc.lead) cond1 = '`tabEnquiry`.lead = "'+doc.lead+'" AND';
  
  return repl('SELECT `tabEnquiry`.`name` FROM `tabEnquiry` WHERE `tabEnquiry`.`docstatus` = 1 AND `tabEnquiry`.status = "Submitted" AND %(cond)s %(cond1)s `tabEnquiry`.`name` LIKE "%s" ORDER BY `tabEnquiry`.`name` ASC LIMIT 50', {cond:cond, cond1:cond1});
}

// Make Sales Order
// =====================================================================================
cur_frm.cscript['Make Sales Order'] = function() {
  var doc = cur_frm.doc;

  if (doc.docstatus == 1) { 
  n = createLocal("Sales Order");
  $c('dt_map', args={
	  'docs':compress_doclist([locals["Sales Order"][n]]),
	  'from_doctype':'Quotation',
	  'to_doctype':'Sales Order',
	  'from_docname':doc.name,
    'from_to_list':"[['Quotation', 'Sales Order'], ['Quotation Detail', 'Sales Order Detail'],['RV Tax Detail','RV Tax Detail'], ['Sales Team', 'Sales Team'], ['TC Detail', 'TC Detail']]"
  }
  , function(r,rt) {
    loaddoc("Sales Order", n);
    }
    );
  }
}

//pull enquiry details
cur_frm.cscript['Pull Enquiry Detail'] = function(doc,cdt,cdn){

  var callback = function(r,rt){
    if(r.message){
      doc.quotation_to = r.message;
      refresh_field('quotation_to');
      cur_frm.cscript.lead_cust_show(doc,cdt,cdn);
      refresh_many(['quotation_details','lead','lead_name','customer','customer_name','contact_person','customer_group','territory','customer_address','contact_no','email_id','territory']);
    }
  }
    
  doc.quotation_to = doc.lead = doc.lead_name =doc.customer = doc.customer_name = doc.contact_person = "";
  doc.customer_address = doc.customer_group = doc.territory = doc.email_id = doc.contact_no = "";
  refresh_many(['quotation_to','lead','lead_name','customer','customer_name','contact_person','customer_group','territory','customer_address','contact_no','email_id','territory']);
    cur_frm.cscript.lead_cust_show(doc,cdt,cdn);
  $c_obj(make_doclist(doc.doctype, doc.name),'pull_enq_details','',callback);

}
//update follow up
//=================================================================================
cur_frm.cscript['Update Follow up'] = function(doc){

  $c_obj(make_doclist(doc.doctype, doc.name),'update_followup_details','',function(r, rt){
    refresh_field('follow_up');
    doc.__unsaved = 0;
    cur_frm.refresh_header();
  });
}


// declare order lost
//-------------------------
cur_frm.cscript['Declare Order Lost'] = function(){
  var qtn_lost_dialog;
  
  set_qtn_lost_dialog = function(doc,cdt,cdn){
    qtn_lost_dialog = new Dialog(400,400,'Add Quotation Lost Reason');
    qtn_lost_dialog.make_body([
      ['HTML', 'Message', '<div class="comment">Please add quotation lost reason</div>'],
      ['Text', 'Quotation Lost Reason'],
      ['HTML', 'Response', '<div class = "comment" id="update_quotation_dialog_response"></div>'],
      ['HTML', 'Add Reason', '<div></div>']
    ]);
    
    var add_reason_btn1 = $a($i(qtn_lost_dialog.widgets['Add Reason']), 'button', 'button');
    add_reason_btn1.innerHTML = 'Add';
    add_reason_btn1.onclick = function(){ qtn_lost_dialog.add(); }
    
    var add_reason_btn2 = $a($i(qtn_lost_dialog.widgets['Add Reason']), 'button', 'button');
    add_reason_btn2.innerHTML = 'Cancel';
    $y(add_reason_btn2,{marginLeft:'4px'});
    add_reason_btn2.onclick = function(){ qtn_lost_dialog.hide();}
    
    qtn_lost_dialog.onshow = function() {
      qtn_lost_dialog.widgets['Quotation Lost Reason'].value = '';
      $i('update_quotation_dialog_response').innerHTML = '';
    }
    
    qtn_lost_dialog.add = function() {
      // sending...
      $i('update_quotation_dialog_response').innerHTML = 'Processing...';
      var arg =  strip(qtn_lost_dialog.widgets['Quotation Lost Reason'].value);
      var call_back = function(r,rt) { 
        if(r.message == 'true'){
          $i('update_quotation_dialog_response').innerHTML = 'Done';
          qtn_lost_dialog.hide();
        }
      }
      if(arg) $c_obj(make_doclist(cur_frm.doc.doctype, cur_frm.doc.name),'declare_order_lost',arg,call_back);
      else msgprint("Please add Quotation lost reason");
    }
  }  
  
  if(!qtn_lost_dialog){
    set_qtn_lost_dialog(doc,cdt,cdn);
  }  
  qtn_lost_dialog.show();
}


// GET REPORT
// ========================================================================================
cur_frm.cscript['Get Report'] = function(doc,cdt,cdn) {
  var callback = function(report){
  report.set_filter('Sales Order Detail', 'Quotation No.',doc.name)
  report.dt.run();
 }
 loadreport('Sales Order Detail','Itemwise Sales Details', callback);
}

// lead get query
//=======================================================================================================================
cur_frm.fields_dict['lead'].get_query = function(doc,cdt,cdn){
  return 'SELECT `tabLead`.name, `tabLead`.lead_name FROM `tabLead` WHERE `tabLead`.%(key)s LIKE "%s"  ORDER BY  `tabLead`.`name` ASC LIMIT 50';
}

//get query select Territory
cur_frm.fields_dict['territory'].get_query = function(doc,cdt,cdn) {
  return 'SELECT `tabTerritory`.`name`,`tabTerritory`.`parent_territory` FROM `tabTerritory` WHERE `tabTerritory`.`is_group` = "No" AND `tabTerritory`.`docstatus`!= 2 AND `tabTerritory`.%(key)s LIKE "%s"  ORDER BY  `tabTerritory`.`name` ASC LIMIT 50';}

//===================== Quotation to validation - either customer or lead mandatory ====================
cur_frm.cscript.quot_to_validate = function(doc,cdt,cdn){
  
  if(doc.quotation_to == 'Lead'){
  
    if(!doc.lead){
      alert("Lead is mandatory.");  
      validated = false; 
    }
  }
  else if(doc.quotation_to == 'Customer'){
   
    if(!doc.customer){
      alert("Customer is mandatory.");
      validated = false;
    }
    else if(!doc.contact_person){
      alert("Contact Person is mandatory.");
      validated = false;
    }
    else if(!doc.customer_group){
      alert("Customer Group is mandatory.");
      validated = false;
    }
  } 
}

//===================validation function =================================

cur_frm.cscript.validate = function(doc,cdt,cdn){
  cur_frm.cscript.quot_to_validate(doc,cdt,cdn);
}