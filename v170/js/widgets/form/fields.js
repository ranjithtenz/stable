// fields.js
//
// Fields are divided into 2 types
// 1. Standard fields are loaded with the libarary
// 2. Special fields are loaded with form.compressed.js
//
//
// + wrapper
// 		+ input_area
//		+ display_area
// ======================================================================================

var no_value_fields = ['Section Break', 'Column Break', 'HTML', 'Table', 'FlexTable', 'Button', 'Image'];
var codeid=0; var code_editors={};

function Field() {	}

Field.prototype.make_body = function() { 
	var ischk = (this.df.fieldtype=='Check' ? 1 : 0);
	
	// parent element
	if(this.parent)
		this.wrapper = $a(this.parent, 'div');
	else
		this.wrapper = document.createElement('div');

	this.label_area = $a(this.wrapper, 'div');
		
	// label
	if(this.with_label) {
		var t = make_table(this.label_area, 1, 3+ischk, null, [], {verticalAlign: 'middle', height: '20px'});
	
		this.label_span = $a($td(t,0,0+ischk), 'span', '', {marginRight:'4px', fontSize:'11px'})
	
		// help icon
		//this.help_icon = $a($td(t,0,1+ischk),'div','wn-icon ic-question',{cursor:'pointer', marginRight:'4px'}); $dh(this.help_icon);
		this.help_icon = $a($td(t,0,1+ischk),'img','',{cursor:'pointer', marginRight:'4px'}); $dh(this.help_icon);
		this.help_icon.src = 'images/icons/help.gif';
	
		// error icon
		this.label_icon = $a($td(t,0,2+ischk),'img','',{marginRight:'4px'}); $dh(this.label_icon);
		this.label_icon.src = 'images/icons/error.gif';

	} else {
		this.label_span = $a(this.label_area, 'span', '', {marginRight:'4px'})
		$dh(this.label_area);
	}

	// make the input areas
	if(ischk && !this.in_grid) {
		this.input_area = $a($td(t,0,0), 'div');
		this.disp_area = $a($td(t,0,0), 'div');
	} else {
		this.input_area = $a(this.wrapper, 'div');
		this.disp_area = $a(this.wrapper, 'div');
	}

	// apply style
	if(this.in_grid) { 
		if(this.label_area) $dh(this.label_area);
	} else {
		this.input_area.className = 'input_area';
		$y(this.wrapper,{marginBottom:'4px'})
	}

	if(this.onmake)this.onmake();
}

Field.prototype.set_label = function() {
	if(this.with_label && this.label_area && this.label!=this.df.label) { 
		this.label_span.innerHTML = this.df.label;this.label = this.df.label; 
	}

}

Field.prototype.set_comment = function() {
	var me = this;
	if(this.df.description) {
		if(this.help_icon) {
			$ds(this.help_icon);
			this.help_icon.title = me.df.description;
			$(this.help_icon).tooltip();
		} 
	} else {
		if(this.help_icon) 	$dh(this.help_icon);
	}
}

// Field Refresh
// --------------------------------------------------------------------------------------------

Field.prototype.get_status = function() {
	// if used in filters
	if(this.in_filter) this.not_in_form = this.in_filter;
	
	if(this.not_in_form) {
		return 'Write';
	}
		
	var fn = this.df.fieldname?this.df.fieldname:this.df.label;
	this.df = get_field(this.doctype, fn, this.docname);

	if(!this.df.permlevel) this.df.permlevel = 0;

	var p = this.perm[this.df.permlevel];
	var ret;

	// permission level
	if(cur_frm.editable && p && p[WRITE])ret='Write';
	else if(p && p[READ])ret='Read';
	else ret='None';

	// binary
	if(this.df.fieldtype=='Binary')
		ret = 'None'; // no display for binary

	// hidden
	if(cint(this.df.hidden))
		ret = 'None';

	// for submit
	if(ret=='Write' && cint(cur_frm.doc.docstatus) > 0) ret = 'Read';

	// allow on submit
	var a_o_s = cint(this.df.allow_on_submit);
	
	if(a_o_s && (this.in_grid || (this.frm && this.frm.not_in_container))) {
		a_o_s = null;
		if(this.in_grid) a_o_s = this.grid.field.df.allow_on_submit; // take from grid
		if(this.frm && this.frm.not_in_container) { a_o_s = cur_grid.field.df.allow_on_submit;} // take from grid
	}
	
	if(cur_frm.editable && a_o_s && cint(cur_frm.doc.docstatus)>0 && !this.df.hidden) {
		tmp_perm = get_perm(cur_frm.doctype, cur_frm.docname, 1);
		if(tmp_perm[this.df.permlevel] && tmp_perm[this.df.permlevel][WRITE])ret='Write';
	}

	return ret;
}


