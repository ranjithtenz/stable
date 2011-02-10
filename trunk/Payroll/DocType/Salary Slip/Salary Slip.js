$import(Payroll Tips Common)

cur_frm.cscript.onload = function(doc,cdt,cdn){
  cur_frm.cscript.get_tips(doc, cdt, cdn);

  if(doc.__islocal && !doc.amended_from){
    var today=new Date()
    month = (today.getMonth()+01).toString();
    if(month.length>1)
      doc.month = month;
    else
      doc.month = '0'+month;
    doc.year = today.getFullYear();
    
    cur_frm.cscript.month(doc,cdt,cdn);
    refresh_many(['month','year','total_days_in_month']);
  }
  if(doc.employee){
    var mydoc = doc
    $c('runserverobj', args={'method':'set_values','docs':compress_doclist (make_doclist (doc.doctype,doc.name))},
      function(r, rt) {
        var doc = locals[mydoc.doctype][mydoc.name];
        refresh_many(['employee_name','branch','department','designation','grade','bank_name','bank_account_no','esic_no','pf_no','earning_details','deduction_details','total_days_in_month','leave_without_pay','payment_days']);
      }
    );
  }
}
cur_frm.cscript.month = function(doc,cdt,cdn){
  if(doc.month && doc.year){
    var mydoc = doc
    $c('runserverobj', args={'method':'leave_details','docs':compress_doclist (make_doclist (doc.doctype,doc.name))},
      function(r, rt) {
        var doc = locals[mydoc.doctype][mydoc.name];
        refresh_many(['total_days_in_month','leave_without_pay','payment_days']);
      }
    );
  }
}
cur_frm.cscript.year = function(doc,cdt,cdn){
  if(doc.month && doc.year){
    var mydoc = doc
    $c('runserverobj', args={'method':'leave_details','docs':compress_doclist (make_doclist (doc.doctype,doc.name))},
      function(r, rt) {
        var doc = locals[mydoc.doctype][mydoc.name];
        refresh_many(['total_days_in_month','leave_without_pay','payment_days']);
      }
    );
  }
}

cur_frm.cscript.employee = function(doc,cdt,cdn){
  var mydoc = doc
  $c('runserverobj', args={'method':'set_values','docs':compress_doclist (make_doclist (doc.doctype,doc.name))},
    function(r, rt) {
      var doc = locals[mydoc.doctype][mydoc.name];
      refresh_many(['employee_name','branch','department','designation','grade','bank_name','bank_account_no','esic_no','pf_no','earning_details','deduction_details','total_days_in_month','leave_without_pay','payment_days']);
    }
  );
}

cur_frm.cscript.refresh = function(doc,cdt,cdn){
  cur_frm.cscript.get_tips(doc, cdt, cdn);

  if(doc.__islocal!=1) doc.flag=1;
  else  doc.flag=0;
  refresh_field('flag');
}