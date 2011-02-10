pscript.onload_GeneralLedger = function() {
  
  // create the tabbed frame
  var t = new TabbedPage($i('fa_tabs_area'));


  if(in_list(session.rt, 'GL Entry')) {
    t.add_tab('General Ledger', function() { if(!pscript.gl_list.has_data())pscript.gl_list.run(); });
    fa_make_gl_tab(t);
  }

  // create a listing of activity

  t.tabs['General Ledger'].show();
}

pscript.load_from_chart_of_acc = function(cust_nm){
  //pscript.c_cont_txt.value = '';
  //pscript.c_comp_txt.value = cust_nm;
  pscript.get_cust_list();
  pscript.tab_area.tabs['Customers'].show();
}


// General Ledger
// --------------

function fa_make_gl_tab(t) {
  t.tabs['General Ledger'].tab_body.style.padding = '16px';
  
  var lst = new Listing(' ',1);
 
  lst.colwidths = ['15%','55%','15%','15%'];
  lst.colnames = ['Date','Detail','Debit','Credit'];
  lst.coltypes = ['Date','Data','Currency','Currency'];    

  lst.get_query = function() {
    this.group_by = ' GROUP BY voucher_no, account';
    this.query = 'SELECT `tabGL Entry`.posting_date, `tabGL Entry`.account, sum(`tabGL Entry`.debit), sum(`tabGL Entry`.credit), `tabGL Entry`.against, `tabGL Entry`.voucher_type, `tabGL Entry`.voucher_no, `tabGL Entry`.remarks FROM `tabGL Entry` WHERE is_cancelled="No"';
    this.query_max = 'select count(*) from `tabGL Entry` where `tabGL Entry`.is_cancelled="No"';
  }
	lst.show_cell = function(cell, ri, ci, d) {
		if(ci==1) {

			// head
			var div1 = $a(cell,'div'); div1.style.marginBottom = '2px';
			div1.innerHTML = 'Account: ' + d[ri][1];

			
			// remarks
			var div1 = $a(cell,'div', 'comment'); div1.style.marginBottom = '2px';
			div1.innerHTML = replace_newlines(d[ri][7]);
			
			// against
			if(d[ri][4]) {
				var div1 = $a(cell,'div','comment'); div1.style.paddingLeft = '8px';
				$a(div1,'span').innerHTML = 'Against: ' + d[ri][4].bold();
			}
			
			// voucher
			var div1 = $a(cell,'div','comment'); div1.style.paddingLeft = '8px';
			$a(div1,'span').innerHTML = 'Voucher: ';
			doc_link(div1,d[ri][5],d[ri][6]);			
		}
		else {
			this.std_cell(d,ri,ci);
		}
	}    
  pscript.gl_list = lst;
  
  lst.make(t.tabs['General Ledger'].tab_body);
  lst.set_default_sort('`tabGL Entry`.posting_date','DESC');

  lst.add_filter('Account','Link','Account','GL Entry','account');
  lst.add_filter('Voucher Type','Select',['All','Payable Voucher','Receivable Voucher','Bank Voucher','Cash Voucher','Credit Card Voucher','Debit Note','Credit Note'].join(NEWLINE),'GL Entry','voucher_type');
  lst.add_filter('From', 'Date', '', 'GL Entry', 'posting_date', '>=');
  lst.add_filter('To', 'Date', '', 'GL Entry', 'posting_date', '<=');

  //lst.filters['Account'].set_value('Abc Hardware - AC');
  //alert(lst.filters['Account'].get_value())
  lst.filters.Account.get_query = function(d) {
    return "SELECT tabAccount.name FROM tabAccount WHERE tabAccount.group_or_ledger = 'Ledger' AND is_active = 'Yes' AND tabAccount.%(key)s LIKE '%s' ORDER BY tabAccount.name ASC LIMIT 50"
  }

  lst.ledger_balance_area = $a(t.tabs['General Ledger'].tab_body,'div','',{margin:'8px 0px',fontSize:'14px'});
  lst.onrun = function() {
    var me = this;
    var f = this.filters['From'].get_value();
    var t = this.filters['To'].get_value();
    var arg = this.filters['Account'].get_value() + '~~~' + (f?f:'') + '~~~' + (t?t:'');
    $c_obj('GL Control', 'get_period_difference', arg, function(r,rt) { me.ledger_balance_area.innerHTML = ('Total for Period: ' + fmt_money(r.message)).bold();} );
  }

}
