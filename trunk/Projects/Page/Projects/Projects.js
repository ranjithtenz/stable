pscript.onload_Projects = function() {
  var d = $i('projects_div');

  // page head
  d.page_head = new PageHeader(d, 'Projects');

  // make tray
  var tray = pscript.home_tasks_maketray(d);
  
  // make projects
  pscript.make_projects_dashboard(d, tray.items.Projects.body)
  
  // chart
  $y(tray.items['Gantt Chart'].body, {margin:'16px 0px'})
  new GanttChart(tray.items['Gantt Chart'].body);

  // make tasks  
  $y(tray.items['Reports'].body, {margin:'16px 0px'})
  pscript.home_tasks_maketasks(d, tray.items.Tasks.body)
  
  // timesheets
  pscript.show_time_sheets(tray.items['Timesheets']);
  
  // view reports  
  pscript.make_proj_reports(tray.items.Reports.body);
  
  tray.items.Tasks.expand();
}

// tray
// ==================================================================================

pscript.home_tasks_maketray = function(d) {
	var tray = new TrayPage(d);
	tray.add_item('Tasks')
	tray.add_item('Projects', function() { $i('projects_div').projects_docbrowser.show(); })
	tray.add_item('Timesheets', function() { $i('projects_div').timesheet_docbrowser.show(); })
	tray.add_item('Gantt Chart')
	tray.add_item('Reports')

	$i('projects_div').tray = tray;

	setTimeout(pscript.projects_set_height, 100);
	set_resize_observer(pscript.projects_set_height);
	
	return tray;
}

pscript.projects_set_height = function() {
	var parent = $i('projects_div');
	$y(parent.tray.body, {height:get_window_height() - parent.page_head.wrapper.offsetHeight + 'px', overflow:'auto'});
}

pscript.show_time_sheets = function(item) {
	$i('projects_div').timesheet_docbrowser = new ItemBrowser(item.body, 'Timesheet', 'Timesheet');
}

// ==================================================================================

pscript.queries_bg_dict = {'Open':'#E9AA4D', 'Closed':'#729C5B', 'Low':'#4683D7', 'Medium':'#F5B800', 'High':'#F16926', 'Urgent':'#FF0000', 'Internal':'#9E9E9E', 'External':'#494949','Pending Review':'#A4C032'};

pscript.home_tasks_listing = function(d) {
  var lst = new Listing('Tasks', 1);

  lst.colwidths = ['10%','50%','40%'];
  lst.dt = 'Ticket';


  // define options
  var opts = {};

  opts.head_main_style = {};
  opts.cell_style = { padding:'4px 2px', borderRight : '0px', borderBottom : '1px solid #AAA', verticalAlign: 'middle'}
  opts.head_style = { padding:'2px', borderBottom : '1px solid #AAA'}
  opts.alt_cell_style = {};
  opts.hide_print = 1;
  opts.no_border = 1;

  opts.show_new = 0;
  opts.hide_export = 1;
  opts.hide_print = 1;
  opts.hide_refresh = 0;
  opts.hide_rec_label = 0;

  lst.opts = opts;

  // query
  lst.get_query = function() {
    this.query = "SELECT name, subject, priority, status, creation, senders_name, allocated_to, external_or_internal, scheduled_date, category FROM `tabTicket` WHERE docstatus != 2";
    this.query_max = "SELECT count(*) FROM `tabTicket` WHERE docstatus != 2";
  }
 
  // output
  lst.show_cell = function(cell,ri,ci,d){
    if(ci==0) {
      var sp = $a(cell, 'div', 'link_type');
      sp.innerHTML = d[ri][0];
     
      sp.onclick = function() { loaddoc('Ticket', this.dn); }
      sp.dn = d[ri][0];

      var sp = $a(cell, 'div', 'comment');
      sp.innerHTML = date.str_to_user(d[ri][4]);

    }

    if(ci==1) {
      $a(cell,'div').innerHTML = d[ri][1];

      // allocated
      if(d[ri][6]) {
        var d2 = $a(cell, 'div','',{fontWeight:'bold', color:'#888'});
        d2.innerHTML = 'Allocated To:' + d[ri][6] + ' / Expected completion by: ' + date.str_to_user(d[ri][8]);
      }
    }

    if(ci==2) {
      var d1 = $a(cell, 'div');
      d1.innerHTML = 'By: ' + d[ri][5];

      // status, priority, internal / external
      var d3 = $a(cell, 'div','',{margin:'4px 0px'});

      var make_tag = function(label) {
        var t = $a(d3, 'span', '', {color:'#FFF', fontWeight:'bold', fontSize:'11px', padding:'2px', marginRight:'4px', backgroundColor:(pscript.queries_bg_dict[label] ? pscript.queries_bg_dict[label] : '#003399')});
        t.innerHTML = label;
      }

      make_tag(d[ri][3]);
      make_tag(d[ri][2]);
      if(d[ri][7])
        make_tag(d[ri][7]);
      if(d[ri][9])
        make_tag(d[ri][9]);

    }

  }

  lst.make(d);

  // filters
  lst.add_filter('Status', 'Select', ['','Open','Pending Review','Closed'].join(NEWLINE), 'Ticket', 'status', '=');
  lst.add_filter('Priority', 'Select', ['','Low','Medium','High','Urgent'].join(NEWLINE), 'Ticket', 'priority', '=');
  lst.add_filter('External or Internal', 'Select', ['','External','Internal'].join(NEWLINE), 'Ticket', 'external_or_internal', '=');
  lst.add_filter('Raised By', 'Data', '', 'Ticket', 'senders_name', 'LIKE');
  lst.add_filter('Allocated To', 'Data', '', 'Ticket', 'allocated_to', 'LIKE');
  lst.add_filter('Category', 'Link', 'Ticket Category', 'Ticket', 'category', '=');
  lst.add_filter('Project', 'Link', 'Project', 'Ticket', 'project', '=');
  lst.add_filter('Subject', 'Data', '', 'Ticket', 'subject', 'LIKE');

  lst.set_default_sort('name', 'DESC');

  lst.run();

  pscript.home_tasks_list = lst;

}

