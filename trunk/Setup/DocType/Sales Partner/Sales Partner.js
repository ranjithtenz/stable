$import(Tips Common)
$import(Contact Control)

cur_frm.cscript.onload = function(doc,dt,dn){
	// history doctypes and scripts
	cur_frm.history_dict = {
		'Sales Order' : 'cur_frm.cscript.make_so_list(this.body, this.doc)',
		'Delivery Note' : 'cur_frm.cscript.make_dn_list(this.body, this.doc)',
		'Sales Invoice' : 'cur_frm.cscript.make_si_list(this.body, this.doc)'
	}
	
	// make contact, history list body
	cur_frm.cscript.make_cl_body();
	cur_frm.cscript.make_hl_body();
}

cur_frm.cscript.refresh = function(doc,dt,dn){
  cur_frm.cscript.get_tips(doc, dt, dn);
  
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

// ******************** ITEM Group ******************************** 
cur_frm.fields_dict['partner_target_details'].grid.get_field("item_group").get_query = function(doc, dt, dn) {
  return 'SELECT `tabItem Group`.`name`,`tabItem Group`.`parent_item_group` FROM `tabItem Group` WHERE `tabItem Group`.is_group="No" AND `tabItem Group`.docstatus != 2 AND `tabItem Group`.%(key)s LIKE "%s" LIMIT 50'
}

// make sales order list
cur_frm.cscript.make_so_list = function(parent, doc){
	var lst = new Listing();
	lst.colwidths = ['5%','20%','20%','15%','20%','20%'];
	lst.colnames = ['Sr.','Id','Status','SO Date','Total Commission','Grand Total'];
	lst.coltypes = ['Data','Link','Data','Data','Currency','Currency'];
	lst.coloptions = ['','Sales Order','','','','',''];

	cur_frm.cscript.set_list_opts(lst);
	
	var q = repl("select name,status,transaction_date, total_commission,grand_total from `tabSales Order` where sales_partner='%(sp)s'", {'sp':doc.name});
	var q_max = repl("select count(name) from `tabSales Order` where sales_partner='%(cust)s'", {'sp':doc.name});
	
	cur_frm.cscript.run_list(lst,parent,q,q_max,doc,'Sales Order','Sales Order');
}

// make delivery note list
cur_frm.cscript.make_dn_list = function(parent,doc){
	var lst = new Listing();
	lst.colwidths = ['5%','20%','20%','15%','20%','20%'];
	lst.colnames = ['Sr.','Id','Status','Date','Total Commission','Grand Total'];
	lst.coltypes = ['Data','Link','Data','Data','Currency','Currency'];
	lst.coloptions = ['','Delivery Note','','','','',''];

	cur_frm.cscript.set_list_opts(lst);

	var q = repl("select name,status,transaction_date, total_commission,grand_total from `tabDelivery Note` where sales_partner='%(sp)s'", {'sp':doc.name});
	var q_max = repl("select count(name) from `tabDelivery Note` where sales_partner='%(cust)s'", {'sp':doc.name});
	
	cur_frm.cscript.run_list(lst,parent,q,q_max,doc,'Delivery Note','Delivery Note');	
}

// make sales invoice list
cur_frm.cscript.make_si_list = function(parent,doc){
	var lst = new Listing();
	lst.colwidths = ['5%','25%','20%','25%','25%'];
	lst.colnames = ['Sr.','Id','Invoice Date','Total Commission','Grand Total'];
	lst.coltypes = ['Data','Link','Data','Data','Currency','Currency'];
	lst.coloptions = ['','Receivable Voucher','','','',''];

	cur_frm.cscript.set_list_opts(lst);

	var q = repl("select name,posting_date, total_commission,grand_total from `tabReceivable Voucher` where sales_partner='%(sp)s'", {'sp':doc.name});
	var q_max = repl("select count(name) from `tabReceivable Voucher` where sales_partner='%(cust)s'", {'sp':doc.name});
	
	cur_frm.cscript.run_list(lst,parent,q,q_max,doc,'Sales Invoice','Receivable Voucher');	
}