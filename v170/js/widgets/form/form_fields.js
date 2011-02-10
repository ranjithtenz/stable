//
// Form Input
// ======================================================================================

_f.ColumnBreak = function() {
	this.set_input = function() { };
}

_f.ColumnBreak.prototype.make_body = function() {
	if((!this.perm[this.df.permlevel]) || (!this.perm[this.df.permlevel][READ]) || this.df.hidden) {
		// no display
		return;
	}

	this.cell = this.frm.layout.addcell(this.df.width);
	$y(this.cell.wrapper, {padding: '8px'});
	_f.cur_col_break_width = this.df.width;

	var fn = this.df.fieldname?this.df.fieldname:this.df.label;
	// header
	if(this.df&&this.df.label){
		this.label = $a(this.cell.wrapper, 'div', 'columnHeading');
		this.label.innerHTML = this.df.label;
	}

}

_f.ColumnBreak.prototype.refresh = function(layout) {
	if(!this.cell)return; // no perm
	
	var fn = this.df.fieldname?this.df.fieldname:this.df.label;
	if(fn) {
		this.df = get_field(this.doctype, fn, this.docname);
	
		// hidden
		if(this.set_hidden!=this.df.hidden) {
			if(this.df.hidden)
				this.cell.hide();
			else
				this.cell.show();
			this.set_hidden = this.df.hidden;
		}
	}
}

// ======================================================================================

_f.SectionBreak = function() {
	this.set_input = function() { };
}

_f.SectionBreak.prototype.make_row = function() {
	this.row = this.frm.layout.addrow();
}

_f.SectionBreak.prototype.make_collapsible = function(head) {
	var me = this;

	var t = make_table($a(head,'div','',{padding:'4px 8px', borderBottom:'1px solid #AAA'}), 1,2, '100%', [null, '60px'], {verticalAlign:'middle'});
	$y(t,{borderCollapse:'collapse'});
		
	this.label = $a($td(t,0,0), 'div', 'sectionHeading');
	this.label.innerHTML = this.df.label?this.df.label:'';
	
	// indent
	$y(this.row.body, { margin:'8px' });

	// exp / collapse
	$y($td(t,0,1),{textAlign:'right'});
	this.exp_icon = $a($td(t,0,1),'div','wn-icon ic-rnd_br_up', {cssFloat:'right'});
	this.exp_icon.onclick = function() { 
		if(me.row.body.style.display.toLowerCase()=='none') me.exp_icon.expand(); 
		else me.exp_icon.collapse(); 
	}
	this.exp_icon.expand = function() { 
		$ds(me.row.body) 
		$ds(me.row.header.head.desc_area);
		me.exp_icon.className = 'wn-icon ic-rnd_br_up';
	}
	this.exp_icon.collapse = function() { 
		$dh(me.row.body) 
		$dh(me.row.header.head.desc_area);
		me.exp_icon.className = 'wn-icon ic-rnd_br_down';
	}
	$y(head,{padding:'2px', margin:'8px'});
		
	// callable functions
	this.collapse = this.exp_icon.collapse;
	this.expand = this.exp_icon.expand;

}

// ======================================================================================

_f.SectionBreak.prototype.make_simple_section = function(with_header, collapsible) {
	var head = $a(this.row.header, 'div', '', {margin:'8px', marginBottom: '8px'});
	this.row.header.head = head;
	var me = this;

	// colour
	var has_col = false;
	if(this.df.colour) {
		has_col = true;
		var col = this.df.colour.split(':')[1];
		if(col!='FFF') {			
			$y(this.row.sub_wrapper, { margin:'8px', padding: '0px' ,backgroundColor: ('#' + col)} );
		}
	}
	
	if(with_header) {
		if(collapsible) {
			if(this.df.label) {
				this.make_collapsible(head);
				
			} else if(!has_col) {
				// divider
				$y(head,{margin:'8px', borderBottom:'1px solid #AAA'});
			}
		} else {
			this.label = $a(head, 'div', 'sectionHeading', { margin:'0px'});
			this.label.innerHTML = this.df.label?this.df.label:'';
		}
	}

	// description
	if(this.df.description) {
		head.desc_area = $a(head, 'div', '', {margin:'0px', padding:'8px 0px', color:'#222', fontSize:'12px'});
		if(this.df.description.length > 240) {
			$($a(head.desc_area, 'div', 'comment')).html(replace_newlines(this.df.description.substr(0,240)) + '...');
			$($a(head.desc_area, 'div', 'link_type', {fontSize:'11px'})).html('more').click(function() { msgprint(me.df.description) });
		} else {
			$($a(head.desc_area, 'div')).html(replace_newlines(this.df.description));
		}
	}
}

// ======================================================================================

