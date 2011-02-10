class DocType:
  def __init__(self,d,dl):
    self.doc, self.doclist = d, dl
    
  # Generate Periods
  #------------------		
  def generate_periods(self, fy):
    ml = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')    

    import webnotes.utils
    from dateutil.relativedelta import relativedelta
    
    
    if not sql("select name from `tabPeriod` where fiscal_year = '%s'" % fy):
      ysd = sql("select year_start_date from `tabFiscal Year` where name = '%s'"%fy)[0][0]
      
      #create period as fiscal year record name
      #----------------------------------------------
      arg = {'pn':fy,'sd':ysd,'ed':webnotes.utils.get_last_day(ysd + relativedelta(months=11)).strftime('%Y-%m-%d'),'pt':'Year','fy':fy}
      self.create_period(arg)
            
      for i in range(12):    
        msd = ysd + relativedelta(months=i)

        arg = {'pn':ml[cint(msd.strftime('%m'))-1] + ' ' + msd.strftime('%Y'),'sd':msd.strftime('%Y-%m-%d'),'ed':webnotes.utils.get_last_day(msd).strftime('%Y-%m-%d'),'pt':'Month','fy':fy}
        self.create_period(arg)
          
  #---------------------------------------------------------
  #create period common function        
  def create_period(self,arg):
    p = Document('Period')
    p.period_name = arg['pn']
    p.start_date = arg['sd']
    p.end_date = arg['ed']
    p.period_type = arg['pt']
    p.fiscal_year = arg['fy']

    try:        
      p.save(1)  
    except NameError, e:
      msgprint('Period %s already exists' % p.period_name)
      raise Exception