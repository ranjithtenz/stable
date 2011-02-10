pscript['onload_My Company'] = function() {
	var wrapper = page_body.pages['My Company'];
	
	// body
	wrapper.head = new PageHeader(wrapper, 'Members');
	wrapper.body = $a(wrapper, 'div');
	wrapper.tab = make_table(wrapper.body, 1, 2, '100%', [200/8+'%',600/8+'%'], {paddingRight:'8px'});
	pscript.myc_make_toolbar(wrapper);
	pscript.myc_make_user_workflow(wrapper);
	pscript.myc_make_list(wrapper);
}

// ----------------------

pscript.myc_make_toolbar = function(wrapper) {
	if(has_common(['System Manager', 'Administrator'], user_roles)){
		wrapper.head.add_button('Add User', function() { wrapper.add_user(); })
		wrapper.head.add_button('Switch User', function() { wrapper.switch_user(); })
	}
}

// ----------------------

pscript.myc_make_user_workflow = function(wrapper) {
	wrapper.add_user = function() {	
		if(!wrapper.add_user_dialog) {
			var d = new Dialog(400,200,'Add User');
			d.make_body([
				['Data','Email Id'],['Data','First Name'],['Data','Last Name']
				,['Select','User Type','',['System User','Partner']],['Button','Add']
			]);
			d.onshow = function() {
				this.clear_inputs();
			}
			
			wrapper.add_user_dialog = d;
			d.widgets['Add'].onclick = function() {
				var me = this;
				arg={
					email_id: d.widgets['Email Id'].value
					,first_name: d.widgets['First Name'].value
					,last_name: d.widgets['Last Name'].value
					,user_type: d.widgets['User Type'].value
				}
				this.set_working();
				var callback = function() {
					me.done_working();
					wrapper.add_user_dialog.hide();
					wrapper.member_list.lst.run();
				}
				$c_obj('Company Control','add_user',JSON.stringify(arg),callback);
			}
		}
		wrapper.add_user_dialog.show();
	}
	wrapper.switch_user = function() {
	}
}

pscript.myc_make_list= function(wrapper) {
	wrapper.member_list = new MemberList(wrapper)
}

//=============================================

MemberList = function(parent) {
	this.profiles = {};
	this.role_objects = {};
	this.properties = {};
	
	this.list_wrapper = $a($td(parent.tab,0,0), 'div');
	this.profile_wrapper = $a($td(parent.tab,0,1), 'div');
	
	this.make_search();
	this.make_filters();
	this.make_list();
}

// ----------------------

MemberList.prototype.make_search = function() {
	var me = this;
	this.search_area = $a(this.wrapper, 'div', '', {textAlign:'center', padding:'8px'});
	this.search_inp = $a(this.search_area, 'input', '', {fontSize:'14px', width:'80%'});
	this.search_inp.set_empty = function() {
		this.value = 'Search'; $fg(this,'#888');
	}
	this.search_inp.onfocus = function() {
		$fg(this,'#000');
		if(this.value=='Search')this.value = '';
	}
	this.search_inp.onchange = function() {
		if(!this.value) this.set_empty();
	}
	this.search_inp.set_empty();
}

// ----------------------

MemberList.prototype.make_filters = function() {

}

// ----------------------

MemberList.prototype.make_list = function() {
	var me = this;
	this.lst_area = $a(this.list_wrapper, 'div');
	this.lst = new Listing('Profiles',1);
	this.lst.colwidths = ['100%'];
	this.lst.get_query = function() {
		var c1 = '';
		if(me.search_inp.value && me.search_inp.value != 'Search') {
			var c1 = repl(' AND (first_name LIKE "%(txt)s" OR last_name LIKE "%(txt)s")', {txt:'%s' + me.search_inp.value + '%'});
		}
		
		this.query = repl("SELECT distinct ifnull(name,''), ifnull(concat_ws(' ', first_name, last_name),''), ifnull(messanger_status,''), ifnull(gender,''), ifnull(file_list,''), ifnull(social_points,0), enabled from tabProfile where docstatus != 2 AND name not in ('Guest','Administrator') %(cond)s ORDER BY name asc",{cond:c1});
		this.query_max = repl("SELECT count(name) from tabProfile where docstatus != 2 AND name not in ('Guest','Administrator') %(cond)s",{cond:c1});
	}
	this.lst.make(this.lst_area);
	this.lst.show_cell= function(cell, ri, ci, d) {
		new MemberItem(cell, d[ri], me);
	}
	this.lst.run();
}