_f.SectionBreak.prototype.add_to_sections = function() {
	this.sec_id = this.frm.sections.length;
	this.frm.sections[this.sec_id] = this;
	this.frm.sections_by_label[this.df.label] = this;
}

_f.cur_sec_header = null;
_f.SectionBreak.prototype.make_body = function() {
	if((!this.perm[this.df.permlevel]) || (!this.perm[this.df.permlevel][READ]) || this.df.hidden) {
		// no display
		return;
	}
	var me = this;

	// header
	if(this.frm.meta.section_style=='Tabbed') {
		if(this.df.options!='Simple') {
			// IE full page ??
			
			this.make_row();
			this.add_to_sections();
			
			this.mytab = this.frm.tabs.add_tab(me.df.label, function() { me.frm.set_section(me.sec_id);});
			
			this.expand = function() { 
				this.row.show(); me.mytab.set_selected();

				this.refresh_footer();
				
				if(me.df.label && cur_frm.cscript[me.df.label] && (!me.in_filter))
					cur_frm.runclientscript(me.df.label, me.doctype, me.docname);
			}
			
			this.collapse = function() { 
				me.row.hide(); me.mytab.hide();
			}

			this.make_row();		
			
			this.make_simple_section(0, 0);
			if(!isIE) this.collapse();
		} else {
			this.row = this.frm.layout.addsubrow();
			this.make_simple_section(1, 1);
		}
	} else if(this.frm.meta.section_style=='Tray') {
		if(this.df.options!='Simple') {
			this.add_to_sections();
			
			this.tray_item = this.frm.tray.add_item(this.df.label, function() { me.frm.set_section(me.sec_id); }, 1);
			
			// expand and collapse the section
			this.collapse = function() { 
				me.row.hide();
				me.tray_item.collapse();
			}
			this.expand = function() {
				me.row.show(); 
				me.tray_item.show_as_expanded();
				
				_f.cur_sec_header = this.header;
				if(me.df.label && cur_frm.cscript[me.df.label] && (!me.in_filter))
					cur_frm.runclientscript(me.df.label, me.doctype, me.docname);

				this.refresh_footer();
			}
	
			this.make_row();
			this.make_simple_section(1, 0);
			if(!isIE)this.collapse();
		} else {
			this.row = this.frm.layout.addsubrow();
			this.make_simple_section(1, 1);
		}
	} else if(this.df){
		this.row = this.frm.layout.addrow();
		this.make_simple_section(1, 1);
	}	
}


// ======================================================================================

_f.SectionBreak.prototype.add_section_button = function(sec_id, east_or_west) {
	var btn = $a($td(this.frm.footer.tab, 0, 1), 'button','',{marginLeft:'4px', fontSize:'11px'});
	btn.innerHTML = this.frm.sections[sec_id].df.label;
	btn.sec_id = sec_id;
	btn.onclick = function() {
		cur_frm.set_section(this.sec_id);
	}
	$(btn).button({icons:{ primary: 'ui-icon-triangle-1-' + east_or_west }});
}

_f.SectionBreak.prototype.refresh_footer = function() {
	if(this.frm.footer) {

		// clear
		$td(this.frm.footer.tab, 0, 1).innerHTML = '';

		// make buttons
		if(in_list(['Tabbed', 'Tray'],this.frm.meta.section_style)) {
			if(this.sec_id>0) {
				this.add_section_button(this.sec_id-1, 'w');
			}
			if(this.sec_id<this.frm.sections.length-1) {
				this.add_section_button(this.sec_id+1, 'e');
			}
		}
	}
}

// ======================================================================================

_f.SectionBreak.prototype.refresh = function(layout) {
	var fn = this.df.fieldname?this.df.fieldname:this.df.label;

	if(fn)
		this.df = get_field(this.doctype, fn, this.docname);

	// hidden
	if(this.set_hidden!=this.df.hidden) {
		if(this.df.hidden) {
			if(this.frm.meta.section_style=='Tabbed') {
				$dh(this.mytab);
			} else if(this.tray_item)
				this.tray_item.hide();
			
			if(this.row)this.row.hide();
		} else {
			if(this.frm.meta.section_style=='Tabbed') {
				$di(this.mytab);
			} else if(this.tray_item)
				this.tray_item.show();

			if(this.expanded)this.row.show();
		}
		this.set_hidden = this.df.hidden;
	}
}

// Image field definition
// ======================================================================================

_f.ImageField = function() { this.images = {}; }
_f.ImageField.prototype = new Field();
_f.ImageField.prototype.onmake = function() {
	this.no_img = $a(this.wrapper, 'div','no_img');
	this.no_img.innerHTML = "No Image";
	$dh(this.no_img);
}

