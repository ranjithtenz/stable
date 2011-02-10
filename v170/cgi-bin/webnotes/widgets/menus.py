import webnotes

def get_menu_items():
	import webnotes.utils

	rl = webnotes.user.get_roles() + [webnotes.session['user']]
	role_options = ["role = '"+r+"'" for r in rl]
	
	sql = webnotes.conn.sql
	menuitems = []
	
	# pages
	pages = sql("select distinct parent from `tabPage Role` where docstatus!=2 and (%s)" % (' OR '.join(role_options)))

	for p in pages:
		tmp = sql("select icon, parent_node, menu_index, show_in_menu from tabPage where name = '%s'" % p[0])
		if tmp and tmp[0][3]:
			menuitems.append(['Page', p[0] or '', tmp[0][1] or '', tmp[0][0] or '', webnotes.utils.cint(tmp[0][2])])
			
	# singles
	tmp = sql("select smallicon, parent_node, menu_index, name from tabDocType where (show_in_menu = 1 and show_in_menu is not null)")
	singles = {}
	for t in tmp: singles[t[3]] = t
		
	for p in webnotes.user.can_read:
		tmp = singles.get(p, None)
		if tmp: menuitems.append([p, p, tmp[1] or '', tmp[0] or '', int(tmp[2] or 0)])
		
	return menuitems
