// Sidebar Menu
SidebarMenu = function() {
	this.menu_items = {};	
	this.menu_lists = {};
	this.menu_dt_details = {};
	this.menu_page = page_body.add_page('Document Browser', function() {
		if(sidebar_menu.cur_node) sidebar_menu.cur_node.show_selected();		
	})

	this.wrapper = $a(this.menu_page,'div','',{margin:'8px'});
	this.head = $a(this.wrapper, 'div', 'standard_title');
	this.body = $a(this.wrapper, 'div');
  
	// make tree
	this.tree_wrapper = $a(page_body.left_sidebar,'div','',{padding:'0px 4px', marginRight:'0px'});
	this.menu_tree = new Tree($a(this.tree_wrapper,'div'),'100%',1);
}

// Menu Click
// ----------

SidebarMenu.prototype.menu_click = function(n) {
  if(n.menu_item.menu_item_type == 'DocType') {
    sidebar_menu.cur_node = n;
    sidebar_menu.show_listing(n.menu_item.name);
  } else if(n.menu_item.menu_item_type == 'New') {
  	newdoc(n.menu_item.link_id);
  } else if(n.menu_item.menu_item_type == 'Single') {
    loaddoc(n.menu_item.link_id, n.menu_item.link_id, null, n); 
    n.toggle();
  } else if(n.menu_item.menu_item_type == 'Page') {
    loadpage(n.menu_item.link_id, n.onload, n); 
    n.toggle();
  } else if(n.menu_item.menu_item_type == 'Report') {
    loadreport(n.menu_item.link_id, n.menu_item.link_content ? n.menu_item.link_content : n.menu_item.menu_item_label, n.onload, n);
  } else {
  	if(n.onload) n.onload();
    n.toggle();
  }
}

// Make Menu
// ----------

pscript.set_menu_style = function(level) {
	var opt = {}
	if(level==0) {
		opt = {
			show_exp_img:0, show_icon:0 
			,label_style:{padding:'4px', cursor: 'pointer',color:'#222',marginBottom:'4px',fontSize:'14px',borderBottom:'1px solid #CCC',fontWeight: 'bold', backgroundColor:'#EEE'}
			//,onselect_style:{color: '#56C'}
			//,ondeselect_style:{color: '#000'}
		}
	} else if(level==1) {
		opt = {
			show_exp_img:0, show_icon:0
			,label_style:{padding:'4px', paddingTop:'0px', marginBottom:'4px', cursor: 'pointer',borderBottom:'1px solid #CCC',fontSize:'12px',marginLeft:'8px'}
			,onselect_style:{fontWeight: 'bold'}
			,ondeselect_style:{fontWeight: 'normal'}
		}
	} if(level>=2) {
		opt = {
			show_exp_img:0, show_icon:0 
			,label_style:{padding:'4px', paddingTop:'0px', marginBottom:'4px', cursor: 'pointer',borderBottom:'1px dashed #EEE',fontSize:'11px',marginLeft:'12px'}
			,onselect_style:{fontWeight: 'bold'}
			,ondeselect_style:{fontWeight: 'normal'}
		}
	}
	return opt
}

SidebarMenu.prototype.make_menu = function(parent) {
  var me = sidebar_menu;
  this.parent = parent;
  var callback = function(r,rt) {
  	// style
  	// -----
  	var level = 0
  	if(parent) level = parent.level;
  	var opt = pscript.set_menu_style(level);

    // add nodes
    // ---------
    for(var i=0;i<r.message.length;i++) {
      var n = me.menu_tree.addNode(
      	parent,
      	r.message[i].menu_item_label,
      	(r.message[i].icon ? 'images/icons/' + r.message[i].icon : ''),
      	me.menu_click,
      	(r.message[i].has_children ? me.make_menu : null),
      	opt);

      n.menu_item = r.message[i];
      if(n.menu_item.onload) {
      	n.onload = eval('var a='+n.menu_item.onload+';a'); // set function
      }
      if(n.menu_item.menu_item_type=='DocType')
        me.menu_items[n.menu_item.name] = n.menu_item;
      // level
      // -----
      if(parent) n.level = parent.level + 1;
      else n.level = 1;
      
      // callback parent tree
    }
    if(parent) { parent.show_expanded(); }
  }
  $c_obj('Menu Control','get_children',parent ? parent.menu_item.name : '', callback);
}

