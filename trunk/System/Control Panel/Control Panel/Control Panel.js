if(user == 'Guest'){
  $dh(page_body.left_sidebar);
}

var current_module;
var is_system_manager = 0;
var module_content_dict = {};
var user_full_nm = {};

// check if session user is system manager
if(inList(user_roles,'System Manager')) is_system_manager = 1;

function startup_setup() {
	if(get_url_arg('embed')) {
		// hide header, footer
		$dh(page_body.banner_area);
		return;
	}

	if(user=='Guest') {
		if(cint(locals['Control Panel']['Control Panel'].sync_with_gateway)) {
			window.location.href = 'https://www.erpnext.com';
			return;
		}
	}

	// page structure
	// --------------
	$y($i('body_div'), {backgroundColor:'#FFF'});
	$td(page_body.wntoolbar.body_tab,0,0).innerHTML = '<i><b>erp</b>next</i>';
	$y($td(page_body.wntoolbar.body_tab,0,0), {width:'140px', color:'#FFF', paddingLeft:'8px', paddingRight:'8px', fontSize:'14px'})
	$dh(page_body.banner_area);
	
	// sidebar
	// -------
	pscript.startup_make_sidebar();
	setTimeout(pscript.startup_set_height,100);

	// border to the body
	// ------------------
	$(page_body.center).css('background-color','#FFF')
	$dh(page_body.footer);

	// for logout and payment
	var callback = function(r,rt) {
		if(cint(locals['Control Panel']['Control Panel'].sync_with_gateway)) {
			login_file = 'https://www.erpnext.com'
		
			// setup toolbar
			pscript.startup_setup_toolbar(r.message);
		}
	}
	$c_obj('Home Control', 'get_login_url', '', callback);
}

// ====================================================================

pscript.startup_set_height = function() {
	// no body overflow
	$y(document.getElementsByTagName('body')[0], {overflow:'hidden'});
	
	$y(page_body.left_sidebar, {height: get_window_height() + 'px', overflow:'auto'});
	$y(page_body.center, {height: get_window_height() + 'px', overflow:'auto'});
	
	resize_observers.push(function() {
		$y(page_body.left_sidebar, {height: get_window_height() + 'px'});	
		$y(page_body.center, {height: get_window_height() + 'px'});	
	});
}

// ====================================================================

pscript.startup_make_sidebar = function() {
	$y(page_body.left_sidebar, {width:(100/9)+'%', paddingTop:'8px'});

	var callback = function(r,rt) {
		// menu
		var ml = r.message; 
		
		for(var m=0; m<ml.length; m++){
			if(ml[m]) {
				var mod = $a(page_body.left_sidebar, 'div');
				$item_normal(mod);
	
				$(mod)
					.click(function() { 
						var me = this;
						$item_selected(this);$bg(this,'#DDD');$fg(this,'#000');
						if(pscript.current_module) $item_normal(pscript.current_module);
	
						if(!locals['Page'][this.details.module_page]);
							$item_set_working(this);
						
						// load the page
						loadpage(this.details.module_page, function() { $item_done_working(me); });
						
						pscript.current_module = this;
					 })
					.hover(
						function() { if(this != pscript.current_module) $item_active(this); }
						,function() { if(this != pscript.current_module) $item_normal(this); }
					)
				mod.onmousedown = function() { $item_pressed(this); }
				mod.onmouseup = function() { $item_selected(this); $bg(this,'#DDD');$fg(this,'#000'); }
				mod.details = ml[m];
	
				// label
				mod.innerHTML = '<img src="images/icons/' + ml[m].module_icon + '" style="margin: -3px 4px -3px 0px">' + ml[m].module_label;
			}
		}
		if(in_list(user_roles, 'System Manager')) {
			var div = $a(page_body.left_sidebar, 'div', 'link_type', {padding:'8px', fontSize:'11px'});
			$(div).html('[edit]').click(function() {loadpage('Module Settings')})
		}
	}
	$c_obj('Home Control', 'get_modules', '', callback);	
}


// ====================================================================