// ==================================================================================

pscript.home_tasks_status = function(d0) {

  d0.innerHTML = '';

  var t1 = make_table(d0,1,2,'100%',['40%','60%'],{padding:'4px 8px'});

  // open / closed
  // -------------
  var s1 = $a($td(t1,0,0), 'div', '', { color:'#888','fontSize':'14px', marginBottom:'8px', display:'none'}); s1.innerHTML = 'Open & Closed Tasks';
  var t_open_closed = make_table($a(s1,'div','',{border:'1px solid #AAA'}),1,3,'100%',[],{height:'24px'});
  s1.mo = $a(s1,'div','',{color:'#888',fontSize:'12px',height:'14px'});

  $y(t_open_closed,{tableLayout:'fixed'});

  // set color and make onclick function - Status
  // --------------------------------------------

  var sfn = function(idx, label) {
    
    var c = $td(t_open_closed,0,idx)
    $y(c,{backgroundColor:pscript.queries_bg_dict[label], cursor:'pointer'});
    c.label = label;
    c.onclick = function() {
       pscript.home_tasks_list.filters['Status'].txt.value = this.label;
       pscript.home_tasks_list.filters['Priority'].txt.value = '';
       pscript.home_tasks_list.run();
    }
    $(c).hover(
      function() { s1.mo.innerHTML = this.label + ': ' + this.style.width; },
      function() { s1.mo.innerHTML = ''; }
    );
  }

  sfn(0,'Open');
  sfn(1,'Pending Review');
  sfn(2,'Closed');

  

  // Priority
  // ----------------------------------------------

  var s2 = $a($td(t1,0,1), 'div', '', { color:'#888','fontSize':'14px', marginBottom:'8px', display:'none'}); s2.innerHTML = 'Status of Open Tasks';
  var t_open_status = make_table($a(s2,'div','',{border:'1px solid #AAA'}),1,4,'100%',[],{height:'24px'});
  $y(t_open_status,{tableLayout:'fixed'});
  s2.mo = $a(s2,'div','',{color:'#888',fontSize:'12px',height:'14px'});


  // set color and make onclick function - Priority
  // ----------------------------------------------

  var pfn = function(idx, label) {
    var c = $td(t_open_status,0,idx)
    $y(c,{backgroundColor:pscript.queries_bg_dict[label], cursor:'pointer'});
    c.label = label;
    c.onclick = function() {
       pscript.home_tasks_list.filters['Status'].txt.value = 'Open';
       pscript.home_tasks_list.filters['Priority'].txt.value = this.label;
       pscript.home_tasks_list.run();
    }
    $(c).hover(
      function() { s2.mo.innerHTML = this.label + ': ' + this.style.width; },
      function() { s2.mo.innerHTML = ''; }
    );

  }

  pfn(0,'Urgent');
  pfn(1,'High');
  pfn(2,'Medium');
  pfn(3,'Low');
  
  // show status
  var callback = function(r,rt) {
    if(r.message.open) {
      $ds(s1); $ds(s2);
      $y($td(t_open_closed,0,0),{width:r.message.open + '%'});
      $y($td(t_open_closed,0,1),{width:r.message.review + '%'});
      $y($td(t_open_closed,0,2),{width:(100-r.message.open-r.message.review) + '%'});
      $y($td(t_open_status,0,0),{width:r.message.urgent + '%'});
      $y($td(t_open_status,0,1),{width:r.message.high + '%'});
      $y($td(t_open_status,0,2),{width:r.message.medium + '%'});
      $y($td(t_open_status,0,3),{width:(100-r.message.urgent-r.message.medium-r.message.high) + '%'});
    }
  }
  $c_obj('Ticket Control','get_status','',callback);

}

