report.customize_filters = function() {
  this.mytabs.items['Select Columns'].hide()
  //this.mytabs.items['More Filters'].hide()
  this.hide_all_filters();
  this.add_filter({fieldname:'follow_up_on', label:'Follow up on', fieldtype:'Select', options:'Lead'+NEWLINE+'Enquiry'+NEWLINE+'Quotation',report_default:'Lead',ignore : 1,parent:'Follow up'});
  this.add_filter({fieldname:'lead_name', label:'Lead', fieldtype:'Link', options:'Lead', report_default:'', ignore : 1, parent:'Follow up'});
  this.add_filter({fieldname:'enq_name', label:'Enquiry', fieldtype:'Link', options:'Enquiry', report_default:'', ignore : 1, parent:'Follow up'});
  this.add_filter({fieldname:'qtn_name', label:'Quotation', fieldtype:'Link', options:'Quotation', report_default:'', ignore : 1, parent:'Follow up'});
  
  this.filter_fields_dict['Follow up'+FILTER_SEP +'Follow up on'].df.in_first_page = 1;
  this.filter_fields_dict['Follow up'+FILTER_SEP +'Lead'].df.in_first_page = 1;
  this.filter_fields_dict['Follow up'+FILTER_SEP +'Enquiry'].df.in_first_page = 1;
  this.filter_fields_dict['Follow up'+FILTER_SEP +'Quotation'].df.in_first_page = 1;
  
  this.filter_fields_dict['Follow up'+FILTER_SEP +'Follow up type'].df.filter_hide = 0;
  this.filter_fields_dict['Follow up'+FILTER_SEP +'From Date'].df.filter_hide = 0;
  this.filter_fields_dict['Follow up'+FILTER_SEP +'To Date'].df.filter_hide = 0;
  //this.filter_fields_dict['Follow up'+FILTER_SEP +'Follow up type'].df.in_first_page = 1;
  //this.filter_fields_dict['Follow up'+FILTER_SEP +'From Date'].df.in_first_page = 1;
  //this.filter_fields_dict['Follow up'+FILTER_SEP +'To Date'].df.in_first_page = 1;
}


report.get_query = function() {
  var follow_up_on=''; var on_id =''; var on_type = ''; var from_date =''; var to_date ='';
  
  follow_up_on = this.filter_fields_dict['Follow up'+FILTER_SEP+'Follow up on'].get_value();
  if(follow_up_on == 'Lead') on_id = this.filter_fields_dict['Follow up'+FILTER_SEP+'Lead'].get_value();   
  else if(follow_up_on == 'Enquiry') on_id = this.filter_fields_dict['Follow up'+FILTER_SEP+'Enquiry'].get_value();   
  else if(follow_up_on == 'Quotation') on_id = this.filter_fields_dict['Follow up'+FILTER_SEP+'Quotation'].get_value();
  
  on_type = this.filter_fields_dict['Follow up'+FILTER_SEP+'Follow up type'].get_value();
  from_date = this.filter_fields_dict['Follow up'+FILTER_SEP+'From Date'].get_value();
  to_date = this.filter_fields_dict['Follow up'+FILTER_SEP+'To Date'].get_value();
  
  if(!follow_up_on) msgprint("Please select 'Follow up on'");
  else {
    var cond1 = '';var cond2 = '';var cond3 = '';var cond4 = '';
    if(on_id) cond1='t1.parent = "'+on_id+'" AND ';
    if(on_type!='') cond2 = 't1.follow_up_type ="'+on_type+'" AND ';
    if(from_date) cond3 = 't1.date >="'+from_date+'" AND ';
    if(to_date) cond4 = 't1.date <"'+to_date+'" AND ';
  }
  
  var q ='SELECT distinct t1.parent AS "Follow up for", t1.date AS "Follow up Date", t1.notes AS "Description", t1.follow_up_type AS "Follow up type" FROM `tabFollow up` t1 WHERE '+cond1+cond2+cond3+cond4+'t1.parenttype = "'+follow_up_on+'"';
  return q;
}