pscript.startup_setup_toolbar = function(flag) {

	// Help
  	// --------------
  	var help_url = login_file + '/index.cgi#Page/Helpdesk'
  	$td(page_body.wntoolbar.menu_table_right,0,1).innerHTML = '<a style="font-weight: bold; color: #FFF" href="'+help_url+'" target="_blank">Tickets</a>';

  	// Manage account
  	// --------------
	if(is_system_manager && flag) {
		var manage_account_url = login_file + '/index.cgi#Page/Manage My Account Page';
		$td(page_body.wntoolbar.menu_table_right,0,3).innerHTML = '<a style="font-weight: bold; color: #FFF" href="'+manage_account_url+'" target="_blank">Buy Credits</a>';
	} else {
		$dh($td(page_body.wntoolbar.menu_table_right,0,3))
	}

	// Live Chat Help
	// --------------
	$td(page_body.wntoolbar.menu_table_right,0,2).innerHTML = '<a style="font-weight: bold; color: #FFF" href="http://www.providesupport.com?messenger=iwebnotes" target="_blank">Live Chat Help</a>';
}

// chart of accounts
// ====================================================================
show_chart_browser = function(nm, chart_type){

  var call_back = function(){
    if(nm == 'Sales Browser'){
      var sb_obj = new SalesBrowser();
      sb_obj.set_val(chart_type);   
    }
    else if(nm == 'Accounts Browser')
      pscript.make_chart(chart_type);
  }
  loadpage(nm,call_back);
}


// Module Page
// ====================================================================

ModulePage = function(parent, module_name, module_label, help_page, callback) {
	this.parent = parent;

	// add to current page
	page_body.cur_page.module_page = this;
		
	this.page_head = new PageHeader(parent, module_label);
	if(help_page) {
		var btn = this.page_head.add_button('Help', function() { loadpage(this.help_page) }, 1, 'ui-icon-help')
		btn.help_page = help_page;
	}
	
	this.wrapper = $a(parent,'div');
	this.module_name = module_name;
	this.transactions = [];
	
	this.get_details();
	
	if(callback) this.callback = function(){ callback(); }
}

// ----------------------------------------------------------------

ModulePage.prototype.add_doc_type = function(details) {
	var me = this;
	
	this.transactions.push(details.doc_name);
	
	var show_docbrowser = function(label) {
		var item = me.tray.items[label]
		if(!item.docbrowser) {
			$item_set_working(me.tray.items[label].ldiv);
			item.docbrowser = new ItemBrowser(item.body, item.details.doc_name, get_doctype_label(item.details.doc_name), item.details.fields);
			item.docbrowser.show(function() { $item_done_working(me.tray.items[label].ldiv); });
		}
	}

	// new tab
	var item = this.tray.add_item(details.display_name, show_docbrowser);
	item.details = details;
	
	// label
	var head = $a(item.body, 'div', '', {fontSize:'18px', marginBottom:'4px'});
	head.innerHTML = get_doctype_label(details.doc_name).bold()
	if(details.description)
		head.innerHTML += '<span style="color: #888; margin-left:8px">' + details.description + '</span>';

	// new button
	if(inList(profile.can_create, details.doc_name)) {
		var btn = $btn($a(item.body, 'div', '', {padding:'8px 0px'}), 
			'+ New ' + get_doctype_label(details.doc_name), 
			function() { newdoc(this.dt); },
			{fontWeight:'bold'}, 'green');
		btn.dt = details.doc_name;
	}
	return item;
}

// ----------------------------------------------------------------

ModulePage.prototype.add_reports = function(il, label, dt_key, sc_key) {
	var report = this.tray.add_item(label, null, null, 1);
	
	var add_report_name = function(dt, sc) {
		var div = $a(report.body, 'div', '', {marginBottom:'6px'});
		var span = $a(div, 'span', 'link_type');
		span.innerHTML = sc; span.dt = dt; span.sc = sc;
		span.onclick = function() { loadreport(this.dt, this.sc); }
	}
	
	// item list
	for(var i=0; i<il.length;i++){
		if(il[i].doc_type == 'Reports' || label=='Custom Reports') {
			add_report_name(il[i][dt_key], il[i][sc_key]);	
		}
	}	
}

// ----------------------------------------------------------------

ModulePage.prototype.add_tools = function(il) {
	var tools = this.tray.add_item('Tools', null, null, 1);
	
	var add_tool = function(is_page, name, label, click_function) {
		var div = $a(tools.body, 'div', '', {marginBottom:'6px'});
		var span = $a(div, 'span', 'link_type');
		span.innerHTML = label; span._name = name;
		if(is_page) {
			if(click_function) {
				span.onclick = function() { eval(this.click_function) }
				span.click_function = click_function;
			} else
				span.onclick = function() { loadpage(this._name); }
		} else
			span.onclick = function() { loaddoc(this._name, this._name); }
	}
	
	// item list
	for(var i=0; i<il.length;i++){
		if(il[i].doc_type == 'Pages') {
			add_tool(1, il[i].doc_name, il[i].display_name, il[i].click_function);	
		}
		else if(il[i].doc_type == 'Single DocType') {
			add_tool(0, il[i].doc_name, il[i].display_name);	
		}
	}	
}

