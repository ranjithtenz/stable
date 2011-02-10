var new_tag_dialog = null;

ItemBrowserPage = function() {
	this.lists = {};
	this.dt_details = {};
	this.cur_list = null;

	this.my_page = page_body.add_page('ItemBrowser');
	this.wrapper = $a(this.my_page,'div');

	var h = $a(this.wrapper, 'div');

	this.body = $a(this.wrapper, 'div', '', {margin:'16px'});

	this.page_head = new PageHeader(h, 'List');
	this.new_button = this.page_head.add_button('New', function() { newdoc(me.cur_dt) }, 1, 'ui-icon-plus', 1)
	
}

// -------------------------------------------------

ItemBrowserPage.prototype.show = function(dt, label, field_list) {
	var me = this;

	if(this.cur_list) $dh(this.cur_list.wrapper);
	
	// page heading
	var l = get_doctype_label(dt)
	this.page_head.main_head.innerHTML = (l.toLowerCase().substr(-4) == 'list') ? l : (l + ' List')

	// button label
	this.page_head.clear_toolbar();
	if(in_list(profile.can_create,dt)) {
		var new_button = this.page_head.add_button('New ' + l, function() { newdoc(this.dt) }, 1, 'ui-icon-plus', 1)
		new_button.dt = dt
	}
	
	if(!me.lists[dt]) {
		me.lists[dt] = new ItemBrowser(me.body, dt, label, field_list);
	}

	me.cur_list = me.lists[dt];
	me.cur_list.show();
	
	page_body.change_to('ItemBrowser');
}

// -------------------------------------------------

ItemBrowser = function(parent, dt, label, field_list) {	
	var me = this;
	this.label = label ? label : dt;
	this.dt = dt;
	this.field_list = field_list;
	this.tag_filter_dict = {};

	this.wrapper = $a(parent, 'div', '', {display:'none'});

	// areas
	this.no_result_area = $a(this.wrapper, 'div', '', {margin: '16px 0px'});
	this.no_result_message = $a(this.no_result_area,'span','',{backgroundColor:'#FFC', padding:'6px'});
	
	this.loading_div = $a(this.wrapper,'div','',{margin:'200px 0px', textAlign:'center', fontSize:'14px', color:'#888', display:'none'});
	this.loading_div.innerHTML = 'Loading...';
	this.body = $a(this.wrapper, 'div');
	this.trend_area = $a(this.body, 'div', '', {margin:'8px 16px'});
	
	// tag filters
	this.tag_filters = $a(this.body, 'div', '', {marginBottom:'8px', display:'none', padding:'6px 8px 8px 8px', backgroundColor:'#FFD'});
	var span = $a(this.tag_filters,'span','',{marginRight:'4px',color:'#444'}); span.innerHTML = '<i>Showing for:</i>';
	this.tag_area = $a(this.tag_filters, 'span');
}

// -------------------------------------------------

ItemBrowser.prototype.show = function(show_callback) {
	var me = this;
	var callback = function(r, rt) {
		if(r.message == 'Yes') {
			if(!me.loaded)
				me.load_details(show_callback);
			else
				me.show_results();
				if(show_callback)show_callback();
		} else {
			me.show_no_result();
			if(show_callback)show_callback();
		}
	}
	$c_obj('Menu Control', 'has_result', this.dt, callback);	
}

// -------------------------------------------------

ItemBrowser.prototype.load_details = function(load_callback) {
	var me = this;
	var callback = function(r,rt) { 
		me.dt_details = r.message;
		if(r.message) {
			me.show_trend(r.message.trend);
			me.make_the_list(me.dt, me.body);
			me.show_results();
			if(load_callback) load_callback();
		}
	}
	$c_obj('Menu Control', 'get_dt_details', this.dt + '~~~' + cstr(this.field_list), callback);
	this.loaded = 1;
}

// -------------------------------------------------

ItemBrowser.prototype.show_results = function() {
	$ds(this.wrapper);
	$dh(this.loading_div);
	$ds(this.body);
	$dh(this.no_result_area);
	set_title(get_doctype_label(this.label));
}

// -------------------------------------------------