Field.prototype.refresh_mandatory = function() { 
	if(this.not_in_form)return;

	// mandatory changes
	if(this.label_area) {
		if(this.df.reqd) {
			this.label_area.style.color= "#d22";
			if(this.txt)$y(this.txt,{backgroundColor:"#FEE"});
			else if(this.input)$y(this.input,{backgroundColor:"#FEE"});
		} else {
			this.label_area.style.color= "#222";
			if(this.txt)$y(this.txt,{backgroundColor:"#FFF"});
			else if(this.input)$y(this.input,{backgroundColor:"#FFF"});
		}
	}
	this.set_reqd = this.df.reqd;
}

Field.prototype.refresh_display = function() {
	// from permission
	if(!this.set_status || this.set_status!=this.disp_status) { // status changed
		if(this.disp_status=='Write') { // write
			if(this.make_input&&(!this.input)) { // make input if reqd
				this.make_input();
				this.set_comment();
				if(this.onmake_input) this.onmake_input();
			}
			
			if(this.show) this.show()
			else { $ds(this.wrapper); }
			
			// input or content
			if(this.input) { // if there, show it!
				$ds(this.input_area);
				$dh(this.disp_area);
				if(this.input.refresh)this.input.refresh();
			} else { // no widget
				$dh(this.input_area);
				$ds(this.disp_area);
			}
		} else if(this.disp_status=='Read') { 
			
			// read
			if(this.show) this.show()
			else $ds(this.wrapper);

			$dh(this.input_area);
			$ds(this.disp_area);
			this.set_comment();

		} else { 
			
			// None - hide all
			if(this.hide) this.hide();
			else $dh(this.wrapper);
		}
		this.set_status = this.disp_status;
	}
}

Field.prototype.refresh = function() { 
	// get status
	this.disp_status = this.get_status();

	// if there is a special refresh in case of table, then this is not valid
	if(this.in_grid 
		&& this.table_refresh 
			&& this.disp_status == 'Write') 
				{ this.table_refresh(); return; }

	this.set_label();
	this.refresh_display();
	this.refresh_mandatory();
	this.refresh_label_icon();
	
	// further refresh
	if(this.onrefresh) this.onrefresh();
	if(this.input&&this.input.refresh) this.input.refresh(this.df);

	if(!this.not_in_form)
		this.set_input(_f.get_value(this.doctype,this.docname,this.df.fieldname));
}

Field.prototype.refresh_label_icon = function() {
	if(this.not_in_form)return;
	
	// mandatory
	if(this.label_icon && this.df.reqd) {
		var v = _f.get_value(this.doctype, this.docname, this.df.fieldname);
	 	if(is_null(v)) 
	 		$ds(this.label_icon);
	 	else 
	 		$dh(this.label_icon);
	} else { $dh(this.label_icon) }
}

// Set / display values
// --------------------------------------------------------------------------------------------

Field.prototype.set = function(val) {
	// not in form
	if(this.not_in_form)
		return;
		
	if((!this.docname) && this.grid) {
		this.docname = this.grid.add_newrow(); // new row
	}
	// cleanup ms word quotes
	if(in_list(['Data','Text','Small Text','Code'], this.df.fieldtype))
		val = clean_smart_quotes(val);
	
	var set_val = val;
	if(this.validate)set_val = this.validate(val);
	_f.set_value(this.doctype, this.docname, this.df.fieldname, set_val);
	this.value = val; // for return
}

Field.prototype.set_input = function(val) {
	this.value = val;
	if(this.input&&this.input.set_input) {
		if(val==null)this.input.set_input('');
		else this.input.set_input(val); // in widget
	}
	var disp_val = val;
	if(val==null) disp_val = ''; 
	this.set_disp(disp_val); // text
}

Field.prototype.run_trigger = function() {
	if(this.not_in_form) {
		return;
	}

	if(this.df.reqd && !is_null(this.get_value()))
		this.set_as_error(0);

	if(cur_frm.cscript[this.df.fieldname])
		cur_frm.runclientscript(this.df.fieldname, this.doctype, this.docname);

	cur_frm.refresh_dependency();
	this.refresh_label_icon();
}

