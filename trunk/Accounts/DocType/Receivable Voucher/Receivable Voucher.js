
cur_frm.cscript.tname = "RV Detail";
cur_frm.cscript.fname = "entries";
cur_frm.cscript.other_fname = "other_charges";
cur_frm.cscript.sales_team_fname = "sales_team";

// print heading
cur_frm.pformat.print_heading = 'Invoice';

$import(Sales Common)
$import(Other Charges)

// On Load
// -------
cur_frm.cscript.onload = function(doc,dt,dn) {

  if(!doc.voucher_date) set_multiple(dt,dn,{voucher_date:get_today()});
  if(!doc.posting_date) set_multiple(dt,dn,{posting_date:get_today()});

  // print hide debit to
  if(doc.customer) get_field(dt, 'debit_to', dn).print_hide = 1;

  if(doc.customer && !doc.debit_to) get_server_fields('get_debit_to','','',doc,dt,dn);
}


// Refresh
// -------
cur_frm.cscript.refresh = function(doc, dt, dn) {

  // Show / Hide button
  cur_frm.clear_custom_buttons();
    
  if(doc.docstatus==1) { 
    cur_frm.add_custom_button('View Ledger', cur_frm.cscript['View Ledger Entry']);
    unhide_field('Repair Outstanding Amt');
    
    if(doc.is_pos==1 && doc.update_stock!=1)
      cur_frm.add_custom_button('Make Delivery', cur_frm.cscript['Make Delivery Note']);
  
    if(doc.outstanding_amount!=0)
      cur_frm.add_custom_button('Make Payment Entry', cur_frm.cscript['Make Bank Voucher']);
  }
  else  
    hide_field('Repair Outstanding Amt');
  cur_frm.cscript.is_opening(doc, dt, dn);
}


//fetch retail transaction related fields
//--------------------------------------------
cur_frm.cscript.is_pos = function(doc,dt,dn){

  if(doc.is_pos == 1){
    
    var callback = function(r,rt){
      
      refresh_many(['debit_to','territory','naming_series','currency','conversion_rate','charge','letter_head','tc_name','price_list_name','company','select_print_heading','terms','other_charges','cash_bank_account']);

    }
    $c_obj(make_doclist(dt,dn),'set_pos_fields','',callback);
  }
}


//refresh advance amount
//-------------------------------------------------

cur_frm.cscript.paid_amount = function(doc,dt,dn){
  doc.outstanding_amount = flt(doc.grand_total) - flt(doc.paid_amount);
  refresh_field('outstanding_amount');
}

// ---------------------- Get project name --------------------------
cur_frm.fields_dict['project_name'].get_query = function(doc, cdt, cdn) {
  var cond = '';
  if(doc.customer) cond = '(`tabProject`.customer = "'+doc.customer+'" OR IFNULL(`tabProject`.customer,"")="") AND';
  return repl('SELECT `tabProject`.name FROM `tabProject` WHERE `tabProject`.status = "Open" AND %(cond)s `tabProject`.name LIKE "%s" ORDER BY `tabProject`.name ASC LIMIT 50', {cond:cond});
}

//---- get customer details ----------------------------
cur_frm.cscript.project_name = function(doc,cdt,cdn){
	$c_obj(make_doclist(doc.doctype, doc.name),'pull_project_customer','', function(r,rt){
	  refresh_many(['customer', 'customer_name','customer_address', 'territory']);
	});
}

//Set debit and credit to zero on adding new row
//----------------------------------------------
cur_frm.fields_dict['entries'].grid.onrowadd = function(doc, cdt, cdn){
  
  cl = getchildren('RV Detail', doc.name, cur_frm.cscript.fname, doc.doctype);
  acc = '';
  cc = '';

  for(var i = 0; i<cl.length; i++) {
    
    if (cl[i].idx == 1){
      acc = cl[i].income_account;
      cc = cl[i].cost_center;
    }
    else{
      if (! cl[i].income_account) { cl[i].income_account = acc; refresh_field('income_account', cl[i].name, 'entries');}
      if (! cl[i].cost_center)  {cl[i].cost_center = cc;refresh_field('cost_center', cl[i].name, 'entries');}
    }
  }
}

cur_frm.cscript.is_opening = function(doc, dt, dn) {
  hide_field('aging_date');
  if (doc.is_opening == 'Yes') unhide_field('aging_date');
}

/* **************************** TRIGGERS ********************************** */

// Set Due Date = posting date + credit days
// -----------------------------------------
cur_frm.cscript.debit_to = function(doc,dt,dn) {

  var callback = function(r,rt){

    refresh_many(['sales_team','customer','customer_name','customer_address','territory','sales_partner','commission_rate','due_date']);
  }
  if(doc.debit_to && doc.posting_date){
    get_server_fields('get_cust_and_due_date','','',doc,dt,dn,1,callback);
  }
}


