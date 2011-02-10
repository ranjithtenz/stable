var home_link_style = {textDecoration:'underline', cursor:'pointer'};

pscript['onload_Event Updates'] = function() {
	if(user=='Guest') {
		loadpage('Login Page');
		return;
	}
	pscript.home_make_body();
	pscript.home_pre_process();
	pscript.home_make_status();
	pscript.home_make_widgets();
}


pscript.home_make_body = function() {
	var wrapper = page_body.pages['Event Updates'];
	wrapper.innerHTML = '';
	wrapper.head = $a(wrapper, 'div');
	// body
	wrapper.main_tab = make_table(wrapper,1,2,'100%',[500/7 + '%',200/7+'%']);
}

pscript.home_pre_process = function(wrapper) {
	var wrapper = page_body.pages['Event Updates'];
	var cp = locals['Control Panel']['Control Panel'];

	// complete registration
	if(in_list(user_roles,'System Manager')) { pscript.complete_registration(); }

	// banner
	if(cp.client_name) {
		var banner = $a(wrapper.head, 'div', '', {borderBottom:'3px solid #444', paddingBottom:'4px'})
		banner.innerHTML = cp.client_name;
	}

	// complete registration
	if(in_list(user_roles,'System Manager')) {
		pscript.complete_registration();
	}
}

// Widgets
// ==================================

pscript.home_make_widgets = function() {
	var wrapper = page_body.pages['Event Updates'];
	var cell = $td(wrapper.main_tab, 0, 1);
	$y(cell,{padding:'0px 8px'});

	new HomeCalendar(new HomeWidget(cell, 'Calendar', 'Event'));
	
	// calendar link
	var div = $a(cell,'div','',{margin:'4px',marginBottom:'16px',textDecoration:'underline',cursor:'pointer',color:'#888'})
	div.innerHTML = 'View Full Calendar';
	div.onclick = function() { loadpage('_calendar'); }
	
	new HomeToDo(new HomeWidget(cell, 'To Do', 'Item'));
	new FeedList($td(wrapper.main_tab, 0, 0));
}

HomeWidget = function(parent, heading, item) {
	var me = this; this.item = item;
	
	this.wrapper = $a(parent, 'div', '', {border:'2px solid #CCC'});
	$(this.wrapper)
		.css('-moz-border-radius','5px').css('-webkit-border-radius','5px')
	
	// head
	this.head = $a(this.wrapper,'div','',{backgroundColor:'#CCC', fontSize:'14px', fontWeight:'bold'});
	this.head.tab = make_table($a(this.head,'div'), 1, 2, '100%', ['90%','10%'], {padding:'4px', verticalAlign:'middle'})
	$td(this.head.tab,0,0).innerHTML = heading;
	this.working_img = $a($td(this.head.tab,0,0),'img','',{marginLeft:'8px'});
	this.working_img.src = 'images/ui/button-load.gif';
	
	// refresh
	this.refresh_btn = $a($td(this.head.tab,0,1),'div','wn-icon ' + 'ic-playback_reload', {cursor:'pointer'});
	this.refresh_btn.onclick = function() { me.refresh(); }
	
	// body
	this.body = $a(this.wrapper,'div','',{padding:'0px 4px 16px 4px'});
	this.footer = $a(this.wrapper,'div','',{padding:'4px',paddingBottom:'8px'});
	
	// add button
	this.add_btn = $btn(this.footer,'+ Add ' + item,function(){me.add()});
}

HomeWidget.prototype.refresh = function() {
	var me = this;
	$di(this.working_img);
		
	var callback = function(r,rt) {
		$dh(me.working_img);
		me.body.innerHTML = '';

		// prepare (for calendar?)
		if(me.decorator.setup_body) me.decorator.setup_body();

		for(var i=0;i<r.message.length;i++) {
			new HomeWidgetItem(me, r.message[i]);
		}
	}
	$c_obj('Home Control',this.get_list_method,'',callback);
}