// -------------------

MemberList.prototype.refresh_toolbar = function() {
	var w = $td(this.tab,1,1);
	w.innerHTML = '';
	var me = this;
	
	if(this.uid == user) {
		$y(w,{margin:'6px 0px',borderTop:'1px solid #AAA',borderBottom:'1px solid #AAA'})
		var pwd_btn = $btn(w,'Change Password',function() { me.change_password() },{marginRight:'4px'})
	}
		
	if(has_common(['Administrator','System Manager'],user_roles)) {
		var roles_btn = $btn(w,'Set Roles',function() { me.show_roles() },{marginRight:'4px'});
		if(this.uid!=user)
			var delete_btn = $btn(w,'Delete User',function() { me.delete_user() });
	}
	
}

// -------------------

MemberList.prototype.change_password = function() {
	
}

// -------------------

MemberList.prototype.delete_user = function() {
	
}

// -------------------

MemberList.prototype.show_roles = function() {
	if(!this.role_objects[this.uid])
		this.role_objects[this.uid] = new RoleObj(this.uid);
	this.role_objects[this.uid].dialog.show();
}

// -------------------

MemberList.prototype.make_profile = function() {
	
	this.tab = make_table(this.profile_wrapper,3,2,'100%',['33%','66%'],{padding:'4px'});

	var lh = $td(this.tab,0,0);
	var rh = $td(this.tab,0,1);

	$y(lh,{textAlign:'right'});
	this.img = $a(lh,'img','',{width:'120px'});
	
	// change image link
	this.change_image_link = $a(lh, 'div', '', {display:'none', fontSize:'11px'});
	var span = $a(this.change_image_link, 'span', 'link_type');
	span.innerHTML = '[Change Image]';
	
	// headers
	this.name_area = $a(rh,'div','',{fontSize:'14px',fontWeight:'bold',marginBottom:'4px'});
	this.email_area = $a(rh,'div','',{fontSize:'11px',marginBottom:'4px',color:'#888'});

	this.status_area = $a(rh,'div','',{marginBottom:'4px'});
	this.status_span = $a(this.status_area,'span');
	this.designation_area = $a(rh,'div','',{marginBottom:'4px'});
	this.points_area = $a(rh,'div','',{fontSize:'28px',fontWeight:'bold',marginBottom:'4px',color:'#777'});
	
	// member properties
	this.properties['bio'] = new MemberProperty(this, 'Bio', 'bio');
	this.properties['interests'] = new MemberProperty(this, 'Interests', 'interests');
	this.properties['activities'] = new MemberProperty(this, 'Activities', 'activities');
}

// -------------------

MemberList.prototype.show_profile = function(uid, member_item) {
	this.uid = uid;
	this.member_item = member_item;

	$dh(this.profile_wrapper);

	if(!this.name_area) this.make_profile();
	if(locals['Profile'] && locals['Profile'][uid]) {
		this.render_profile(uid);
		return;
	}

	var me = this;
	var callback = function(r,rt) {
		me.render_profile(uid);
	}
	$c('webnotes.widgets.form.getdoc', {'name':uid, 'doctype':'Profile', 'user':user}, callback);	// onload

}

// -------------------

MemberList.prototype.render_profile = function(uid) {
	// set info
	var me = this;
	this.profile = locals['Profile'][uid];
	
	// name
	if(cstr(this.profile.first_name) || cstr(this.profile.last_name)) {
		this.name_area.innerHTML = cstr(this.profile.first_name) + ' ' + cstr(this.profile.last_name);
	} else {
		this.name_area.innerHTML = this.profile.name;
	}
	
	// email
	this.email_area.innerHTML = this.profile.name;

	this.refresh_status();
	
	// designation
	this.designation_area.innerHTML = cstr(this.profile.designation);
	this.points_area.innerHTML = cint(this.profile.social_points);
	
	$dh(this.change_image_link);
	if(uid==user) {
		$ds(this.change_image_link);
		this.change_image_link.onclick = function() { me.change_image(); }
	}
	
	this.refresh_image();
	this.refresh_toolbar();
	for(var key in this.properties)
		this.properties[key].refresh();

	$ds(this.profile_wrapper);
	$dh(this.member_item.working_img);
}

// -------------------

MemberList.prototype.refresh_image = function(img_id) {
	set_user_img(this.img, this.uid, null, img_id)
}

