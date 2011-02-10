pscript['onload_Personalize Page'] = function(){
	
	// header and toolbar
	var h = new PageHeader('personalize_h','Personalize','Personalize settings like company banner, print format header.');
	
	h.add_button('Save', function(){ pscript.save_personalize(); },1,'ui-icon-disk');
	
	// body
	var dv = $a('personalize_b','div','',{textAlign:'center'});
	
	pscript.f_lst = {};
  
  // Date format
  //pscript.make_date_format(dv);
  
  // company banner
  pscript.make_company_banner(dv);
  
  // letter head
  //pscript.make_letter_head(dv);

  if(!pscript.upload_obj){
    pscript.upload_obj = new pscript.UploadObj();
  }
  
  if(!pscript.html_obj){
    pscript.html_obj = new pscript.HtmlObj();
  }
}
  
// make table structure
pscript.make_pp_body = function(parent,lbl,desc){
  
  var p = $a(parent,'div','',{marginBottom:'20px'});	
	var t = make_table(p,1,3,'98%',[null,'38%','38%'],{textAlign:'left', marginRight:'20px'});

	// label
  var l = $a($td(t,0,0),'div','',{fontWeight:'14px', fontWeight:'bold', marginRight:'20px', width:'100%', textAlign:'right', verticalAlign:'middle'});
  l.innerHTML = lbl ? lbl : '';

	//desc
  var d = $a($td(t,0,2),'div','',{color:'#888', width:'100%', verticalAlign:'middle', marginLeft:'20px'});
  d.innerHTML = desc ? desc : '';
  
  var b = $a($td(t,0,1),'div','',{marginLeft:'20px', textAlign:'center'});
  return b;
}

// make radio options
pscript.make_pp_options = function(parent,nm,img_fld,html_fld){
  
	$y(parent,{marginLeft:'20px'});
	
  var img = $a(parent,'button','button','',{display:'inline'}); img.innerHTML = 'Upload Image';
  img.nm = nm; img.fld_nm = img_fld;
  img.onclick = function(){ pscript.upload_obj.show(this.nm, this.fld_nm); }
  
  var sep = $a(parent,'div','',{margin:'0px 10px', display:'inline'});
  sep.innerHTML = 'OR';
  
  var html = $a(parent,'button','button','',{display:'inline'}); html.innerHTML = 'Edit';
  html.nm = nm; html.fld_nm = html_fld;
  
  html.onclick = function(){ pscript.html_obj.show(this.nm, this.fld_nm); }
}

// make date format
pscript.make_date_format = function(parent){
  
  var lbl = 'Date Format';
  var desc = 'The date format will be used throughout this account.';
  
  var body = pscript.make_pp_body(parent,lbl,desc);
  
  var sel = $a(body,'select','',{width:'200px', textAlign:'center'});
  var lst = ['dd-mm-yyyy', 'dd/mm/yyyy', 'mm-dd-yyyy', 'mm/dd/yyyy', 'yyyy-mm-dd'];
		
  var cp = locals['Control Panel']['Control Panel'];
  if(cp['date_format']){ var def_df = cp['date_format']; }
  else{ var def_df =  'dd-mm-yyyy'; }
		
  add_sel_options(sel,lst, def_df);
  pscript.f_lst['date_format'] = sel;
}
  
// make company banner
pscript.make_company_banner = function(parent){
  var lbl = 'Company Banner';
  var desc = 'You can upload banner image of size 600 x 60 pixels(or less) else it will be resized to scale.<br><b>OR</b><br>You can edit.';

  var body = pscript.make_pp_body(parent,lbl,desc);
  
  // select if image or html
  pscript.make_pp_options(body,'banner_options','client_logo','client_name');
  
  pscript.pp_banner_div = $a(body,'div','',{margin:'8px 0px', width:'200px', overflow:'auto', textAlign:'center'});
  
  pscript.set_pp_banner();
}

// make letter head
pscript.make_letter_head = function(parent){
  var lbl = 'Letter Head';
  var desc = 'You can upload letter head image of size 600 x 60 pixels(or less)<br><b>OR</b><br>You can edit.<br><br>Letter head will be used in all your prints.';

  var body = pscript.make_pp_body(parent,lbl,desc);
  
  // select if image or html
  pscript.make_pp_options(body,'letter_head_options','letter_head_image','letter_head');
  
  pscript.pp_lh_div = $a(body,'div','',{margin:'8px 0px', width:'200px', overflow:'auto', textAlign:'center'});

  pscript.set_pp_lh();
}