// queries trend
// ==================================================================================

pscript.home_tasks_trends = function(d1,days){
  // first clear
  d1.innerHTML = '';
  
  var trend_tbl = make_table(d1,1,days,'100%',[],{marginRight:'10px',width:'40px', verticalAlign:'bottom'});
  
  var callback = function(r,rt){
    dict = r.message;
  
    // find max
    var max = 0;
    for(d in dict) { if(dict[d].Open > max)max=dict[d].Open; if(dict[d].Closed > max)max=dict[d].Closed; }
  
    // render
    for(d in dict){
      
      var w = $a($td(trend_tbl,0,d),'div','',{cursor:'pointer'});
      w.data = dict[d];
      w.onclick = function() {
        msgprint(this.data.Day + ': ' + this.data.Open + ' Opened / ' + this.data.Closed + ' Closed.');
      }
      
      var t = make_table(w,1,2,'40px',['20px','20px'],{verticalAlign:'bottom', textAlign:'center', height:'25px'});
      $y(t, {margin:'0px auto'});
      
      // open
      var ht = (dict[d]['Open'] * 100 / max) + '%'; 
      $a($td(t,0,0),'div','',{width:'20px',backgroundColor:pscript.queries_bg_dict.Open, height:ht});
           
      // closed
      var ht = (dict[d]['Closed'] * 100 / max) + '%';
      $a($td(t,0,1),'div','',{width:'20px',backgroundColor:pscript.queries_bg_dict.Closed, height:ht});
      
      var lab = $a(w,'div','',{textAlign:'center', marginTop:'4px', fontSize:'11px', color:'#777'});
      lab.innerHTML = dict[d]['Day'];
    }
  }
  $c_obj('Ticket Control','get_activity',days,callback);
}

// Tasks
// ==================================================================================

pscript.home_tasks_maketasks = function(parent, body) {

  // refresh button
  // --------------
  var btn = $a($a(body, 'div','',{textAlign:'right', height:'16px', margin:'4px 0px'}), 'div', 'wn-icon ic-playback_reload', {cssFloat:'right'});

  // snapshot
  var d0 = $a(body,'div','',{marginBottom:'8px'});
  pscript.home_tasks_status(d0);
  
  // activity trend
  var d1 = $a(body,'div','',{marginBottom:'8px'});
  pscript.home_tasks_trends(d1,7);

  $(btn).click(function() { pscript.home_tasks_status(d0);pscript.home_tasks_trends(d1,7); })


  // new ticket button
  if(in_list(profile.can_create, 'Ticket')) {
  	parent.page_head.add_button('New Task', function() { newdoc('Ticket') }, 0, 'ui-icon-plus');
  	parent.page_head.add_button('New Timesheet', function() { newdoc('Timesheet') }, 0, 'ui-icon-plus');
  }

  // make listing
  pscript.home_tasks_listing(body);
}

// Milestones
// =====================================================================================

