$import(Contact Control)

cur_frm.cscript.onload = function(doc,dt,dn){

	// history doctypes and scripts
	cur_frm.history_dict = {
		'Purchase Order' : 'cur_frm.cscript.make_po_list(this.body, this.doc)',
		'Purchase Receipt' : 'cur_frm.cscript.make_pr_list(this.body, this.doc)',
		'Purchase Invoice' : 'cur_frm.cscript.make_pi_list(this.body, this.doc)'
	}
	
	// make contact, history list body
	cur_frm.cscript.make_cl_body();
	cur_frm.cscript.make_hl_body();
}

cur_frm.cscript.refresh = function(doc,dt,dn) {
  if(sys_defaults.supp_master_name == 'Supplier Name')
    hide_field('naming_series');
  else
    unhide_field('naming_series'); 
    
  if(doc.__islocal){
  	if(doc.country) cur_frm.cscript.get_states(doc,dt,dn);
  	
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

// make purchase order list
cur_frm.cscript.make_po_list = function(parent, doc){
	var lst = new Listing();
	lst.colwidths = ['5%','25%','20%','25%','25%'];
	lst.colnames = ['Sr.','Id','Status','PO Date','Grand Total'];
	lst.coltypes = ['Data','Link','Data','Data','Currency'];
	lst.coloptions = ['','Purchase Order','','','',''];

	cur_frm.cscript.set_list_opts(lst);

	var q = repl("select name,status,transaction_date, grand_total from `tabPurchase Order` where supplier='%(sup)s'", {'sup':doc.name});
	var q_max = repl("select count(name) from `tabPurchase Order` where supplier='%(sup)s'", {'sup':doc.name});
	
	cur_frm.cscript.run_list(lst,parent,q,q_max,doc,'Purchase Order','Purchase Order');
}

// make purchase receipt list
cur_frm.cscript.make_pr_list = function(parent,doc){
	var lst = new Listing();
	lst.colwidths = ['5%','20%','20%','20%','15%','20%'];
	lst.colnames = ['Sr.','Id','Status','Receipt Date','% Billed','Grand Total'];
	lst.coltypes = ['Data','Link','Data','Data','Currency','Currency'];
	lst.coloptions = ['','Purchase Receipt','','','',''];

	cur_frm.cscript.set_list_opts(lst);
	
	var q = repl("select name,status,transaction_date,per_billed,grand_total from `tabPurchase Receipt` where supplier='%(sup)s'", {'sup':doc.name});
	var q_max = repl("select count(name) from `tabPurchase Receipt` where supplier='%(sup)s'", {'sup':doc.name});
	
	cur_frm.cscript.run_list(lst,parent,q,q_max,doc,'Purchase Receipt','Purchase Receipt');
}

// make purchase invoice list
cur_frm.cscript.make_pi_list = function(parent,doc){
	var lst = new Listing();
	lst.colwidths = ['5%','20%','20%','20%','15%','20%'];
	lst.colnames = ['Sr.','Id','Voucher Date','Credit To','Bill Date','Grand Total'];
	lst.coltypes = ['Data','Link','Data','Data','Currency','Currency'];
	lst.coloptions = ['','Payable Voucher','','','',''];

	cur_frm.cscript.set_list_opts(lst);

	var q = repl("select name,voucher_date,credit_to,bill_date,grand_total from `tabPayable Voucher` where supplier='%(sup)s'", {'sup':doc.name});
	var q_max = repl("select count(name) from `tabPayable Voucher` where supplier='%(sup)s'", {'sup':doc.name});
	
	cur_frm.cscript.run_list(lst,parent,q,q_max,doc,'Purchase Invoice','Payable Voucher');	
}