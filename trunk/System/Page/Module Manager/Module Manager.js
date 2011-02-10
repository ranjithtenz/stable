pscript['onload_Module Manager'] = function() {
	var w = page_body.pages['Module Manager'];

	// head
	w.head = new PageHeader(w, 'Module Manager');

	// tray
	w.body = $a(w,'div');
	w.tray = new TrayPage(w.body,null,'200px');

	// main table
	pscript.make_modules();	
}

// make modules
// -------------------------------------------------

pscript.make_modules = function() {
	var w = page_body.pages['Module Manager'];

	// clear
	$dh(w.body);

	add_space_holder(w.body);
	$c_obj('Module Manager','get_module_list','',pscript.mod_man_show);
}

// render module list
// -------------------------------------------------

pscript.mod_man_show = function(r,rt) {
	var w = page_body.pages['Module Manager'];
	var ml = r.message;
	pscript.mod_ml = ml;

	this.modules =[];
	remove_space_holder();	

	// render Overview
	pscript.mod_man_overview(w, r.message);

	// render modules
	for(var i=0; i<ml.length; i++) {
		this.modules.push(new ManagerModule(ml[i]));
	}
	
	$ds(w.body);
}

// -------------------------------------------------

pscript.mod_man_overview = function(w, ml) {
	var item = w.tray.add_item('Module Manager', null, 0, 1)

	// buttons for update everything and control panel
	var tb_div = $a(item.body, 'div', '', {padding:'8px', marginBottom:'8px', backgroundColor:'#EEF'});
	
	var btn1 = $a(tb_div, 'button');
	$(btn1).html('Update All').click(pscript.mod_update_all).button();

	var btn2 = $a(tb_div, 'button');
	$(btn2).html('Update Control Panel').click(pscript.mod_update_cp).button();

	// var module list with updates
	for(var i=0; i<ml.length; i++) {
		var div = $a(item.body, 'div', '', {margin:'8px 0px'});
		var tab = make_table(div,1,2,'',['200px','100px']);
		$td(tab,0,0).innerHTML = ml[i][0].bold();
		$td(tab,0,1).innerHTML = ml[i][3];
		if(ml[i][3]=='Not Installed') {
			// not installed
			$y($td(tab,0,1),{color:'#666'});
		} else if (ml[i][3]=='Installed' && ml[i][2]!=ml[i][1].update_date) {
			// not updated
			$y($td(tab,0,1),{color:'ORANGE'});
		} else {
			// updated
			$y($td(tab,0,1),{color:'GREEN'});
		}
	}
	
	item.expand();
}

// -------------------------------------------------

pscript.mod_update_cp = function() {
	var callback = function(r,rt) {
		if(!r.exc) msgprint('Updated!')
	}
	$c_obj('Module Manager','update_cp', '', callback);
}

// -------------------------------------------------

pscript.mod_update_all = function() {
	//$c_obj('Module Manager','update_cp', '', callback)	
}

// MM_Module
// -------------------------------------------------

ManagerModule = function(det) {
	var me = this;
	
	this.det = det;
	var w = page_body.pages['Module Manager'];
	
	// add tray item
	this.item = w.tray.add_item(det[0], function() { me.show() }, 0, 1);
	this.item.manager_module = this;
}

// -------------------------------------------------

ManagerModule.prototype.make_button = function(parent, label, mod, import_or_export) {
	var btn = $a(parent,'button');
	btn.mod = mod;
	btn.import_or_export = import_or_export;
	$(btn).html(label).click(function() { 
		pscript.mod_server_call(this.mod, this.import_or_export, 'module'); 
	}).button();
	return btn;
}

// -------------------------------------------------

ManagerModule.prototype.show = function() {
	if(!this.loaded) this.refresh();
}


// -------------------------------------------------

ManagerModule.prototype.refresh = function() {
	var me = this;
	var callback = function(r, rt) {
		me.in_files_list = r.message.in_files;
		me.in_system_list = r.message.in_system;
		me.render();
	}
	$c_obj('Module Manager','get_module_details',this.det[0],callback)
	me.loaded = 1;
}


// -------------------------------------------------

ManagerModule.prototype.render = function() {
	this.item.body.innerHTML = ''; // clear
	this.render_status();
	this.render_items();
}

// -------------------------------------------------

