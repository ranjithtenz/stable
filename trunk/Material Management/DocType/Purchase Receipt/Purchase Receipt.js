cur_frm.cscript.tname = "Purchase Receipt Detail";
cur_frm.cscript.fname = "purchase_receipt_details";
cur_frm.cscript.other_fname = "purchase_tax_details";

$import(Purchase Common)
$import(Purchase Other Charges)

//========================== On Load ================================================================
cur_frm.cscript.onload = function(doc, cdt, cdn) {

  if(!doc.fiscal_year && doc.__islocal){ set_default_values(doc);}
  if (!doc.posting_date) doc.posting_date = dateutil.obj_to_str(new Date());
  if (!doc.transaction_date) doc.transaction_date = dateutil.obj_to_str(new Date());
  if (!doc.status) doc.status = 'Draft';

  if(doc.__islocal){ 
    cur_frm.cscript.get_default_schedule_date(doc);
  }  
  msgprint(doc.naming_series);
  msgprint(doc.posting_time);
  //refresh_many(['naming_series', 'posting_time']);
  msgprint("after refresh");
  msgprint(doc.naming_series);
  msgprint(doc.posting_time);
}

//========================== Refresh ===============================================================
cur_frm.cscript.refresh = function(doc, cdt, cdn) { 

  // Unhide Fields in Next Steps
  // ---------------------------------
  cur_frm.clear_custom_buttons();
  if(doc.docstatus == 1){
    var ch = getchildren('Purchase Receipt Detail',doc.name,'purchase_receipt_details');
    allow_billing = 0;
    for(var i in ch){
      if(ch[i].qty > ch[i].billed_qty) allow_billing = 1;
    }
   cur_frm.add_custom_button('Make Purchase Invoice', cur_frm.cscript['Make Purchase Invoice']);
  }
  else{
    hide_field(['Repair Purchase Receipt']);
  }
}

//================ create new contact ============================================================================
cur_frm.cscript.new_contact = function(){
  tn = createLocal('Contact');
  locals['Contact'][tn].is_supplier = 1;
  if(doc.supplier) locals['Contact'][tn].supplier = doc.supplier;
  loaddoc('Contact', tn);
}

//======================= posting date =============================
cur_frm.cscript.transaction_date = function(doc,cdt,cdn){
  if(doc.__islocal){ 
    cur_frm.cscript.get_default_schedule_date(doc);
  }
}

// ***************** Get project name *****************
cur_frm.fields_dict['project_name'].get_query = function(doc, cdt, cdn) {
  return 'SELECT `tabProject`.name FROM `tabProject` WHERE `tabProject`.status = "Open" AND `tabProject`.name LIKE "%s" ORDER BY `tabProject`.name ASC LIMIT 50';
}


//========================= Overloaded query for link batch_no =============================================================
cur_frm.fields_dict['purchase_receipt_details'].grid.get_field('batch_no').get_query= function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  if(d.item_code){
    return "SELECT tabBatch.name FROM tabBatch WHERE tabBatch.item = '"+ d.item_code +"' AND `tabBatch`.`name` like '%s' ORDER BY `tabBatch`.`name` DESC LIMIT 50"
  }
  else{
    alert("Please enter Item Code.");
  }
}

// ***************** Get Contact Person based on supplier selected *****************
cur_frm.fields_dict['contact_person'].get_query = function(doc, cdt, cdn) {
  return 'SELECT `tabContact`.contact_name FROM `tabContact` WHERE `tabContact`.is_supplier = 1 AND `tabContact`.supplier = "'+ doc.supplier+'" AND `tabContact`.docstatus != 2 AND `tabContact`.docstatus != 2 AND `tabContact`.contact_name LIKE "%s" ORDER BY `tabContact`.contact_name ASC LIMIT 50';
}

cur_frm.cscript.select_print_heading = function(doc,cdt,cdn){
  if(doc.select_print_heading){
    // print heading
    cur_frm.pformat.print_heading = doc.select_print_heading;
  }
  else
    cur_frm.pformat.print_heading = "Purchase Receipt";
}
// ***************** Get Print Heading  *****************
cur_frm.fields_dict['select_print_heading'].get_query = function(doc, cdt, cdn) {
  return 'SELECT `tabPrint Heading`.name FROM `tabPrint Heading` WHERE `tabPrint Heading`.docstatus !=2 AND `tabPrint Heading`.name LIKE "%s" ORDER BY `tabPrint Heading`.name ASC LIMIT 50';
}

//========================= Received Qty =============================================================

cur_frm.cscript.received_qty = function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  ret = {
      'qty' : 0,
      'stock_qty': 0,
      'rejected_qty' : 0
    }
  set_multiple('Purchase Receipt Detail', cdn, ret, 'purchase_receipt_details');
  cur_frm.cscript.calc_amount(doc, 2);
}

//======================== Qty (Accepted Qty) =========================================================

cur_frm.cscript.qty = function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  // Step 1 :=> Check If Qty > Received Qty
  if (flt(d.qty) > flt(d.received_qty)) {
    alert("Accepted Qty cannot be greater than Received Qty")
    ret = {
      'qty' : 0,
      'stock_qty': 0,
      'rejected_qty' : 0
    }
    // => Set Qty = 0 and rejected_qty = 0
    set_multiple('Purchase Receipt Detail', cdn, ret, 'purchase_receipt_details');
    cur_frm.cscript.calc_amount(doc, 2);
    // => Return
    return
  }
  // Step 2 :=> Check IF Qty <= REceived Qty
  else {
    ret = {
      'rejected_qty':flt(d.received_qty) - flt(d.qty)
    }
    // => Set Rejected Qty = Received Qty - Qty
    set_multiple('Purchase Receipt Detail', cdn, ret, 'purchase_receipt_details');
    // => Calculate Amount
    cur_frm.cscript.calc_amount(doc, 2);
    cur_frm.cscript.update_stock_qty(doc,cdt,cdn);
  }  
}

