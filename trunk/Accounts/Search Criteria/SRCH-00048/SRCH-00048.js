report.customize_filters = function() {
  this.hide_all_filters();

  this.filter_fields_dict['Payable Voucher'+FILTER_SEP +'From Voucher Date'].df.filter_hide = 0;
  this.filter_fields_dict['Payable Voucher'+FILTER_SEP +'To Voucher Date'].df.filter_hide = 0;
  this.filter_fields_dict['Payable Voucher'+FILTER_SEP +'Credit To'].df.filter_hide = 0;
  this.filter_fields_dict['Payable Voucher'+FILTER_SEP +'Is Opening'].df.filter_hide = 0;
  this.filter_fields_dict['Payable Voucher'+FILTER_SEP +'Company'].df.filter_hide = 0;
  this.filter_fields_dict['PV Detail'+FILTER_SEP +'Item'].df.filter_hide = 0;
  this.filter_fields_dict['Payable Voucher'+FILTER_SEP +'From Posting Date'].df.filter_hide = 0;
  this.filter_fields_dict['Payable Voucher'+FILTER_SEP +'To Posting Date'].df.filter_hide = 0;

  this.filter_fields_dict['Payable Voucher'+FILTER_SEP +'From Posting Date'].df.in_first_page = 1;
  this.filter_fields_dict['Payable Voucher'+FILTER_SEP +'To Posting Date'].df.in_first_page = 1;
  this.filter_fields_dict['PV Detail'+FILTER_SEP +'Item'].df.in_first_page = 1;

  this.filter_fields_dict['Payable Voucher'+FILTER_SEP +'From Posting Date'].df['report_default'] = sys_defaults.year_start_date;
  this.filter_fields_dict['Payable Voucher'+FILTER_SEP +'To Posting Date'].df['report_default'] = dateutil.obj_to_str(new Date());
  this.filter_fields_dict['Payable Voucher'+FILTER_SEP +'Company'].df['report_default']=sys_defaults.company

}