// Posting Date
// ------------
cur_frm.cscript.posting_date = cur_frm.cscript.debit_to;


// Customer
// --------
cur_frm.cscript.customer = function(doc,dt,dn) {

  if(doc.customer) {
    // print hide debit_to
    get_field(dt, 'debit_to', dn).print_hide = 1;
    var callback = function(r, rt){
      refresh_field('sales_team');
      if(doc.debit_to) cur_frm.cscript.debit_to(doc,dt,dn);
    }
    get_server_fields('pull_cust_details','','',doc, cdt, cdn, 1, callback);
  } 
  else{
    doc.customer_name = '';
    doc.customer_address = '';
  }
  refresh_many(['customer_name','customer_address','territory']);
  
}


// Get Items based on SO or DN Selected
// -------------------------------------
cur_frm.cscript['Get Items'] = function(doc, dt, dn) {
  $c_obj(make_doclist(doc.doctype,doc.name),'pull_details','',
    function(r, rt) {
      //var d = locals[doc.doctype][doc.name];
      doc.sales_order_main = '';
      doc.delivery_note_main = '';
      refresh_field('sales_order_main');
      refresh_field('delivery_note_main');
      refresh_field('entries');
    }
  );
}


// Allocated Amount in advances table
// -----------------------------------
cur_frm.cscript.allocated_amount = function(doc,cdt,cdn){
  cur_frm.cscript.calc_adjustment_amount(doc,cdt,cdn);
}

//Make Delivery Note Button
//-----------------------------

cur_frm.cscript['Make Delivery Note'] = function() {

  var doc = cur_frm.doc
  n = createLocal('Delivery Note');
  $c('dt_map', args={
    'docs':compress_doclist([locals['Delivery Note'][n]]),
    'from_doctype':doc.doctype,
    'to_doctype':'Delivery Note',
    'from_docname':doc.name,
    'from_to_list':"[['Receivable Voucher','Delivery Note'],['RV Detail','Delivery Note Detail'],['RV Tax Detail','RV Tax Detail'],['Sales Team','Sales Team']]"
    }, function(r,rt) {
       loaddoc('Delivery Note', n);
    }
  );
}



// Make Bank Voucher Button
// -------------------------
cur_frm.cscript['Make Bank Voucher'] = function(doc, dt, dn) {
  cur_frm.cscript.make_jv(cur_frm.doc);
}


/* ***************************** Get Query Functions ************************** */

// Debit To
// ---------
cur_frm.fields_dict.debit_to.get_query = function(doc) {
  return 'SELECT tabAccount.name FROM tabAccount WHERE tabAccount.debit_or_credit="Debit" AND tabAccount.is_pl_account = "No" AND tabAccount.group_or_ledger="Ledger" AND tabAccount.docstatus!=2 AND tabAccount.company="'+doc.company+'" AND tabAccount.%(key)s LIKE "%s"'
}


// Income Account in Details Table
// --------------------------------
cur_frm.fields_dict.entries.grid.get_field("income_account").get_query = function(doc) {
  return 'SELECT tabAccount.name FROM tabAccount WHERE tabAccount.debit_or_credit="Credit" AND tabAccount.group_or_ledger="Ledger" AND tabAccount.docstatus!=2 AND tabAccount.company="'+doc.company+'" AND tabAccount.account_type ="Income Account" AND tabAccount.%(key)s LIKE "%s"'
}

cur_frm.cscript.income_account = function(doc, cdt, cdn){
  var d = locals[cdt][cdn];
  if(d.idx == 1 && d.income_account){
    var cl = getchildren('RV Detail', doc.name, cur_frm.cscript.fname, doc.doctype);
    for(var i = 0; i < cl.length; i++){
      if(!cl[i].income_account) cl[i].income_account = d.income_account;
    }
  }
  refresh_field(cur_frm.cscript.fname);
}

// Cost Center in Details Table
// -----------------------------
cur_frm.fields_dict.entries.grid.get_field("cost_center").get_query = function(doc) {
  return 'SELECT `tabCost Center`.`name` FROM `tabCost Center` WHERE `tabCost Center`.`company_name` = "' +doc.company+'" AND `tabCost Center`.%(key)s LIKE "%s" AND `tabCost Center`.`group_or_ledger` = "Ledger" AND `tabCost Center`.`docstatus`!= 2 ORDER BY  `tabCost Center`.`name` ASC LIMIT 50';
}

cur_frm.cscript.cost_center = function(doc, cdt, cdn){
  var d = locals[cdt][cdn];
  if(d.idx == 1 && d.cost_center){
    var cl = getchildren('RV Detail', doc.name, cur_frm.cscript.fname, doc.doctype);
    for(var i = 0; i < cl.length; i++){
      if(!cl[i].cost_center) cl[i].cost_center = d.cost_center;
    }
  }
  refresh_field(cur_frm.cscript.fname);
}


