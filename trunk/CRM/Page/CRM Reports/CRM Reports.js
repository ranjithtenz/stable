pscript['onload_CRM Reports'] = function(){
	var h = new PageHeader('crm_report_header','CRM Reports','');
	$dh(h.toolbar_area);
	
	var lst = [['Sales Order Detail','Sales Orderwise Pending Amount To Deliver'],['Target Detail', 'Variance Report'],['Sales Order Detail','Sales Orderwise Pending Amount To Bill'],['Sales Order Detail', 'Sales Order Pending Items'],['Delivery Note', 'Monthly Despatched Trend'],['Delivery Note Packing Detail', 'Sales Orderwise Pending Packing Item Summary'],['Delivery Note Detail', 'Itemwise Delivery Details'],['Profile', 'Yearly Transaction Summary'], ['Sales Order', 'Sales Agentwise Discount']];
  
	//pscript.list_setup_master($i('crm_reports'), lst);	// parent, list of doctypes, page title
}