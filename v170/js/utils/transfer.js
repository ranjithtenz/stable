/*******
Account Login
*******/

var conn = {'src':{'user':'Administrator', 'path':'/v160', 'password':'admin', 'server':'localhost'}, 'tar':{'user':'Administrator', 'path':'/v160'}};
var acc_dialog;

function set_source() {
  if(!acc_dialog) {
    setup_acc_dialog();
    setup_transfer();
  }
  acc_dialog.type = 'src';
  acc_dialog.show();
}
function set_target() {
  if(!acc_dialog) {
    setup_acc_dialog();
  }
  acc_dialog.type = 'tar';
  acc_dialog.show();
}

function setup_transfer() {
	var sel = $i('trans_type');
	add_sel_options(sel,['Select','Module','Query'],'Select');
	sel.onchange = function() {
		if(sel_val(this)=='Module') {
			$ds('module_section'); $dh('query_section'); $dh('select_section');
		}
		else if(sel_val(this)=='Query') {
			$ds('query_section'); $dh('module_section'); $dh('select_section');
		}
		else if(sel_val(this)=='Select') {
			$ds('select_section'); $dh('query_section'); $dh('module_section');
		}
	}
}

function setup_acc_dialog() {
  acc_dialog = new Dialog(400,400,'Account Setup');
  acc_dialog.make_body([
		['Data', '*Server'],
		['HTML', 'Path Comment', '<div class="comment">Example: "72.55.168.105" or "www.kfcommunity.com"</div>'],
		['Data', 'Path'],
		['HTML', 'Path Comment', '<div class="comment">Example: "/v160"'],
		['Data', 'Account'],
		['Data', '*Admin Login'],
		['Password', '*Admin Password'],
		['Button', 'Set']
	]);
  acc_dialog.onshow = function() {
  	if(this.type=='tar')this.set_title('Setup Target');
  	if(this.type=='src')this.set_title('Setup Source');

	// show values
  	acc_dialog.widgets['*Server'].value = conn[acc_dialog.type].server ? conn[acc_dialog.type].server : '';
  	acc_dialog.widgets['Path'].value = conn[acc_dialog.type].path ? conn[acc_dialog.type].path : '';
  	acc_dialog.widgets['Account'].value = conn[acc_dialog.type].account ? conn[acc_dialog.type].account : '';
  	acc_dialog.widgets['*Admin Login'].value = conn[acc_dialog.type].user ? conn[acc_dialog.type].user : '';
  	acc_dialog.widgets['*Admin Password'].value = conn[acc_dialog.type].pwd ? conn[acc_dialog.type].pwd : '';
  }
  acc_dialog.widgets['Set'].onclick = function() {
    // validate
    if(!acc_dialog.widgets['*Server'].value) {
    	alert('Server is mandatory'); return
    }
    if(!acc_dialog.widgets['*Admin Login'].value) {
    	alert('Admin Login is mandatory'); return
    }
    if(!acc_dialog.widgets['*Admin Password'].value) {
    	alert('Admin Password is mandatory'); return
    }
  
  	conn[acc_dialog.type].server = acc_dialog.widgets['*Server'].value;
  	conn[acc_dialog.type].path = acc_dialog.widgets['Path'].value;
  	conn[acc_dialog.type].account = acc_dialog.widgets['Account'].value;
  	conn[acc_dialog.type].user = acc_dialog.widgets['*Admin Login'].value;
  	conn[acc_dialog.type].pwd = acc_dialog.widgets['*Admin Password'].value;
  	
	$i(acc_dialog.type+'_status').innerHTML = '<span style="color: BLUE">Logging in...</span>';
  	login(acc_dialog.type)
  	acc_dialog.hide();
  }
}

