// -------------
// Menu Display
// -------------

cur_frm.cscript.issingle = function(doc, cdt, cdn) {
  if(doc.issingle)
    unhide_field('show_in_menu');
  else {
    doc.show_in_menu = 0;
    hide_field('show_in_menu');
    hide_field('parent_node');
    hide_field('Parent HTML');
    hide_field('Menu HTML');
    hide_field('menu_index');
    hide_field('smallicon');
  }
}

cur_frm.cscript.show_in_menu = function(doc, cdt, cdn) {
  if(doc.show_in_menu) {
    unhide_field('parent_node');
    unhide_field('Parent HTML');
    unhide_field('Menu HTML');
    unhide_field('menu_index');
    unhide_field('smallicon');
  } else {
    hide_field('parent_node');
    hide_field('Parent HTML');
    hide_field('Menu HTML');
    hide_field('menu_index');
    hide_field('smallicon');
  } 
}

// Attachment

cur_frm.cscript.allow_attach = function(doc, cdt, cdn) {
  if(doc.allow_attach) {
    unhide_field('max_attachments');
  } else {
    hide_field('max_attachments');
  }
}

cur_frm.cscript.onload = function(doc, cdt, cdn) {
  this.issingle(doc, cdt, cdn);
  this.allow_attach(doc, cdt, cdn);
  this.show_in_menu(doc, cdt, cdn);
}

cur_frm.cscript.validate = function(doc, cdt, cdn) {
  doc.server_code_compiled = null;
}