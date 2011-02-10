pscript.onload_Stock = function(){
  var parent = $i('stock_div');
  new ModulePage(parent,'Material Management','Stock','How Do I - Inventory');
}

pscript.refresh_Stock = function() {
  if(page_body.cur_page.module_page)
    page_body.cur_page.module_page.show_updates();
}