pscript['onload_Inventory Setup'] = function(){
	var h = new PageHeader('is_header', 'Inventory Setup','Masters for setting your Inventory');
	$dh(h.toolbar_area);
	
	var callback = function(r,rt){
		pg = r.message['Pages'];
		frm = r.message['Forms'];
		
		if(pg && pg.length){
			pscript.list_setup_master($i('inventory_setup'),'Page',pg);
		}
		
		if(frm && frm.length){
			pscript.list_setup_master($i('inventory_setup'),'DocType',frm);
		}
	}
	
	$c_obj('Report Control','get_setup_details','Material Management',callback);
	
}