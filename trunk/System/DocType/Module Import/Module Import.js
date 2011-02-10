cur_frm.cscript['Login'] = function() {
  var callback = function(r,rt) {
    cur_frm.cscript.make_modules_table(r.message);
  }

  $c_obj([cur_frm.doc], 'get_remote_modules', '', callback);
}

cur_frm.cscript.make_modules_table = function(ml) {

  // clear parent
  var w = get_field_obj('Module HTML').wrapper;
  if(w.module_list) w.module_list.innerHTML = '';
  else w.module_list = $a(w, 'div', '', {'margin':'8px 0px'} );

  // head
  var div = $a(w.module_list, 'div', '', {marginBottom:'8px', 'fontWeight':'bold', padding:'4px', backgroundColor:'#EEE'});
  div.innerHTML = "Select Modules to Import"

  // make table
  var t = make_table(w.module_list, ml.length, 2, '68%', ['20px', null], {padding: '4px'});

  // add data
  for(var i=0; i<ml.length; i++) {
    var c0 = $td(t,i,0);
    c0.chk = $a_input(c0, 'checkbox');
    c0.module_name = ml[i];
    $td(t,i,1).innerHTML = ml[i];
  }

  // import button
  var btn = $a(w.module_list, 'button','',{margin:'8px 0px'});
  $(btn).html('Import').click(function() { cur_frm.cscript.do_import(); });

  // log
  cur_frm.log_area = $a(w.module_list, 'div', '', {margin:'8px 0px', padding:'4px', backgroundColor:'#EEF'});

  cur_frm.module_tab = t;
}


//
cur_frm.cscript.do_import = function() {
  cur_frm.cur_row_idx = 0;
  cur_frm.log_area.innerHTML = '';
  cur_frm.cscript.do_next();
}

cur_frm.cscript.do_next = function() {
  // more rows?

  if (cur_frm.cur_row_idx < cur_frm.module_tab.rows.length) {
    for(var i=cur_frm.cur_row_idx; i<cur_frm.module_tab.rows.length; i++) {
      
      // checked?
      if($td(cur_frm.module_tab, i, 0).chk.checked) {
        cur_frm.cur_row_idx = i + 1;
        cur_frm.cscript.start_import($td(cur_frm.module_tab, i, 0).module_name);
        return;
      }
    }
  }
}

cur_frm.cscript.start_import = function(module) {
  cur_frm.log_area.innerHTML += '<b>Importing ' + module + '...</b><br>';
  var callback = function(r,rt) {
    cur_frm.log_area.innerHTML += replace_newlines(r.message) + '<br>';
    cur_frm.cscript.do_next();
  }
  $c_obj([cur_frm.doc], 'import_module', module, callback);
}