function login(t) {
	$c('acctr_get_sid', {
		'server': conn[t].server,
		'path': conn[t].path,
		'account': conn[t].account,
		'user': conn[t].user,
		'pwd': conn[t].pwd,
		}, function(r, rt) {
			if(r.exc)alert(rt);
			//alert(rt);
			if(r.sid) { 
				conn[t].sid = r.sid;
				conn[t].dbx = r.dbx ? r.dbx : '';
				conn[t].__account = r.__account;
				$i(t+'_status').innerHTML = '<span style="color: GREEN">Logged In</span>';
				$i(t+'_server').innerHTML = conn[t].server;
				$i(t+'_account').innerHTML = conn[t].account;
				conn[t].dt_list = r.dt_list;
				conn[t].moduledef_list = r.moduledef_list;
				show_doctypes(t);
				if(t=='tar') {
					// show transfer
					$ds('transfer_wrapper');
				}
			} else {
				$i(t+'_status').innerHTML = '<span style="color: RED">Error</span>';
				$i(t+'_server').innerHTML = conn[t].server;
				$i(t+'_account').innerHTML = conn[t].account;			
			}
		});
}

/*******
Show Doctypes
*******/

function show_doctypes(t) {

	// show target
	$ds('target_wrapper');

	// show select
	$ds(t+'_select_area');
	$ds(t+'_tools_area');
	$i(t+'_filter').value = '';

	var sel = $i(t+'_dtlist');

	if(conn[t].dt_list) {
		var dl = conn[t].dt_list.split('\n');
		add_sel_options(sel, dl);
	} else {
		alert("No DocTypes Found");
	}
	
	if(t=='src' && conn[t].moduledef_list) {
		var dl = conn[t].moduledef_list.split('\n');
		add_sel_options($i('trans_moduledef'), dl);
		$i('trans_moduledef').selectedIndex = 0;
	}
}

function show_dtlist(t, dt, do_not_clear, limit, no_system) {
	sys_dt = ['DocType', 'DocField', 'DocPerm', 'DocFormat', 'Print Format',
'Page', 'Page Role', 'Profile', 'Role', 'UserRole', 'Control Panel', 
'DefaultValue', 'Event', 'Event Role', 'Event User', 'ToDo Item', 'File Data',
'Announcement', 'Ticket', 'Module', 'Module Item', 'Module Role', 'Search Criteria'];
	sys_role = ['Administrator', 'System Manager', 'All'];
	sys_mod = ['Admin'];
	
	var fn = function(r, rt) {
		if(r.exc)alert(r.exc);
	
		var dl = [];	
		if(r.dt_list)
			dl = r.dt_list.split('\n');
		var tab = $i(t+'_dt_list');

		// del rows
		if(!do_not_clear && tab.rows) {
			while(tab.rows.length) tab.deleteRow(0);
			conn[t].chk_list = [];
		}

		// add new rows
		for(var i=0; i<dl.length; i++) {
			var allow=1;
			if(no_system && dt == 'DocType' && in_list(sys_dt, dl[i])) allow = 0;
			if(no_system && dt == 'Role' && in_list(sys_role, dl[i])) allow = 0;
			if(no_system && dt == 'Module' && in_list(sys_mod, dl[i])) allow = 0;
			if(allow) {
				var r = tab.insertRow(tab.rows.length);
				var c0 = r.insertCell(0);
	
				c0.style.width = '30px';
				if(t=='src') {
					var chk = $a(c0, 'input');
					chk.setAttribute('type', 'checkbox');
					chk.dt = dt;
					chk.dn = dl[i];
					conn[t].chk_list[conn[t].chk_list.length] = chk;
				}
				
				var c1 = r.insertCell(1);
				c1.innerHTML = dl[i];
				if(t=='src')$ds('src_dt_btn');
			}
		}
	}
	var dt = dt?dt:sel_val($i(t+'_dtlist'));
	$c('acctr_get_dtlist', {
		'sid':conn[t].sid
		,'dbx':conn[t].dbx
		,'server':conn[t].server
		,'__account':conn[t].__account
		,'dt':dt
		,'txt': $i(t+'_filter').value
		,'path':conn[t].path
		,'limit':limit?limit:''
		 }, fn);
}

