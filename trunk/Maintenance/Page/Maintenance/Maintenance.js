pscript.onload_Maintenance = function(){
  var parent = $i('maintenance_div');
  new ModulePage(parent,'Maintenance','Support');
}

pscript.refresh_Maintenance = function() {
  if(page_body.cur_page.module_page)
    page_body.cur_page.module_page.show_updates();
}