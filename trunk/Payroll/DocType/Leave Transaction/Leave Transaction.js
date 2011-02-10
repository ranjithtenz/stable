//make all fields null
field_values= function (doc, cdt, cdn){
  doc.leave_transaction_type = doc.allocation_type = doc.deduction_type = doc.from_date = doc.to_date ='';
  doc.half_day = doc.total_leave = 0;
}

//==============================================================================================
//common function when change leave_transaction_type
change_lev_trans_type = function(doc,cdt,cdn,unhide_lst,hide_lst){
  doc.allocation_type = '';
  doc.deduction_type = '';
  doc.total_leave = 0.0;
  doc.half_day = 0;
  refresh_many(['total_leave','half_day']);
  unhide_field(unhide_lst);
  hide_field(hide_lst);
}

// Set Common Fields
// // -------------------------------------------------------------------------------------------
cnf_set_fields = function(doc,cdt,cdn){

  if(doc.leave_transaction_type == 'Allocation'){
    hide_lst = ['deduction_type','Calculate Leave Days','half_day','encashment_date'];
    unhide_lst = ['allocation_type','from_date','to_date','total_leave'];
    change_lev_trans_type(doc, cdt, cdn, unhide_lst, hide_lst);
  }
  else if(doc.leave_transaction_type == 'Deduction') {
    hide_lst = ['allocation_type','half_day','encashment_date'];
    unhide_lst = ['deduction_type','from_date','to_date','total_leave','Calculate Leave Days'];
    change_lev_trans_type(doc, cdt, cdn, unhide_lst, hide_lst);
  }
  else if (doc.leave_transaction_type == 'Expired') {
    hide_lst = ['allocation_type','deduction_type','half_day','from_date','to_date','Calculate Leave Days','encashment_date'];
    unhide_lst = 'total_leave';
    change_lev_trans_type(doc, cdt, cdn, unhide_lst, hide_lst);
  }
}

// Leave Transaction Type
// -------------------------------------------------------------------------------------------
cur_frm.cscript.leave_transaction_type = function (doc, cdt, cdn){
  if((doc.leave_transaction_type == '') && (doc.leave_type != 'Leave Without Pay'))
    hide_field(['allocation_type','deduction_type','half_day','from_date','to_date','Calculate Leave Days','encashment_date','total_leave']);
  
  else if(doc.leave_type == 'Leave Without Pay'){ 
    doc.leave_transaction_type = 'Deduction';
    doc.deduction_type = 'Leave';
    refresh_many(['leave_transaction_type','deduction_type']);
  }
  else{
    cnf_set_fields(doc,cdt,cdn); 
  }
}

//==============================================================================================

// Onload

cur_frm.cscript.onload = function(doc, cdt, cdn) {
  
  if(!doc.status) set_multiple(cdt,cdn,{status:'Unsaved'});
  pscript.all_field = ['leave_transaction_type','pre_balance','allocation_type','deduction_type','half_day','from_date','to_date','Calculate Leave Days','encashment_date','total_leave'];
  hide_field(pscript.all_field);
  if(doc.__islocal){
   
    doc.employee = doc.leave_type = '';
    refresh_many(['employee','leave_type']);
    field_values(doc, cdt, cdn);
    
  }
  else{
    if(doc.leave_type == 'Leave Without Pay')
      unhide_field(['leave_transaction_type', 'deduction_type','from_date', 'to_date', 'total_leave', 'Calculate Leave Days']);
    if(doc.leave_typee == 'Compensatory Off')
      unhide_field(['from_date', 'to_date', 'total_leave', 'Calculate Leave Days']);

    if(doc.leave_type != 'Leave Without Pay' || doc.leave_type != 'Compensatory Off'){
      unhide_field(['pre_balance', 'leave_transaction_type']);
    
      if (doc.leave_transaction_type == 'Allocation')
        unhide_field(['allocation_type', 'from_date', 'to_date', 'total_leave']);
      
      if (doc.leave_transaction_type == 'Deduction')
        unhide_field(['deduction_type', 'from_date', 'to_date','total_leave', 'Calculate Leave Days']);
      
      if (doc.deduction_type == 'Leave')
        unhide_field ('half_day');
     
      if (doc.deduction_type == 'Encashment')
        unhide_field (['from_date', 'to_date','total_leave', 'Calculate Leave Days']);
      
      if (doc.leave_transaction_type == 'Expired')
        unhide_field ('total_leave');
    }
  }
}

// ================================================================================================

cal_pre_bal= function (doc, cdt, cdn){
  
  field_values(doc, cdt, cdn);
  hide_field(pscript.all_field);
  
  if(doc.fiscal_year != '' && doc.employee != '' && doc.leave_type != '') {
    
    if (doc.leave_type == 'Compensatory Off')
      unhide_field(['to_date', 'from_date','total_leave','Calculate Leave Days']);
    
    else if(doc.leave_type == 'Leave Without Pay'){
      unhide_field(['to_date', 'from_date','total_leave','deduction_type', 'leave_transaction_type', 'Calculate Leave Days']);
      doc.leave_transaction_type = 'Deduction';
      doc.deduction_type = 'Leave';
      refresh_many(['deduction_type','leave_transaction_type']);
    }
    
    else {
      hide_field(['to_date','from_date','deduction_type', 'half_day', 'allocation_type','Calculate Leave Days','total_leave']);    
      unhide_field(['leave_transaction_type','pre_balance']);
    
      $c('runserverobj', args={'method':'get_prv_bal','docs':compress_doclist([doc])},
        function(r, rt) {
          var doc = locals[cdt][cdn];
          if (flt(r.message)==0) doc.pre_balance = 0.0;
          else doc.pre_balance = flt(r.message);
          refresh_field('pre_balance');
        }
      );
    }
  }    
}

