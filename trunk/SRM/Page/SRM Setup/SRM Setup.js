pscript['onload_SRM Setup'] = function(){
	var h = new PageHeader('ss_header','Buying Setup','Masters for setting your buying process');
	$dh(h.toolbar_area);
	
	var callback = function(r,rt){
		pg = r.message['Pages'];
		frm = r.message['Forms'];
		
		if(pg && pg.length){
			pscript.list_setup_master($i('srm_setup'),'Page',pg);
		}
		
		if(frm && frm.length){
			pscript.list_setup_master($i('srm_setup'),'DocType',frm);
		}
	}
	
	$c_obj('Report Control','get_setup_details','SRM',callback);
}