class DocType:
  def __init__(self, doc, doclist):
    self.doc = doc
    self.doclist = doclist
    
  
  # Get Roles and Modules on loading Permission Engine
  # ----------------------------------------------------- 
  def get_doctype_list(self):
    ret = sql("""SELECT `name` FROM tabDocType 
      WHERE ifnull(docstatus,0)=0 
      AND ifnull(istable,0)=0
      AND ifnull(issingle,0)=0
      AND `module` NOT IN ('System','Utilities','Setup Masters','Roles','Recycle Bin','Mapper','Application Internal','Development')
      ORDER BY `name` ASC""")
    
    rl = [''] + [a[0] for a in sql("select name from tabRole where ifnull(docstatus,0)=0")]
    
    return {'doctypes': [r[0] for r in ret], 'roles': rl}
    

  # Get Perm Level, Perm type of Doctypes of Module and Role Selected
  # -------------------------------------------------------------------
  def get_permissions(self,doctype):
    ret = []
      
    # Get permtype for the role selected
    ptype = sql("select `role`,`permlevel`,`read`,`write`,`create`,`submit`,`cancel`,`amend` from tabDocPerm where `parent` = %s order by `permlevel` ASC",doctype,as_dict = 1)

    # to convert 0L in 0 in values of dictionary
    for p in ptype:
      for key in p:
        if key!='role':
          p[key] = cint(p[key])
      ret.append(p)
            
    # fields list
    fl = ['', 'owner'] + [l[0] for l in sql("select fieldname from tabDocField where parent=%s and fieldtype='Link' and ifnull(options,'')!=''", doctype)]
            
    return {'perms':ret, 'fields':fl}
    
  # get default values
  # ------------------
  def get_defaults(self, arg):
    match_key, with_profiles = arg.split('~~~')
    
    pl = ol = []
  
    # defaults
    dl = [a for a in sql("select parent, ifnull(parenttype,'') as parenttype, ifnull(defvalue,'') as defvalue from tabDefaultValue where defkey=%s order by parenttype desc, parent asc", match_key, as_dict=1)]

    # options
    tn = sql("select options from tabDocField where fieldname=%s and fieldtype='Link' and docstatus=0 limit 1", match_key)[0][0]
    ol = [''] + [a[0] for a in sql("select name from `tab%s` where ifnull(docstatus,0)=0" % tn)]

    # roles
    if with_profiles=='Yes':	    
      # profiles
      pl = [''] + [a[0] for a in sql("select name from tabProfile where ifnull(enabled,0)=1")]
	

    return {'dl':dl, 'pl':pl, 'ol':ol}

  # delete default
  # ----------------------
  def delete_default(self, arg):
    parent, defkey, defvalue = arg.split('~~~')
    sql("delete from tabDefaultValue where parent=%s and defkey=%s and defvalue=%s", (parent, defkey, defvalue))

  # add default
  # ----------------------
  def add_default(self, arg):
    parent, parenttype, defkey, defvalue = arg.split('~~~')

    if sql("select name from tabDefaultValue where parent=%s and defkey=%s and defvalue=%s", (parent, defkey, defvalue)):
      msgprint("This rule already exists!")
      return
          
    dv = Document('DefaultValue')
    dv.parent = parent
    dv.parenttype = parenttype
    dv.parentfield = 'defaults'
    dv.defkey = defkey
    dv.defvalue = defvalue
    dv.save(1)
    return dv.fields

  # Add Permissions
  # ----------------------
  def add_permission(self,args=''):
    parent, role, level = eval(args)
    
    if sql("select name from tabDocPerm where parent=%s and role=%s and permlevel=%s", (parent, role, level)):
      msgprint("This permission rule already exists!")
      return
    
    d = Document('DocPerm')
    d.parent = parent
    d.parenttype = 'DocType'
    d.parentfield = 'permissions'
    d.role = role
    d.permlevel = level
    d.docstatus = 0
    d.save(1)
    
    sql("update tabDocType set modified = %s where name = %s",(now(), parent))


  # Update Permissions
  # ----------------------
  def update_permissions(self,args=''):
    args = eval(args)
    di = args['perm_dict']
    doctype_keys = di.keys()  # ['Enquiry','Competitor','Zone','State']
    for parent in doctype_keys:
      for permlevel in di[parent].keys():
        for role in di[parent][permlevel].keys(): 
        
          # check if Permissions for that perm level and Role exists
          exists = sql("select name from tabDocPerm where parent = %s and role = %s and permlevel = %s",(parent, role, permlevel))

          # Get values of dictionary of Perm Level
          pd = di[parent][permlevel][role]
        
          # update
          if exists and (1 in pd.values()):
            sql("update tabDocPerm set `read` = %s, `write` = %s, `create` = %s, `submit` = %s, `cancel` = %s, `amend` = %s, `match`=%s where parent = %s and role = %s and permlevel = %s",(pd['read'],pd['write'],pd['create'],pd['submit'],pd['cancel'],pd['amend'], pd.get('match'), parent, role, permlevel))
            
          # new
          elif not exists and (1 in pd.values()):
            dtype_obj = get_obj('DocType', d, with_children = 1)
            ch = addchild(dtype_obj.doc,'permissions','DocPerm', 1, dtype_obj.doclist)
            ch.permlevel = i
            ch.role = role
            ch.read = pd['read']
            ch.write = pd['write']
            ch.create = pd['create']
            ch.submit = pd['submit']
            ch.cancel = pd['cancel']
            ch.amend = pd['amend']
            ch.match = pd.get('match','')
            ch.save(1)

          # delete
          elif exists and (1 not in pd.values()):
            sql("delete from tabDocPerm where parent = %s and role = %s and permlevel = %s",(parent, role, permlevel))
          
          sql("update tabDocType set modified = %s where name = %s",(now(), parent))
    msgprint("Permissions Updated")
        
  # Get Fields based on DocType and Permlevel
  # ----------------------------------------------
  def get_fields(self, args = ''):
    ret = {}
    args = eval(args)
    table_fields_dict = {}
    table_exists = sql("Select options from tabDocField where fieldtype = 'Table' and parent = %s",args['dt'])
    if table_exists:
      for d in table_exists:
        table_fields_dict[d[0]]= sql("select label,fieldtype,fieldname,options from tabDocField where parent = %s and permlevel = %s",(d[0],args['permlevel']),as_dict = 1)
      
    parent_fields_dict = sql("select label, fieldtype, fieldname, options from tabDocField where parent = %s and permlevel = %s and fieldtype not in ('Section Break','Column Break')",(args['dt'],args['permlevel']),as_dict = 1)
    
    ret['parent_fields_dict'] = parent_fields_dict
    ret['table_fields_dict'] = table_fields_dict
   
    return ret
    