Field.prototype.set_disp_html = function(t) {
	if(this.disp_area){
		this.disp_area.innerHTML = (t==null ? '' : t);
		if(t)this.disp_area.className = 'disp_area';
		if(!t)this.disp_area.className = 'disp_area_no_val';
	}
}

Field.prototype.set_disp = function(val) { 
	this.set_disp_html(val);
}

Field.prototype.set_as_error = function(set) { 
	if(this.in_grid || this.not_in_form) return;
	
	var w = this.txt ? this.txt : this.input;
	if(set) {
		$y(w, {border: '2px solid RED'});
		
	} else {
		$y(w, {border: '1px solid #888'});	
	}
}

// Show in GRID
// --------------------------------------------------------------------------------------------

// for grids (activate against a particular record in the table
Field.prototype.activate = function(docname) {
	this.docname = docname;
	this.refresh();

	if(this.input) {
		this.input.isactive = true;
		var v = _f.get_value(this.doctype, this.docname, this.df.fieldname);
		this.last_value=v;
		// set input value

		if(this.input.onchange && this.input.get_value && this.input.get_value() !=v) {
			if(this.validate)
				this.input.set_value(this.validate(v));
			else 
				this.input.set_value((v==null)?'':v);
			if(this.format_input)
				this.format_input();
		}
		
		if(this.input.focus){
			try{this.input.focus();} catch(e){} // IE Fix - Unexpected call???
		}
	}
	if(this.txt) {
		try{this.txt.focus();} catch(e){} // IE Fix - Unexpected call???
		this.txt.isactive = true;
		if(this.btn)this.btn.isactive = true;
		this.txt.field_object = this;
	}
}
// ======================================================================================

function DataField() { } DataField.prototype = new Field();
DataField.prototype.with_label = 1;
DataField.prototype.make_input = function() {
	var me = this;
	this.input = $a(this.input_area, 'input');

	if(this.df.fieldtype=='Password') {
		if(isIE) {
			this.input_area.innerHTML = '<input type="password">'; // IE fix
			this.input = this.input_area.childNodes[0];
		} else {
			this.input.setAttribute('type', 'password');
		}
	}

	this.get_value= function() {
		var v = this.input.value;
		if(this.validate)v = this.validate(v);
		return v;
	}

	this.input.name = this.df.fieldname;
	this.input.onchange = function() {
		if(!me.last_value)me.last_value='';
		if(me.validate)
			me.input.value = me.validate(me.input.value);
		me.set(me.input.value);
		if(me.format_input)
			me.format_input();
		if(in_list(['Currency','Float','Int'], me.df.fieldtype)) {
			if(flt(me.last_value)==flt(me.input.value)) {
				me.last_value = me.input.value;
				return; // do not run trigger
			}
		}
		me.last_value = me.input.value;
		me.run_trigger();
	}
	this.input.set_input = function(val) { 
		if(val==null)val='';
		me.input.value = val; 
		if(me.format_input)me.format_input();
	}
}
DataField.prototype.validate = function(v) {
	if(this.df.options == 'Phone') {
		if(v+''=='')return '';
		v1 = ''
		// phone may start with + and must only have numbers later, '-' and ' ' are stripped
		v = v.replace(/ /g, '').replace(/-/g, '').replace(/\(/g, '').replace(/\)/g, '');

		// allow initial +,0,00
		if(v && v.substr(0,1)=='+') {
			v1 = '+'; v = v.substr(1);
		}
		if(v && v.substr(0,2)=='00') {
			v1 += '00'; v = v.substr(2);
		} 
		if(v && v.substr(0,1)=='0') {
			v1 += '0'; v = v.substr(1);
		}
		v1 += cint(v) + '';
		return v1;
	} else if(this.df.options == 'Email') {
		if(v+''=='')return '';
		if(!validate_email(v)) {
			msgprint(this.df.label + ': ' + v + ' is not a valid email id');
			return '';
		} else
			return v;
	} else {
		return v;	
	}	
}

DataField.prototype.onrefresh = function() {
	if(this.input&&this.df.colour) {
		var col = '#'+this.df.colour.split(':')[1];
		$bg(this.input,col);
	}
}

// ======================================================================================

function ReadOnlyField() { } ReadOnlyField.prototype = new Field();
ReadOnlyField.prototype.with_label = 1;

// ======================================================================================

