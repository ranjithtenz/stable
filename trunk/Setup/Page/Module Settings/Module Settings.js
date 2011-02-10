// Module settings client

var _ms = {}

// Get all modules
pscript['onload_Module Settings'] = function() {

	var parent = $i('module_settings');
	parent.innerHTML = '';

	// page header
	new PageHeader(parent,'Module Settings');

	var wrapper = $a(parent,'div', '', {margin:'16px'});
	
	// comments
	var intro = $a(wrapper, 'div', '', {marginBottom:'16px', fontSize:'14px'});
	intro.innerHTML = 'Set the order of the modules side-bar and selectively show and hide modules. These changes will apply to all users!';

	var toolbar = $a(wrapper,'div','',{marginBottom:'16px'});
	_ms.make_action(toolbar);	

	// get modules
	_ms.mod_div = $a(wrapper,'div','',{width:'300px'});
	_ms.get_settings();
}

// get modules
_ms.get_settings = function(){

	var parent = _ms.mod_div;
	parent.innerHTML = '';
	add_space_holder(parent);

	var callback = function(r, rt){
		var ml = r.message;
		
		if(ml){
			remove_space_holder();
			_ms.make_ui(parent, ml);
		}
	}
	
	$c_obj('Home Control','get_settings','',callback);
}


// make ui
_ms.make_ui = function(parent, ml){

	_ms.mod_dict = {};
	_ms.mc_dict = {};
	_ms.len = ml.length - 1;
	
	for(i=0; i<ml.length; i++){
		var c = _ms.make_container(parent, i);
		_ms.make_module(c, ml[i], i);		
	}
}

// make action
_ms.make_action = function(parent){

	var t = make_table(parent,1,2,'100%',['200px',null]);
		
	var dv = $a($td(t,0,0),'div');

	// save btn
	var c = $a(dv,'div','green_buttons',{display:'inline'});
	_ms.save_btn = $a(c,'button','',{marginRight:'8px'});
	
	$(_ms.save_btn)
		.html('Save')
		.button({icons : {primary : 'ui-icon-disk'}})
		.click(function(){ _ms.save(); })

	// cancel btn
	_ms.cancel_btn = $a(dv,'button','',{marginRight:'30px'});
	
	$(_ms.cancel_btn)
		.html('Reset')
		.button({icons : {primary : 'ui-icon-arrowreturnthick-1-w'}})
		.click(function(){ _ms.cancel(); })
	
	// msg
	$y($td(t,0,1),{verticalAlign:'middle'});
	
	var msg = $a($td(t,0,1),'div');
	_ms.msg = $a(msg,'span','',{padding:'2px 6px', fontSize:'14px'});
}

// make container
_ms.make_container = function(parent, seq){

	var parent = $a(parent,'div','_ms_container');
	
	var t = make_table(parent,1,2,'100%',['10px',null],{verticalAlign:'middle'});
	
	$a($td(t,0,0),'h3').innerHTML = seq+1;
	
	_ms.mc_dict[seq] = parent;
	
	// container
	var c = $td(t,0,1);
	return c;
}

// class Module
_ms.make_module = function(parent, ml_dict, seq){
	
	var w = $a(parent, 'div','',{padding:'4px 8px'});
	w.id = ml_dict.name;
	w.is_hidden = ml_dict.is_hidden ? ml_dict.is_hidden : 'No';
	
	// label, move up - down, hide
	var t = make_table(w,1,6,'100%',['20px',null,'30px','30px','30px'],{marginRight:'30px', verticalAlign:'middle', textAlign:'center'});
	
	$y($td(t,0,0), {verticalAlign:'middle', textAlign:'left'});
	// icon
	icon = $a($td(t,0,0),'img','',{marginRight:'5px'});

	
	$y($td(t,0,1), {textAlign:'left'});
	
	// label	
	var lbl = $a($td(t,0,1),'h4');
	lbl.innerHTML = ml_dict.module_label;
	
	// up arrow
	w.up = $a($td(t,0,2),'div','wn-icon ic-arrow_top');
	w.up.seq = seq;
	
	w.up.onclick = function(){ _ms.move_up(this.seq); }
	
	if(seq == 0) $dh(w.up);
	
	// down arrow
	w.down = $a($td(t,0,3),'div', 'wn-icon ic-arrow_bottom');
	w.down.seq = seq;
	
	w.down.onclick = function(){ _ms.move_down(this.seq); }
	
	if(seq == _ms.len) $dh(w.down)
	
	//action

	// show
	var show = $a($td(t,0,4),'span','link_type');
	show.innerHTML = 'Show';
	show.icon = icon;
	show.parent = w;
		
	show.onclick = function(){
		this.parent.is_hidden = 'No';
		this.icon.src = 'images/icons/accept.gif';
		
		$dh(this);
		$ds(this.hide_link);
	}

	// hide
	var hide = $a($td(t,0,4),'span','link_type');
	hide.innerHTML = 'Hide';
	hide.icon = icon;
	hide.parent = w;
	
	hide.onclick = function(){
		this.parent.is_hidden = 'Yes';
		this.icon.src = 'images/icons/cancel.gif';
				
		$dh(this);
		$ds(this.show_link);
	}
	
	show.hide_link = hide;
	hide.show_link = show;
	
	if(ml_dict.is_hidden == 'Yes'){
		$ds(show); $dh(hide);
		icon.src = 'images/icons/cancel.gif';
	}
	else{
		$dh(show); $ds(hide);
		icon.src = 'images/icons/accept.gif';		
	}
	
	_ms.mod_dict[seq] = w;
	_ms.mc_dict[seq].mod = w;
}

