pscript['onload_CRM Setup'] = function(){
	var h = new PageHeader('crm_header','Selling Setup','Masters for setting your selling process (CRM)');
	$dh(h.toolbar_area);
	
	//var lst = [['Competitor',''],['Contact','contact master'],['Country','Country master'],['Currency',''],['Customer','Customer and contact details'],['Customer Group','Customer category'],['Market Segment',''],['Order Lost Reason',''],['Price List','Price list master'],['Sales BOM','Sales BOM master'],['Sales Partner'],['Sales Person',''],['State','state master'],['Terms And Conditions','Terms And Conditions master'],['Territory','Business territory'],['Zone','Zone master']];
  	var callback = function(r,rt){
		pg = r.message['Pages'];
		frm = r.message['Forms'];
		
		if(pg && pg.length){
			pscript.list_setup_master($i('crm_setup'),'Page',pg);
		}
		
		if(frm && frm.length){
			pscript.list_setup_master($i('crm_setup'),'DocType',frm);
		}
	}
	
	$c_obj('Report Control','get_setup_details','CRM',callback);
}