//======================== Rejected Qty =========================================================
cur_frm.cscript.rejected_qty = function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  // Step 1 :=> Check If Rejected Qty > Received Qty
  if (flt(d.rejected_qty) > flt(d.received_qty)) {
    alert("Rejected Qty cannot be greater than Received Qty") 
    ret = {
      'qty' : 0,
      'stock_qty': 0,
      'rejected_qty' : 0
    }
    // => Set Qty = 0 and rejected_qty = 0
    set_multiple('Purchase Receipt Detail', cdn, ret, 'purchase_receipt_details');
    cur_frm.cscript.calc_amount(doc, 2);
    // => Return
    return
  }
  // Step 2 :=> Check IF Rejected Qty <= REceived Qty
  else {
    ret = {
      'qty':flt(d.received_qty) - flt(d.rejected_qty)
    }
    // => Set Qty = Received Qty - Rejected Qty
    set_multiple('Purchase Receipt Detail', cdn, ret, 'purchase_receipt_details');
    // Calculate Amount
    cur_frm.cscript.calc_amount(doc, 2);
    cur_frm.cscript.update_stock_qty(doc,cdt,cdn);
  }
}

//================================= Purchase Order No Get Query ====================================
cur_frm.fields_dict['purchase_order_no'].get_query = function(doc) {
  if (doc.supplier)
    return 'SELECT DISTINCT `tabPurchase Order`.`name` FROM `tabPurchase Order` WHERE `tabPurchase Order`.`supplier` = "' +doc.supplier + '" and`tabPurchase Order`.`docstatus` = 1 and `tabPurchase Order`.`status` != "Stopped" and ifnull(`tabPurchase Order`.`per_received`, 0) < 100  and `tabPurchase Order`.`currency` = ifnull("' +doc.currency+ '","") and `tabPurchase Order`.company = "'+ doc.company +'" and `tabPurchase Order`.%(key)s LIKE "%s" ORDER BY `tabPurchase Order`.`name` DESC LIMIT 50';
  else
    return 'SELECT DISTINCT `tabPurchase Order`.`name` FROM `tabPurchase Order` WHERE `tabPurchase Order`.`docstatus` = 1 and `tabPurchase Order`.`company` = "'+ doc.company +'" and `tabPurchase Order`.`status` != "Stopped" and ifnull(`tabPurchase Order`.`per_received`, 0) < 100 and `tabPurchase Order`.%(key)s LIKE "%s" ORDER BY `tabPurchase Order`.`name` DESC LIMIT 50';
}

// QA INspection report get_query
//---------------------------------

cur_frm.fields_dict.purchase_receipt_details.grid.get_field("qa_no").get_query = function(doc) {
  return 'SELECT `tabQA Inspection Report`.name FROM `tabQA Inspection Report` WHERE `tabQA Inspection Report`.docstatus = 1 AND `tabQA Inspection Report`.%(key)s LIKE "%s"';
}

// On Button Click Functions
// ------------------------------------------------------------------------------


// ================================ Make Purchase Invoice ==========================================
cur_frm.cscript['Make Purchase Invoice'] = function() {
  n = createLocal('Payable Voucher');
  $c('dt_map', args={
    'docs':compress_doclist([locals['Payable Voucher'][n]]),
    'from_doctype': cur_frm.doc.doctype,
    'to_doctype':'Payable Voucher',
    'from_docname': cur_frm.doc.name,
    'from_to_list':"[['Purchase Receipt','Payable Voucher'],['Purchase Receipt Detail','PV Detail']]"
    }, function(r,rt) {
       loaddoc('Payable Voucher', n);
    }
  );
}




//****************** For print sales order no and date*************************
cur_frm.pformat.purchase_order_no = function(doc, cdt, cdn){
  //function to make row of table
  
  var make_row = function(title,val1, val2, bold){
    var bstart = '<b>'; var bend = '</b>';

    return '<tr><td style="width:39%;">'+(bold?bstart:'')+title+(bold?bend:'')+'</td>'
     +'<td style="width:61%;text-align:left;">'+val1+(val2?' ('+dateutil.str_to_user(val2)+')':'')+'</td>'
     +'</tr>'
  }

  out ='';
  
  var cl = getchildren('Purchase Receipt Detail',doc.name,'purchase_receipt_details');

  // outer table  
  var out='<div><table class="noborder" style="width:100%"><tr><td style="width: 50%"></td><td>';
  
  // main table
  out +='<table class="noborder" style="width:100%">';

  // add rows
  if(cl.length){
    prevdoc_list = new Array();
    for(var i=0;i<cl.length;i++){
      if(cl[i].prevdoc_doctype == 'Purchase Order' && cl[i].prevdoc_docname && prevdoc_list.indexOf(cl[i].prevdoc_docname) == -1) {
        prevdoc_list.push(cl[i].prevdoc_docname);
        if(prevdoc_list.length ==1)
          out += make_row(cl[i].prevdoc_doctype, cl[i].prevdoc_docname, cl[i].prevdoc_date,0);
        else
          out += make_row('', cl[i].prevdoc_docname, cl[i].prevdoc_date,0);
      }
    }
  }

  out +='</table></td></tr></table></div>';

  return out;
}
