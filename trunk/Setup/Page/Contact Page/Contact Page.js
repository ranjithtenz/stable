pscript['onload_Contact Page'] = function(){
 	var wrapper = page_body.pages['Contact Page'];
 	wrapper.listings = {};
  
 	wrapper.head = new PageHeader(wrapper,'Contacts Manager','Manage your contacts');
	wrapper.head.add_button('+ New Contact',function(){ newdoc('Contact'); },1,'ui-icon-plusthick', 1);
	
	wrapper.tray = new TrayPage(wrapper);
	wrapper.tray.add_item('Customers', function(label) { wrapper.show_listing(label); }, null, 1);
	wrapper.tray.add_item('Suppliers', function(label) { wrapper.show_listing(label); }, null, 1);
	wrapper.tray.add_item('Sales Partners', function(label) { wrapper.show_listing(label); }, null, 1);

	wrapper.show_listing = function(label) {
		if(!wrapper.listings[label]) {
			wrapper.listings[label] = new ContactListing(label, wrapper.tray.items[label].body);
			wrapper.listings[label].lst.run();
		}
	}

	wrapper.tray.items['Customers'].expand();
	// make listings onshow	
}

ContactListing = function(label, parent) {
	var label_fields = {
		'Customers':['customer_name','is_customer'],
		'Suppliers':['supplier_name','is_supplier'],
		'Sales Partners':['sales_partner','is_sales_partner']
	}
	
	
	// make the list
	var l = new Listing('',1);
	l.colwidths = ['70%','15%','15%'];
	l.get_query = function() {
		this.query = "select name, contact_name, email_id, contact_no, "+ label_fields[label][0] +", department, designation from tabContact where "+label_fields[label][1]+"=1 and docstatus!=2"
		this.query_max = "select count(*) from tabContact where "+label_fields[label][1]+"=1 and docstatus!=2"
	}
	l.show_cell = function(cell, ri, ci, d) {
		if(ci==0) {
			// link
			var div = $a(cell, 'div', '', {padding:'2px 0px'});
			var span = $a(div,'span','link_type')
			span.innerHTML = d[ri][1] + ' (' + d[ri][0] + ')';
			span.dn = d[ri][0];
			span.onclick = function() { loaddoc('Contact',this.dn) }
			
			// org & designation
			if(d[ri][5] || d[ri][6] || d[ri][4]) {
				var div = $a(cell, 'div', '', {padding:'2px 0px',color:'#444',fontSize:'11px'});

				var tmp = [];
				if(d[ri][6]) tmp.push(d[ri][6]);
				if(d[ri][5]) tmp.push(d[ri][5]);
				if(d[ri][4]) tmp.push(d[ri][4].bold());
				
				if(tmp.length)
					div.innerHTML = tmp.join(', ');
			}
			
			// contact details
			var div = $a(cell, 'div', '', {padding:'2px 0px',color:'#444',fontSize:'11px'});

			var tmp = [];
			if(d[ri][2]) tmp.push('Email'.bold() + ': ' + d[ri][2]);
			if(d[ri][3]) tmp.push('Phone'.bold() + ': ' + d[ri][3]);
			
			if(tmp.length)
				div.innerHTML = tmp.join(' | ');
		}
	}	
	l.make(parent);

	// filters
	l.add_filter('Contact Name', 'Data', '', 'Contact', 'contact_name', 'LIKE');
	l.add_filter(label.substr(0,label.length-1), 'Data', '', 'Contact', label_fields[label][0], 'LIKE');
	
	l.sort_by = 'contact_name';
	l.sort_order = 'ASC'
	
	this.lst = l;
}

// callers -------------------------

//manage customer contact
pscript.load_contact_page = function(label, key){
	var wrapper = page_body.pages['Contact Page'];
	wrapper.tray.items[label].expand();
	wrapper.listings[label].lst.filters['Contact Name'].input.value = '';
	wrapper.listings[label].lst.filters[label.substr(0,label.length-1)].input.value = key;
}

pscript.load_from_customer = function(key){
	pscript.load_contact_page('Customers',key)
}
pscript.load_from_supplier = function(key){
	pscript.load_contact_page('Suppliers',key)
}
pscript.load_from_partner = function(key){
	pscript.load_contact_page('Sales Partners',key)
}
