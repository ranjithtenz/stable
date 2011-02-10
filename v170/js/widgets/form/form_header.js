_f.FrmHeader = function(parent) {
	var me = this;
	this.wrapper = $a(parent, 'div');

	this.page_head = new PageHeader(this.wrapper);
	//$y(this.page_head.wrapper, {marginBottom:'0px'});
	
	// doctype
	this.dt_area = $a(this.page_head.main_head, 'span', '', {fontSize:'18px', marginRight:'8px', fontWeight:'bold'})
	
	// name
	this.dn_area = $a(this.page_head.main_head, 'span', '', {fontSize:'14px', fontWeight:'normal', marginRight:'8px'})

	// timestamp
	this.timestamp_area = $a(this.page_head.main_head, 'span', '', {marginRight:'8px', cursfontWeight:'normal', cursor:'pointer', color:'#00B', fontSize:'11px', fontWeight:'normal', textDecoration:'underline', textShadow:'none'});
	this.timestamp_area.innerHTML = 'more info';
	
	// status
	this.status_area = $a(this.page_head.main_head, 'span', '', {marginRight:'8px', marginBottom:'2px', cursor:'pointer', textShadow:'none'})
}
_f.FrmHeader.prototype.show = function() {  $ds(this.wrapper); }
_f.FrmHeader.prototype.hide = function() {  $dh(this.wrapper); }

// toolbar buttons
// =======================================================================

_f.FrmHeader.prototype.refresh= function() {

	var me = this;
	var p = cur_frm.get_doc_perms();
	
	this.page_head.clear_toolbar();

	// Edit
	if(cur_frm.meta.read_only_onload && !cur_frm.doc.__islocal) {
		if(!cur_frm.editable)
				this.page_head.add_button('Edit', function() { 
					cur_frm.edit_doc();
				}, 1, 'ui-icon-document', 1
			);
		else
			this.page_head.add_button('Print View', function() { 
				cur_frm.is_editable[cur_frm.docname] = 0;				
				cur_frm.refresh(); }, 1, 'ui-icon-document' );	
	}

	
	// Save
	if(cur_frm.editable && cint(cur_frm.doc.docstatus)==0 && p[WRITE])
		this.page_head.add_button('Save', function() { cur_frm.save('Save');}, 1, 'ui-icon-disk',1);
	
	// Submit
	if(cint(cur_frm.doc.docstatus)==0 && p[SUBMIT] && (!cur_frm.doc.__islocal))
		this.page_head.add_button('Submit', function() { cur_frm.savesubmit(); }, 0, 'ui-icon-locked');

	// Update after sumit
	if(cint(cur_frm.doc.docstatus)==1 && p[SUBMIT]) {
		this.update_btn = this.page_head.add_button('Update', function() { cur_frm.saveupdate(); }, 1, 'ui-icon-disk', 1);
		if(!cur_frm.doc.__unsaved) $dh(this.update_btn);
	}
	
	// Cancel
	if(cint(cur_frm.doc.docstatus)==1  && p[CANCEL])
		this.page_head.add_button('Cancel', function() { cur_frm.savecancel() }, 0, 'ui-icon-closethick');

	// Amend
	if(cint(cur_frm.doc.docstatus)==2  && p[AMEND])
		this.page_head.add_button('Amend', function() { cur_frm.amend_doc() }, 0, 'ui-icon-scissors');

	// New
	if(in_list(profile.can_create, cur_frm.doctype)) {
		this.page_head.add_button('New', function() { new_doc() }, 0, 'ui-icon-document');
	}
	
	// Refresh
	this.page_head.add_button('Refresh', function() { cur_frm.reload_doc(); }, 0, 'ui-icon-refresh');
	
	// Print
	if(!cur_frm.meta.allow_print)
		this.page_head.add_button('Print', function() { cur_frm.print_doc(); }, 0, 'ui-icon-print');
	
	// Email
	if(!cur_frm.meta.allow_email)
		this.page_head.add_button('Email', function() { cur_frm.email_doc(); }, 0, 'ui-icon-mail-closed');
	
	// Copy
	if(in_list(profile.can_create, cur_frm.doctype) && !cur_frm.meta.allow_copy)
		this.page_head.add_button('Copy', function() { cur_frm.copy_doc(); }, 0, 'ui-icon-copy');

	// Trash
	if(cur_frm.meta.allow_trash && cint(cur_frm.doc.docstatus) != 2 && (!cur_frm.doc.__islocal) && p[CANCEL])
		this.page_head.add_button('Trash', function() { cur_frm.savetrash() }, 0, 'ui-icon-trash');	
	
	// add comment
	this.comment_btn = this.page_head.add_button('Comments', function() { cur_frm.show_comments(); }, 0, 'ui-icon-comment');
}