function HTMLField() { } HTMLField.prototype = new Field();
HTMLField.prototype.set_disp = function(val) { this.disp_area.innerHTML = val; }
HTMLField.prototype.set_input = function(val) { if(val) this.set_disp(val); }
HTMLField.prototype.onrefresh = function() { this.set_disp(this.df.options?this.df.options:''); }

// ======================================================================================

var datepicker_active = 0;

function DateField() { } DateField.prototype = new Field();
DateField.prototype.with_label = 1;
DateField.prototype.make_input = function() {

	var me = this;
	this.user_fmt = locals['Control Panel']['Control Panel'].date_format;
	if(!this.user_fmt)this.user_fmt = 'dd-mm-yy';

	this.input = $a(this.input_area, 'input');
	$(this.input).datepicker({
		dateFormat: me.user_fmt.replace('yyyy','yy'), 
		altFormat:'yy-mm-dd', 
		changeYear: true,
		beforeShow: function(input, inst) { 
			datepicker_active = 1 
		},
		onClose: function(dateText, inst) { 
			datepicker_active = 0 
			if(_f.cur_grid_cell)
				_f.cur_grid_cell.grid.cell_deselect();	
		}
	});
	
	var me = this;

	me.input.onchange = function() {
		if(me.not_in_form) return;
		// input as dd-mm-yyyy
		if(this.value==null)this.value='';

		me.set(dateutil.user_to_str(me.input.value));
		me.run_trigger();
	}
	me.input.set_input = function(val) {
		if(val==null)val='';
		else val=dateutil.str_to_user(val);
		me.input.value = val;
	}
	me.get_value = function() {
		return dateutil.str_to_user(me.input.value);
	}
}
DateField.prototype.set_disp = function(val) {
	var v = dateutil.str_to_user(val);
	if(v==null)v = '';
	this.set_disp_html(v);
}
DateField.prototype.validate = function(v) {
	if(!v) return;
	var me = this;
	this.clear = function() {
		msgprint ("Date must be in format " + this.user_fmt);
		me.input.set_input('');
		return '';
	}
	var t = v.split('-');
	if(t.length!=3) { return this.clear(); }
	else if(cint(t[1])>12 || cint(t[1])<1) { return this.clear(); }
	else if(cint(t[2])>31 || cint(t[2])<1) { return this.clear(); }
	return v;
};

// ======================================================================================

// for ensuring in AutoSuggest that 2 values are not set in quick succession due to un intentional event call
var _last_link_value = null;

// reference when a new record is created via link
function LinkField() { } LinkField.prototype = new Field();
LinkField.prototype.with_label = 1;
LinkField.prototype.make_input = function() { 
	var me = this;
	
	if(me.df.no_buttons) {
		this.txt = $a(this.input_area, 'input');
		this.input = this.txt;	
	} else {
		makeinput_popup(this, 'ic-zoom', 'ic-sq_next', 'ic-sq_plus');
	
		// setup buttons
		me.setup_buttons();

		me.onrefresh = function() {
			if(me.can_create && cur_frm.doc.docstatus==0) $ds(me.btn2);
			else $dh(me.btn2);
		}
	}


	me.txt.field_object = this;		
	// set onchange triggers
	me.set_onchange();
	me.input.set_input = function(val) {
		if(val==undefined)val='';
		me.txt.value = val;
	}

	me.get_value = function() { return me.txt.value; }

		
	// add auto suggest
	var opts = {
		script: '',
		json: true,
		maxresults: 10,
		link_field: me
	};
	this.as = new AutoSuggest(me.txt, opts);
	
}

LinkField.prototype.setup_buttons = function() { 
	var me = this;

	// magnifier - search
	me.btn.onclick = function() {
		selector.set(me, me.df.options, me.df.label);
		selector.show(me.txt);
	}

	// open
	if(me.btn1)me.btn1.onclick = function() {
		if(me.txt.value && me.df.options) { loaddoc(me.df.options, me.txt.value); }
	}	
	// add button - for inline creation of records
	me.can_create = 0;
	if((!me.not_in_form) && in_list(profile.can_create, me.df.options)) {
		me.can_create = 1;
		me.btn2.onclick = function() { 
			var on_save_callback = function(new_rec) {
				if(new_rec) {
					var d = _f.calling_doc_stack.pop(); // patch for composites
					
					locals[d[0]][d[1]][me.df.fieldname] = new_rec;
					me.refresh();
					
					if(me.grid)me.grid.refresh();
				}
			}
			_f.calling_doc_stack.push([me.doctype, me.docname]);
			new_doc(me.df.options, null, 1, on_save_callback, me.doctype, me.docname, me.frm.not_in_container); 
		}
	} else {
		$dh(me.btn2); $y($td(me.tab,0,2), {width:'0px'});
	}
}