ManagerModule.prototype.render_status = function() {
	var det = this.det;
	var h = $a(this.item.body, 'div', '', {padding:'8px', marginBottom:'8px', backgroundColor:'#EEF'});
	
	// status
	
	var status_div = $a(h, 'div', '', {marginBottom:'8px'});
	status_div.innerHTML = det[3];
	
	// import / export buttons
	var div = $a(h, 'div', '', {marginBottom:'8px'});
	if(det[3]=='Not Installed') {

		// not installed
		this.make_button(div, 'Install', det[0], 'import');
		this.make_button(div, 'Import Files', det[0], 'import_attach');

	} else if (det[3]=='Installed' && det[2]!=det[1].update_date) {

		// not updated
		this.make_button(div, 'Update', det[0], 'import');
		this.make_button(div, 'Import Files', det[0], 'import_attach');

		$y(status_div,{color:'ORANGE'});
	} else {

		// updated
		$y(status_div,{color:'GREEN'});
		this.make_button(div, 'Update', det[0], 'import');
		this.make_button(div, 'Import Files', det[0], 'import_attach');
	}
	
	// export button
	if(det[3]!='Not Installed') {
		this.make_button(div, 'Export',det[0], 'export');
	}

	// refresh
	var btn = this.make_button(div, 'Refresh',det[0], 'export');
	var me = this;
	btn.onclick = function() {
		me.refresh();
	}

	
	this.header = h;
}

// -------------------------------------------------

ManagerModule.prototype.build_status = function() {
	this.all_items = {}
	var me = this;
	
	var scan = function(dict, list) {
		for(var i=0; i<list.length; i++) {
			var t = list[i];
			if(!dict[t[0]]) dict[t[0]] = {};
			if(!dict[t[0]][t[1]]) dict[t[0]][t[1]] = t[2];

			if(!me.all_items[t[0]]) me.all_items[t[0]] = {};
			if(!me.all_items[t[0]][t[1]]) me.all_items[t[0]][t[1]] = 1;
		}	
		
	}
	this.in_files = {};
	scan(this.in_files, this.in_files_list);

	this.in_system = {};
	scan(this.in_system, this.in_system_list);
}

// -------------------------------------------------

ManagerModule.prototype.render_items = function() {
	var w = $a(this.item.body, 'div');
	this.build_status();
	var dt_list = keys(this.all_items).sort();
	
	for(var i=0; i< dt_list.length; i++) {
		var item_list = keys(this.all_items[dt_list[i]]).sort();
		for(j=0; j< item_list.length; j++) {
			var dt = dt_list[i]; var dn = item_list[j];
			var mf = this.in_files[dt] ? this.in_files[dt][dn] : null;
			var ms = this.in_system[dt] ? this.in_system[dt][dn] : null;

			new ManagerModuleItem(this, w, dt, dn, mf, ms);
		}
	}
}


// -------------------------------------------------

ManagerModuleItem = function(mm, parent, dt, dn, modified_file, modified_system) {
	this.dt = dt; this.dn = dn; var modified = false; var fcolor = '#000'; this.mm = mm;

	var div = $a(parent,'div');
	if(modified_file && modified_system) {
		if(modified_file != modified_system) {
			modified=true;
			var fcolor='RED';
			
			// newly changed items on top
			if(parent.firstChild)
				parent.insertBefore(div, parent.firstChild);
			else
				parent.appendChild(div);
		}
	}
	
	this.tab = make_table(div, 1, 6, null, ['20px','20px','160px','160px', '100px', '100px'], {padding:'2px', verticalAlign:'middle'});
	$td(this.tab,0,2).innerHTML = dt;
	$td(this.tab,0,3).innerHTML = dn;

	$y($td(this.tab,0,2),{color:fcolor});
	$y($td(this.tab,0,3),{color:fcolor});
	
	// in files
	if(mm.in_files[dt] && mm.in_files[dt][dn]) 
		$td(this.tab,0,1).innerHTML = '<img src="images/icons/folder.gif">';
		
	// in system
	if(mm.in_system[dt] && mm.in_system[dt][dn]) 
		$td(this.tab,0,0).innerHTML = '<img src="images/icons/database.png">';
		
	// import button
	this.make_button($td(this.tab,0,4),'Import','import');
	
	// export button
	this.make_button($td(this.tab,0,5),'Export','export');
}

// -------------------------------------------------

ManagerModuleItem.prototype.make_button = function(parent, label, import_or_export) {
	var me = this;
	var btn = $a(parent,'button');
	btn.import_or_export = import_or_export;
	$(btn).html(label).click(function() {
		if(this.import_or_export=='export')
			var arg = JSON.stringify([[me.dt, me.dn], me.mm.det[0]]);
		else
			var arg = JSON.stringify([me.mm.det[0], me.dt, me.dn]);
			
		pscript.mod_server_call(arg, this.import_or_export, 'item'); 
	}).button();
}

// server call
// -------------------------------------------------

pscript.mod_server_call = function(mod, import_or_export, module_or_item) {
	var w = page_body.pages['Module Manager'];
	
	// import
	var callback = function(r,rt) {
		msgprint(replace_newlines(r.message.join(NEWLINE)));
		w.tray.cur_item.manager_module.refresh();
	}
	$c_obj('Module Manager',import_or_export + '_' + module_or_item, mod, callback);
}