pscript.make_projects_milestones = function(w, ml) {
  // head

  var h = $a(w,'h3'); $(h).html('Upcoming Milestones');
  var c = $a(w,'div','comment',{fontSize:'11px',marginBottom:'8px'}); $(c).html('You can add milestones by adding them in the Project');

  var t = make_table($a(w,'div','', {marginBottom:'24px'}), 2, 7, '100%', [], {padding:'2px', verticalAlign:'top', border:'1px solid #888'});

  var today = new Date();
  var flag = 0;

  for(var i=0; i<7; i++) {
    var dt = today;

    // make date heads
    $y($td(t,0,i), {textAlign:'center', backgroundColor:'#DDD'});
    var l = date.obj_to_user(dt);
    if(i==0) l= 'Today';
    if(i==1) l= 'Tomorrow';

    $td(t,0,i).innerHTML = l;

    // add milestones
    for(var mi=0; mi<ml.length; mi++) {
     
     // if milestone on this day
     if(ml[mi][0]==date.obj_to_str(dt)) {
        flag = 1;

        var d1 = $a($td(t,1,i), 'div', 'link_type', {margin:'4px 0px'});
        d1.dn = ml[mi][2];
        d1.onclick = function() { loaddoc('Project', this.dn); }
        d1.innerHTML = ml[mi][1] + ' (' + ml[mi][2] + ')';

      }
    }

    var dt = date.add_days(today, 1);

  }
  if(!flag) $dh(w);
}

// =====================================================================================

pscript.make_projects_dashboard = function(parent, body) {

  var w = $a(body, 'div');

  // make projects
  var callback = function(r,rt) {
    
    // show milestones
    pscript.make_projects_milestones(w, r.message.ml)
    
    // new project button
    if(in_list(profile.can_create, 'Project')) {
      parent.page_head.add_button('New Project', function() { newdoc('Project') }, 0, 'ui-icon-plus');
    }
    
  }
  $c_obj('Project Control','get_projects','Open',callback);
  
  parent.projects_docbrowser = new ItemBrowser(body, 'Project', 'Project');
  set_title('Projects');  
}

// Gantt Chart
// ==========================================================================

GanttChart = function(parent) {
	this.wrapper = $a(parent, 'div');
	//this.head = new PageHeader(this.wrapper, 'Gantt Chart');

	this.toolbar_area = $a(this.wrapper, 'div','',{padding:'16px', border:'1px solid #AAA'});
	this.toolbar_tab = make_table(this.toolbar_area, 1, 4, '100%', ['25%', '25%','25%', '25%']);
	this.grid_area = $a(this.wrapper, 'div', '', {margin: '16px 0px'});

	this.get_init_data();
	//this.make_grid();
}

GanttChart.prototype.get_init_data = function() {
	var me = this;
	var callback = function(r,rt) {
		me.pl = r.message.pl.sort();
		me.rl = r.message.rl.sort();

		me.make_toolbar();
	}
	$c_obj('Project Control','get_init_data','', callback);
}

GanttChart.prototype.make_filter = function(label, idx) {
	var w = $a($td(this.toolbar_tab,0,idx), 'div','',{marginBottom:'8px'});
	var l = $a(w, 'div','',{fontSize:'11px'}); l.innerHTML = label;
	return w;
}

GanttChart.prototype.make_select = function(label, options,idx) {
	var w = this.make_filter(label,idx);
	var s = $a(w, 'select','',{width:'100px'}); add_sel_options(s, add_lists(['All'],options));
	return s;
}

GanttChart.prototype.make_date = function(label,idx) {
	var w = this.make_filter(label,idx);
	var i = $a(w, 'input');

	var user_fmt = locals['Control Panel']['Control Panel'].date_format;
	if(!this.user_fmt)this.user_fmt = 'dd-mm-yy';

	$(i).datepicker({
		dateFormat: user_fmt.replace('yyyy','yy'), 
		altFormat:'yy-mm-dd', 
		changeYear: true
	});
	
	return i;
}

GanttChart.prototype.make_toolbar = function() {

	// resource / project
	this.r_sel = this.make_select('Resource', this.rl, 0);
	this.p_sel = this.make_select('Project', this.pl, 1);
	
	// start / end
	this.s_date = this.make_date('Start Date', 2); this.s_date.value = date.str_to_user(date.month_start());
	this.e_date = this.make_date('End Date', 3); this.e_date.value = date.str_to_user(date.month_end());
	
	// button
	var me = this;
	var btn = $a($a(this.toolbar_area,'div','green_buttons'),'button'); 
	btn.innerHTML = 'Make'; 
        $(btn).button();
	btn.onclick = function() { me.refresh(); }
}