//-------------------------------------------------------------------------------------
cur_frm.cscript.fiscal_year = function (doc, cdt, cdn){ cal_pre_bal(doc, cdt, cdn);}

//-------------------------------------------------------------------------------------
cur_frm.cscript.employee = function (doc, cdt, cdn){ cal_pre_bal(doc, cdt, cdn);}

// Leave Type
//-------------------------------------------------------------------------------------

cur_frm.cscript.leave_type = function (doc, cdt, cdn){
  if (doc.fiscal_year == ''|| doc.employee == '') {
    alert("Please select fiscal year & employee")
    doc.leave_type = '';
    refresh_field('leave_type');
  }
  else  cal_pre_bal(doc, cdt, cdn);
}

// ================================================================================================
//carry forward
carry_forward = function(doc,cdt,cdn){
  $c('runserverobj', args={'method':'get_carry_fwd_days','docs':compress_doclist([doc])},
    function(r, rt) {
      var doc = locals[cdt][cdn];
      if (flt(r.message)==0) doc.total_leave = 0.0;
      else  doc.total_leave = flt(r.message);
      refresh_many(['pre_balance','total_leave']);
    }
  );
}
//----------------------------------------------------------------------
//get previous balance
get_previous_balance = function(doc,cdt,cdn){
  $c('runserverobj', args={'method':'get_prv_bal','docs':compress_doclist([doc])},
    function(r, rt) {
    
      var doc = locals[cdt][cdn];
      if (flt(r.message)==0) doc.pre_balance = 0.0;
      else doc.pre_balance = flt(r.message);
      doc.total_leave = 0.0;
      refresh_many(['pre_balance','total_leave']);
    }
  );
}

//----------------------------------------------------------------------
// Allocation Type

cur_frm.cscript.allocation_type = function (doc, cdt, cdn){

  hide_field(['encashment_date','half_day','Calculate Leave Days']);
  unhide_field(['total_leave','from_date','to_date']);
  
  if (doc.allocation_type == 'Carry Forward'){
    carry_forward(doc,cdt,cdn);
  }
  else {
    get_previous_balance(doc,cdt,cdn);
  }
}

// ================================================================================================
// Half Day

cur_frm.cscript.half_day = function (doc, cdt, cdn){
  if(doc.half_day == 1){
    hide_field(['to_date','Calculate Leave Days']);
    doc.total_leave = 0.5;
  }
  else {
    unhide_field(['to_date','Calculate Leave Days']);
    doc.total_leave = 0;
  }
  refresh_field('total_leave');
}

// Validation For From Date
// ================================================================================================
cur_frm.cscript.from_date = function (doc, cdt, cdn){    
  $c('runserverobj', args={'method':'joining_date_validation','docs':compress_doclist([doc])},
    function(r2, rt) {
      var doc = locals[cdt][cdn];
      if (r2.message) {
        alert("From date must be greater than joining date");
        doc.from_date = '';
        refresh_field('from_date');
      }
    }
  );  
}

// Validation For To Date
// ================================================================================================
cur_frm.cscript.to_date = function (doc, cdt, cdn){
  $c('runserverobj', args={'method':'joining_date_validation','docs':compress_doclist([doc])},
    function(r2, rt) {
    var doc = locals[cdt][cdn];
      if (r2.message) {
        alert("To date must be greater than joining date");
        doc.to_date = '';
        refresh_field('to_date');
      }
    }
  );  
}

// Deduction Type
// ================================================================================================
check_deduction_type = function(doc,cdt,cdn){
  if(doc.deduction_type == '') 
      hide_field(['encashment_date','half_day','total_leave','Calculate Leave Days','from_date','to_date']); 
      
    else if(doc.deduction_type == 'Leave') {
      hide_field('encashment_date'); 
      unhide_field(['total_leave','Calculate Leave Days','from_date','to_date','half_day']);
    }
    else if(doc.deduction_type == 'Encashment') { 
      hide_field(['Calculate Leave Days','from_date','to_date','half_day']);
      unhide_field(['encashment_date','total_leave']); 
    }
    else hide_field(['half_day','encashment_date']);
    doc.total_leave = doc.half_day = 0; 
    refresh_many(['total_leave','half_day']);
}

//--------------------------------------------------------------------------------------------------
//change of deducion type
cur_frm.cscript.deduction_type = function (doc, cdt, cdn){
  if(doc.leave_type == 'Leave Without Pay'){
    doc.leave_transaction_type = 'Deduction';
    doc.deduction_type = 'Leave';
    refresh_many(['leave_transaction_type','deduction_type']);
  }
  else  check_deduction_type(doc,cdt,cdn);
}

//--------------------------------------------------------------------------------------------------
cur_frm.fields_dict['leave_type'].get_query = function(doc) {
    return 'SELECT `tabLeave Type`.`name` FROM `tabLeave Type` WHERE `tabLeave Type`.`docstatus` !=2 ORDER BY `tabLeave Type`.`name` LIMIT 50';
}