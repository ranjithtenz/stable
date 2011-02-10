pscript.onload_Buying = function(){
  var parent = $i('buying_div');
  new ModulePage(parent,'SRM','Buying');
}

pscript.refresh_Buying = function() {
  if(page_body.cur_page.module_page)
    page_body.cur_page.module_page.show_updates();
}