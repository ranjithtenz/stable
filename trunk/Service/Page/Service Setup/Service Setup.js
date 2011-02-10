pscript['onload_Service Setup'] = function(){
	var h = new PageHeader('service_header','Service Setup','Setup all Service masters');
	$dh(h.toolbar_area);
	
	var callback = function(r,rt){
		pg = r.message['Pages'];
		frm = r.message['Forms'];
		
		if(pg && pg.length){
			pscript.list_setup_master($i('service_setup'),'Page',pg);
		}
		
		if(frm && frm.length){
			pscript.list_setup_master($i('service_setup'),'DocType',frm);
		}
	}
	
	$c_obj('Report Control','get_setup_details','Service',callback);
}