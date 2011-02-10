pscript['onload_Sales Reports'] = function(){
	var h = new PageHeader('sr_header','Sales Reports');
	
	var callback = function(r,rt){
		report_list = r.message['CRM'];
		
		var dv = $a('sr_body','div');
	
		rcount = 0;
		for(i=0; i<report_list.length;i++){
			if(rcount > 1){ rcount = 0; }
			else{ rcount = rcount; }
			
			if(rcount == 0){
				var tab = make_table(dv,1,2,'100%',['50%','50%']);
			}
			
			new HomeMenuReport($td(tab,0,Math.floor(i%2)), report_list[i][1], report_list[i][2]);
			rcount += 1;
		}
	}
	$c_obj('Report Control','get_reports','CRM',callback);
	/*
	report_list = [
				['Sales Order','Open Sales Orders'],
				['Sales Order Detail','Periodic Sales Summary'],
				['Sales Order Detail','Itemwise Sales Details'],
				['Territory','Territory Sales - Variance Report'],
				['Sales Order Detail','Sales Orderwise Booking & Delivery Summary'],
				['Sales Order Detail','Sales Orderwise Pending Amount To Deliver'],
				['Target Detail','Variance Report'],
				['Sales Order Detail','Sales Orderwise Pending Amount To Bill'],
				['Sales Order Detail','Sales Order Pending Items'],
				['Delivery Note','Monthly Despatched Trend'],
				['Delivery Note Packing Detail','Sales Orderwise Pending Packing Item Summary'],
				['Delivery Note Detail','Itemwise Delivery Details'],
				['Profile','Yearly Transaction Summary'],
				['Sales Order','Sales Agentwise Discount']
				]
	var dv = $a('sr_body','div');
	
	rcount = 0;
	for(i=0; i<report_list.length;i++){
		if(rcount > 1){ rcount = 0; }
		else{ rcount = rcount; }
		
		if(rcount == 0){
			var tab = make_table(dv,1,2,'100%',['50%','50%']);
		}
		
		new HomeMenuReport($td(tab,0,Math.floor(i%2)), report_list[i][0], report_list[i][1]);
		rcount += 1;
	}*/
}