HomeWidget.prototype.make_dialog = function() {
	var me = this;
	if(!this.dialog) {
		this.dialog = new Dialog(400,400,'New ' + this.item);
		this.dialog.make_body(this.dialog_fields);
		this.dialog.widgets['Save'].onclick = function() {
			this.set_working();
			me.decorator.save(this);	
		}
	}
}

HomeWidget.prototype.add = function() {
	this.make_dialog();
	this.decorator.clear_dialog();
	this.dialog.show();
}

// Item
// --------

HomeWidgetItem = function(widget, det) {
	var me = this; this.det = det; this.widget = widget;
	
	this.widget = widget; this.det = det;
	
	// parent
	if(widget.decorator.get_item_parent) parent = widget.decorator.get_item_parent(det);
	else parent = widget.body;
	
	// wrapper
	this.wrapper = $a(parent, 'div','',{padding:'4px'});
	this.tab = make_table(this.wrapper, 1, 3, '100%', ['90%', '5%', '5%'],{padding:'2px'});

	// buttons
	this.edit_btn = $a($td(this.tab,0,1),'div','wn-icon ' + 'ic-doc_edit', {cursor:'pointer'});
	this.edit_btn.onclick = function() { me.edit(); }

	this.del_btn = $a($td(this.tab,0,2),'div','wn-icon ' + 'ic-trash', {cursor:'pointer'});
	this.del_btn.onclick = function() { me.delete_item(); }

	widget.decorator.render_item(this, det);
}

HomeWidgetItem.prototype.edit = function() {
	this.widget.make_dialog();
	this.widget.decorator.set_dialog_values(this.det);
	this.widget.dialog.show();
}

HomeWidgetItem.prototype.delete_item = function() {
	var me = this;
	this.wrapper.innerHTML = '<span style="color:#888">Deleting...</span>';
	var callback = function(r,rt) {
		$(me.wrapper).slideUp();
	}
	$c_obj('Home Control',this.widget.delete_method, this.widget.get_item_id(this.det) ,callback);
		
}

// Calendar
// ===========================

HomeCalendar = function(widget) {
	this.widget = widget;

	// methods
	this.widget.get_list_method = 'get_events_list'
	this.widget.delete_method = 'delete_event';
	this.widget.get_item_id = function(det) { return det.name; }

	this.widget.decorator = this;

	var hl = [];
	for(var i=0; i<24; i++) {
		hl.push(((i+8) % 24) + ':00');
	}

	this.widget.dialog_fields = [
		['Date','Event Date']
		,['Select','Time','',hl]
		,['Text','Description']
		,['Button','Save']
	];

	this.widget.refresh();
}

// create calendar grid
// --------------------
HomeCalendar.prototype.setup_body = function() {
	var w = this.widget;
	w.date_blocks = {};
	var td = new Date();
	for(var i=0; i<7; i++) {
		var dt = dateutil.obj_to_str(dateutil.add_days(td,i));
		var div = $a(w.body, 'div', '', {padding:'4px 0px', borderBottom:'1px solid #AAA',display:'none'});
		div.head = $a(div, 'div', '', {fontWeight:'bold', paddingBottom:'4px'});
		div.head.innerHTML  = (i==0 ? 'Today' : (i==1 ? 'Tomorrow' : dateutil.str_to_user(dt)))
		w.date_blocks[dt] = div;
	}
}

HomeCalendar.prototype.get_item_parent = function(det) {
	var d = this.widget.date_blocks[det.event_date]; $ds(d);
	return d;
}

HomeCalendar.prototype.render_item = function(item, det) {
	$td(item.tab, 0, 0).innerHTML = '<span style="color:#888">' + det.event_hour + ':</span> ' + det.description;
	if(det.ref_type && det.ref_name) {
		var span=$a($a($td(item.tab, 0, 0),'div'),'span','link_type');
		span.innerHTML = det.ref_name; span.dt = det.ref_type;
		span.onclick = function() { loaddoc(this.ref_type, this.innerHTML); }
	}
}