// -------------------

MemberList.prototype.refresh_status = function() {
	this.profile = locals['Profile'][this.uid]

	if(!this.profile.enabled) {
		$fg(this.name_area,'#999');
		$fg(this.member_item.name_link,'#999'); 
	} else {
		$fg(this.name_area,'#000');
		$fg(this.member_item.name_link,'#00F');
	}

	this.status_span.innerHTML = this.profile.enabled ? 'Enabled' : 'Disabled';

	// set styles and buttons
	if(has_common(['Administrator','System Manager'],user_roles)) {
		this.set_enable_button();
	}
}

// -------------------

MemberList.prototype.set_enable_button = function() {
	var me = this;
	var act = this.profile.enabled ? 'Disable' : 'Enable';
	
	if(this.status_button) {
		this.status_button.innerHTML = act;	
	} else {	
		// make the button
		this.status_button = $btn(this.status_area, act, function() {
			var callback = function(r,rt) {
				locals['Profile'][me.profile.name].enabled = cint(r.message);
				me.status_button.done_working();
				me.refresh_status();
			}
			this.set_working();
			$c_obj('Company Control',this.innerHTML.toLowerCase()+'_profile',me.profile.name,callback);
		}, {marginLeft:'8px'}, null, 1);
	}
	if(this.uid==user) $dh(this.status_button); else $di(this.status_button);
}

// -------------------

pscript.user_image_upload = function(fid) {
	msgprint('File Uploaded');
	var mlist = page_body.pages['My Company'].member_list;
	
	if(fid) {
		mlist.change_dialog.hide();
		mlist.refresh_image(fid);
	}
}

MemberList.prototype.change_image = function() {
	if(!this.change_dialog) {
	
		var d = new Dialog(400,200,'Set Photo');
		d.make_body([
			['HTML','wrapper']
		]);	
	
		var w = d.widgets['wrapper'];
		this.uploader = new Uploader(w, {thumbnail:'80px', server_obj:'Company Control', method:'update_profile_image'}, pscript.user_image_upload)
		this.change_dialog = d;
	}
	this.change_dialog.show();
}

//=============================================

MemberProperty = function(mlist, label, fieldname) {
	this.label = label;
	this.fieldname = fieldname;
	this.mlist = mlist;
	var me = this;
	
	this.tab = make_table(mlist.profile_wrapper,1,2,'100%',['33%','66%'],{padding:'4px',color:'#444',lineHeight:'1.4em'});
	$td(this.tab,0,0).innerHTML = label
	$y($td(this.tab,0,0), {textAlign:'right'});
	
	this.val_area = $a($td(this.tab,0,1),'div');
	
	this.edit_link = $a($a($td(this.tab,0,1), 'div'), 'span', 'link_type',{fontSize:'11px'});
	this.edit_link.innerHTML = '[Edit]';
	this.edit_link.onclick = function() { me.edit(); }
}

// -------------------

MemberProperty.prototype.refresh = function(val) {
	if(val)
		locals.Profile[this.mlist.uid][this.fieldname] = val;
	var val = locals.Profile[this.mlist.uid][this.fieldname];

	this.val_area.innerHTML = val ? replace_newlines(val) : '[Not updated]';
	$ds(this.val_area); $dh(this.btn); $dh(this.input);
	
	if(this.mlist.uid==user) 
		$ds(this.edit_link);
	else 
		$dh(this.edit_link);
}

// -------------------

MemberProperty.prototype.edit = function() {
	var me = this;
	if(!this.input) {
		this.input = $a($td(this.tab,0,1), 'textarea', '', {width:'80%', height:'200px'});
		this.btn = $btn($td(this.tab,0,1), 'Update', function() { me.update() }, {marginTop:'5px'}, '', 1);
	}
	$ds(this.input); $ds(this.btn); $dh(this.val_area); $dh(this.edit_link);
	this.input.value = cstr(locals.Profile[this.mlist.uid][this.fieldname]);
}

// -------------------

MemberProperty.prototype.update = function() {
	var me = this;
	this.btn.set_working();
	var callback = function(r,rt) {
		me.btn.done_working();
		me.refresh(r.message);
	}
	$c_obj('Company Control','update_profile_property', JSON.stringify({name:this.mlist.uid, fieldname:this.fieldname, value:this.input.value}), callback)
}

//=============================================

