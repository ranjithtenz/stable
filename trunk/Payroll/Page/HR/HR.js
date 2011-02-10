pscript.onload_HR = function(){
  var parent = $i('hr_div');
  new ModulePage(parent,'Payroll','Human Resource');
}

pscript.refresh_HR = function() {
  if(page_body.cur_page.module_page)
    page_body.cur_page.module_page.show_updates();
}