LinkField.prototype.set_onchange = function() { 
	var me = this;
	me.txt.onchange = function() { 
		// check values are not set in quick succession due to un-intentional event call
		if(_last_link_value) return
			
		// not in form, do nothing
		if(me.not_in_form) return;
		
		// same value, do nothing
		if(cur_frm) {
			if(me.txt.value == locals[me.doctype][me.docname][me.df.fieldname]) { 
				me.set(me.txt.value); // one more time, grid bug?
				return; 
			}
		}
		
		if(me.as && me.as.ul) {
			// still setting value
		} else {
			me.set(me.txt.value);
			
			_last_link_value = me.txt.value;
			setTimeout('_last_link_value=null', 500);
			
			// deselect cell if in grid
			if(_f.cur_grid_cell)
				_f.cur_grid_cell.grid.cell_deselect();
			
			// run trigger if value is cleared
			if(!me.txt.value) {
				me.run_trigger();
				return;
			}

			// validate the value just entered
			var fetch = '';
			if(cur_frm.fetch_dict[me.df.fieldname])
				fetch = cur_frm.fetch_dict[me.df.fieldname].columns.join(', ');
				
			$c('webnotes.widgets.form.validate_link', {'value':me.txt.value, 'options':me.df.options, 'fetch': fetch}, function(r,rt) { 
				if(selector && selector.display) return; // selecting from popup
				
				if(r.message=='Ok') {
					me.run_trigger();
					
					// set fetch values
					if(r.fetch_values) me.set_fetch_values(r.fetch_values);
				} else {
					var astr = '';
					if(in_list(profile.can_create, me.df.options)) astr = repl('<br><br><span class="link_type" onclick="newdoc(\'%(dt)s\')">Click here</span> to create a new %(dtl)s', {dt:me.df.options, dtl:get_doctype_label(me.df.options)})
					msgprint(repl('error:<b>%(val)s</b> is not a valid %(dt)s.<br><br>You must first create a new %(dt)s <b>%(val)s</b> and then select its value. To find an existing %(dt)s, click on the magnifying glass next to the field.%(add)s', {val:me.txt.value, dt:get_doctype_label(me.df.options), add:astr})); 
					me.txt.value = ''; 
					me.set('');
				}
			});
			
		}
	}
}
LinkField.prototype.set_fetch_values = function(fetch_values) { 
	var fl = cur_frm.fetch_dict[this.df.fieldname].fields;
	for(var i=0; i< fl.length; i++) {
		locals[this.doctype][this.docname][fl[i]] = fetch_values[i];
		if(!this.grid) {
			refresh_field(fl[i]);
			
			// call trigger on the target field
			if(cur_frm.fields_dict[fl[i]]) // on main
				cur_frm.fields_dict[fl[i]].run_trigger();
		}
	}
	// refresh grid
	if(this.grid) this.grid.refresh();
}

LinkField.prototype.set_get_query = function() { 
	if(this.get_query)return;

	if(this.grid) {
		var f = this.grid.get_field(this.df.fieldname);
		if(f.get_query) this.get_query = f.get_query;
	}
}

LinkField.prototype.set_disp = function(val) {
	var t = null; 
	if(val)t = "<a href=\'javascript:loaddoc(\""+this.df.options+"\", \""+val+"\")\'>"+val+"</a>";
	this.set_disp_html(t);
}

// ======================================================================================

function IntField() { } IntField.prototype = new DataField();
IntField.prototype.validate = function(v) {
	if(isNaN(parseInt(v)))return null;
	return cint(v);
}; 
IntField.prototype.format_input = function() {
	if(this.input.value==null) this.input.value='';
}

// ======================================================================================

function FloatField() { } FloatField.prototype = new DataField();
FloatField.prototype.validate = function(v) {
	var v= parseFloat(v); if(isNaN(v))return null;
	return v;
};
FloatField.prototype.format_input = function() {
	if(this.input.value==null) this.input.value='';
}

// ======================================================================================