MemberItem = function(parent, det, mlist) {
	var me = this;
	this.det = det;
	this.tab = make_table(parent, 1,2,'100%', ['30%', '60%'], {padding:'4px'});
	
	// avatar
	this.img = $a($td(this.tab,0,0),'img','',{width:'40px'});
	set_user_img(this.img, det[0], null, 
		(det[4] ? det[4].split(NEWLINE)[0].split(',')[1] : ('no_img_' + (det[3]=='Female' ? 'f' : 'm'))));
	
	// name
	var div = $a($td(this.tab, 0, 1), 'div', '', {fontWeight: 'bold',padding:'2px 0px'});
	this.name_link = $a(div,'span','link_type');
	this.name_link.innerHTML = det[1] ? det[1] : det[0];
	this.name_link.onclick = function() {
		$ds(me.working_img);
		mlist.show_profile(me.det[0], me); 
	}
	if(!det[6]) { $fg(this.name_link,'#999'); }

	// "you" tag
	if(user==det[0]) {
		var span = $a(div,'span','',{backgroundColor:'#4AC',padding:'2px',color:'#FFF',fontSize:'11px',marginLeft:'4px'});
		$br(span,'3px');
		span.innerHTML = 'You'
	}
	
	var span = $a(div,'span');
	span.innerHTML = ' ('+cint(det[5])+')';
	
	// email id
	var div = $a($td(this.tab, 0, 1), 'div', '', {color: '#888', fontSize:'11px'});
	div.innerHTML = det[0];
	
	// status update
	var div = $a($td(this.tab, 0, 1), 'div', '', {color: '#444'});
	div.innerHTML = det[2];
	
	// working img
	var div = $a($td(this.tab, 0, 1), 'div');
	this.working_img = $a(div,'img','',{display:'none'}); 
	this.working_img.src = 'images/ui/button-load.gif';
	
	// show initial
	if(user==det[0]) me.name_link.onclick();
}

// ========================== Role object =====================================

pscript.all_roles = null;

RoleObj = function(profile_id){
	this.roles_dict = {};
	this.profile_id = profile_id;
	this.setup_done = 0;

	var d = new Dialog(500,500,'Assign Roles');
	d.make_body([
		['HTML','roles']
	]);
	
	this.dialog = d;
	this.make_role_body(profile_id);
	this.body.innerHTML = '<span style="color:#888">Loading...</span> <img src="images/ui/button-load.gif">'
	var me=this;

	d.onshow = function() {
		if(!me.setup_done)
			me.get_all_roles(me.profile_id);
	}
}

// make role body
RoleObj.prototype.make_role_body = function(id){
	var me = this;
	var d = this.dialog;
	this.role_div = $a(d.widgets['roles'],'div');
	
	this.head = $a(this.role_div,'div','',{marginLeft:'4px', marginBottom:'4px',fontWeight:'bold'});
	this.body = $a(this.role_div,'div');
	this.footer = $a(this.role_div,'div');
	
	this.update_btn = $btn(this.footer,'Update',function() { me.update_roles(me.profile_id); },{marginRight:'4px'},'',1);	
}

// get all roles
RoleObj.prototype.get_all_roles = function(id){
	if(pscript.all_roles) {
		this.make_roles(id);
		return;
	}

	var me = this;
	var callback = function(r,rt){
		pscript.all_roles = r.message;
		me.make_roles(id);
	}
	$c_obj('Company Control','get_all_roles','',callback);
}

// make roles
RoleObj.prototype.make_roles = function(id){
	var me = this;
	var list = pscript.all_roles;
	me.setup_done = 1;
	me.body.innerHTML = '';
		
	var tbl = make_table( me.body, cint(list.length / 2) + 1,4,'100%',['5%','45%','5%','45%'],{padding:'4px'});
	var in_right = 0; var ridx = 0;

	for(i=0;i<list.length;i++){
		var cidx = in_right * 2;
		
		me.make_checkbox(tbl, ridx, cidx, list[i]);
		me.make_label(tbl, ridx, cidx + 1, list[i]);

		// change column
		if(in_right) {in_right = 0; ridx++ } else in_right = 1;
	}
	me.get_user_roles(id);
}

// make checkbox
RoleObj.prototype.make_checkbox = function(tbl,ridx,cidx, role){
	var me = this;
	
	var a = $a_input($a($td(tbl, ridx, cidx),'div'),'checkbox');
	a.role = role;
	me.roles_dict[role] = a;
	
	$y(a,{width:'20px'});
	$y($td(tbl, ridx, cidx),{textAlign:'right'});
}


