class DocType:
  def __init__(self, d, dl):
    self.doc, self.doclist = d, dl

#---------------------------------------------------------------------------------------------------------------------------------------------  
  def get_bal(self,arg):
    bal = sql("select `tabAccount Balance`.balance,`tabAccount`.debit_or_credit from `tabAccount`,`tabAccount Balance` where `tabAccount Balance`.parent=%s and `tabAccount Balance`.period=%s and `tabAccount Balance`.parent=`tabAccount`.name ",(arg,self.doc.current_fiscal_year))
    if bal:
      return fmt_money(flt(bal[0][0])) + ' ' + bal[0][1]
#-----------------------------------------------------------------------------------------------------------------------------------  
# Update display info in control panel
  def update_control_panel(self):
    if self.doc.bg_color:
      sql("update `tabSingles` set value='%s'  where doctype='Control Panel' and field='background_color'"%self.doc.bg_color)
    else:
      msgprint("No background color is mentioned")
    if self.doc.letter_head:
      sql("update `tabSingles` set value='%s' where doctype='Control Panel' and field='letter_head'"%self.doc.letter_head)
    else:
      msgprint("No Letter Head is mentioned")

# =========================================================================================================================================

  # Update Default
  # ---------------
  def set_system_default(self, defkey, defvalue):
    det = sql("select defvalue from `tabDefaultValue` where defkey = %s and parent not like 'old_parent%%'", (defkey))
    if not det:
      con_obj = get_obj(dt = 'Control Panel',with_children = 1)
      child = addchild(con_obj.doc,'system_defaults','DefaultValue',0)
      child.defkey = defkey
      child.defvalue = defvalue
      child.save()
    elif det and det[0][0] != defvalue:
      set_default(defkey, defvalue)

    if defkey == 'fiscal_year':
      ysd = sql("select year_start_date from `tabFiscal Year` where name=%s", defvalue)
      ysd = ysd and ysd[0][0] or ''
      if ysd:
        set_default('year_start_date', ysd.strftime('%Y-%m-%d'))
        set_default('year_end_date', get_last_day(get_first_day(ysd,0,11)).strftime('%Y-%m-%d'))


  # Update
  # --------
  def update_cp(self):
    def_list = [['fiscal_year',self.doc.current_fiscal_year],
                ['company',self.doc.default_company],
                ['currency',self.doc.default_currency],
                ['price_list_name',self.doc.default_price_list],
                ['item_group',self.doc.default_item_group],
                ['customer_group',self.doc.default_customer_group],
                ['cust_master_name',self.doc.cust_master_name], 
                ['supplier_type',self.doc.default_supplier_type],
                ['supp_master_name',self.doc.supp_master_name], 
                ['territory',self.doc.default_territory],
                ['stock_uom',self.doc.default_stock_uom],
                ['valuation_method',self.doc.default_valuation_method]]

    for d in def_list:
      self.set_system_default(d[0],d[1])
    # Update Currency Format
    sql("update `tabSingles` set value = '%s' where field = 'currency_format' and doctype = 'Control Panel'" % self.doc.default_currency_format)
    sql("update `tabSingles` set value = '%s' where field = 'date_format' and doctype = 'Control Panel'" %self.doc.date_format)

    import webnotes.utils
    return webnotes.utils.get_defaults()