function CurrencyField() { } CurrencyField.prototype = new DataField();
CurrencyField.prototype.format_input = function() { 
	var v = fmt_money(this.input.value); 
	if(this.not_in_form) {
		if(!flt(this.input.value)) v = ''; // blank in filter
	}
	this.input.value = v;
}

CurrencyField.prototype.validate = function(v) { 
	if(v==null || v=='')
		return 0; 
	return flt(v,2); 
}
CurrencyField.prototype.set_disp = function(val) { 
	var v = fmt_money(val); 
	this.set_disp_html(v);
}
CurrencyField.prototype.onmake_input = function() {
	if(!this.input) return;
	this.input.onfocus = function() {
		if(flt(this.value)==0)this.select();
	}
}

// ======================================================================================

function CheckField() { } CheckField.prototype = new Field();
CheckField.prototype.with_label = 1;
CheckField.prototype.validate = function(v) {
	var v= parseInt(v); if(isNaN(v))return 0;
	return v;
}; 
CheckField.prototype.onmake = function() {
	this.checkimg = $a(this.disp_area, 'div');
	var img = $a(this.checkimg, 'img');
	img.src = 'images/ui/tick.gif';
	$dh(this.checkimg);
}

CheckField.prototype.make_input = function() { var me = this;
	this.input = $a_input(this.input_area,'checkbox');
	$y(this.input, {width:"16px", border:'0px', margin:'2px'}); // no specs for checkbox
	this.input.onchange = function() {
		me.set(this.checked?1:0);
		me.run_trigger();
	}
	if(isIE){
		this.input.onclick = this.input.onchange;
		$y(this.input, {margin:'-1px'});
	}
	this.input.set_input = function(v) {
		v = parseInt(v); if(isNaN(v)) v = 0;
		if(v) me.input.checked = true;
		else me.input.checked=false;
	}

	this.get_value= function() {
		return this.input.checked?1:0;
	}

}
CheckField.prototype.set_disp = function(val) {
	if (val){ $ds(this.checkimg); } 
	else { $dh(this.checkimg); }
}

// ======================================================================================


function TextField() { } TextField.prototype = new Field();
TextField.prototype.with_label = 1;
TextField.prototype.set_disp = function(val) { 
	this.disp_area.innerHTML = replace_newlines(val);
}
TextField.prototype.make_input = function() {
	var me = this; 
	
	if(this.in_grid)
		return; // do nothing, text dialog will take over
	
	this.input = $a(this.input_area, 'textarea');
	this.input.wrap = 'off';
	if(this.df.fieldtype=='Small Text')
		this.input.style.height = "80px";
	this.input.set_input = function(v) {
		me.input.value = v;
	}
	this.input.onchange = function() {
		me.set(me.input.value); 
		me.run_trigger();
	}
	this.get_value= function() {
		return this.input.value;
	}
}

// text dialog
var text_dialog;
function make_text_dialog() {
	var d = new Dialog(520,410,'Edit Text');
	d.make_body([
		['Text', 'Enter Text'],
		['Button', 'Update']
	]);
	d.widgets['Update'].onclick = function() {
		var t = this.dialog;
		t.field.set(t.widgets['Enter Text'].value);
		t.hide();
	}
	d.onshow = function() {
		this.widgets['Enter Text'].style.height = '300px';
		var v = _f.get_value(this.field.doctype,this.field.docname,this.field.df.fieldname);
		this.widgets['Enter Text'].value = v==null?'':v;
		this.widgets['Enter Text'].focus();
	}
	d.onhide = function() {
		if(_f.cur_grid_cell)
			_f.cur_grid_cell.grid.cell_deselect();
	}
	text_dialog = d;
}

TextField.prototype.table_refresh = function() {
	if(!this.text_dialog)
		make_text_dialog();
	text_dialog.set_title('Enter text for "'+ this.df.label +'"'); 
	text_dialog.field = this;
	text_dialog.show();
}


// Select
// ======================================================================================