HomeCalendar.prototype.clear_dialog = function() {
	this.set_dialog_values({event_date:get_today(), event_hour:'8:00', description:''});
}

HomeCalendar.prototype.set_dialog_values = function(det) {
	var d = this.widget.dialog;
	d.widgets['Event Date'].value = dateutil.str_to_user(det.event_date);
	d.widgets['Time'].value = cint(det.event_hour.split(':')) + ':00';
	d.widgets['Description'].value = det.description;
	d.det = det;
}

HomeCalendar.prototype.save = function(btn) {
	var d = this.widget.dialog;
	var me = this;
	d.det.event_date = dateutil.user_to_str(d.widgets['Event Date'].value);
	d.det.event_hour = d.widgets['Time'].value;
	d.det.description = d.widgets['Description'].value;
	d.det.owner = user;
	if(!d.det.event_type)
		d.det.event_type = 'Private';
	
	var callback = function(r,rt) {
		btn.done_working();
		me.widget.dialog.hide();
		me.widget.refresh();
	}
	$c_obj('Home Control','edit_event',JSON.stringify(d.det),callback);	
}

// Todo
// ===========================

HomeToDo = function(widget) {
	this.widget = widget;

	// methods
	this.widget.get_list_method = 'get_todo_list';
	this.widget.delete_method = 'remove_todo_item';
	this.widget.get_item_id = function(det) { return det[0]; }

	this.widget.decorator = this;

	this.widget.dialog_fields = [
		['Date','Date']
		,['Text','Description']
		,['Check','Completed']
		,['Select','Priority','',['Medium','High','Low']]
		,['Button','Save']
	];

	this.widget.refresh();	
}

HomeToDo.prototype.render_item = function(item, det) {
	
	// priority tag
	var div = $a($td(item.tab, 0, 0), 'div', '', {margin:'4px 0px'});
	var span = $a(div, 'span', '', {padding:'2px',color:'#FFF',fontSize:'10px'
		,backgroundColor:(det[3]=='Low' ? '#888' : (det[3]=='High' ? '#EDA857' : '#687FD3'))});
		
	$(span).css('-moz-border-radius','3px').css('-webkit-border-radius','3px');
	span.innerHTML = det[3];

	// text
	var span = $a(div, 'span', '', {paddingLeft:'8px'});
	span.innerHTML = det[1];
	if(det[4]) $y(span,{textDecoration:'line-through'});
}

HomeToDo.prototype.clear_dialog = function() {
	this.set_dialog_values(['','',get_today(),'Medium',0]);
}

HomeToDo.prototype.set_dialog_values = function(det) {
	var d = this.widget.dialog;
	d.widgets['Date'].value = dateutil.str_to_user(det[2]);
	d.widgets['Priority'].value = det[3];
	d.widgets['Description'].value = det[1];
	d.widgets['Completed'].checked = det[4];
	d.det = det;
}

HomeToDo.prototype.save = function(btn) {
	var d = this.widget.dialog;
	var me = this;
	
	var det = {}
	det.date = dateutil.user_to_str(d.widgets['Date'].value);
	det.priority = d.widgets['Priority'].value;
	det.description = d.widgets['Description'].value;
	det.name = d.det ? d.det[0] : '';
	det.checked = (d.widgets['Completed'].checked ? 1 : 0);

	
	var callback = function(r,rt) {
		btn.done_working();
		me.widget.dialog.hide();
		me.widget.refresh();
	}
	$c_obj('Home Control','add_todo_item',JSON.stringify(det),callback);	
}

// Feed
// ==================================


FeedList = function(parent) {
	// settings
	this.auto_feed_off = 0;
	
	this.wrapper = $a(parent, 'div');
	this.make_head();
	this.make_status_input();
	this.make_list();
	this.list.run();
}