// move up
_ms.move_up = function(seq){
	
	if(seq != 0){
		var new_seq = seq - 1;
		
		cur_wrapper = _ms.mod_dict[seq];
		prev_wrapper = _ms.mod_dict[new_seq];
		
		var cur_parent = cur_wrapper.parentNode;
		var new_parent = prev_wrapper.parentNode;
		
		cur_parent.removeChild(cur_wrapper);
		new_parent.removeChild(prev_wrapper);
		
		new_parent.appendChild(cur_wrapper);
		cur_parent.appendChild(prev_wrapper);
		
		prev_wrapper.seq = seq;
		prev_wrapper.up.seq = seq;
		prev_wrapper.down.seq = seq;
		_ms.mod_dict[seq] = prev_wrapper;
		
		_ms.set_enabled(prev_wrapper);
		
		cur_wrapper.seq = new_seq;
		cur_wrapper.up.seq = new_seq;
		cur_wrapper.down.seq = new_seq;
		_ms.mod_dict[new_seq] = cur_wrapper;
		
		_ms.set_enabled(cur_wrapper);
		
		$y(_ms.mc_dict[new_seq], {backgroundColor:'#ffd'});
		
		var fn = function(){ var tmp = _ms.mc_dict[new_seq]; $y(tmp, {backgroundColor:'#eef'}); }
		setTimeout(fn, 2000);
	}
	
}

// move down
_ms.move_down = function(seq){
	
	if(seq != _ms.len){
		var new_seq = seq + 1;

		cur_wrapper = _ms.mod_dict[seq];
		next_wrapper = _ms.mod_dict[new_seq];
		
		var cur_parent = cur_wrapper.parentNode;
		var new_parent = next_wrapper.parentNode;
		
		cur_parent.removeChild(cur_wrapper);
		new_parent.removeChild(next_wrapper);
		
		new_parent.appendChild(cur_wrapper);
		cur_parent.appendChild(next_wrapper);

		next_wrapper.seq = seq;
		next_wrapper.up.seq = seq;
		next_wrapper.down.seq = seq;		
		_ms.mod_dict[seq] = next_wrapper;

		_ms.set_enabled(next_wrapper);
		
		cur_wrapper.seq = new_seq;
		cur_wrapper.up.seq = new_seq;
		cur_wrapper.down.seq = new_seq;
		_ms.mod_dict[new_seq] = cur_wrapper;
		
		
		_ms.set_enabled(cur_wrapper);
		
		$y(_ms.mc_dict[new_seq], {backgroundColor:'#ffd'});
		
		
		var fn = function(){ var tmp = _ms.mc_dict[new_seq];	 $y(tmp, {backgroundColor:'#eef'}); }
		setTimeout(fn, 2000);
	}

}

// set enabled
_ms.set_enabled = function(mod){
  if(mod.seq == 0) $dh(mod.up)
  else $ds(mod.up)
  
  if(mod.seq == _ms.len) $dh(mod.down)
  else $ds(mod.down)
}

// save settings
_ms.save = function(){
	var args = {};
	
	for(d in _ms.mod_dict){
		args[_ms.mod_dict[d].id] = {'module_seq' : d, 'is_hidden' : _ms.mod_dict[d].is_hidden}
	}

	var callback = function(r,rt){
		if(!r.exc){
			_ms.msg.innerHTML = "Your settings have been saved, Refresh the page to see changes.";
			$y(_ms.msg,{backgroundColor:'#ffd'});
			
			var fn = function(){
				_ms.msg.innerHTML = '';
				$y(_ms.msg,{backgroundColor:'#fff'});
			}
			setTimeout(fn,3000);
		}
			//msgprint("Your settings have been saved.",1);
	}
	
	$c_obj('Home Control','set_settings', JSON.stringify(args), callback);
}

// cancel settings
_ms.cancel = function(){
	_ms.get_settings();
}