ItemBrowser.prototype.show_trend = function(trend) {
	var maxval = 0;
	for(var key in trend) { if(trend[key]>maxval) maxval = trend[key] };

	// head
	var div = $a(this.trend_area, 'div','',{marginLeft:'32px', color:'#888'}); div.innerHTML = 'Activity in last 30 days';
	var wrapper_tab = make_table(this.trend_area, 1, 2, '100%', ['20px',null], {padding:'2px 4px',fontSize:'10px',color:'#888'});

	// y-label
	var ylab_tab = make_table($td(wrapper_tab,0,0),2,1,'100%',['100%'],{verticalAlign:'top', textAlign:'right',height:'24px'});
	$td(ylab_tab,0,0).innerHTML = maxval;

	$y($td(ylab_tab,1,0),{verticalAlign:'bottom'});
	$td(ylab_tab,1,0).innerHTML = '0';

	// infogrid
	var tab = make_table($td(wrapper_tab,0,1), 1, 30, '100%', [], 
		{width:10/3 + '%', border:'1px solid #DDD', height:'40px', verticalAlign:'bottom', textAlign:'center', padding:'2px'});
		
	// labels
	var labtab = make_table($td(wrapper_tab,0,1), 1, 6, '100%', [], 
		{width:100/6 + '%', border:'1px solid #FFF', height:'16px',color:'#888',textAlign:'right',fontSize:'10px'});
	
	for(var i=0; i<30; i++) {
		var div = $a($td(tab,0,29-i),'div','',{backgroundColor:'#4AC', width:'50%', margin:'auto', height:(trend[i+''] ? (trend[i+'']*100/maxval) : 0) + '%'});
		div.setAttribute('title', trend[i] + ' records');
		
		// date string
		if(i % 5 == 0) {
			$td(labtab,0,5-(i/5)).innerHTML = dateutil.obj_to_user(dateutil.add_days(new Date(), -i));
			$y($td(tab,0,i-1),{'backgroundColor':'#EEE'});
		}
	}
	$td(labtab,0,5).innerHTML = 'Today';
}

// -------------------------------------------------

ItemBrowser.prototype.show_no_result = function() {
	$ds(this.wrapper);
	$dh(this.loading_div);
	$dh(this.body);	
	$ds(this.no_result_area);
	this.no_result_message.innerHTML = repl('No %(dt)s records found. <span class="link_type" onclick="newdoc(\'%(dt)s\')">Click here</span> to create your first %(dt)s', {dt:get_doctype_label(this.dt)});
	set_title(get_doctype_label(this.label));
}

// -------------------------------------------------

ItemBrowser.prototype.make_new = function(dt, label, field_list) {
	// make the list
	this.make_the_list(dt, this.body);
}

// -------------------------------------------------

ItemBrowser.prototype.add_tag_conditions = function(q) {
	var me = this;
	
	if(keys(me.tag_filter_dict).length) {
		var cl = [];
		for(var key in me.tag_filter_dict) {
			var val = key;
			var op = '=';
				
			var fn = me.tag_filter_dict[key].fieldname;
				
			// conditions based on user tags
			if(fn=='docstatus')val=(key=='Draft'?'0':'1');
			if(fn=='_user_tags'){ val='%,'+key + '%'; op=' LIKE '; }
				
			cl.push(q.table + '.`' + fn + '`'+op+'"' + val + '"');
		}
		if(cl)
			q.conds += ' AND ' + cl.join(' AND ') + ' ';
	}
}
	
// -------------------------------------------------
	
ItemBrowser.prototype.make_the_list  = function(dt, wrapper) {
	var me = this;
	var lst = new Listing(dt, 1);
	lst.dt = dt;
	lst.cl = this.dt_details.columns;

	lst.opts = {
		cell_style : {padding:'6px 2px'},
		alt_cell_style : {backgroundColor:'#FFFFFF'},
		hide_export : 1,
		hide_print : 1,
		hide_rec_label: 0,
		show_calc: 0,
		show_empty_tab : 0,
		show_no_records_label: 1,
		show_new: 0,
		show_report: 1,
		no_border: 1,
		append_records: 1
	}
		
	if(user_defaults.hide_report_builder) lst.opts.show_report = 0;
	
	// build th query
	lst.is_std_query = 1;
	lst.get_query = function() {
		q = {};
		var fl = [];
		q.table = repl('`tab%(dt)s`', {dt:this.dt});
	
		// columns
		for(var i=0;i<this.cl.length;i++) fl.push(q.table+'.`'+this.cl[i][0]+'`')

		if(me.dt_details.submittable)
			fl.push(q.table + '.docstatus');

		// columns
		q.fields = fl.join(', ');

		// conitions
		q.conds = q.table + '.docstatus < 2 ';
		
		// filter conditions
		me.add_tag_conditions(q);
		
		this.query = repl("SELECT %(fields)s FROM %(table)s WHERE %(conds)s", q);
		this.query_max = repl("SELECT COUNT(*) FROM %(table)s WHERE %(conds)s", q);
	}
	
	// make the columns
	lst.colwidths=['100%']; lst.coltypes=['Data']; lst.coloptions = [''];
	
	// show cell
	lst.show_cell = function(cell, ri, ci, d) {
		new ItemBrowserItem(cell, d[ri], me);		
	}
	
	lst.make(wrapper);

	// add the filters
	var sf = me.dt_details.filters;
	for(var i=0;i< sf.length;i++) {
		var fname = sf[i][0]; var label = sf[i][1]; var ftype = sf[i][2]; var fopts = sf[i][3];

		if(in_list(['Int','Currency','Float','Date'], ftype)) {
			lst.add_filter('From '+label, ftype, fopts, dt, fname, '>=');
			lst.add_filter('To '+label, ftype, fopts, dt, fname, '<=');
		} else {
			lst.add_filter(label, ftype, fopts, dt, fname, (in_list(['Data','Text','Link'], ftype) ? 'LIKE' : ''));
		}
	}
	
	// default sort
	lst.set_default_sort('modified', 'DESC');
	this.lst = lst;
	lst.run();
}