SidebarMenu.prototype.show_listing = function(mid) {
  // get DocType Details
  // -------------------
  var me = sidebar_menu;
  var mi = me.menu_items[mid];
  if(!me.menu_dt_details[mid]) {
    $c_obj('Menu Control', 'get_dt_details', mi.link_id + '~~~' + mi.doctype_fields, 
      function(r,rt) { me.menu_dt_details[mi.name] = r.message; if(r.message) me.show_listing(mi.name); });
    return;
  }

  me.head.innerHTML = mi.menu_item_label;

  if(me.cur_menu_lst) 
    $dh(me.cur_menu_lst.wrapper);

  if(!me.menu_lists[mi.name]) {

    var lst = new Listing(mi.menu_item_label);
    lst.cl = me.menu_dt_details[mi.name].columns;
    lst.dt = mi.link_id;

    lst.opts = {
		cell_style : {padding:'3px 2px',borderBottom:'1px dashed #CCC'},
		alt_cell_style : {backgroundColor:'#FFFFFF'},
		head_style : {overflow:'hidden',verticalAlign:'middle',fontWeight:'bold',padding:'2px'},
		head_main_style : {padding:'0px'},
		hide_export : 1,
		hide_print : 1,
		hide_refresh : 0,
		hide_rec_label: 0,
		show_calc: 0,
		show_empty_tab : 0,
		show_bottom_paging: 0,
		round_corners: 0,
		no_border: 1,
		show_new: 1,
		show_report: 1
    }
    
    if(user_defaults.hide_report_builder) lst.opts.show_report = 0;
    
    lst.is_std_query = 1;
    lst.get_query = function() {
      q = {};
      var fl = [];
      q.table = repl('`tab%(dt)s`', {dt:this.dt});
      
      for(var i=0;i<this.cl.length;i++) fl.push(q.table+'.`'+this.cl[i][0]+'`')
      q.fields = fl.join(', ');
      q.conds = q.table + '.docstatus < 2 ';
      
      this.query = repl("SELECT %(fields)s FROM %(table)s WHERE %(conds)s", q);
      this.query_max = repl("SELECT COUNT(*) FROM %(table)s WHERE %(conds)s", q);
    }
  
    lst.colwidths=['5%']; lst.colnames=['Sr']; lst.coltypes=['Data']; lst.coloptions = [''];

    for(var i=0;i < lst.cl.length;i++) {
      lst.colwidths[i+1] = cint(100/lst.cl.length) + '%';
      lst.colnames[i+1] = lst.cl[i][1];
      lst.coltypes[i+1] = lst.cl[i][2];
      lst.coloptions[i+1] = lst.cl[i][3];
      
      lst.add_sort(i+1, lst.cl[i][0]);
    }

    lst.make($a(this.body, 'div', '', {display:'none'}));

    var sf = me.menu_dt_details[mi.name].filters;
    for(var i=0;i< sf.length;i++) {
      var fname = sf[i][0]; var label = sf[i][1]; var ftype = sf[i][2]; var fopts = sf[i][3];

      if(in_list(['Int','Currency','Float','Date'], ftype)) {
        lst.add_filter('From '+label, ftype, fopts, mi.link_id, fname, '>=');
        lst.add_filter('To '+label, ftype, fopts, mi.link_id, fname, '<=');
      } else {
        lst.add_filter(label, ftype, fopts, mi.link_id, fname, (in_list(['Data','Text','Link'], ftype) ? 'LIKE' : ''));
      }
    }
    me.menu_lists[mi.name] = lst;
    
    // default sort
    lst.set_default_sort('name', in_list(lst.coltypes, 'Date') ? 'DESC' : 'ASC')
    lst.run();
  }

  $ds(me.menu_lists[mi.name].wrapper);
  page_body.change_to('Document Browser');

  me.cur_menu_lst = me.menu_lists[mi.name];
  
}

