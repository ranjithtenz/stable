
// Validation For To Date
// ================================================================================================
cur_frm.cscript.to_date = function(doc, cdt, cdn) {
  $c('runserverobj', args={'method':'to_date_validation','docs':compress_doclist([doc])},
    function(r, rt) {
    var doc = locals[cdt][cdn];
    if (r.message) {
      alert("To date cannot be before from date");
      doc.to_date = '';
      refresh_field('to_date');
    }
    }
  ); 
}

// Allocation Type
// ================================================================================================
cur_frm.cscript.allocation_type = function (doc, cdt, cdn){
  doc.no_of_days = '';
  refresh_field('no_of_days');
}

//get query
cur_frm.fields_dict['leave_type'].get_query = function(doc,cdt,cdn){
  return 'SELECT `tabLeave Type`.name FROM `tabLeave Type` WHERE `tabLeave Type`.name NOT IN("Leave Without Pay","Compensatory Off") AND `tabLeave Type`.docstatus !=2 AND `tabLeave Type`.name LIKE "%s" ORDER BY `tabLeave Type`.name ASC LIMIT 50';
}