function get_core() {
	show_dtlist('src','Search Criteria', 0, 500,1);
	setTimeout("show_dtlist('src','Page', 1, 500,1);",1000);
	setTimeout("show_dtlist('src','DocType', 1, 500,1);",2000);
	setTimeout("show_dtlist('src','Print Format', 1, 500,1);",3000);
	setTimeout("show_dtlist('src','Role', 1, 500,1);",4000);
}

function select_all() {
	for(var i=0; i < conn['src'].chk_list.length; i++) {
		conn['src'].chk_list[i].checked = 1;
	}
}

/*******
Transfer
*******/

var tlist = [];
function set_for_transfer() {
	var cl = conn['src'].chk_list;
	tlist = [];

	var tab = $i('trans_list');
	for(var i=0;i<cl.length;i++) {
		if(cl[i].checked) {
			var r = tab.insertRow(0);
			var c0 = r.insertCell(0);
			c0.style.width = '60%';
			var c1 = r.insertCell(1);
			c0.innerHTML = cl[i].dn + ' ('+cl[i].dt+')';
			tlist[tlist.length] = [cl[i].dt, cl[i].dn, c1, ''];
		}
		cl[i].checked = 0;
	}
	
	// show clear btn
	if(tlist) { $ds('clear_btn'); }
}

function clear_transfer() {
	var tab = $i('trans_list');
	// del rows
	if(tab.rows)
		while(tab.rows.length) tab.deleteRow(0);

	tlist = [];
	
	$i('trans_msg').innerHTML = '';
}

function single_transfer(dt, dn, cell, query, moduledef) {
	cell.innerHTML = 'Migrating...';
	args = {
			'src_server': conn['src'].server,
			'src_path': conn['src'].path,
			'src_sid': conn['src'].sid,
			'src_dbx': conn['src'].dbx,
			'src__account':conn['src'].__account,
			

			'tar_server': conn['tar'].server,
			'tar_path': conn['tar'].path,
			'tar_sid': conn['tar'].sid,
			'tar_dbx': conn['tar'].dbx,
			'tar__account':conn['tar'].__account,
			
			'ovr':($i('trans_ovr').checked ? 1 : 0),
			'ignore':($i('trans_ignore').checked ? 1 : 0),
			'onupdate':($i('trans_onupdate').checked ? 1 : 0)
		};
		
	if(dt) args.dt = dt;
	if(dn) args.dn = dn;
	if(query)args.query = query;
	if(moduledef)args.moduledef = moduledef;
	
	$c('acctr_do_transfer', args, function(r, rt) {
			if(r.exc)alert(r.exc);
			cell.innerHTML = r.message;
			if(dt)
				setTimeout('do_next_transfer()', 100);
		}
	);
}

var cancel = 0;
var tidx;
var in_transfer;
function do_next_transfer() {
	// completed
	if(tidx >= tlist.length) {
		//alert('Completed');
		$i('go_btn').innerHTML = 'Go';
		in_transfer = 0;
		return;
	}
	
	// cancelled
	if(cancel) {
		alert('Cancelled');
		$i('go_btn').innerHTML = 'Go';
		in_transfer = 0;
		return;
	}
	

	// 
	single_transfer(tlist[tidx][0], tlist[tidx][1], tlist[tidx][2]);
	tidx++;

}

function do_transfer() {
	if(in_transfer) {
		cancel = 1;
		$i('go_btn').innerHTML = 'Cancelling...';
		return;
	}
	// 
	if(sel_val($i('trans_type')) == 'Query') {
		$i('trans_msg').innerHTML = 'Sending Query...';
		single_transfer('', '', $i('trans_msg'), $i('trans_query').value);
	} else if(sel_val($i('trans_type')) == 'Module') {
		$i('trans_msg').innerHTML = 'Sending Module Def...';
		single_transfer('', '', $i('trans_msg'), '', sel_val($i('trans_moduledef')));
	} else {
		cancel = 0;
		tidx = 0;
		in_transfer = 1;
		$i('go_btn').innerHTML = 'Cancel';
		do_next_transfer();
	}
}

function clear_recycle_bin() {
}