FeedList.prototype.make_head = function() {
	var me = this;
	this.head = $a(this.wrapper, 'div', '', {padding:'4px',backgroundColor:'#CCC',marginBottom:'8px',fontSize:'14px'});
	$br(this.head,'3px');
	
	var span = $a(this.head,'span','', {padding:'0px 8px'}); span.innerHTML = 'Recent Updates'.bold();

	// all
	var span = $a(this.head,'span','',home_link_style); $y(span,{borderLeft:'1px solid #888',padding:'0px 8px',});
	span.innerHTML = 'All'; span.onclick = function() { me.auto_feed_off = 0; me.list.run() }

	// comments
	var span = $a(this.head,'span','',home_link_style); $y(span,{borderLeft:'1px solid #888',padding:'0px 8px',});
	span.innerHTML = 'Comments'; span.onclick = function() { me.auto_feed_off = 1; me.list.run() }

}

FeedList.prototype.make_status_input = function() {
	var me = this;
	this.status_area = $a(this.wrapper, 'div', '', {padding:'4px'});

	this.status_inp = $a(this.status_area, 'input', '', {fontSize:'14px', width:'50%'});
	this.status_inp.set_empty = function() {
		this.value = 'Share something...'; $fg(this,'#888');
		$dh(this.status_btn);
	}
	this.status_inp.onfocus = function() {
		$fg(this,'#000');
		if(this.value=='Share something...')this.value = '';
		$ds(me.status_btn);
	}
	this.status_inp.onchange = function() {
		if(!this.value) this.set_empty();
	}
	this.status_inp.set_empty();
	this.status_btn = $btn(this.status_area, 'Share', function() { me.share_status(); }, {fontSize:'14px', marginLeft:'8px'}, 0, 1);
	$y(this.status_btn.loading_img, {marginBottom:'0px'});

	$dh(this.status_btn);
}

FeedList.prototype.share_status = function() {
	var me = this;
	if(!this.status_inp.value) return;
	var callback = function() {
		me.status_inp.set_empty();
		me.status_btn.done_working();
		me.list.run();
	}
	this.status_btn.set_working();
	$c_obj('Feed Control', 'add_feed', this.status_inp.value, callback);
}

FeedList.prototype.make_list = function() {
	var l = new Listing('Feed List',1);
	var me = this;

	// style
	l.colwidths = ['100%']; l.page_len = 20;	
	l.opts.alt_cell_style = {backgroundColor:'#FFF'}; l.opts.no_border = 1; l.keyword = 'feeds';
	
	// build query
	l.get_query = function(){
		var condn = me.auto_feed_off ? ' and (t1.doc_name is null or t1.doc_name ="")' : '';
		this.query = repl('select t1.name, t1.feed, t1.feed_owner, t1.can_view, t1.doc_name, t1.doc_label, t1.doc_no, t1.action, t1.latest_comments, t1.total_comments, t1.modified, concat_ws(" ", t2.first_name, t2.last_name),t2.social_points, t2.social_badge from tabFeed t1, tabProfile t2 where t1.feed_owner = t2.name%(condn)s order by t1.modified desc',{'condn':condn});
		this.query_max = repl('select count(t1.name) from tabFeed t1, tabProfile t2 where t1.feed_owner = t2.name%(condn)s',{'condn':condn});
	}
	
	// render list ui
	l.show_cell = function(cell,ri,ci,d){ me.render_feed(cell,ri,ci,d); }
	
	// onrun
	l.onrun = function(){ $(me.wrapper).fadeIn(); if(me.after_run) me.after_run(); }
	
	// make
	l.make($a(this.wrapper,'div'));
	$dh(l.btn_area);

	this.list = l;
}

FeedList.prototype.render_feed = function(cell,ri,ci,d) {
	new FeedItem(cell, d[ri], this);
}

// Item
// -------------------------------

