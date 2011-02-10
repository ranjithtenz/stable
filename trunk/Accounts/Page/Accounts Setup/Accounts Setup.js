pscript['onload_Accounts Setup'] = function(){
	var h = new PageHeader('as_header', 'Accounts Setup', 'Masters for setting your accounts');
	$dh(h.toolbar_area);

		var callback = function(r,rt){
		pg = r.message['Pages'];
		frm = r.message['Forms'];
		
		if(pg && pg.length){
			pscript.list_setup_master($i('accounts_setup'),'Page',pg);
		}
		
		if(frm && frm.length){
			pscript.list_setup_master($i('accounts_setup'),'DocType',frm);
		}
	}
	
	$c_obj('Report Control','get_setup_details','Accounts',callback);
}