GanttChart.prototype.get_data = function() {
	var me = this;
	var callback = function(r, rt) {
		me.tasks = r.message;
		me.show_tasks(); 
	}
	$c_obj('Project Control','get_tasks',
		[date.str_to_user(this.s_date.value), 
		date.str_to_user(this.e_date.value), 
		sel_val(this.p_sel), 
		sel_val(this.r_sel)].join('~~~')
	, callback)
}

GanttChart.prototype.make_grid = function() {
	// clear earlier chart
	this.grid_area.innerHTML = '';
	this.grid = new GanttGrid(this, this.s_date.value, this.e_date.value);
}

GanttChart.prototype.refresh = function() {
	this.get_data();
}
	
GanttChart.prototype.show_tasks = function() {
	this.make_grid();
	for(var i=0; i<this.tasks.length; i++) {
		new GanttTask(this.grid, this.tasks[i], i)
	}
}

// ==========================================================================

GanttGrid = function(chart, s_date, e_date) {
	this.chart = chart;
	this.s_date = s_date;

	this.wrapper = $a(chart.grid_area, 'div');
	this.start_date = date.str_to_obj(date.str_to_user(s_date));
	this.end_date = date.str_to_obj(date.str_to_user(e_date));

	this.n_days = date.get_diff(this.end_date, this.start_date) + 1;	
	this.g_width = 100 / this.n_days + '%';	

	this.make();
}

GanttGrid.prototype.make_grid = function() {
	// grid -----------
	var ht = this.chart.tasks.length * 40 + 'px';
	this.grid = $a($td(this.body, 0, 1), 'div', '', {border:'2px solid #888', height: ht, position:'relative'});	

	this.grid_tab = make_table(this.grid, 1, this.n_days, '100%', [], {width:this.g_width, borderLeft:'1px solid #DDD', height: ht});
	$y(this.grid_tab,{tableLayout:'fixed'});

	this.task_area = $a(this.grid, 'div', '', {position:'absolute', height:ht, width: '100%', top:'0px'});
}

GanttGrid.prototype.make_labels = function() {
	// labels ------------
	this.x_labels = $a($td(this.body, 0, 1), 'div', '', {marginTop:'8px'});	
	this.x_lab_tab = make_table(this.x_labels, 1, this.n_days, '100%', [], {width:this.g_width, fontSize:'10px'});
	$y(this.x_lab_tab,{tableLayout:'fixed'});
	
	var d = this.start_date;
	var today = new Date();
	for(var i=0; i<this.n_days; i++) {
		if(d.getDay()==0) {
			$td(this.x_lab_tab,0,i).innerHTML = d.getDate() + '-' + month_list[d.getMonth()];
			$y($td(this.grid_tab,0,i),{borderLeft:'1px solid RED'})
		}
		if(d.getDate()==today.getDate() && d.getMonth()==today.getMonth() && d.getYear() == today.getYear()) {
			$y($td(this.grid_tab,0,i),{borderLeft:'2px solid #000'})
		}
		var d = date.add_days(this.start_date, 1);
	}
	this.start_date = date.str_to_obj(date.str_to_user(this.s_date));
}

GanttGrid.prototype.make = function() {
	this.body = make_table(this.wrapper, 1, 2, '100%', ['30%','70%']);
	this.make_grid();
	this.make_labels();
	this.y_labels = $a($td(this.body, 0, 0), 'div', '', {marginTop:'2px', position:'relative'});	
}

GanttGrid.prototype.get_x = function(dt) {
	var d = date.str_to_obj(dt); // convert to obj
	return flt(date.get_diff(d, this.start_date)+1) / flt(date.get_diff(this.end_date, this.start_date)+1) * 100;
}

// ==========================================================================

