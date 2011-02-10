class DocType:
  def __init__(self, d, dl):
    self.doc, self.doclist = d, dl

  def get_bal(self,arg):
    msgprint(arg)
    bal = sql("select balance,debit_or_credit from tabAccount where name=%s", arg)
    msgprint(bal)
    return fmt_money(flt(bal[0][0])) + ' ' + bal[0][1]

  def on_update(self):
    set_default('fiscal_year', self.doc.current_fiscal_year)
    ysd = sql("select year_start_date from `tabFiscal Year` where name=%s", self.doc.current_fiscal_year)[0][0]
    set_default('year_start_date', ysd.strftime('%Y-%m-%d'))
    set_default('year_end_date', get_last_day(get_first_day(ysd,0,11)).strftime('%Y-%m-%d'))

  def get_bank_defaults(self, arg):
    return {
      'def_bv_type': self.doc.default_bank_voucher_type,
      'def_bv_series': self.doc.default_bank_voucher_series,
      'def_bank_account': self.doc.default_bank_account,
      'bank_balance': self.get_bal(self.doc.default_bank_account),
      'acc_balance': self.get_bal(arg),
    }