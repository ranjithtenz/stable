$import(Tips Common)
$import(Contact Control)

cur_frm.cscript.onload = function(doc,dt,dn){

	// history doctypes and scripts
	cur_frm.history_dict = {
		'Quotation' : 'cur_frm.cscript.make_qtn_list(this.body, this.doc)',
		'Sales Order' : 'cur_frm.cscript.make_so_list(this.body, this.doc)',
		'Delivery Note' : 'cur_frm.cscript.make_dn_list(this.body, this.doc)',
		'Sales Invoice' : 'cur_frm.cscript.make_si_list(this.body, this.doc)'
	}

	// make contact, history list body
	cur_frm.cscript.make_cl_body();
	cur_frm.cscript.make_hl_body();
	
	if(doc.country) cur_frm.cscript.get_states(doc,dt,dn);


}

cur_frm.cscript.refresh = function(doc,dt,dn) {
	if(sys_defaults.cust_master_name == 'Customer Name')
		hide_field('naming_series');
	else
		unhide_field('naming_series');
  if(doc.country){ cur_frm.cscript.country(doc,dt,dn);}
	if(doc.__islocal){
		// set message
		cur_frm.cscript.set_cl_msg(doc);
		cur_frm.cscript.set_hl_msg(doc);
	}
	else{
		// make lists
		cur_frm.cscript.make_contact(doc,dt,dn);
		cur_frm.cscript.make_history(doc,dt,dn);
	}
}

cur_frm.cscript.CGHelp = function(doc,dt,dn){
	var call_back = function(){

		var sb_obj = new SalesBrowser();				
		sb_obj.set_val('Customer Group');
	}
	loadpage('Sales Browser',call_back);
}

cur_frm.cscript.validate = function(doc, dt, dn) {
		// below part is commented coz it does not allow '.', need to find soln which only disallows "'"
	/*var regex = /^[a-zA-Z0-9_ ]+$/;
	if(doc.__islocal && regex.test(doc.customer_name)==false)
	{
		alert("Please enter a valid Customer name.");
		validated = false;
	} */

}

cur_frm.cscript.show_workorders = function() {
	loadreport("Sales Order", "Work Order List", function(f) { 
		f.set_filter("Sales Order", "Customer Name", cur_frm.doc.name);
	});
}

//get query select Customer Group
cur_frm.fields_dict['customer_group'].get_query = function(doc,dt,dn) {
	return 'SELECT `tabCustomer Group`.`name`, `tabCustomer Group`.`parent_customer_group` FROM `tabCustomer Group` WHERE `tabCustomer Group`.`is_group` = "No" AND `tabCustomer Group`.`docstatus`!= 2 AND `tabCustomer Group`.%(key)s LIKE "%s" ORDER BY	`tabCustomer Group`.`name` ASC LIMIT 50';
}

//get query for lead
cur_frm.fields_dict['lead_name'].get_query = function(doc,dt,dn){
	return 'SELECT `tabLead`.`name` FROM `tabLead` WHERE `tabLead`.`status`!="Converted" AND `tabLead`.%(key)s LIKE "%s" ORDER BY `tabLead`.`name` ASC LIMIT 50';
}

// make quotation list
cur_frm.cscript.make_qtn_list = function(parent,doc){

	var lst = new Listing();
	lst.colwidths = ['5%','20%','20%','20%','20%','15%'];
	lst.colnames = ['Sr.','Id','Status','Quotation Date','Contact Person','Grand Total'];
	lst.coltypes = ['Data','Link','Data','Data','Data','Currency'];
	lst.coloptions = ['','Quotation','','','',''];

	// set list opts
	cur_frm.cscript.set_list_opts(lst);

	var q = repl("select name,status,transaction_date, contact_person, grand_total from tabQuotation where customer='%(cust)s'", {'cust':doc.name});
	var q_max = repl("select count(name) from tabQuotation where customer='%(cust)s'", {'cust':doc.name});
	
	cur_frm.cscript.run_list(lst,parent,q,q_max,doc,'Quotation','Quotation');
}

// make so list
cur_frm.cscript.make_so_list = function(parent,doc){
	var lst = new Listing();
	lst.colwidths = ['5%','20%','20%','30%','25%'];
	lst.colnames = ['Sr.','Id','Status','Sales Order Date','Grand Total'];
	lst.coltypes = ['Data','Link','Data','Data','Currency'];
	lst.coloptions = ['','Sales Order','','',''];

	// set list opts
	cur_frm.cscript.set_list_opts(lst);

	var q = repl("select name,status,transaction_date, grand_total from `tabSales Order` where customer='%(cust)s'", {'cust':doc.name});
	var q_max = repl("select count(name) from `tabSales Order` where customer='%(cust)s'", {'cust':doc.name});
	
	cur_frm.cscript.run_list(lst,parent,q,q_max,doc,'Sales Order','Sales Order');
}

// make dn list
cur_frm.cscript.make_dn_list = function(parent,doc){
	var lst = new Listing();
	lst.colwidths = ['5%','20%','20%','20%','20%','15%'];
	lst.colnames = ['Sr.','Id','Status','Delivery Note Date','Territory','Grand Total'];
	lst.coltypes = ['Data','Link','Data','Data','Link','Currency'];
	lst.coloptions = ['','Delivery Note','','','Territory',''];

	// set list opts
	cur_frm.cscript.set_list_opts(lst);

	var q = repl("select name,status,transaction_date,territory,grand_total from `tabDelivery Note` where customer='%(cust)s'", {'cust':doc.name});
	var q_max = repl("select count(name) from `tabDelivery Note` where customer='%(cust)s'", {'cust':doc.name});
	
	cur_frm.cscript.run_list(lst,parent,q,q_max,doc,'Delivery Note','Delivery Note');
}

// make si list
cur_frm.cscript.make_si_list = function(parent,doc){
	var lst = new Listing();
	lst.colwidths = ['5%','20%','20%','20%','20%','15%'];
	lst.colnames = ['Sr.','Id','Posting Date','Due Date','Debit To','Grand Total'];
	lst.coltypes = ['Data','Link','Data','Data','Link','Currency'];
	lst.coloptions = ['','Receivable Voucher','','','Account',''];

	// set list opts
	cur_frm.cscript.set_list_opts(lst);

	var q = repl("select name,posting_date,due_date,debit_to,grand_total from `tabReceivable Voucher` where customer='%(cust)s'", {'cust':doc.name});
	var q_max = repl("select count(name) from `tabReceivable Voucher` where customer='%(cust)s'", {'cust':doc.name});
	
	cur_frm.cscript.run_list(lst,parent,q,q_max,doc,'Sales Invoice','Receivable Voucher');
}