// make label
RoleObj.prototype.make_label = function(tbl, ridx, cidx, role){
	var me = this;
	
	var t = make_table($td(tbl, ridx, cidx),1,2,null,['16px', null],{marginRight:'5px'});
	$td(t,0,1).innerHTML= role;
}

// get user roles
RoleObj.prototype.get_user_roles = function(id){
	var me = this;
	me.head.innerHTML = 'Roles for ' + id;
	
	$ds(me.role_div);
	$dh(me.help_div);
	
	var callback = function(r,rt){
			me.set_user_roles(r.message);
	}
	$c_obj('Company Control','get_user_roles', id,callback);
}


// set user roles
RoleObj.prototype.set_user_roles = function(list){
	var me = this;
	for(d in me.roles_dict){
		me.roles_dict[d].checked = 0;
	}
	for(l=0; l<list.length; l++){
		me.roles_dict[list[l]].checked = 1;
	}
}


// update roles
RoleObj.prototype.update_roles = function(id){
	var me = this;
	
	if(me.roles_dict['Administrator'].checked){
		var c = confirm("You have assigned Administrator role to this profile.\nThis profile will have acess to core functionality and will be able to change it.\n\nDo you want to continue anyway?")
		if(!c) return;
	}
	
	if(id == user && has_common(['System Manager'], user_roles) && !me.roles_dict['System Manager'].checked){
		var callback = function(r,rt){
			if(r.message){
				if(r.message > 1){
					var c = confirm("You have unchecked the System Manager role.\nYou will lose administrative rights and will not be able to set roles.\n\nDo you want to continue anyway?");
					if(!c) return;
				}
				else{
					var c = "There should be atleast one user with System Manager role.";
					me.roles_dict['System Manager'].checked = 1;
				}
			}
			me.set_roles(id);
		}
		$c_obj('Company Control','get_sm_count','',callback);
	}
	else{
		me.set_roles(id);
	}
}

// set roles
RoleObj.prototype.set_roles = function(id){

	var me = this;
	var role_list = [];
	
	for(d in me.roles_dict){
		if(me.roles_dict[d].checked){
			role_list.push(d);
		}
	}

	var callback = function(r,rt){
		me.update_btn.done_working();
		me.dialog.hide();
	}
	var arg = {'usr':id, 'role_list':role_list};
	me.update_btn.set_working();
	$c_obj('Company Control','update_roles',docstring(arg), callback);

}

//=============================================

// Remove User Object
// ---------------------------------------------------------------------------------------------
RemoveUserObj = function(uid){
	var me = this;

	var callback = function(r, rt){
		if(r.message){		
			var d = new Dialog(400,100,'Remove Users');
		
			d.make_body([['HTML', 'remove_user_div']]);
			me.dialog = d;
			var src = 'https://'+r.message+'/index.cgi?usr='+uid+'&acc='+locals['Control Panel']['Control Panel'].account_id+'#Page/Remove User';
			$a(d.widgets['remove_user_div'],'div').innerHTML = '<iframe src = "'+src+'" width = "100%" height = "100px" style = "border: 0px solid #ffffff"></iframe>';
			me.dialog.show();
			me.dialog.onhide = function(){global_search_object.search();}
		}
		else{
			msgprint("To use this feature for first time please logout and login again in your system");
			return;
		}
	}
	$c_obj('Company Control','get_login_url','',callback);
}

// Switch user Obj
// -------------------
SwitchUserObj = function(){
	var me = this;
	var callback = function(r, rt){
		if(r.message){		
			var d = new Dialog(450,200,'Switch User');
			d.make_body([['HTML', 'switch_user_div']]);
			me.dialog = d;
			var src = 'https://'+r.message+'/index.cgi?acc='+locals['Control Panel']['Control Panel'].account_id+'#Page/Switch User';
			$a(d.widgets['switch_user_div'],'div').innerHTML = '<iframe src = "'+src+'" width = "100%" height = "150px" style = "border: 0px solid #ffffff"></iframe>';
			me.dialog.show();
			me.dialog.onhide = function(){global_search_object.search();}
		}
		else{
			msgprint("To use this feature for first time please logout and login again in your system");
			return;
		}
	}
	$c_obj('Company Control','get_login_url','',callback);
}