// ----------------------------------------------------------------

ModulePage.prototype.add_items = function(il) {
	// tips area
	//this.tips_area = $a(this.tray.body, 'div');
	this.show_flag = null;
	
	// item list
	for(var i=0; i<il.length;i++){
		if(il[i].doc_type == 'Forms') {
			var item = this.add_doc_type(il[i]);
			if(!this.show_flag) { item.expand(); this.show_flag = 1 }
		}
	}
}

// get module details
// ----------------------------------------------------------------

ModulePage.prototype.get_details = function() {
	var me = this;
	
	var callback = function(r,rt){
		// widget code

		if(r.message.il) {
			me.tray = new TrayPage(me.wrapper);
			$y(me.tray.tab,{tableLayout:'fixed'});
			me.add_items(r.message.il);
			me.add_reports(r.message.il, 'Reports', 'doc_name', 'display_name');
			me.add_tools(r.message.il);
			if(r.message.custom_reports.length)
				me.add_reports(r.message.custom_reports, 'Custom Reports', 'doc_type', 'criteria_name');
			if(!me.show_flag) me.tray.items.Reports.expand();
	
			// set height
			setTimeout(pscript.module_page_set_height, 100);
			set_resize_observer(pscript.module_page_set_height);
		}

		else if(r.message.wl) {
			obj = eval(r.message.wl);
			if(obj){ 
				me.wrapper.appendChild(obj); 
				$(obj).fadeIn();
			}
		}

				
		// callback
		if(me.callback) me.callback();
		me.show_updates();
	
		remove_space_holder();
	}
	
	$c_obj('Home Control', 'get_module_details', me.module_name, callback);
}

// ----------------------------------------------------------------

pscript.module_page_set_height = function() {
	var mp = page_body.cur_page.module_page;
	if(mp)
		$y(mp.tray.body, {height:get_window_height() - mp.page_head.wrapper.offsetHeight + 'px', overflow:'auto'});
}

// ----------------------------------------------------------------

ModulePage.prototype.show_updates = function() {
	if(!this.tips_area) return;
	var me = this;
	var can_read_dt = [];
	$y(this.tips_area, {backgroundColor:'#FFD', padding:'4px', height:'16px', color: '#444'});

	var tl = this.transactions;
	for(var i=0; i<tl.length; i++) {
		if(in_list(profile.can_read, tl[i]))
			can_read_dt.push(tl[i])
	}

	var args = {'module':this.module_name, 'tr_list':can_read_dt}
	$c_obj('Module Tip Control', 'get_module_activity', JSON.stringify(args), function(r,rt) {
		if(r.message) {
			var temp = r.message;
			var act_str = [];
			for(tp in temp) {
				var dt = get_doctype_label(tp);
				act_str.push(temp[tp] + ' ' + (temp[tp] > 1 ? get_plural(dt) : dt));
			}
			$(me.tips_area).html('<span style="color:#C70">New in last 7 days:</span> ' + act_str.join(', ')).css('display','block');
		} else {
			$(me.tips_area).html('<span style="color:#C70;">No new records in last 7 days</span>').css('display','block');
		}
	});
}

// get plural
// ====================================================================

get_plural = function(str){
	if(str.charAt(str.length-1).toLowerCase() == 'y')	return str.substr(0, str.length-1) + 'ies'
	else return str + 's';
}

// set user fullname
// ====================================================================
pscript.set_user_fullname = function(ele,username,get_latest){
	
	var set_it = function(){
		if(ele)
			ele.innerHTML = user_full_nm[username];
	}
	
	if(get_latest){
		$c_obj('Home Control','get_user_fullname',username, function(r,rt){ user_full_nm[username] = r.message; set_it(); });
	}
	else{
		if(user_full_nm[username]){
			set_it();
		}
		
		else
			$c_obj('Home Control','get_user_fullname',username, function(r,rt){ user_full_nm[username] = r.message; set_it(); });
	}
}



// 
startup_setup();