// ========================== ITEM ==================================

function ItemBrowserItem(parent, det, ib) {
	this.wrapper = $a(parent, 'div');
	this.det = det;
	this.ib = ib;
	this.dn = det[0];
	
	this.make_details()
	this.make_tags()
	this.add_timestamp()
}

// -------------------------------------------------

ItemBrowserItem.prototype.make_details = function() {

	// link
	var me = this;
	var div = $a(this.wrapper, 'div');
	
	var span = $a(div, 'span', 'link_type', {fontWeight:'bold'});
	span.innerHTML = me.dn;
	span.onclick = function() { loaddoc(me.ib.dt, me.dn); }
	
	// properties
	var tmp = [];
	var cl = me.ib.dt_details.columns;

	
	for(var i=3; i<me.det.length; i++) {
		if(cl[i] && cl[i][1] && me.det[i]) {
			// has status, group or type in the label
			if(cl[i][1].indexOf('Status') != -1 || 
				cl[i][1].indexOf('Group') != -1 || 
				cl[i][1].indexOf('Type') != -1) {
					me.add_tag(me.det[i], 1, cl[i][0]);	
			} else {

				// separator
				if(i>2) {
					var span = $a(div,'span'); span.innerHTML = ',';
				}
				
				// label
				var span = $a(div,'span','',{color:'#888'});
				span.innerHTML = ' ' + cl[i][1] + ': ';
				
				// value
				var span = $a(div,'span');
				$s(span,me.det[i],(cl[i][2]=='Link'?'Data':cl[i][2]), cl[i][3]);
			}
		}
	}

}

// -------------------------------------------------

ItemBrowserItem.prototype.make_tags = function() {
	// docstatus tag
	var docstatus = cint(this.det[this.det.length - 1]);
	if(this.ib.dt_details.submittable) 
		{ this.add_tag((docstatus ? 'Submitted' : 'Draft'), 1, 'docstatus'); }

	// make custom tags
	if(this.det[2]) {
		var tl = this.det[2].split(',');
		for(var i=0; i<tl.length; i++) if(tl[i]) this.add_tag(tl[i], 0, '_user_tags');
	}

	// "Add Tag"
	this.make_add_tag();
}

// -------------------------------------------------

ItemBrowserItem.prototype.add_timestamp = function() {
	// time
	var div = $a(this.wrapper, 'div', '', {color:'#888', fontSize:'11px'});
	div.innerHTML = comment_when(this.det[1]);
}

// -------------------------------------------------

ItemBrowserItem.prototype.make_tag_area = function() {
	var div = $a(this.wrapper, 'div', '', {margin:'3px 0px', padding:'3px 0px'});
	this.tag_area = $a(div, 'span', '', {marginRight:'4px'});
	this.add_tag_area = $a(div, 'span');
	this.tag_list = [];
}

// -------------------------------------------------

ItemBrowserItem.prototype.add_tag = function(label, static, fieldname) {
	var me = this;

	if(!this.tag_area) this.make_tag_area();	
	if(in_list(this.tag_list, label)) return; // no double tags
	
	// tag area
	var tag = new ItemBrowserTag(this.tag_area, label, this.ib.dt, this.dn, static);
	tag.remove = function(tag_ref) {
		var callback = function(r,rt) {
			// clear tag
			$dh(tag_ref.body);
			
			// remove from tag_list
			var nl=[]; for(var i in me.tag_list) if(me.tag_list[i]!=tag_ref.label) nl.push(me.tag_list[i]);
			me.tag_list = nl;
		}
		$c_obj('Menu Control', 'remove_tag', JSON.stringify([me.ib.dt, me.dn, tag_ref.label]), callback)
		$bg(tag_ref.body,'#DDD');
	}
	tag.fieldname = fieldname;
	
	this.set_tag_fitler(tag);
	this.tag_list.push(label);
}