function SelectField() { } SelectField.prototype = new Field();
SelectField.prototype.with_label = 1;
SelectField.prototype.make_input = function() { 
	var me = this;
	var opt=[];
	
	if(this.not_in_form && (!this.df.single_select)) {

		// multiple select
		this.input = $a(this.input_area, 'select');
		this.input.multiple = true;
		this.input.style.height = '4em';
		this.txt = this.input;
		this.input.lab = $a(this.input_area, 'div', {fontSize:'9px',color:'#999'});
		this.input.lab.innerHTML = '(Use Ctrl+Click to select multiple or de-select)'
	} else {

		// Single select
		this.input = new SelectWidget(this.input_area, [], '80%');	

		this.txt = this.input.inp;
		if(this.input.custom_select) {
			this.btn = this.input.btn;
			$y(this.input.wrapper, {marginLeft:'1px'});
		}
		
		// for reference
		this.txt.field_object = this;
		this.txt.fieldname = this.df.fieldname;

		this.txt.onchange = function() {
			if(me.validate)
				me.validate();
			me.set(me.txt.value);
			// IE grid disappears
			if(isIE && me.in_grid) {
				$dh(_f.cur_grid_cell.grid.wrapper);
				$ds(_f.cur_grid_cell.grid.wrapper);
			}
			
			me.run_trigger();
		}
	}

	// set as single (to be called from report builder)
	this.set_as_single = function() {
		this.input.multiple = false;
		this.input.style.height = null; // default
		$dh(this.input.lab)
	}
	
	// refresh options list
	this.refresh_options = function(options) {
		if(options)
			me.df.options = options;

		me.options_list = me.df.options?me.df.options.split('\n'):[];
		
		// add options
		empty_select(this.input);
		add_sel_options(this.input, me.options_list);
		
	}
	
	// refresh options
	this.onrefresh = function() {
		this.refresh_options();

		if(this.not_in_form) {
			this.input.value = '';
			return;
		}
		
		if(_f.get_value)
			var v = _f.get_value(this.doctype,this.docname,this.df.fieldname);
		else {
			if(this.options_list)
				var v = this.options_list[0];
			else
				var v = null;
		}
		this.input.set_input(v);
	}
	
	this.input.set_input=function(v) {
		if(!v) {
			if(!me.input.multiple) {
				if(me.docname) { // if called from onload without docname being set on fields
					if(me.options_list) {
						me.set(me.options_list[0]);
						me.txt.value = me.options_list[0];
					} else {
						me.txt.value = '';
					}
				}
			}
		} else {
			if(me.options_list && in_list(me.options_list, v)) {
				if(me.input.multiple) {
					for(var i=0; i<me.input.options.length; i++) {
						me.input.options[i].selected = 0;
						if(me.input.options[i].value && me.input.options[i].value == v)
							me.input.options[i].selected = 1;
					}
				} else {
					me.txt.value = v;
				}
			}
		}
	}
	this.get_value= function() {
		if(me.input.multiple) {
			var l = [];
			for(var i=0;i<me.input.options.length; i++ ) {
				if(me.input.options[i].selected)l[l.length] = me.input.options[i].value;
			}
			return l;
		} else {
			if(me.txt.options) {
				return sel_val(me.txt);
			}
			return me.txt.value;
		}
	}
	this.refresh();
}

// Time
// ======================================================================================

function TimeField() { } TimeField.prototype = new Field();
TimeField.prototype.with_label = 1;

TimeField.prototype.get_time = function() {
	return time_to_hhmm(sel_val(this.input_hr), sel_val(this.input_mn), sel_val(this.input_am));
}
TimeField.prototype.set_time = function(v) {	
	//show_alert(ret);
	ret = time_to_ampm(v);
	this.input_hr.inp.value = ret[0];
	this.input_mn.inp.value = ret[1];
	this.input_am.inp.value = ret[2];
}
TimeField.prototype.make_input = function() { var me = this;
	this.input = $a(this.input_area, 'div', 'time_field');
	
	var t = make_table(this.input, 1, 3, '200px');

	var opt_hr = ['1','2','3','4','5','6','7','8','9','10','11','12'];
	var opt_mn = ['00','05','10','15','20','25','30','35','40','45','50','55'];
	var opt_am = ['AM','PM'];

	this.input_hr = new SelectWidget($td(t,0,0), opt_hr, '60px');
	this.input_mn = new SelectWidget($td(t,0,1), opt_mn, '60px');
	this.input_am = new SelectWidget($td(t,0,2), opt_am, '60px');

	this.input_hr.inp.isactive = 1; this.input_mn.inp.isactive = 1; this.input_am.inp.isactive = 1;
	if(this.input_hr.btn) {
		this.input_hr.btn.isactive = 1; this.input_mn.btn.isactive = 1; this.input_am.btn.isactive = 1;
	}
	
	var onchange_fn = function() {
		me.set(me.get_time()); 
		me.run_trigger();
	}
	
	this.input_hr.inp.onchange = onchange_fn;
	this.input_mn.inp.onchange = onchange_fn;
	this.input_am.inp.onchange = onchange_fn;
	
	this.onrefresh = function() {
		var v = _f.get_value ? _f.get_value(me.doctype,me.docname,me.df.fieldname) : null;
		me.set_time(v);
		if(!v)
			me.set(me.get_time());
	}
	
	this.input.set_input=function(v) {
		if(v==null)v='';
		me.set_time(v);
	}

	this.get_value = function() {
		return this.get_time();
	}
	this.refresh();
}

