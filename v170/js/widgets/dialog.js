//
// Dialog
//

var cur_dialog;
var top_index=91;

function Dialog(w, h, title, content) {

	this.wrapper = $a(popup_cont, 'div', 'dialog_wrapper');
	this.w = w;
	this.h = h;

	$w(this.wrapper,w + 'px');
	
	this.head = $a(this.wrapper, 'div', 'dialog_head');
	this.body = $a(this.wrapper, 'div', 'dialog_body');
	
	this.make_head(title);
	if(content)this.make_body(content);

	this.onshow = '';
	this.oncancel = '';
	this.no_cancel_flag = 0; // allow to cancel
	this.display = false;
	var me = this;
}

Dialog.prototype.make_head = function(title) {
	var t = make_table(this.head,1,2,'100%',['100%','16px'],{padding:'2px'});
	
	//$y(t,{borderBottom:'1px solid #DDD'});
	$y($td(t,0,0),{paddingLeft:'16px',fontWeight:'bold',fontSize:'14px',textAlign:'center'});
	$y($td(t,0,1),{textAlign:'right'});	

	var img = $a($td(t,0,01),'img','',{cursor:'pointer'});
	img.src='images/icons/close.gif';
	this.title_text = $td(t,0,0);
	if(!title)title='';
	this.title_text.innerHTML = title;

	var me = this;
	img.onclick = function() {
		if(me.oncancel)me.oncancel();
		me.hide();
	}
	this.cancel_img = img;
}

Dialog.prototype.no_cancel = function() {
	$dh(this.cancel_img);
	this.no_cancel_flag = 1;	
}

Dialog.prototype.show = function() {
	// already live, do nothing
	if(this.display)
		return;

	// place it at the center
	var d = get_screen_dims();
	this.wrapper.style.left  = ((d.w - this.w)/2) + 'px';
	
	if(!cint(this.h)) {
		this.wrapper.style.top = '60px';
	} else {
		var t = (get_scroll_top() + ((d.h - this.h)/2));
		this.wrapper.style.top = (t<60 ? 60 : t) + 'px';
	}
	
	// place it on top
	top_index++;
	$y(this.wrapper,{zIndex:top_index});

	// show it
	$ds(this.wrapper);

	// hide background
	freeze();

	this.display = true;
	cur_dialog = this;

	// call onshow
	if(this.onshow)this.onshow();
}

Dialog.prototype.hide = function() {
	var me = this;
	unfreeze();
	if(this.onhide)this.onhide();
	$dh(this.wrapper);
	
	if(cur_autosug) cur_autosug.clearSuggestions();
	
	this.display = false;
	cur_dialog = null;
}

Dialog.prototype.set_title = function(title) { if(!title)title=''; this.title_text.innerHTML = title.bold(); }

Dialog.prototype.make_body = function(content) {
	this.rows = {}; this.widgets = {};
	for(var i in content) this.make_row(content[i]);
}

Dialog.prototype.clear_inputs = function(d) {
	for(var wid in this.widgets) {
		var w = this.widgets[wid];

		var tn = w.tagName ? w.tagName.toLowerCase() : '';
		if(tn=='input' || tn=='textarea') {
			w.value = '';
		} else if(tn=='select') {
			sel_val(w.options[0].value);
		} else if(w.txt) {
			w.txt.value = '';
		} else if(w.input) {
			w.input.value = '';
		}
	}
}

Dialog.prototype.make_row = function(d) {
	var me = this;
	
	this.rows[d[1]] = $a(this.body, 'div', 'dialog_row');
	var row = this.rows[d[1]];

	if(d[0]!='HTML') {
		var t = make_table(row,1,2,'100%',['30%','70%']);
		row.tab = t;
		var c1 = $td(t,0,0);
		var c2 = $td(t,0,1);
		if(d[0]!='Check' && d[0]!='Button')
			$t(c1, d[1]);
	}
	
	if(d[0]=='HTML') {
		if(d[2])row.innerHTML = d[2];
		this.widgets[d[1]]=row;
	} 
	else if(d[0]=='Check') {
		var i = $a_input(c2, 'checkbox','',{width:'20px'});
		c1.innerHTML = d[1];
		this.widgets[d[1]] = i;
	} 
	else if(d[0]=='Data') {
		c1.innerHTML = d[1];
		c2.style.overflow = 'auto';
		this.widgets[d[1]] = $a(c2, 'input');
		if(d[2])$a(c2, 'div', 'comment').innerHTML = d[2];
	} 
	else if(d[0]=='Link') {
		c1.innerHTML = d[1];
		var f = make_field({fieldtype:'Link', 'label':d[1], 'options':d[2]}, '', c2, this, 0, 1);
		f.not_in_form = 1;
		f.dialog = this;
		f.refresh();
		this.widgets[d[1]] = f.input;
	}
	else if(d[0]=='Date') {
		c1.innerHTML = d[1];
		var f = make_field({fieldtype:'Date', 'label':d[1], 'options':d[2]}, '', c2, this, 0, 1);
		f.not_in_form = 1;
		f.refresh();
		f.dialog = this;
		this.widgets[d[1]] = f.input;
	}
	else if(d[0]=='Password') {
		c1.innerHTML = d[1];
		c2.style.overflow = 'auto';
		this.widgets[d[1]] = $a_input(c2, 'password');
		if(d[3])$a(c2, 'div', 'comment').innerHTML = d[3];
		
	} 
	else if(d[0]=='Select') {
		c1.innerHTML = d[1];
		this.widgets[d[1]] = $a(c2, 'select', '', {width:'160px'})
		if(d[2])$a(c2, 'div', 'comment').innerHTML = d[2];
		if(d[3])add_sel_options(this.widgets[d[1]], d[3], d[3][0]);
	} 
	else if(d[0]=='Text') {
		c1.innerHTML = d[1];
		c2.style.overflow = 'auto';
		this.widgets[d[1]] = $a(c2, 'textarea');		
		if(d[2])$a(c2, 'div', 'comment').innerHTML = d[2];
	} 
	else if(d[0]=='Button') {
		c2.style.height = '32px';
		c2.style.textAlign = 'right';
		var b = $btn(c2, d[1], null, null, null, 1);
		b.dialog = me;
		if(d[2]) {
			b._onclick = d[2];
			b.onclick = function() { this._onclick(me); }
		}
		this.widgets[d[1]] = b;
	}
}

// Close dialog on Escape
keypress_observers.push(new function() {
	this.notify_keypress = function(e, kc) {
		if(cur_dialog && kc==27 && !cur_dialog.no_cancel_flag) 
			cur_dialog.hide();
	}
});