// -------------------------------------------------

ItemBrowserItem.prototype.set_tag_fitler = function(tag) {
	var me = this;
	tag.onclick = function(tag_ref) {
		
		// check if exists
		if(in_list(keys(me.ib.tag_filter_dict), tag.label)) return;
		
		// create a tag in filters
		var filter_tag = new ItemBrowserTag(me.ib.tag_area, tag_ref.label, me.ib.dt, null, 0);
		filter_tag.ib = me.ib;
		filter_tag.fieldname = tag_ref.fieldname;

		// remove tag from filters
		filter_tag.remove = function(tag_ref_remove) {
			var ib = tag_ref_remove.ib;
			$(tag_ref_remove.body).fadeOut();
			delete ib.tag_filter_dict[tag_ref_remove.label];
			
			// hide everything?
			if(!keys(ib.tag_filter_dict).length) {
				$(ib.tag_filters).slideUp(); // hide
			}
			
			// run
			ib.lst.run();
		}

		// add to dict
		me.ib.tag_filter_dict[tag_ref.label] = filter_tag;
		$ds(me.ib.tag_filters);
		
		// run
		me.ib.lst.run();
	}
}

// -------------------------------------------------

ItemBrowserItem.prototype.new_tag = function() {
	var me = this;
	
	if(!new_tag_dialog) {
		var d = new Dialog(400,200,'New Tag');
		d.make_body([['HTML','Tag'],['Button','Save']])
		d.tag_input = make_field({fieldtype:'Link', label:'New Tag', options:'Tag', no_buttons:1}, '', 
			d.widgets['Tag'], this, 0, 1);
		d.tag_input.not_in_form = 1;
		d.tag_input.refresh();
		
		$y(d.tag_input.txt, {width:'80%'});

		// save
		d.widgets['Save'].onclick = function() {
			var val = strip(d.tag_input.txt.value);
			if(!val) {
				msgprint("Please type something");
				return;
			}
			
			if(val.search(/^[a-z0-9\s]+$/i)==-1) {
				msgprint("Special charaters, commas etc not allowed in tags");
				return;
			}
			
			var callback = function(r,rt) {
				new_tag_dialog.tag_input.txt.value= '';
				new_tag_dialog.hide();

				if(!r.message) return;
				new_tag_dialog.ibi.add_tag(r.message, 0, '_user_tags');
			}
			$c_obj('Menu Control','add_tag',JSON.stringify(
				[new_tag_dialog.ibi.ib.dt, new_tag_dialog.ibi.dn, val]), callback);
		}
		new_tag_dialog = d;
	}
	new_tag_dialog.ibi = me;
	new_tag_dialog.show();
}

// -------------------------------------------------

ItemBrowserItem.prototype.make_add_tag = function() {
	if(!this.tag_area) this.make_tag_area();

	var me = this;

	this.add_tag_span = $a(this.add_tag_area, 'span', '', {color:'#888', textDecoration:'underline', cursor:'pointer',marginLeft:'4px',fontSize:'11px'});
	this.add_tag_span.innerHTML = 'Add tag';
	this.add_tag_span.onclick = function() {
		// show tag link
		me.new_tag();
		
	}
}

// ========================== Tag ==================================

function ItemBrowserTag(parent, label, dt, dn, static) {
	this.dt = dt; this.dn = dn; this.label = label;
	var me = this;
	
	// tag area
	this.body = $a(parent,'span','',{padding:'2px 4px', backgroundColor:'#489', color:'#FFF', marginRight:'4px', fontSize:'11px', cursor:'pointer'});
	$(this.body).hover(
		function() { $bg(this,'#4AC'); }
		,function() { $bg(this,'#489'); }
	);
	
	$br(this.body,'3px');

	var span = $a(this.body,'span');
	span.innerHTML = label;
	span.onclick = function() { if(me.onclick) me.onclick(me); }
	
	if(!static) {
		var span = $a(this.body,'span');
		span.innerHTML += ' |';
		
		var span = $a(this.body,'span');
		span.innerHTML = ' x'
		span.onclick = function() { me.remove(me); }
	}	
}