FeedItem = function(cell, det, feedlist) {
	this.det = det; this.feedlist = feedlist;
	this.wrapper = $a(cell,'div','',{marginBottom:'4px'});
	this.tab = make_table(this.wrapper, 1, 2, '100%', [(100/6)+'%', (500/7)+'%']);

	// image
	$y($td(this.tab,0,0),{textAlign:'right',paddingRight:'4px'});
	this.img = $a($td(this.tab,0,0), 'img','',{width:'40px'});
	set_user_img(this.img, det[2]);
	
	// text
	this.text_area = $a($td(this.tab,0,1), 'div');
	if(det[4]) {
		// reference
		this.render_references(this.text_area, det);
	} else {
		this.text_area.innerHTML = '<b>' + det[11] + ' (' + det[12] + '): </b>' + det[1];
	}
	
	if(feedlist) {
		this.make_comment_toolbar();
		this.render_comments();
	}
}
FeedItem.prototype.render_references = function(div, det) {
	// name
	div.innerHTML = '<b>' + det[11] + ' (' + det[12] + '): </b> has ' + det[7] + ' ';
	var l = det[6].split(',');
	
	// doctype
	var span = $a(div, 'span'); span.innerHTML = det[5] + '&nbsp;';

	// records
	for(var i=0;i<(l.length > 5 ? 5 : l.length);i++) {
		if(i>0) {
			var comma_span = $a(div, 'span'); comma_span.innerHTML += ', '; //comma-space
		}
		var span = $a(div, 'span', 'link_type');
		span.innerHTML = l[i]; span.dt = det[4]; span.dn = l[i];
		span.onclick = function() { loaddoc(this.dt, this.dn); }
	}
	if(l.length>5) {
		div.innerHTML += ' and ' + (l.length-5) + ' more record' + (l.length > 6 ? 's': '');
	}
}


FeedItem.prototype.render_comments = function() {
	// render existing comments / in reverse order
	var cl = eval(this.det[8]);
	if(cl) {
		for(var i=0; i<cl.length; i++) {
			new FeedComment($td(this.tab,0,1), cl[cl.length-1-i]);
		}
	}
}
FeedItem.prototype.make_comment_toolbar = function() {
	var me = this;
	this.tbar =  $a($td(this.tab,0,1), 'div', '', {margin:'4px 0px', color:'#888', fontSize:'11px'});
	
	// time
	var t = comment_when(this.det[10]);
	var span = $a(this.tbar, 'span', '', {paddingRight:'8px'});
	span.innerHTML = t;
	
	// if # comments, show
	if(this.det[9]) {
		var span = $a(this.tbar, 'span', '', {paddingRight:'8px'});
		span.innerHTML = this.det[9] + ' comment' + (this.det[9]>1 ? 's' : '');
		
		// link for all comments
		if(this.det[9]>2) {
			var span = $a(this.tbar, 'span', '', {paddingRight:'8px', textDecoration:'underline', cursor:'pointer'});
			span.innerHTML = 'Show All'; span.onclick = function() { me.show_all_comments(); }
		}
	}

	// add comment link
	var span = $a(this.tbar, 'span', '', {paddingRight:'8px', textDecoration:'underline', cursor:'pointer'});
	span.innerHTML = 'Add Comment';
	span.onclick = function() { me.add_comment(); }
}

FeedItem.prototype.show_all_comments = function() {
	var me = this;
	
	if(!me.all_comments_dialog){
		var d = new Dialog(500,400,'All Comments');
		d.make_body([['HTML','cmt_body']]);
		me.all_comments_dialog = d;
	}

	var d = me.all_comments_dialog;
	
	var callback = function(r,rt){
		var lst = r.message;
		
		if(lst && lst.length){
			d.widgets['cmt_body'].innerHTML = '';
			var parent = $a(d.widgets['cmt_body'],'div');

			if(lst.length > 5) $y(parent,{overflow:'auto', width:'100%', height:'300px'})
		
			// render the comments
			for(i=lst.length-1; i>=0; i--){
				new FeedComment(parent, lst[i]);
			}
		}
		d.show();
	}
	
	$c_obj('Feed Control','show_all_comments',me.det[0],callback);

}

