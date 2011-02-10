pscript['onload_Production Setup'] = function(){
	var h = new PageHeader('ps_header','Production Setup','Masters for setting Production');
	$dh(h.toolbar_area);
	
	var callback = function(r,rt){
		pg = r.message['Pages'];
		frm = r.message['Forms'];
		
		if(pg && pg.length){
			pscript.list_setup_master($i('production_setup'),'Page',pg);
		}
		
		if(frm && frm.length){
			pscript.list_setup_master($i('production_setup'),'DocType',frm);
		}
	}
	
	$c_obj('Report Control','get_setup_details','Production',callback);
}