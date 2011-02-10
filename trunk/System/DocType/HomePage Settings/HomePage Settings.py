class DocType:
  def __init__(self,doc,doclist=[]):
    self.doc = doc
    self.doclist = doclist

  def autoname(self):
    rep_nm = self.doc.doctype_name + '-' + 'Settings'
    if sql("select name from `tabHomePage Settings` where name=%s",rep_nm):
      msgprint("Settings for this form already created, please open existing form to do any changes.")
      raise Exception
    else:
      self.doc.name = rep_nm
      
  def get_filter_details(self,arg=''):
    dt_det = sql("select label, fieldtype, options, fieldname from tabDocField where parent=%s and label=%s and fieldname != ''",(self.doc.doctype_name,arg),as_dict=1)
    
    if(dt_det[0]['options'] and dt_det[0]['options'].startswith('link:')):
      opt_dt = dt_det[0]['options'].split(':')[1]
      opt_lst = ['All']
      opts = sql("select name from `tab%s`" % opt_dt)
      for o in range(len(opts)):
        opt_lst.append(opts[o][0])
      opt = NEWLINE.join(opt_lst)

      ret = {
        'field_label_fr' : dt_det and dt_det[0]['label'] or '',
        'field_type_fr'  : dt_det and dt_det[0]['fieldtype'] or '',
        'options_fr'     : opt,
        'field_name_fr'  : dt_det and dt_det[0]['fieldname'] or '',
        'table_name_fr'  : self.doc.doctype_name 
      }

    else:
      ret = {
        'field_label_fr' : dt_det and dt_det[0]['label'] or '',
        'field_type_fr'  : dt_det and dt_det[0]['fieldtype'] or '',
        'options_fr'     : dt_det and dt_det[0]['options'] or '',
        'field_name_fr'  : dt_det and dt_det[0]['fieldname'] or '',
        'table_name_fr'  : self.doc.doctype_name 
      } 
    return cstr(ret)
    
  def get_field_details(self,arg=''):
    dt_det = sql("select label, fieldtype, options, fieldname from tabDocField where parent=%s and label=%s and fieldname != ''",(self.doc.doctype_name,arg),as_dict=1)
    ret = {
      'field_label_fd' : dt_det and dt_det[0]['label'] or '',
      'field_type_fd'  : dt_det and dt_det[0]['fieldtype'] or '',
      'options_fd'     : dt_det and dt_det[0]['options'] or '',
      'field_name_fd'  : dt_det and dt_det[0]['fieldname'] or '',
      'table_name_fd'  : self.doc.doctype_name 
    }
    return cstr(ret)    