FeedItem.prototype.add_comment = function() {
	var me = this;
	if(!this.comment_dialog) {
		var d = new Dialog(360,360,'Add a Comment');
		d.make_body([['Text','Comment'], ['Button','Save']]);
		d.onshow = function() {
			d.widgets['Comment'].value = '';
		}
		d.widgets['Save'].onclick = function() {
			var c = d.widgets['Comment'].value;
			if(!c) { msgprint("You must write a comment first!"); return; }

			var args = {
				cmt:c, cmt_by: user, cmt_by_fullname: user_fullname, dt: 'Feed', dn: me.det[0]
			};
			
			var callback = function(r,rt){
				d.hide();
				me.feedlist.list.run();
			}
			$c_obj('Feed Control', 'add_comment', JSON.stringify(args),callback);			
		}
		this.comment_dialog = d;
	}
	this.comment_dialog.show();
}

// Comment
// -------------------------------

FeedComment = function(parent, det) {
	this.wrapper =  $a(parent, 'div', '', {margin:'4px 0px', color:'#888', fontSize:'11px'});
	this.tab = make_table($a(this.wrapper,'div'), 1, 2, '100%', [null,'20px']);
	$td(this.tab, 0, 0).innerHTML = '<b>' + det[3] + ': </b>' + det[1];
	
	// if owner, then delete button
	if(det[2]==user) {
		this.del_btn = $a($td(this.tab,0,1),'div','wn-icon ' + 'ic-trash', {cursor:'pointer'});
		this.del_btn.onclick = function() {
			$c_obj('');
		}
	}
}

// Status bar
// ==================================

pscript.home_make_status = function() {
	var wrapper = page_body.pages['Event Updates'];

	var div = $a(wrapper.head,'div','',{borderBottom:'1px solid #AAA', marginBottom:'8px'});
	var tab = make_table(div, 1, 3, null, [], {padding:'4px 6px', cursor:'pointer', color:'#666', textDecoration:'underline'});
	
	// messages
	$td(tab,0,0).innerHTML = 'Messages...';
	$td(tab,0,0).onclick = function() { loadpage('Messages') }
	
	// users
	$td(tab,0,1).innerHTML = 'Online Users...';
	$td(tab,0,1).onclick = function() { loadpage('My Company') }

	// get values
	$c_obj('Home Control', 'get_status_details', user,
		function(r,rt) { 
			$td(tab,0,0).innerHTML = 'Messages (' + r.message.unread + ')'; 
			$td(tab,0,1).innerHTML = r.message.user_count + ' user'+(r.message.user_count >1 ? 's': '')+' online';
		});
	
	// wip montior
	$td(tab,0,2).innerHTML = 'Work In Progress';
	$td(tab,0,2).onclick = function() { loadpage('WIP Monitor') }
	$y($td(tab,0,2),{borderRight:'0px'});	
}

// complete my company registration
// --------------------------------
pscript.complete_registration = function()
{
	var reg_callback = function(r, rt){
		if(r.message == 'No'){
			var d = new Dialog(400, 200, "Please Complete Your Registration");
			if(user != 'Administrator'){
				d.no_cancel(); // Hide close image
				$dh(page_body.wntoolbar.wrapper);
			}
			$($a(d.body,'div','', {margin:'8px', color:'#888'})).html('<b>Company Name : </b>'+locals['Control Panel']['Control Panel'].company_name);      

			d.make_body(
		  [
		  	['Data','Company Abbreviation'],
		  	['Select','Fiscal Year Start Date'],
		  	['Select','Default Currency'],
		  	['Button','Save'],
			]);

			//d.widgets['Save'].disabled = true;      // disable Save button
			pscript.make_dialog_field(d);

			// submit details
			d.widgets['Save'].onclick = function()
			{
				flag = pscript.validate_fields(d);
				if(flag)
				{
					var args = [
						locals['Control Panel']['Control Panel'].company_name,
						d.widgets['Company Abbreviation'].value,
						d.widgets['Fiscal Year Start Date'].value,
						d.widgets['Default Currency'].value
					];
					
					$c_obj('Setup Control','setup_account',JSON.stringify(args),function(r, rt){
						sys_defaults = r.message;
						d.hide();
						$ds(page_body.wntoolbar.wrapper);
					});
				}
			}
			d.show();
		}
	}
	$c_obj('Home Control','registration_complete','',reg_callback);
}

