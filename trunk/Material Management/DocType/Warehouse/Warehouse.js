/*cur_frm.cscript.onload = function(doc,cdt,cdn){
  if(doc.__islocal!=1){
    cur_frm.cscript.auto_indent_mail(doc,cdt,cdn);
  }
}

cur_frm.cscript.auto_indent_mail = function(doc,cdt,cdn){
  if(doc.auto_indent_mail == 'Yes')
    unhide_field('email_id');  
  else{
    doc.email_id = '';
    refresh_field('email_id');
    hide_field('email_id');  
  }
}*/

$import(Tips Common)

//--------- ONLOAD -------------
cur_frm.cscript.onload = function(doc, cdt, cdn) {
  cur_frm.cscript.get_tips(doc, cdt, cdn);
}

cur_frm.cscript.refresh = function(doc, cdt, cdn) {
  cur_frm.cscript.get_tips(doc, cdt, cdn);
}

cur_frm.cscript['Get Report'] = function(doc,cdt,cdn) {
  var query = 
   'SELECT '+
   ' `tabBin`.`item_code`,'+
   ' `tabBin`.`actual_qty`,'+
   ' `tabBin`.`ordered_qty`,'+
   ' `tabBin`.`reserved_qty`,'+
   ' `tabBin`.`indented_qty`'+
   ' FROM '+
   ' `tabBin`'+
   ' WHERE '+
   ' `tabBin`.`warehouse` = "' + doc.name + '"'+
   'GROUP BY ' + 
   ' `tabBin`.`item_code`'
   ' ORDER BY '+
   ' `tabBin`.`item_code`';

  show_data_table('Output HTML', query, '500px');
}

cur_frm.cscript.country = function(doc, cdt, cdn) {
  var mydoc=doc;
  $c('runserverobj', args={'method':'check_state', 'docs':compress_doclist([doc])},
    function(r,rt){
      if(r.message) {
        var doc = locals[mydoc.doctype][mydoc.name];
        doc.state = '';
        get_field(doc.doctype, 'state' , doc.name).options = r.message;
        refresh_field('state');
      }
    }  
  );
}