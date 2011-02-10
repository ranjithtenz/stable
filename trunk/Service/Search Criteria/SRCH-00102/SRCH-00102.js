report.customize_filters = function() {
  this.mytabs.items['Select Columns'].hide();
  this.filter_fields_dict['Service Quotation'+FILTER_SEP +'ID'].df.in_first_page = 1;
  this.filter_fields_dict['Service Quotation'+FILTER_SEP +'Company'].df['report_default'] = sys_defaults.company;
  this.filter_fields_dict['Service Quotation'+FILTER_SEP +'Fiscal Year'].df['report_default'] = sys_defaults.fiscal_year;
  this.filter_fields_dict['Service Quotation Detail'+FILTER_SEP +'Item Code'].df.in_first_page = 1;
  this.filter_fields_dict['Service Quotation'+FILTER_SEP +'Company'].df.in_first_page = 0;
  this.filter_fields_dict['Service Quotation'+FILTER_SEP +'From Quotation Date'].df['report_default'] = sys_defaults.year_start_date;
  this.filter_fields_dict['Service Quotation'+FILTER_SEP +'To Quotation Date'].df['report_default'] = dateutil.obj_to_str(new Date());

}