// complete my company registration
// --------------------------------
pscript.complete_registration = function()
{
	var reg_callback = function(r, rt){
		if(r.message == 'No'){
			var d = new Dialog(400, 200, "Please Complete Your Registration");
			if(user != 'Administrator'){
				d.no_cancel(); // Hide close image
				$dh(page_body.wntoolbar.wrapper);
			}
			$($a(d.body,'div','', {margin:'8px', color:'#888'})).html('<b>Company Name : </b>'+locals['Control Panel']['Control Panel'].company_name);      

			d.make_body(
		  [
		  	['Data','Company Abbreviation'],
		  	['Select','Fiscal Year Start Date'],
		  	['Select','Default Currency'],
		  	['Button','Save'],
			]);

			//d.widgets['Save'].disabled = true;      // disable Save button
			pscript.make_dialog_field(d);

			// submit details
			d.widgets['Save'].onclick = function()
			{
				flag = pscript.validate_fields(d);
				if(flag)
				{
					var args = [
						locals['Control Panel']['Control Panel'].company_name,
						d.widgets['Company Abbreviation'].value,
						d.widgets['Fiscal Year Start Date'].value,
						d.widgets['Default Currency'].value
					];
					
					$c_obj('Setup Control','setup_account',JSON.stringify(args),function(r, rt){
						sys_defaults = r.message;
						d.hide();
						$ds(page_body.wntoolbar.wrapper);
					});
				}
			}
			d.show();
		}
	}
	$c_obj('Home Control','registration_complete','',reg_callback);
}

// make dialog fields
// ------------------
pscript.make_dialog_field = function(d)
{
	// fiscal year format 
	fisc_format = d.widgets['Fiscal Year Start Date'];
	add_sel_options(fisc_format, ['', '1st Jan', '1st Apr', '1st Jul', '1st Oct']);
  
	// default currency
	currency_list = ['', 'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN', 'BYR', 'BZD', 'CAD', 'CDF', 'CFA', 'CFP', 'CHF', 'CLP', 'CNY', 'COP', 'CRC', 'CUC', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EEK', 'EGP', 'ERN', 'ETB', 'EUR', 'EURO', 'FJD', 'FKP', 'FMG', 'GBP', 'GEL', 'GHS', 'GIP', 'GMD', 'GNF', 'GQE', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LTL', 'LVL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRO', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZM', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NRs', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RMB', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SCR', 'SDG', 'SDR', 'SEK', 'SGD', 'SHP', 'SOS', 'SRD', 'STD', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TRY', 'TTD', 'TWD', 'TZS', 'UAE', 'UAH', 'UGX', 'USD', 'USh', 'UYU', 'UZS', 'VEB', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XDR', 'XOF', 'XPF', 'YEN', 'YER', 'YTL', 'ZAR', 'ZMK', 'ZWR'];
	currency = d.widgets['Default Currency'];
	add_sel_options(currency, currency_list);
}


// validate fields
// ---------------
pscript.validate_fields = function(d)
{
	var lst = ['Company Abbreviation', 'Fiscal Year Start Date', 'Default Currency'];
	var msg = 'Please enter the following fields';
	var flag = 1;
	for(var i=0; i<lst.length; i++)
	{
		if(!d.widgets[lst[i]].value){
			flag = 0;
			msg = msg + NEWLINE + lst[i];
		}
	}

	if(!flag)  alert(msg);
	return flag;
}
