//168
// Refresh
// --------
cur_frm.cscript.refresh = function(doc, cdt, cdn) {
  if(!doc.__islocal) get_field(doc.doctype, 'dt' , doc.name).permlevel = 1;
  cur_frm.cscript.dt(doc, cdt, cdn);
}


cur_frm.cscript.has_special_chars = function(t) {
  var iChars = "!@#$%^&*()+=-[]\\\';,./{}|\":<>?";
  for (var i = 0; i < t.length; i++) {
    if (iChars.indexOf(t.charAt(i)) != -1) {
      return true;
    }
  }
  return false;
}


// Label
// ------
cur_frm.cscript.label = function(doc){
  if(doc.label && cur_frm.cscript.has_special_chars(doc.label)){
    cur_frm.fields_dict['Label Help'].disp_area.innerHTML = '<font color = "red">Special Characters are not allowed</font>';
    doc.label = '';
    refresh_field('label');
  }
  else
    cur_frm.fields_dict['Label Help'].disp_area.innerHTML = '';
}


// Get Field Label based on DocType
// ---------------------------------
cur_frm.cscript.dt = function(doc, cdt, cdn) {
  var callback = function(r, rt){
    
    set_field_options('insert_after', r.message);
  }
  $c_obj([doc], 'get_fields_label', '', callback);
}


cur_frm.fields_dict['dt'].get_query = function(doc, dt, dn) {
  return 'SELECT tabDocType.name FROM tabDocType WHERE IFNULL(tabDocType.issingle,0)=0 AND tabDocType.name LIKE "%s" ORDER BY name ASC LIMIT 50'
}


cur_frm.cscript.fieldtype = function(doc, dt, dn) {
  if(doc.fieldtype == 'Link') cur_frm.fields_dict['Options Help'].disp_area.innerHTML = 'Please enter name of the document you want this field to be linked to in <b>Options</b>.<br> Eg.: Customer';
  else if(doc.fieldtype == 'Select') cur_frm.fields_dict['Options Help'].disp_area.innerHTML = 'Please enter values in <b>Options</b> separated by enter. <br>Eg.: <b>Field:</b> Country <br><b>Options:</b><br>China<br>India<br>United States<br><br><b> OR </b><br>You can also link it to existing Documents.<br>Eg.: <b>link:</b>Customer';
  else cur_frm.fields_dict['Options Help'].disp_area.innerHTML = '';
}