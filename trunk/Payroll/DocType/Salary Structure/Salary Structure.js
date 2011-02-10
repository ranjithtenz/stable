$import(Payroll Tips Common)

cur_frm.cscript.onload = function(doc, cdt, cdn){
  cur_frm.cscript.get_tips(doc, cdt, cdn);

  if(!doc.employee){
    doc.backup_employee='';
  }
  if(!cur_frm.log_div){
    cur_frm.log_div = $a(cur_frm.fields_dict['Log'].wrapper,'div','',{border:'1px solid #CCC', backgroundColor:'#DDD'});
  }
  
  if(!doc.__islocal){
    unhide_field(['Salary Structure','Re-apply Rules']);
    cur_frm.log_div.innerHTML = doc.log_info;
  }
  else {
    cur_frm.log_div.innerHTML = '';
    hide_field('Salary Structure'); 
  }
}


//=======================================================================
cur_frm.cscript['Make IT Checklist']=function(doc,cdt,cdn){
  
  var itc = LocalDB.create('IT Checklist');
  itc = locals['IT Checklist'][itc];
  itc.employee = doc.employee;
  itc.fiscal_year = sys_defaults.fiscal_year;
  itc.is_cheklist_active='Yes';
  loaddoc('IT Checklist', itc.name);
 
}


//=======================================================================
cur_frm.cscript['Make Salary Slip']=function(doc,cdt,cdn){

  var mydoc = doc;
  $c('runserverobj', args={'method':'set_ss_values','docs':compress_doclist (make_doclist (doc.doctype,doc.name))},
      function(r, rt) {

     var doc = locals[mydoc.doctype][mydoc.name];
      var ss = LocalDB.create('Salary Slip');
      ss = locals['Salary Slip'][ss];
      ss.employee = doc.employee;
      ss.employee_name = doc.employee_name;
      ss.department = doc.department;
      ss.designation = doc.designation;
      ss.branch = doc.branch;
      ss.grade = doc.grade;
      ss.fiscal_year = sys_defaults.fiscal_year; 
      ss.bank_name = r.message['bank_name'];
      ss.bank_account_no = r.message['bank_ac_no'];
      ss.esic_no=r.message['esic_no'];
      ss.pf_no= r.message['pf_no'];
      loaddoc('Salary Slip', ss.name);
    }  
  );
 
}

//=======================================================================
cur_frm.cscript.refresh = function(doc, cdt, cdn){
  cur_frm.cscript.get_tips(doc, cdt, cdn);

  cur_frm.cscript.onload(doc, cdt, cdn);
  if(doc.__islocal!=1){
    unhide_field(['Make IT Checklist','Make Salary Slip']);
    cur_frm.log_div.innerHTML = doc.log_info;
  }
  else{
    hide_field(['Make IT Checklist','Make Salary Slip']);
  }
}


//=======================================================================
cur_frm.cscript.employee = function(doc, cdt, cdn){
  var mydoc = doc
  flag = 0;
  if((doc.docstatus == 0) && (doc.backup_employee != '' ) && (doc.employee != doc.backup_employee)){
    var check = confirm("Do you Really want to Change Employee " + doc.employee);
    if(!check){
      doc.employee = doc.backup_employee;
      refresh_field('employee');
      flag = 1;
    }
  }

  if((flag != 1) && (doc.employee != doc.backup_employee)){
    $c_obj(make_doclist(doc.doctype, doc.name), 'set_values', '',
function(r, rt) { refresh_many(['employee_name','branch','designation','department','grade','employee','backup_employee','earning_details']); });
  }
}

//=======================================================================
cur_frm.cscript['Apply Rules']=function(doc, cdt, cdn){
 
  if(!doc.__islocal){
  var mydoc = doc

  var call_back1 = function(r, rt){
    
    var doc = locals[mydoc.doctype][mydoc.name];
    var msg1='';
    unhide_field('Re-apply Rules');
    if(r.message){
      
      for(var i=0;i<(r.message).length; i++){
        msg1 +='<br>' +'<pre>' + r.message[i] +'</pre>'; 
      }
       
      doc.log_info = msg1;
      cur_frm.log_div.innerHTML = msg1;
    }
    refresh_many(['log_info','total','deduction_details','earning_details','total_earning','total_deduction']);    
  }
  $c('runserverobj', args={'method':'make_earning_deduction_table','docs':compress_doclist (make_doclist (doc.doctype,doc.name))}, call_back1);
  }
  else{
    alert("Please save salary structure before processing further.");
  }   
}