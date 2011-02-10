cur_frm.cscript.onload = function(doc,dt,dn){
  if(!doc.return_date) set_multiple(dt,dn,{return_date:get_today()});
   doc.delivery_note_no = '';
  doc.purchase_receipt_no = '';
  doc.return_type ='';
  hide_field('return_details','Return Details');
  refresh_field('return_details','Return Details');
}

cur_frm.cscript.return_type = function(doc, cdt, cdn) {
  //get_server_fields('clear_return_table','','',doc, cdt, cdn, 1);
  if(doc.return_type == 'Sales Return'){
    unhide_field('delivery_note_no','Delivery Note No');
    hide_field('purchase_receipt_no','Purchase Receipt No');
    unhide_field('Make Credit Note');
    hide_field('Make Debit Note');
  } 
  if(doc.return_type == 'Purchase Return'){
    unhide_field('purchase_receipt_no','Purchase Receipt No');
    hide_field('delivery_note_no','Delivery Note No');
    unhide_field('Make Debit Note');
    hide_field('Make Credit Note');
  }
  unhide_field('Make Excise Invoice');
  unhide_field('Get Items');  
  hide_field('return_details','Return Details');
  unhide_field('Make Stock Entry');

}

cur_frm.cscript['Get Items'] = function(doc, cdt, cdn) {
  var callback = function(r,rt) {
    cur_frm.cscript.max_returned = r.message;
    cur_frm.cscript.dno(doc,cdt,cdn);
  }
  unhide_field('return_details','Return Details');
  $c_obj(make_doclist(doc.doctype, doc.name),'pull_details','',callback);

}

cur_frm.cscript.dno = function(doc,cdt,cdn){
  if(doc.delivery_note_no){
    cur_frm.cscript.doc_no = doc.delivery_note_no;
  }
  else if(doc.purchase_receipt_no){
    cur_frm.cscript.doc_no = doc.purchase_receipt_no;
  }
  doc.delivery_note_no = ''
  doc.purchase_receipt_no = '' 
  refresh_field('delivery_note_no');
  refresh_field('purchase_receipt_no');
  refresh_field('return_details');
}

cur_frm.cscript['Make Stock Entry'] = function(doc, dt, dn) {

  cur_frm.cscript.make_se(doc,dt,dn);
}

cur_frm.cscript.make_se = function(doc, dt, dn){

  if(cur_frm.cscript.max_returned){

    var se = LocalDB.create('Stock Entry');
    se = locals['Stock Entry'][se];

    var comp_name = cur_frm.cscript.max_returned.length;
    se.posting_date = dateutil.obj_to_str(new Date());
    se.transfer_date = dateutil.obj_to_str(new Date());
    se.remarks = doc.return_type + ' of ' + cur_frm.cscript.doc_no;
    if(doc.return_type == 'Sales Return'){
      se.delivery_note_no = doc.delivery_note_no;
    }
    else if(doc.return_type == 'Purchase Return'){
      se.purchase_receipt_no = doc.purchase_receipt_no;
    }

    se.company = cur_frm.cscript.max_returned[comp_name-1];
    se.fiscal_year = sys_defaults.fiscal_year;
    se.purpose = doc.return_type;
    var flg  = 0
    var doc = locals[doc.doctype][doc.name];
    el = getchildren('Return Detail',doc.name,'return_details');
    var len = el.length;
    try{
      for(var i = 0; i< len; i++){
        if(el[i].returned_qty){
          var d1 = LocalDB.add_child(se, 'Stock Entry Detail', 'mtn_details');
          d1.detail_name = el[i].detail_name;
          d1.item_code = el[i].item_code;
          d1.description = el[i].description;
          d1.transfer_qty = el[i].returned_qty;
          d1.stock_uom = el[i].uom;
          d1.incoming_rate = el[i].rate;
        }
        else{
          throw('Please Enter number of quantities to be returned');
        }
      }
    }
    catch(e){
      alert("Error : "+e);
      flg = 1;
    }
    if(flg == 0){
      loaddoc('Stock Entry', se.name);
    }
  }
  else{ alert("Please retrieve items again by clicking on 'Get Items' button");}
}

cur_frm.cscript['Make Excise Invoice'] = function(doc, dt, dn) {
  var excise = LocalDB.create('Journal Voucher');
  excise = locals['Journal Voucher'][excise];
  excise.voucher_type = 'Excise Voucher';
  loaddoc('Journal Voucher',excise.name);
}

cur_frm.cscript['Make Debit Note'] = function(doc, dt, dn) {

  var calback = function(r,rt){
    var ent_det = r.message;
    
    var debit = LocalDB.create('Journal Voucher');
    debit = locals['Journal Voucher'][debit];
    
    debit.voucher_type = 'Debit Note';
    debit.company = ent_det[0];
    debit.fiscal_year = sys_defaults.fiscal_year;
    debit.is_opening = 'No';
    debit.posting_date = dateutil.obj_to_str(new Date());
    debit.voucher_date = dateutil.obj_to_str(new Date());
    var d1 = LocalDB.add_child(debit,'Journal Voucher Detail','entries')
    d1.account = ent_det[1]
    loaddoc('Journal Voucher',debit.name);
  }
  $c_obj(make_doclist(doc.doctype, doc.name),'get_voucher_det','',calback);
  
}

cur_frm.cscript['Make Credit Note'] = function(doc, dt, dn) {

  var c_back = function(r,rt){
    var ent_det = r.message;
    
    var credit = LocalDB.create('Journal Voucher');
    credit = locals['Journal Voucher'][credit];

    
    credit.voucher_type = 'Credit Note';
    credit.company = ent_det[0];
    credit.fiscal_year = sys_defaults.fiscal_year;
    credit.is_opening = 'No';
    credit.posting_date = dateutil.obj_to_str(new Date());
    credit.voucher_date = dateutil.obj_to_str(new Date());
    var d1 = LocalDB.add_child(credit,'Journal Voucher Detail','entries')
    d1.account = ent_det[1]
    loaddoc('Journal Voucher',credit.name);
  }  
  $c_obj(make_doclist(doc.doctype, doc.name),'get_voucher_det','',c_back);
}