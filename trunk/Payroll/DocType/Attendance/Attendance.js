cur_frm.cscript.onload = function(doc, cdt, cdn){

  //hide unhide leave type field based on status
  /*if(doc.leave_type) cur_frm.cscript.status(doc,cdt,cdn);
  else hide_field('leave_type');*/ 

}

//hide unhide leave type based on status
/*
cur_frm.cscript.status = function(doc,cdt,cdn){
  if(doc.status == 'Present'){ 
    doc.leave_type = '';
    refresh_field('leave_type');
    hide_field('leave_type');
  }
  else unhide_field('leave_type');
}*/

//get employee's name based on employee id selected
cur_frm.cscript.employee = function(doc,cdt,cdn){
  if(doc.employee) get_server_fields('get_emp_name', '', '', doc, cdt, cdn, 1);
  refresh_field('employee_name'); 
}