GanttTask = function(grid, data, idx) {
	// start_date, end_date, name, status
	this.start_date = data[3];
	this.end_date = data[4];

	// label
	this.label = $a(grid.y_labels, 'div', '', {'top':(idx*40) + 'px', overflow:'hidden', position:'absolute', 'width':'100%', height: '40px'});
	var l1 = $a(this.label, 'div', 'link_type'); l1.innerHTML = data[0]; l1.dn = data[7]; l1.onclick = function() { loaddoc('Ticket', this.dn) };
	var l2 = $a(this.label, 'div', '', {fontSize:'10px'}); l2.innerHTML = data[1];

  

	// bar
	var col = pscript.queries_bg_dict[data[5]];
        if(data[6]!='Open') col = pscript.queries_bg_dict[data[6]];
	this.body = $a(grid.task_area, 'div','',{backgroundColor:col, height:'12px', position:'absolute'});

  //bar info
  this.body_info = $a(this.body, 'div','',{backgroundColor:'#CCC', position:'absolute', zIndex:20});

	var x1 = grid.get_x(this.start_date);
	var x2 = grid.get_x(this.end_date);

	if(x1<=0)x1=0;
  else x1 -=100/flt(date.get_diff(grid.end_date, grid.start_date)+1);
	if(x2>=100)x2=100;
//  else x2+=100/flt(date.get_diff(grid.end_date, grid.start_date)+1);
	
	$y(this.body, { 
		top: idx * 40 + 14 + 'px',
		left: x1 + '%',
		width: (x2-x1) + '%',
		zIndex: 1
	})
	
	// divider
	if(idx) {
		var d1 = $a(grid.task_area, 'div','',{borderBottom: '1px solid #AAA', position:'absolute', width:'100%', top:(idx*40) + 'px'});
		var d2 = $a(grid.y_labels, 'div','',{borderBottom: '1px solid #AAA', position:'absolute', width:'100%', top:(idx*40) + 'px'});
	}
	
	this.make_tooltip(data);
}

GanttTask.prototype.make_tooltip = function(d) {
	var t = '<div>';
  if(d[0]) t += '<b>Task: </b>' + d[0];
	if(d[5]) t += '<br><b>Priority: </b>' + d[5];
	if(d[6]) t += '<br><b>Status: </b>' + d[6];
	if(d[1]) t += '<br><b>Allocated To: </b>' + d[1];
	if(d[2]) t += '<br><b>Project: </b>' + d[2];
	if(d[3]) t += '<br><b>From: </b>' + date.str_to_user(d[3]);
	if(d[4]) t += '<br><b>To: </b>' + date.str_to_user(d[4]);
  t += '</div>';

	this.body.title = t;
	//this.label.title = t;
	$(this.body).tooltip();	
	//$(this.label).tooltip();
  /*
  $(this.body).hover(
    function() {
      this.body_info.innerHTML = t;
    },
    function() {this.body_info.innerHTML = '';}
  );
*/
}

// ==========================================================================

pscript.make_proj_reports = function(parent) {
  var me = this;
  
  var rl = [
  ['Projectwise Sales Details','Sales Order','Sales Order','Sales Orders by Project'],
  ['Projectwise Purchase Details','Purchase Order','Purchase Order','Purchase Orders by Project'],
  ['Projectwise Delivered Qty and Costs','Delivery Note Detail','Delivery Note','Delivery Notes by Project'],
  ['Projectwise Pending Qty and Costs','Sales Order Detail','Sales Order','Pending items by Project, based on sales order'],
  ['Projectwise Tracking of All Stock Movements','Project','Project', 'Projectwise tracking of stock movements'],
  ['Projectwise Contribution Report','Project','Project', 'Projectwise contribution'],
  ['Projectwise Delivery and Material Cost','Sales Order Detail','Sales Order','Projectwise Delivery and Material Cost'],
  ['Dispatch Report','Delivery Note Detail','Delivery Note','Items delivered by project'],
  ['Timesheet Report','Timesheet Detail','Timesheet','Timesheet items by project']
  ]
  
  for(var i =0; i<rl.length; i++){
    if(in_list(profile.can_read, rl[i][2])) {
      var div = $a(parent, 'div', '', {marginBottom: '8px'});
      var tab = make_table(div, 1, 2, '80%', ['30%', '70%']);
      var span = $a($td(tab, 0, 0), 'span', 'link_type');
      span.innerHTML = rl[i][0]; span.dt = rl[i][1]; span.sc = rl[i][0];
      span.onclick = function() { loadreport(this.dt, this.sc) }
      
      $y($td(tab, 0, 1), {color:'#888'});
      $td(tab, 0, 1).innerHTML = rl[i][3];
    }
  }
}