TimeField.prototype.set_disp=function(v) {
	var t = time_to_ampm(v);
	var t = t[0]+':'+t[1]+' '+t[2];
	this.set_disp_html(t);
}

// ======================================================================================
// Used by date and link fields

function makeinput_popup(me, iconsrc, iconsrc1, iconsrc2) {
	me.input = $a(me.input_area, 'div');
	if(!me.not_in_form)
		$y(me.input, {width:'80%'});
		
	me.input.set_width = function(w) {
		$y(me.input, {width:(w-2)+'px'});
	}
	
	var tab = $a(me.input, 'table');
	me.tab = tab;
	
	$y(tab, {width:'100%', borderCollapse:'collapse', tableLayout:'fixed'});
	
	var c0 = tab.insertRow(0).insertCell(0);
	var c1 = tab.rows[0].insertCell(1);
	
	$y(c1,{width: '20px'});
	me.txt = $a($a($a(c0, 'div', '', {paddingRight:'8px'}), 'div'), 'input', '', {width:'100%'});

	me.btn = $a(c1, 'div', 'wn-icon ' + iconsrc, {width:'16px'});

	if(iconsrc1) // link
		me.btn.setAttribute('title','Search');
	else // date
		me.btn.setAttribute('title','Select Date');

	if(iconsrc1) {
		var c2 = tab.rows[0].insertCell(2);
		$y(c2,{width: '20px'});
		me.btn1 = $a(c2, 'div', 'wn-icon ' + iconsrc1, {width:'16px'});
		me.btn1.setAttribute('title','Open Link');
	}

	if(iconsrc2) {
		var c3 = tab.rows[0].insertCell(3);
		$y(c3,{width: '20px'});
		me.btn2 = $a(c3, 'div', 'wn-icon ' + iconsrc2, {width:'16px'});
		me.btn2.setAttribute('title','Create New');
		$dh(me.btn2);
	}
		
	if(me.df.colour)
		me.txt.style.background = '#'+me.df.colour.split(':')[1];
	me.txt.name = me.df.fieldname;

	me.setdisabled = function(tf) { me.txt.disabled = tf; }
}


var tmpid = 0;


// ======================================================================================

function make_field(docfield, doctype, parent, frm, in_grid, hide_label) { // Factory

	switch(docfield.fieldtype.toLowerCase()) {
		
		// general fields
		case 'data':var f = new DataField(); break;
		case 'password':var f = new DataField(); break;
		case 'int':var f = new IntField(); break;
		case 'float':var f = new FloatField(); break;
		case 'currency':var f = new CurrencyField(); break;
		case 'read only':var f = new ReadOnlyField(); break;
		case 'link':var f = new LinkField(); break;
		case 'date':var f = new DateField(); break;
		case 'time':var f = new TimeField(); break;
		case 'html':var f = new HTMLField(); break;
		case 'check':var f = new CheckField(); break;
		case 'text':var f = new TextField(); break;
		case 'small text':var f = new TextField(); break;
		case 'select':var f = new SelectField(); break;
		
		// form fields
		case 'code':var f = new _f.CodeField(); break;
		case 'text editor':var f = new _f.CodeField(); break;
		case 'button':var f = new _f.ButtonField(); break;
		case 'table':var f = new _f.TableField(); break;
		case 'section break':var f= new _f.SectionBreak(); break;
		case 'column break':var f= new _f.ColumnBreak(); break;
		case 'image':var f= new _f.ImageField(); break;
	}

	f.parent 	= parent;
	f.doctype 	= doctype;
	f.df 		= docfield;
	f.perm 		= frm.perm;
	if(_f)
		f.col_break_width = _f.cur_col_break_width;

	if(in_grid) {
		f.in_grid = true;
		f.with_label = 0;
	}
	if(hide_label) {
		f.with_label = 0;
	}
	if(frm)
		f.frm = frm;
	if(f.init) f.init();
	f.make_body();
	return f;
}

