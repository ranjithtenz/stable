class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d,dl

	# --------------------------------------------------------------
	def get_children(self, arg='', only_type='', in_roles=[]):

		type_cond = only_type and (" and menu_item_type='%s'" % only_type) or ''
		
		if globals().has_key('version') and version=='v170':
			import webnotes
			roles = webnotes.user.get_roles()
			all_read = webnotes.user.can_get_report
		else:		
			roles = in_roles or session['data']['roles']
			all_read = session['data']['all_readtypes']
			
		cl = sql("select name, menu_item_label, menu_item_type, link_id, link_content, has_children, icon, `order`, criteria_name, doctype_fields, onload from `tabMenu Item` where ifnull(disabled,'No')!='Yes' and ifnull(parent_menu_item,'')='%s' %s order by `order` asc" % (arg, type_cond), as_dict=1)
		ol = []
		for c in cl:
			c['has_children'] = cint(c['has_children'])
			c['order'] = cint(c['order'])
			for k in c.keys(): 
				if c[k]==None: c[k] = ''

			# check permission
			if c['menu_item_type'] in ('DocType','Single','Report'):
				if c['link_id'] in all_read:
					ol.append(c)
			elif c['menu_item_type']=='Page':
				# page
				if c['link_id'].startswith('_'):
					ol.append(c)
				elif has_common([r[0] for r in sql("select role from `tabPage Role` where parent=%s", c['link_id'])], roles):
					ol.append(c)
			elif cstr(c['menu_item_type'])=='':
				# sections
				if has_common([r[0] for r in sql("select role from `tabMenu Item Role` where parent=%s", c['name'])], roles):
					ol.append(c)
			else:
				ol.append(c)
		
		return ol

	# --------------------------------------------------------------
	def has_result(self, dt):
		return sql("select name from `tab%s` limit 1" % dt) and 'Yes' or 'No'

	# --------------------------------------------------------------

	def is_submittable(self, dt):
		return sql("select name from tabDocPerm where parent=%s and ifnull(submit,0)=1 and docstatus<1 limit 1", dt)

	# --------------------------------------------------------------
	def get_dt_trend(self, dt):
		ret = {}
		for r in sql("select datediff(now(),modified), count(*) from `tab%s` where datediff(now(),modified) between 0 and 30 group by date(modified)" % dt):
			ret[cint(r[0])] = cint(r[1])
		return ret

	# --------------------------------------------------------------

	def get_columns(self, out, sf, fl, dt):
		if not fl:
			fl = sf
			out['field_list'] = NEWLINE.join(fl)
		else:
			fl = fl.split(NEWLINE)
			fl = [f.split(',')[0] for f in fl]


		res = []
		for f in fl:
			if f:
				res += [[c or '' for c in r] for r in sql("select fieldname, label, fieldtype, options from tabDocField where parent='%s' and fieldname='%s'" % (dt, f))]
				
		return res

	# --------------------------------------------------------------

	def check_user_tags(self, dt):
		try:
			sql("select `_user_tags` from `tab%s` limit 1" % dt)
		except Exception, e:
			if e.args[0] == 1054:
				sql("alter table `tab%s` add column `_user_tags` varchar(180)" % dt)

	# --------------------------------------------------------------
	# NOTE: THIS SHOULD BE CACHED IN DOCTYPE CACHE
	# --------------------------------------------------------------
	
	def get_dt_details(self, arg):
		dt, fl = arg.split('~~~')
		submittable = self.is_submittable(dt) and 1 or 0
	 
		out = {'submittable':submittable}

		# filters
		# -------

		sf = sql("select search_fields from tabDocType where name=%s", dt)[0][0] or ''
		sf = [s.strip() for s in sf.split(',')]
		if sf and sf[0]:
			res = sql("select fieldname, label, fieldtype, options from tabDocField where parent='%s' and fieldname in (%s)" % (dt, '"'+'","'.join(sf)+'"'))
		else:
			res = []

		# select "link" options
		res = [[c or '' for c in r] for r in res]
		for r in res:
			if r[2]=='Select' and r[3] and r[3].startswith('link:'):
				tdt = r[3][5:]
				ol = sql("select name from `tab%s` where docstatus!=2 order by name asc" % tdt)
				r[3] = NEWLINE.join([''] + [o[0] for o in ol])

		if not res:
			out['filters'] = [['name', 'ID', 'Data', '']]
		else:
			out['filters'] = [['name', 'ID', 'Data', '']] + res
		
		# columns
		# -------
		res = self.get_columns(out, sf, fl, dt)
		
		self.check_user_tags(dt)
		
		out['columns'] = [['name', 'ID', 'Link', dt], ['modified', 'Modified', 'Data', ''], ['_user_tags', 'Tags', 'Data', '']] + res
		out['trend'] = self.get_dt_trend(dt)
		
		return out

	# --------------------------------------------------------------

	def get_tags(self, dt, dn):
		tl = sql("select ifnull(_user_tags,'') from tab%s where name=%s" % (dt,'%s'), dn)[0][0]
		return tl and tl.split(',') or []
	
	# --------------------------------------------------------------

	def update_tags(self, dt, dn, tl):
		if len(','.join(tl)) > 179:
			msgprint("Too many tags")
			raise Exception
			
		sql("update tab%s set _user_tags=%s where name=%s" % (dt,'%s','%s'), (',' + ','.join(tl), dn))

	# --------------------------------------------------------------

	def create_tag(self,tag):
		try:
			mytag = sql("select name from tabTag where name=%s", tag)[0][0]
		except IndexError, e:
			sql("insert into tabTag(name) values (%s)", tag)
		except Exception, e:
			if e.args[0]==1146:
				sql("create table `tabTag`(`name` varchar(180), primary key (`name`))")

	# --------------------------------------------------------------

	def add_tag(self,arg):
		dt, dn, tag = eval(arg)
		
		# create tag in tag table
		self.create_tag(tag)
		
		# add in _user_tags
		tl = self.get_tags(dt, dn)
		
		if not tag in tl:
			tl.append(tag)
			self.update_tags(dt, dn, tl)
			
		return tag
 
 	# --------------------------------------------------------------

 	def remove_tag(self,arg):
		dt, dn, tag = eval(arg)
		tl = self.get_tags(dt, dn)				
		self.update_tags(dt, dn, filter(lambda x:x!=tag, tl))
		