pscript.onload_Accounts = function(){
  var parent = $i('accounts_div');
  new ModulePage(parent,'Accounts','Accounts','How Do I - Accounts');
}

pscript.refresh_Accounts = function() {
  if(page_body.cur_page.module_page)
    page_body.cur_page.module_page.show_updates();
}