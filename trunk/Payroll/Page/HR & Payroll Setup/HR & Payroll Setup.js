pscript['onload_HR & Payroll Setup'] = function(){
	var h = new PageHeader('payroll_header','HR & Payroll Setup','Setup all HR & Payroll masters');
	$dh(h.toolbar_area);
	
	var callback = function(r,rt){
		pg = r.message['Pages'];
		frm = r.message['Forms'];
		
		if(pg && pg.length){
			pscript.list_setup_master($i('payroll_setup'),'Page',pg);
		}
		
		if(frm && frm.length){
			pscript.list_setup_master($i('payroll_setup'),'DocType',frm);
		}
	}
	
	$c_obj('Report Control','get_setup_details','Payroll',callback);
}