_f.ImageField.prototype.get_image_src = function(doc) {
	if(doc.file_list) {
		file = doc.file_list.split(',');
		// if image
		extn = file[0].split('.');
		extn = extn[extn.length - 1].toLowerCase();
		var img_extn_list = ['gif', 'jpg', 'bmp', 'jpeg', 'jp2', 'cgm',  'ief', 'jpm', 'jpx', 'png', 'tiff', 'jpe', 'tif'];

		if(in_list(img_extn_list, extn)) {
			var src = outUrl + "?cmd=downloadfile&file_id="+file[1];
		}
	} else {
		var src = "";
	}
	return src;
}
_f.ImageField.prototype.onrefresh = function() { 
	var me = this;
	if(!this.images[this.docname]) this.images[this.docname] = $a(this.wrapper, 'img');
	else $di(this.images[this.docname]);
	
	var img = this.images[this.docname]
	
	// hide all other
	for(var dn in this.images) if(dn!=this.docname)$dh(this.images[dn]);

	var doc = locals[this.frm.doctype][this.frm.docname];
	
	if(!this.df.options) var src = this.get_image_src(doc);
	else var src = outUrl + '?cmd=get_file&fname='+this.df.options+"&__account="+account_id + (__sid150 ? ("&sid150="+__sid150) : '');

	
	if(src) {
		$dh(this.no_img);
		if(img.getAttribute('src')!=src) img.setAttribute('src',src);
		canvas = this.wrapper;
		canvas.img = this.images[this.docname];
		canvas.style.overflow = "auto";
		$w(canvas, "100%");
	
		if(!this.col_break_width)this.col_break_width = '100%';
		var allow_width = cint(1000 * (cint(this.col_break_width)-10) / 100);

		if((!img.naturalWidth) || cint(img.naturalWidth)>allow_width)
			$w(img, allow_width + 'px');

	} else {
		$ds(this.no_img);
	}
}
_f.ImageField.prototype.set_disp = function (val) { }
_f.ImageField.prototype.set = function (val) { }

// ======================================================================================

_f.ButtonField = function() { };
_f.ButtonField.prototype = new Field();
_f.ButtonField.prototype.init = function() {
	this.prev_button = null;
	// if previous field is a button, add it to the same div!
	
	// button-set structure
	// + wrapper (1st button)
	// 		+ input_area
	//			+ button_area
	//			+ button_area
	//			+ button_area
	
	if(cur_frm && 
		cur_frm.fields[cur_frm.fields.length-1] &&
			cur_frm.fields[cur_frm.fields.length-1].df.fieldtype=='Button') {
				
		this.make_body = function() {
			this.prev_button = cur_frm.fields[cur_frm.fields.length-1];
			if(!this.prev_button.prev_button) {
				// first button, make the button area
				this.prev_button.button_area = $a(this.prev_button.input_area, 'span');
			}
			this.wrapper = this.prev_button.wrapper;
			this.input_area = this.prev_button.input_area;
			this.disp_area = this.prev_button.disp_area;
			
			// all buttons in the same input_area
			this.button_area = $a(this.prev_button.input_area, 'span');
		}
	}
}
_f.ButtonField.prototype.make_input = function() { var me = this;
	if(!this.prev_button) {
		$y(this.input_area,{marginTop:'4px', marginBottom: '4px'});
	}

	// make a button area for one button
	if(!this.button_area) this.button_area = $a(this.input_area, 'span','',{marginRight:'4px'});
	
	// make the input
	this.input = $btn(this.button_area, 
		me.df.label.substr(0,20) + ((me.df.label.length>20) ? '..' : ''), {width:'170px', fontWeight:'bold'}, null, 1)
	this.input.onclick = function() {
		this.set_disabled();
		if(cur_frm.cscript[me.df.label] && (!me.in_filter)) {			
			cur_frm.runclientscript(me.df.label, me.doctype, me.docname);
			this.set_enabled();
		} else {
			this.set_working();
			cur_frm.runscript(me.df.options, me);
		}
	}
}

_f.ButtonField.prototype.hide = function() { 
	$dh(this.button_area);
};

_f.ButtonField.prototype.show = function() { 
	$ds(this.button_area);
};


_f.ButtonField.prototype.set = function(v) { }; // No Setter
_f.ButtonField.prototype.set_disp = function(val) {  } // No Disp on readonly

// Table
// ======================================================================================

_f.TableField = function() { };
_f.TableField.prototype = new Field();
_f.TableField.prototype.make_body = function() {
	if(this.perm[this.df.permlevel] && this.perm[this.df.permlevel][READ]) {
		// add comment area
		if(this.df.description) {
			this.comment_area = $a(this.parent, 'div', 'comment', {padding:'0px 8px 8px 8px'});
			this.comment_area.innerHTML = this.df.description;
		}
		this.grid = new _f.FormGrid(this);
		if(this.frm)this.frm.grids[this.frm.grids.length] = this;
		this.grid.make_buttons();
	}
}