#----------------- field arrangement ----------------------
  #check current idx
  def get_curr_idx(self, chk_for, chk_type, resp_fld, resp_type, doctype):
    ret ={}
    curr_idx_detail = sql("select idx,name from `tabDocField` where %s='%s' and parent='%s'"% (chk_type, chk_for, doctype))
    curr_idx = curr_idx_detail and curr_idx_detail[0][0] or 0
    nm = curr_idx_detail and curr_idx_detail[0][1] or ''
    
    resp_fld_idx = sql("select idx from `tabDocField` where %s='%s' and parent='%s'"% (resp_type, resp_fld, doctype))
    resp_fld_idx = resp_fld_idx and resp_fld_idx[0][0] or 0
    ret = {'move_curr_idx': curr_idx, 'move_nm':nm, 'resp_fld_idx':resp_fld_idx}
    return ret
  
  def move_field(self, arg):
    arg1 =[]
    arg1 = arg    
    for z in arg1:
      field_dict ={}
      chk_for=chk_type=resp_fld=resp_type=position=new_idx=''
      
      if z.get('move_fieldname'):
        chk_for, chk_type = z['move_fieldname'], 'fieldname'
      elif z.get('move_label'):
        chk_for, chk_type = z['move_label'], 'label'
      
      if z.get('after_fieldname'):
        resp_fld, resp_type, position = z['after_fieldname'], 'fieldname', 'after'
      elif z.get('after_label'):
        resp_fld, resp_type, position = z['after_label'], 'label', 'after'
      elif z.get('before_fieldname'):
        resp_fld, resp_type, position = z['before_fieldname'], 'fieldname', 'before'
      elif z.get('before_label'):
        resp_fld, resp_type, position = z['before_label'], 'label', 'before'
      
      doctype = z['doctype']
      
      if chk_for and chk_type and resp_fld and doctype:
        field_dict = self.get_curr_idx(chk_for, chk_type, resp_fld, resp_type, doctype)
        
        #get new idx
        if position == 'before':
          new_idx = cint(field_dict['resp_fld_idx'])
        elif position == 'after':
          new_idx = cint(field_dict['resp_fld_idx'])+1
        
        #update
        sql("start transaction")
        sql("update `tabDocField` set idx=%s where name=%s", (new_idx,field_dict['move_nm']))
        sql("update `tabDocField` set idx=idx+1 where idx>=%s and idx<%s and name!=%s", (new_idx,field_dict['move_curr_idx'],field_dict['move_nm'])) 
        sql("Commit")
        msgprint("Field idx updated for field "+chk_for)
      else:
        msgprint("Please specify either fieldname or label for field to be moved and also for the field before/after which it should be placed and doctype name")
  
  #------------ delete unwanted fields-----------------
  #structure is arg = {'doctype_nm1':[{'delete_label':'label_nm1', 'delete_fieldname':'field_nm1'}, {'delete_label':'label_nm2', 'delete_fieldname':'field_nm2'},........], 'doctype_nm2':[{}, {}],.................}
  def delete_fields(self, arg):
    #arg1 =[]
    arg1 = arg
    
    for m in arg1:
      fld_lst =[]
      no_fld_lst =[]
      doctype = m
      for n in arg1[m]:
        chk_for=chk_type=''
        if n.get('delete_label'):
          chk_for, chk_type = n['delete_label'], 'label'
        if n.get('delete_fieldname'):
          chk_for, chk_type = n['delete_fieldname'], 'fieldname'
      
        if chk_for and chk_type and doctype:
          chk = sql("select name from `tabDocField` where %s='%s' and parent='%s'"%(chk_type, chk_for, doctype))
          if chk:
            sql("start transaction")
            sql("delete from `tabDocField` where %s='%s' and parent='%s'"% (chk_type, chk_for, doctype))
            sql("Commit")
            fld_lst.append(chk_for)
          else:
            no_fld_lst.append(chk_for)
        else:
          msgprint("Please provide doctype name and field name or field label")
      msgprint("fields deleted of doctype "+cstr(m)+" :: "+cstr(fld_lst))
      msgprint("fields not found in doctype "+cstr(m)+" :: "+cstr(no_fld_lst))
  
  #delete fieldname
  def delete_fieldname(self, arg):
    #arg1 =[]
    arg1 = arg
    
    for m in arg1:
      fld_lst =[]
      no_fld_lst =[]
      doctype = m
      for n in arg1[m]:
        chk_for = chk_type=''
        chk_for, chk_type = n, 'fieldname'
      
        if chk_for and chk_type and doctype:
          chk = sql("select name from `tabDocField` where fieldname='%s' and parent='%s'"%(chk_for, doctype))
          if chk:
            sql("start transaction")
            sql("delete from `tabDocField` where %s='%s' and parent='%s'"% (chk_type, chk_for, doctype))
            sql("Commit")
            fld_lst.append(chk_for)
          else:
            no_fld_lst.append(chk_for)
        else:
          msgprint("Please provide doctype name and field name")
      msgprint("fields deleted of doctype "+cstr(m)+" :: "+cstr(fld_lst))
      msgprint("fields not found in doctype "+cstr(m)+" :: "+cstr(no_fld_lst))
  
  #delete fieldname
  def delete_labels(self, arg):
    #arg1 =[]
    arg1 = arg
    
    for m in arg1:
      fld_lst =[]
      no_fld_lst =[]
      doctype = m
      for n in arg1[m]:
        chk_for = chk_type=''
        chk_for, chk_type = n, 'label'
        
        if chk_for and chk_type and doctype:
          chk = sql("select name from `tabDocField` where label='%s' and parent='%s'"%(chk_for, doctype))
          if chk:
            sql("start transaction")
            sql("delete from `tabDocField` where %s='%s' and parent='%s'"% (chk_type, chk_for, doctype))
            sql("Commit")
            fld_lst.append(chk_for)
          else:
            no_fld_lst.append(chk_for)
        else:
          msgprint("Please provide doctype name and field label")
      msgprint("fields deleted of doctype "+cstr(m)+" :: "+cstr(fld_lst))
      msgprint("fields not found in doctype "+cstr(m)+" :: "+cstr(no_fld_lst))

  #---------------function update label------------------------------------  
  #arg = {dt : [[lbl,fnm], []]}
  def update_label(self,arg):
    for i in arg:
      ch_lbl=[]     
      for j in arg[i]:
        if not j[0] or not j[1]:
          msgprint('Please enter both fieldname and label.')
        else:
          sql('Start Transaction')
          sql("update `tabDocField` set label = '%s' where fieldname = '%s' and parent = '%s'"%(j[0],j[1],i))
          ch_lbl.append(j)
          sql('Commit')
      msgprint(i+'==>'+cstr(ch_lbl))