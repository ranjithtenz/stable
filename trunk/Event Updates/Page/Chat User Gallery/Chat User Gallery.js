// Chat User Gallery Page
pscript['onload_Chat User Gallery'] = function(){
	user_gallery = new ChatUserGallery();
	user_gallery.show($i('chat'));
	user_gallery.refresh();
}

//====================================================== Chat User Gallery ==============================================================
// class ChatUserGallery
ChatUserGallery = function(){
	this.wrapper = $a(null,'div','',{width:'300px', border:'1px solid #CCC', padding:'4px'});
}

// make user profiles
ChatUserGallery.prototype.make_profile = function(lst, frm){
	var me = this;
	
	if(lst && lst.length){
		for(i=0; i<lst.length;i++){
			var cp = new ChatUserProfile(me.wrapper);
			cp.set_profile(frm,lst[i][1], lst[i][0], lst[i][2],'');                     // from, display name, name, status, image
		}
	}
}

// refresh user gallery
ChatUserGallery.prototype.refresh = function(){
	var me = this;
	var callback = function(r,rt){
		var usr = r.message.usr;
		var on = r.message.on;
		var off = r.message.off;

		me.wrapper.innerHTML = '';

		me.make_profile(usr,'My Profile');
		me.make_profile(on,'Online Profile');
		me.make_profile(off,'Offline Profile');
		
		var fn = function(){ me.refresh(); }
		setTimeout(fn,10000);
	}

	$c_obj('Home Control','get_users','',callback,1);
}

// show chat user gallery
ChatUserGallery.prototype.show = function(parent){
	var me = this;
	if(me.wrapper.parentNode) me.wrapper.parentNode.removeChild(me.wrapper);
	parent.appendChild(me.wrapper);
}

//======================================================= Chat User Profile ====================================================
// class ChatUserProfile
ChatUserProfile = function(parent){
    this.wrapper = $a(parent,'div');
    
    var t = make_table(this.wrapper,1,2,'100%',['44px',null]);
    this.image = $a($td(t,0,0),'img','',{width:'40px', padding:'4px'});
    
    this.profile = $a($td(t,0,1),'div','',{padding:'4px'});
		
    this.nm = $a(this.profile,'span','',{color:'#0AB', fontSize:'12px'});

    var status_tbl = this.make_status(this.profile,'');
		this.status_bullet = status_tbl.ic;
		this.status = status_tbl.nm;
		$y(this.status, {color:'#888', cursor:'auto'});
}

// make status div
ChatUserProfile.prototype.make_status = function(parent){
	var me = this;
	var t = make_table(parent,1,2,null,['15px',null],{verticalAlign:'middle'});
	t.ic = $a($td(t,0,0),'div','status');
	t.nm = $a($td(t,0,1),'span','',{cursor:'pointer'});
	return t;
}

// make status option
ChatUserProfile.prototype.make_status_opts = function(){
	var me = this;
	
	me.status_opts = $a(me.profile,'div','',{padding:'4px', backgroundColor:'#FFD', marginTop:'4px'});
	$dh(me.status_opts);
		
	var lst = ['Available', 'Busy', 'Offline'];
	for(i=0; i<lst.length; i++){
		var st = me.make_status(me.status_opts);
		
		$y(st.ic, {backgroundColor:pscript.im_status[lst[i]]});
		
		st.nm.innerHTML = lst[i];
		st.nm.onclick = function(){ $(me.status_opts).slideToggle(); me.update_status(this.innerHTML); }
	}
}

// update status
ChatUserProfile.prototype.update_status = function(status){
	var me = this;
	
	var callback = function(r,rt){
		$y(me.status_bullet,{backgroundColor:pscript.im_status[status]});
		me.status.innerHTML = status;
	}
  
	$c_obj('Home Control','update_status',status,callback,1);
}

// set user profile
ChatUserProfile.prototype.set_profile = function(frm,usr_dn, usr_id, status, img){
	var me = this;

	// profile image
	me.image.src = 'images/ui/no_img/no_img_m.gif';
		
	// profile name
	me.nm.innerHTML = usr_dn;
	me.nm.id = usr_id;
	me.nm.dn = usr_dn;

	if(frm == 'My Profile'){
		$y(me.nm, {cursor:'auto'});
		$y(me.wrapper, {backgroundColor:'#DDF'});
		
		// set status
		var t = make_table(me.profile, 1, 2, null,[null, null], {paddingRight:'16px'});
		
    me.status_link = $a($td(t,0,0), 'span', 'link_type',{color:'#555', textDecoration:'underline',cursor:'pointer'});
    me.status_link.innerHTML = 'Set your status';
    me.status_link.onclick = function(){
    	$(me.status_opts).slideToggle();
    };
    
		me.make_status_opts();
	}
	else{
		$y(me.nm, {cursor:'pointer'});
		
		me.nm.onclick = function(){
			var wl = pscript.chat_windows;
			
			if(!pscript.window_exist(user, this.id)){
				pscript.make_chat_window(user, user_fullname, this.id, this.dn, '', '','');
			}
			else{
				for(i=0; i<wl.length; i++){
					if(wl[i].sender == this.id || wl[i].receiver == this.id){
						if(!wl[i].shown) wl[i].show();
					}
				}
			}
		}
	}
	
	$y(me.status_bullet,{backgroundColor:pscript.im_status[status]});
	this.status.innerHTML = status;
}