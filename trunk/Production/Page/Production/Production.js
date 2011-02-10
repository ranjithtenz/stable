pscript.onload_Production = function(){
  var parent = $i('production_div');
  new ModulePage(parent,'Production','Production');
}

pscript.refresh_Production = function() {
  if(page_body.cur_page.module_page)
    page_body.cur_page.module_page.show_updates();
}