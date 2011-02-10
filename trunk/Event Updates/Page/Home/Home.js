pscript['onload_Home'] = function(){
	var parent = $i('home_div');
	var ph = new PageHeader(parent, 'Home');
	var body = $a(parent, 'div', '', {margin: '16px'});
	
	parent.tab = $a(body, 'table')
	pscript.show_modules(parent)
}

pscript.show_modules = function(body) {
	var per_row = 4;
	var callback = function(r,rt){		
	
		// menu
		var ml = r.message; 
		var ci=0;
		var t = body.tab;
		
		for(var m=0; m<ml.length; m++){
			if(ci==0) 
				t.insertRow(t.rows.length);
			var cell = t.rows[t.rows.length-1].insertCell(ci);
			$y(cell, {padding:'8px', width:'56px'});
			ci++;
			if(ci==per_row) ci=0; 
			
			var mod = new ModuleMenu($td(t,t.rows.length-1,ci-1), ml, m);
		}
	}
	$c_obj('Home Control', 'get_modules', '', callback);
}

// Module Menu
ModuleMenu = function(parent, ml, m){
	this.wrapper = $a(parent, 'div','',{padding:'4px', cursor:'pointer'});
		
	// icon
	this.icon = $a(this.wrapper,'div', 'back_img ' + ml[m]['module_label'],{margin:'auto'});

	// tooltip
	set_custom_tooltip(this.icon, ml[m]['module_label']);
	
	// module page
	this.wrapper.module_page = ml[m]['module_page'];
		
	this.wrapper.onclick = function(){
		loadpage(this.module_page);
	}
}
