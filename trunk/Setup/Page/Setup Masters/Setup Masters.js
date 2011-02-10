pscript['onload_Setup Masters'] = function(){
	var h = new PageHeader('setup_header','Setup Masters','');
	$dh(h.toolbar_area);
	
	//var lst = [['Competitor',''],['Contact','contact master'],['Country','Country master'],['Currency',''],['Customer','Customer and contact details'],['Customer Group','Customer category'],['Market Segment',''],['Order Lost Reason',''],['Price List','Price list master'],['Sales BOM','Sales BOM master'],['Sales Partner'],['Sales Person',''],['State','state master'],['Term','Terms And Conditions master'],['Territory','Business territory'],['Zone','Zone master']];
 
  var callback = function(r,rt){
		pg = r.message['Pages'];
		frm = r.message['Forms'];
		
		if(pg && pg.length){
			pscript.list_setup_master($i('setup_masters'),'Page',pg);
		}
		
		if(frm && frm.length){
			pscript.list_setup_master($i('setup_masters'),'DocType',frm);
		}
	}
	
	$c_obj('Report Control','get_setup_details','Setup',callback);	// parent, list of doctypes, page title
}