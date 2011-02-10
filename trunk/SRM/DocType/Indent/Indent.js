cur_frm.cscript.tname = "Indent Detail";
cur_frm.cscript.fname = "indent_details";

$import(Purchase Common)

//========================== On Load =================================================
cur_frm.cscript.onload = function(doc, cdt, cdn) {
  
  if (!doc.transaction_date) doc.transaction_date = dateutil.obj_to_str(new Date())
  if (!doc.status) doc.status = 'Draft';
  
  // set naming series
  callback = function(r,rt) { 
    var doc = locals[cdt][cdn];
    
    if(r.message) { 
      set_field_options('naming_series', NEWLINE+r.message); 
    }  

    // second call
    if(doc.__islocal){ 
      cur_frm.cscript.get_default_schedule_date(doc);
    }

  }
  $c_obj('Naming Series','get_series_options',cdt,callback);  
}

//======================= Refresh =====================================
cur_frm.cscript.refresh = function(doc, cdt, cdn) { 

  // Unhide Fields in Next Steps
  // ---------------------------------
  
  cur_frm.clear_custom_buttons();

  if(doc.docstatus == 1 && doc.status != 'Stopped'){
    var ch = getchildren('Indent Detail',doc.name,'indent_details');
    var is_closed = 1;
    for(var i in ch){
      if(flt(ch[i].qty) > flt(ch[i].ordered_qty)) is_closed = 0;
    }
    if(!is_closed) {
  	  cur_frm.add_custom_button('Make RFQ', cur_frm.cscript['Create RFQ'])
  	  cur_frm.add_custom_button('Make Purchase Order', cur_frm.cscript['Make Purchase Order'])
  	  cur_frm.add_custom_button('Stop Indent', cur_frm.cscript['Stop Indent'])
    }
  }
 
  if(doc.docstatus == 1 && doc.status == 'Stopped')
    cur_frm.add_custom_button('Unstop Indent', cur_frm.cscript['Unstop Indent'])
    
  if(doc.docstatus == 1)
    unhide_field(['Repair Indent']);
  else
    hide_field(['Repair Indent']);
}

//======================= validation ===================================
cur_frm.cscript.validate = function(doc,cdt,cdn){
  is_item_table(doc,cdt,cdn);
}
//======================= transaction date =============================
cur_frm.cscript.transaction_date = function(doc,cdt,cdn){
  if(doc.__islocal){ 
    cur_frm.cscript.get_default_schedule_date(doc);
  }
}

//=================== Quantity ===================================================================
cur_frm.cscript.qty = function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  if (flt(d.qty) < flt(d.min_order_qty))
    alert("Warning: Indent Qty is less than Minimum Order Qty");
}

// On Button Click Functions
// ------------------------------------------------------------------------------

// Make Purchase Order
cur_frm.cscript['Make Purchase Order'] = function() {
  var doc = cur_frm.doc;
  n = createLocal('Purchase Order');
  $c('dt_map', args={
    'docs':compress_doclist([locals['Purchase Order'][n]]),
    'from_doctype':doc.doctype,
    'to_doctype':'Purchase Order',
    'from_docname':doc.name,
    'from_to_list':"[['Indent','Purchase Order'],['Indent Detail','PO Detail']]"
    }, function(r,rt) {
       loaddoc('Purchase Order', n);
    }
  );
}

// Make RFQ
cur_frm.cscript['Create RFQ'] = function() {
  var doc = cur_frm.doc;
  n = createLocal('RFQ');
  $c('dt_map', args={
    'docs':compress_doclist([locals['RFQ'][n]]),
    'from_doctype':doc.doctype,
    'to_doctype':'RFQ',
    'from_docname':doc.name,
    'from_to_list':"[['Indent','RFQ'],['Indent Detail','RFQ Detail']]"
    }, function(r,rt) {
       loaddoc('RFQ', n);
    }
  );
}


// Stop INDENT
// ==================================================================================================
cur_frm.cscript['Stop Indent'] = function() {
  var doc = cur_frm.doc;
  var check = confirm("Do you really want to STOP this Indent?");

  if (check) {
    $c('runserverobj', args={'method':'update_status', 'arg': 'Stopped', 'docs': compress_doclist(make_doclist(doc.doctype, doc.name))}, function(r,rt) {
      cur_frm.refresh();
    });
  }
}

// Un Stop INDENT
//====================================================================================================
cur_frm.cscript['Unstop Indent'] = function(){
  var doc = cur_frm.doc
  var check = confirm("Do you really want to UNSTOP this Indent?");
  
  if (check) {
    $c('runserverobj', args={'method':'update_status', 'arg': 'Submitted','docs': compress_doclist(make_doclist(doc.doctype, doc.name))}, function(r,rt) {
      cur_frm.refresh();
      
    });
  }
}