// Sales Order
// -----------
cur_frm.fields_dict.sales_order_main.get_query = function(doc) {
  if (doc.customer)
    return 'SELECT DISTINCT `tabSales Order`.`name` FROM `tabSales Order` WHERE `tabSales Order`.company = "' + doc.company + '" and `tabSales Order`.`docstatus` = 1 and `tabSales Order`.`status` != "Stopped" and ifnull(`tabSales Order`.per_billed,0) < 100 and `tabSales Order`.`customer` =  "' + doc.customer + '" and `tabSales Order`.%(key)s LIKE "%s" ORDER BY `tabSales Order`.`name` DESC LIMIT 50';
  else
    return 'SELECT DISTINCT `tabSales Order`.`name` FROM `tabSales Order` WHERE `tabSales Order`.company = "' + doc.company + '" and `tabSales Order`.`docstatus` = 1 and `tabSales Order`.`status` != "Stopped" and ifnull(`tabSales Order`.per_billed,0) < 100 and `tabSales Order`.%(key)s LIKE "%s" ORDER BY `tabSales Order`.`name` DESC LIMIT 50';
}

// Delivery Note
// --------------
cur_frm.fields_dict.delivery_note_main.get_query = function(doc) {
  if (doc.customer)
    return 'SELECT DISTINCT `tabDelivery Note`.`name` FROM `tabDelivery Note` WHERE `tabDelivery Note`.company = "' + doc.company + '" and `tabDelivery Note`.`docstatus` = 1 and ifnull(`tabDelivery Note`.per_billed,0) < 100 and `tabDelivery Note`.`customer` =  "' + doc.customer + '" and `tabDelivery Note`.%(key)s LIKE "%s" ORDER BY `tabDelivery Note`.`name` DESC LIMIT 50';
  else
    return 'SELECT DISTINCT `tabDelivery Note`.`name` FROM `tabDelivery Note` WHERE `tabDelivery Note`.company = "' + doc.company + '" and `tabDelivery Note`.`docstatus` = 1 and ifnull(`tabDelivery Note`.per_billed,0) < 100 and `tabDelivery Note`.%(key)s LIKE "%s" ORDER BY `tabDelivery Note`.`name` DESC LIMIT 50';
}



/* **************************************** Utility Functions *************************************** */

// Details Calculation
// --------------------
cur_frm.cscript.calc_adjustment_amount = function(doc,cdt,cdn) {
  var doc = locals[doc.doctype][doc.name];
  var el = getchildren('Advance Adjustment Detail',doc.name,'advance_adjustment_details');
  var total_adjustment_amt = 0
  for(var i in el) {
      total_adjustment_amt += flt(el[i].allocated_amount)
  }
  doc.total_advance = flt(total_adjustment_amt);
  doc.outstanding_amount = flt(doc.grand_total) - flt(total_adjustment_amt) - flt(doc.paid_amount);
  refresh_many(['total_advance','outstanding_amount']);
}


// Make Journal Voucher
// --------------------
cur_frm.cscript.make_jv = function(doc, dt, dn) {
  var jv = LocalDB.create('Journal Voucher');
  jv = locals['Journal Voucher'][jv];
  jv.voucher_type = 'Bank Voucher';

  jv.company = doc.company;
  jv.remark = repl('Payment received against invoice %(vn)s for %(rem)s', {vn:doc.name, rem:doc.remarks});
  jv.fiscal_year = doc.fiscal_year;
  
  // debit to creditor
  var d1 = LocalDB.add_child(jv, 'Journal Voucher Detail', 'entries');
  d1.account = doc.debit_to;
  d1.credit = doc.outstanding_amount;
  d1.against_invoice = doc.name;

  
  // credit to bank
  var d1 = LocalDB.add_child(jv, 'Journal Voucher Detail', 'entries');
  d1.debit = doc.outstanding_amount;
  
  loaddoc('Journal Voucher', jv.name);
}


/****************** Get Accounting Entry *****************/
cur_frm.cscript['View Ledger Entry'] = function(){
  var callback = function(report){
    report.set_filter('GL Entry', 'Voucher No',cur_frm.doc.name);
    report.dt.run();
  }
  loadreport('GL Entry','General Ledger', callback);
}

//get query select Territory
//=======================================================================================================================
cur_frm.fields_dict['territory'].get_query = function(doc,cdt,cdn) {
  return 'SELECT `tabTerritory`.`name`,`tabTerritory`.`parent_territory` FROM `tabTerritory` WHERE `tabTerritory`.`is_group` = "No" AND `tabTerritory`.`docstatus`!= 2 AND `tabTerritory`.%(key)s LIKE "%s"  ORDER BY  `tabTerritory`.`name` ASC LIMIT 50';
}