_f.TableField.prototype.refresh = function() {
	if(!this.grid)return;
	
	// hide / show grid
	var st = this.get_status();

	if(!this.df['default']) 
		this.df['default']='';

	this.grid.can_add_rows = false;
	this.grid.can_edit = false
	if(st=='Write') {
		if(cur_frm.editable && this.perm[this.df.permlevel] && this.perm[this.df.permlevel][WRITE]) {
			this.grid.can_edit = true;
			if(this.df['default'].toLowerCase()!='no toolbar')
				this.grid.can_add_rows = true;
		}
		if(cur_frm.editable 
			&& this.df.allow_on_submit 
				&& cur_frm.doc.docstatus == 1 
					&& this.df['default'].toLowerCase()!='no toolbar') {
				this.grid.can_add_rows = true;
				this.grid.can_edit = true;
		}
	}
	
	if(this.old_status!=st) {
		if(st=='Write') {
			// nothing
			this.grid.show();
		} else if(st=='Read') {
			this.grid.show();
		} else {
			this.grid.hide();
		}
		this.old_status = st; // save this if next time
	}

	this.grid.refresh();
}

_f.TableField.prototype.set = function(v) { }; // nothing
_f.TableField.prototype.set_input = function(v) { }; // nothing

// ==============================================================

_f.CodeField = function() { };
_f.CodeField.prototype = new Field();
_f.CodeField.prototype.make_input = function() {
	var me = this;
	$ds(this.label_area);
	this.label_area.innerHTML = this.df.label;
	this.input = $a(this.input_area, 'textarea','code_text',{fontSize:'12px'});
	this.myid = 'code-'+codeid;
	this.input.setAttribute('id',this.myid);
	codeid++;


	this.input.setAttribute('wrap', 'off');
	this.input.set_input = function(v) {
		if(me.editor) {
			me.editor.setContent(v); // tinyMCE
		} else {
			me.input.value = v;
			me.input.innerHTML = v;
		}
	}
	this.input.onchange = function() {
		if(me.editor) {
			me.set(me.editor.getContent()); // tinyMCE
		} else {
			me.set(me.input.value);
		}
		me.run_trigger();
	}
	this.get_value= function() {
		if(me.editor) {
			return me.editor.getContent(); // tinyMCE
		} else {
			return this.input.value;
		}
	}
	if(this.df.fieldtype=='Text Editor') {
		code_editors[me.df.fieldname] = me;
		if(!tinymce_loaded) {
			tinymce_loaded = 1;
			tinyMCE_GZ.init({
				strict_loading_mode: true,
				themes : "advanced",
				plugins : "style,table,indicime",
				languages : "en",
				disk_cache : true
			}, function() { me.setup_editor() });
		} else {
			this.setup_editor();
		}
	} else {
		$y(me.input, {fontFamily:'Courier, Fixed'});
	}
}
_f.CodeField.prototype.set_disp = function(val) {
	$y(this.disp_area, {width:'90%'})
	if(this.df.fieldtype=='Text Editor') {
		this.disp_area.innerHTML = val;
	} else {
		this.disp_area.innerHTML = '<textarea class="code_text" readonly=1>'+val+'</textarea>';
	}
}
_f.CodeField.prototype.setup_editor = function() {
	var me = this;
	// make the editor
	tinyMCE.init({
		theme : "advanced",
		mode : "none",
		//elements: me.myid,
		strict_loading_mode: true,
		plugins:"table,style,indicime",
		theme_advanced_toolbar_location : "top",
		theme_advanced_toolbar_align : "left",
		theme_advanced_statusbar_location : "bottom",
		extended_valid_elements: "div[id|dir|class|align|style]",

		// w/h
		width: '100%',
		height: '360px',

		// buttons
		theme_advanced_buttons1 : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect",
		theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,cleanup,help,code,|,forecolor,backcolor,|,indicime,indicimehelp",
		theme_advanced_buttons3 : "tablecontrols,styleprops,|,hr,removeformat,visualaid,|,sub,sup",

		// framework integation
		init_instance_callback : "code_editors."+ this.df.fieldname+".editor_init_callback",
		onchange_callback : "code_editors."+ this.df.fieldname+".input.onchange"
	});

	this.editor_init_callback = function() {
		if(cur_frm)
			cur_frm.fields_dict[me.df.fieldname].editor = tinyMCE.get(me.myid);
	}
	tinyMCE.execCommand("mceAddControl",false,me.myid);
	cur_frm.tinymce_id_list.push(me.myid);
}

// ======================================================================================

