// setup code

if(!cur_frm.fields_dict.html.input == 0) {
  // force initialization (to make the element)
  cur_frm.fields_dict.html.make_input();
  var myid = cur_frm.fields_dict.html.input.getAttribute("id");


  // make the editor
  tinyMCE.init({
    theme : "advanced",
    mode : "exact",
    elements: myid,
    plugins:"table,style",
    theme_advanced_toolbar_location : "top",
    theme_advanced_toolbar_align : "left",
    theme_advanced_statusbar_location : "bottom",

    // w/h
    width: '100%',
    height: '360px',

    // buttons
    theme_advanced_buttons1 : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect",
    theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,cleanup,help,code,|,forecolor,backcolor",
    theme_advanced_buttons3 : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,ltr,rtl",

    // framework integation
    init_instance_callback : "cur_frm.cscript.editor_init_callback",
    onchange_callback : "cur_frm.fields_dict.html.input.onchange"

  });

  // set the editor (on callback)
  cur_frm.cscript.editor_init_callback = function(inst) {
    cur_frm.fields_dict.html.editor = tinyMCE.get(cur_frm.fields_dict.html.input.getAttribute("id"));
  }
}
