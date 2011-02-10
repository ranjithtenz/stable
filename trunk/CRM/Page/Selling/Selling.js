pscript.onload_Selling = function(){
  var parent = $i('selling_div');
  new ModulePage(parent,'CRM','Selling','How Do I - CRM');
}

pscript.refresh_Selling = function() {
  if(page_body.cur_page.module_page)
    page_body.cur_page.module_page.show_updates();
}