// image upload div
pscript.UploadObj = function(){
  var me = this;
  
  var d = new Dialog(500,null,'Upload Image');
  
  d.make_body([
    ['HTML', 'upload_html']
  ])
  
	var dv = $a(d.widgets['upload_html'],'div');  
	dv.innerHTML = '<iframe id="ul_iframe" name="ul_iframe" src="blank1.html" style="width:100px; height:100px; border:0px"></iframe>';

	var dv = $a(d.widgets['upload_html'],'div');
	dv.innerHTML = '<form method="POST" enctype="multipart/form-data" action="'+outUrl+'" target="ul_iframe"></form>';

	var ul_form = dv.childNodes[0];
	
	var f_list = [];

	// file data
	var inp_fdata = $a_input($a(ul_form,'span'),'file',{name:'filedata'});
  
  var inp = $a_input($a(ul_form,'span'),'submit'); inp.value = 'Upload'; $y(inp,{width:'100px'});
	var inp_btn = $a_input($a(ul_form,'span'),'hidden',{name:'cmd'}); inp_btn.value = 'upload_many';
	var inp_opt = $a_input($a(ul_form,'span'),'hidden',{name:'form_name'});
  var inp_fld = $a_input($a(ul_form,'span'),'hidden',{name:'field_name'});
	var inp_host = $a_input($a(ul_form,'span'),'hidden',{name:'host'});
	var inp_acx = $a_input($a(ul_form,'span'),'hidden',{name:'acx'});

  this.obj = d;
  this.inp_opt = inp_opt;
  this.inp_fld = inp_fld;
  this.inp_fdata = inp_fdata;
	this.inp_host = inp_host;
	this.inp_acx = inp_acx;
  
  this.show = function(nm, fld_nm){
    me.inp_opt.value = nm;
    me.inp_fld.value = fld_nm;
    me.inp_fdata.value = '';
		me.inp_host.value = window.location.host;
		
		var cp = locals['Control Panel']['Control Panel'];
		me.inp_acx.value = cp['account_id'];

    me.obj.show();
  }
}

// html obj
pscript.HtmlObj = function(){
  var me = this;
  
  var d = new Dialog(500,null,'Edit');
  
  d.make_body([
    ['Text','HTML Header'],
    ['HTML','HTML Action']
  ]);
  
  this.obj = d;
  this.opt = '';
  this.fld = '';
  
  d.widgets['HTML Header'].id = "pp_html";
  this.ele = d.widgets['HTML Header'];
  
  this.show = function(nm,fld){
    me.opt = nm;
    me.fld = fld;
		
		var cp = locals['Control Panel']['Control Panel'];
		var fld_value = cp[fld] ? cp[fld] : '';
    
    if(me.is_tinymce){
			me.editor.setContent(fld_value);
    }else{
      me.ele.value = fld_value;
			me.ele.focus();
    }
    me.obj.show();
  }
  
  var dv = $a(d.widgets['HTML Action'],'div');
  var save = $a(dv,'button','button'); save.innerHTML = 'Save';
  
  save.onclick = function(){
    
    var html = me.is_tinymce ? strip(me.editor.getContent()) : strip(me.ele.value);

    if(me.opt == 'banner_options'){
      var banner_callback = function(r,rt){
        //me.obj.hide();
        pscript.set_pp_banner();
      }
      $c_obj('Personalize Page Control', 'set_banner', html, banner_callback);
    }
    else if(me.opt == 'letter_head_options'){
      var lh_callback = function(r,rt){
        me.obj.hide();
        pscript.set_pp_lh();
      }
      
      $c_obj('Personalize Page Control', 'set_letter_head', html, lh_callback);
    }
  }
  
  var cancel = $a(dv,'button','button'); cancel.innerHTML = 'Cancel';
  cancel.onclick = function(){
    me.obj.hide();
  }
  
  me.set_editor(1);
}

// set tinymce editor
pscript.HtmlObj.prototype.set_editor = function(is_tinymce){
  
  var me = this;

  if(is_tinymce){
    //loading tinymce files for first time
    if(!tinymce_loaded) {
      tinymce_loaded = 1;
      tinyMCE_GZ.init({
        themes : "advanced",
        plugins : "style,table",
        languages : "en",
        disk_cache : true
      }, function() { me.set_TinyMCE() });
    }else {
      me.set_TinyMCE();
    }
		me.is_tinymce = 1;
	}
	else{
		me.is_tinymce = 0;
	}
}

// set tinymce
pscript.HtmlObj.prototype.set_TinyMCE = function(){
  
  var me = this;
	var ele = me.ele;
  
  // make the editor
  tinyMCE.init({
    theme : "advanced",
    mode : "exact",
    elements: ele.id,
    plugins:"table,style,indicime",
    theme_advanced_toolbar_location : "top",
    theme_advanced_toolbar_align : "center",
    theme_advanced_statusbar_location : "bottom",
    extended_valid_elements: "div[id|dir|class|align|style]",

    // w/h
    width: '100%',
    height: '50px',

    // buttons
   /* theme_advanced_buttons1 : "bold,italic,underline,strikethrough,blockquote,|,forecolor,backcolor,bullist,numlist,|,undo,redo,|,image,code",*/

    theme_advanced_buttons1 : "save,newdocument,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull",
    theme_advanced_buttons2 : "formatselect,fontselect,fontsizeselect,|,indicime,indicimehelp",
    theme_advanced_buttons3 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,code,|,forecolor,backcolor",

    // callback function with editor instance.
    init_instance_callback : "editor_init_callback"
  });

  // set the editor (on callback)
  editor_init_callback = function(inst) {
    me.editor = tinyMCE.get(ele.id);
    me.editor.focus();
  }
}

// set banner
pscript.set_pp_banner = function(){
  var callback = function(r,rt){
    pscript.pp_banner_div.innerHTML = r.message;
  }
  $c_obj('Personalize Page Control','get_banner','',callback);
}

// set letter head
pscript.set_pp_lh = function(){
  var callback = function(r,rt){
    pscript.pp_lh_div.innerHTML = r.message;
  }
  
  $c_obj('Personalize Page Control','get_letter_head','',callback);
}

// pscript save personalize
pscript.save_personalize = function(){
	var args = {};
	args.date_format = pscript.f_lst['date_format'].value;
	
	var callback = function(r,rt){
		msgprint("Your settings has been saved, please reload page.")
	}
	$c_obj('Personalize Page Control','update_cp',docstring(args),callback);
}