_f.FrmHeader.prototype.show_toolbar = function() { $ds(this.wrapper); this.refresh(); }
_f.FrmHeader.prototype.hide_toolbar = function() { $dh(this.wrapper); }

// refresh toolbar
// -------------------------------------------------------------------

_f.FrmHeader.prototype.refresh_toolbar = function() {
	var m = cur_frm.meta;
	
	if(m.hide_heading) { 
		// no heading... poof
		this.hide(); 
	} else {
		this.show();
		
		// with or without toolbar?
		if(m.hide_toolbar) { 
			this.hide_toolbar();
		} else {
			this.show_toolbar();
		}
	}
	this.refresh_comments();
}

_f.FrmHeader.prototype.refresh_comments = function() {
	if(!cur_frm.no_of_comments) cur_frm.no_of_comments = 0;
	if(this.comments_btn)
		this.comment_btn.innerHTML = 'Comments ('+cur_frm.no_of_comments+')';
}

// refresh heading and labels
// -------------------------------------------------------------------

_f.FrmHeader.prototype.get_timestamp = function(doc) {
	var scrub_date = function(d) {
		if(d)t=d.split(' ');else return '';
		return dateutil.str_to_user(t[0]) + ' ' + t[1];
	}
	
	return repl("Created: %(c_by)s %(c_on)s %(m_by)s %(m_on)s</span>", 
		{c_by:doc.owner
		,c_on:scrub_date(doc.creation ? doc.creation:'')
		,m_by:doc.modified_by?('<br> Modified: '+doc.modified_by):''
		,m_on:doc.modified ? ('on '+scrub_date(doc.modified)) : ''} );
}

// make the status tag
// -------------------------------------------------------------------

_f.FrmHeader.prototype.get_status_tags = function(doc, f) {

	var make_tag = function(label, col) {
		var s= $a(null, 'span', '', {padding: '2px', backgroundColor:col, color:'#FFF', fontWeight:'bold', marginLeft:(f.meta.issingle ? '0px' : '8px'), fontSize:'11px'});
		$(s).css('-moz-border-radius','3px').css('-webkit-border-radius','3px')
		s.innerHTML = label;
		return s;
	}

	var sp1 = null; var sp2 = null;
	if(doc.__islocal) {
		label = 'Unsaved Draft'; col = '#F81';

	} else if(doc.__unsaved) {
		label = 'Not Saved'; col = '#F81';
		if(doc.docstatus==1 && this.update_btn) $ds(this.update_btn);

	} else if(cint(doc.docstatus)==0) {
		label = 'Saved'; col = '#0A1';

		// if submittable, show it
		if(f.get_doc_perms()[SUBMIT]) {
			sp2 = make_tag('To Be Submitted', '#888');
		}

	} else if(cint(doc.docstatus)==1) {
		label = 'Submitted'; col = '#44F';

	} else if(cint(doc.docstatus)==2) {
		label = 'Cancelled'; col = '#F44';
	}

	sp1 = make_tag(label, col);
	this.set_in_recent(doc, col);

	return [sp1, sp2];
}

// refresh "recent" tag colour
// -------------------------------------------------------------------

_f.FrmHeader.prototype.set_in_recent = function(doc, col) {
	var tn = $i('rec_'+doc.doctype+'-'+doc.name);
	if(tn)
		$y(tn,{backgroundColor:col}); 
}


// refresh the labels!
// -------------------------------------------------------------------

_f.FrmHeader.prototype.refresh_labels = function(f) {
	var ph = this.page_head;
	
	// main title
	this.dt_area.innerHTML = get_doctype_label(f.doctype);
	
	// sub title
	this.dn_area.innerHTML = '';
	if(!f.meta.issingle)
		this.dn_area.innerHTML = f.docname;

	// get the doc
	var doc = locals[f.doctype][f.docname];
	
	// get the tags
	var sl = this.get_status_tags(doc, f)

	// add the tags
	var t = this.status_area;
	t.innerHTML = '';
	t.appendChild(sl[0]);
	if(sl[1])t.appendChild(sl[1]);

	// timestamp
	//var ts = $a(null, 'span', '', {fontSize:'11px'});
	new CustomTooltip(this.timestamp_area, this.get_timestamp(doc));
	//ph.tag_area.innerHTML = '';
	//ph.tag_area.appendChild(ts);
}