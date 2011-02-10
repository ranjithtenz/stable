import webnotes

form = webnotes.form
session = webnotes.session
sql = webnotes.conn.sql
out = webnotes.response

def get_search_criteria_list(dt):
	sc_list = sql("select criteria_name, doc_type from `tabSearch Criteria` where doc_type = '%s' or parent_doc_type = '%s'" % (dt, dt))
	return [list(s) for s in sc_list]

def load_report_list():
	webnotes.response['rep_list'] = get_search_criteria_list(form.getvalue('dt'))

	
# Get, scrub metadata
# ====================================================================

def get_sql_tables(q):
	if q.find('WHERE') != -1:
		tl = q.split('FROM')[1].split('WHERE')[0].split(',')
	elif q.find('GROUP BY') != -1:
		tl = q.split('FROM')[1].split('GROUP BY')[0].split(',')
	else:
		tl = q.split('FROM')[1].split('ORDER BY')[0].split(',')
	return [t.strip().strip('`')[3:] for t in tl]

def get_sql_fields(q):
	fl = q.split('SELECT')[1].split('FROM')[0].split(',')

	for i in range(len(fl)):
		tmp = fl[i].strip()
		if tmp.lower().startswith('distinct'):
			fl[i] = tmp[9:]
		if ' AS ' in tmp:
			fl[i] = '.' + tmp.split(' AS ')[1][1:-1] # no doctype only aliased

	fl = [f.split('.') for f in fl]
	return [(f[0].strip().strip('`')[3:], f[1].strip().strip('`')) for f in fl]

def get_parent_dt(dt):
	pdt = ''
	if sql('select name from `tabDocType` where istable=1 and name="%s"' % dt):
		res = sql('select parent from `tabDocField` where fieldtype="Table" and options="%s"' % dt)
		if res: pdt = res[0][0]
	return pdt

def get_sql_meta(tl):
	meta = {}
	for dt in tl:
		meta[dt] = {'owner':('Owner', '', '', '100'), 'creation':('Created on', 'Date', '', '100'), 'modified':('Last modified on', 'Date', '', '100'), 'modified_by':('Modified By', '', '', '100')}

		# for table doctype, the ID is the parent id
		pdt = get_parent_dt(dt)
		if pdt: meta[dt]['parent'] = ('ID', 'Link', pdt, '200')
			
		res = sql("select fieldname, label, fieldtype, options, width from tabDocField where parent='%s'" % dt)
		for r in res:
			if r[0]:
				meta[dt][r[0]] = (r[1], r[2], r[3], r[4]);
		meta[dt]['name'] = ('ID', 'Link', dt, '200')
			
	return meta

# Additional conditions to fulfill match permission rules
# ====================================================================

def getmatchcondition(dt, ud, ur):
	res = sql("SELECT `role`, `match` FROM tabDocPerm WHERE parent = '%s' AND (`read`=1) AND permlevel = 0" % dt)
	cond = []
	for r in res:
		if r[0] in ur: # role applicable to user
			if r[1]:
				defvalues = ud.get(r[1],['_NA'])
				for d in defvalues:
					cond.append('`tab%s`.`%s`="%s"' % (dt, r[1], d))
			else: # nomatch i.e. full read rights
				return ''

	return ' OR '.join(cond)
	
def add_match_conditions(q, tl, ur, ud):
	sl = []
	for dt in tl:
		s = getmatchcondition(dt, ud, ur)
		if s: 
			sl.append(s)

	# insert the conditions
	if sl:
		condition_st  = q.find('WHERE')!=-1 and ' AND ' or ' WHERE '

		condition_end = q.find('ORDER BY')!=-1 and 'ORDER BY' or 'LIMIT'
		condition_end = q.find('GROUP BY')!=-1 and 'GROUP BY' or condition_end
		
		if q.find('ORDER BY')!=-1 or q.find('LIMIT')!=-1 or q.find('GROUP BY')!=-1: # if query continues beyond conditions
			q = q.split(condition_end)
			q = q[0] + condition_st + '(' + ' OR '.join(sl) + ') ' + condition_end + q[1]
		else:
			q = q + condition_st + '(' + ' OR '.join(sl) + ')'
			
	return q

# execute server-side script from Search Criteria
# ====================================================================

def exec_report(code, res, colnames=[], colwidths=[], coltypes=[], coloptions=[], filter_values={}, query='', from_export=0):
	col_idx, i, out, style, header_html, footer_html, page_template = {}, 0, None, [], '', '', ''
	for c in colnames:
		col_idx[c] = i
		i+=1
	
	# load globals (api)
	from webnotes import *
	from webnotes.utils import *
	from webnotes.model.doc import *
	from webnotes.model.doclist import getlist
	from webnotes.model.db_schema import updatedb
	from webnotes.model.code import get_obj

	set = webnotes.conn.set
	sql = webnotes.conn.sql
	get_value = webnotes.conn.get_value
	convert_to_lists = webnotes.conn.convert_to_lists
	NEWLINE = '\n'

	exec str(code)
	
	if out!=None:
		res = out

	return res, style, header_html, footer_html, page_template
	
# ====================================================================

def build_description_simple():

	import MySQLdb
	colnames, coltypes, coloptions, colwidths = [], [], [], []

	for m in webnotes.conn.get_description():
		colnames.append(m[0])
		if m[1] in MySQLdb.NUMBER:
			coltypes.append('Currency')
		elif m[1] in MySQLdb.DATE:
			coltypes.append('Date')
		else:
			coltypes.append('Data')
		coloptions.append('')
		colwidths.append('100')
	
	return colnames, coltypes, coloptions, colwidths

# ====================================================================

def build_description_standard(meta, fl):

	colnames, coltypes, coloptions, colwidths = [], [], [], []

	for f in fl:
		if meta.has_key(f[0]) and meta[f[0]].has_key(f[1]):
			colnames.append(meta[f[0]][f[1]][0] or f[1])
			coltypes.append(meta[f[0]][f[1]][1] or '')
			coloptions.append(meta[f[0]][f[1]][2] or '')
			colwidths.append(meta[f[0]][f[1]][3] or '100')
		else:
			colnames.append(f[1])
			coltypes.append('')
			coloptions.append('')
			colwidths.append('100')

	return colnames, coltypes, coloptions, colwidths

# Entry Point - Run the query
# ====================================================================

def runquery(q='', ret=0, from_export=0):
	import webnotes.utils
	
	
	# CASE A: Simple Query
	# --------------------
	if form.getvalue('simple_query') or form.getvalue('is_simple'):
		q = form.getvalue('simple_query') or form.getvalue('query')
		if q.split()[0].lower() != 'select':
			raise Exception, 'Query must be a SELECT'
					
		res = webnotes.conn.convert_to_lists(sql(q))
		
		# build colnames etc from metadata
		colnames, coltypes, coloptions, colwidths = [], [], [], []
		
	# CASE B: Standard Query
	# -----------------------
	else:
		if not q: q = form.getvalue('query')

		tl, fl= get_sql_tables(q), get_sql_fields(q)
		meta = get_sql_meta(tl)
		
		colnames, coltypes, coloptions, colwidths = build_description_standard(meta, fl)
	
		q = add_match_conditions(q, tl, webnotes.user.roles, webnotes.user.get_defaults())
		
		# replace special variables
		q = q.replace('__user', session['user'])
		q = q.replace('__today', webnotes.utils.nowdate())
		
		res = webnotes.conn.convert_to_lists(sql(q))
		
	# run server script
	# -----------------
	style, header_html, footer_html, page_template = '', '', '', ''
	if form.has_key('sc_id') and form.getvalue('sc_id'):
		from webnotes.model.doc import Document
		code = Document("Search Criteria", form.getvalue('sc_id')).server_script
		if code:
			filter_values = form.has_key('filter_values') and eval(form.getvalue('filter_values','')) or {}
			res, style, header_html, footer_html, page_template = exec_report(code, res, colnames, colwidths, coltypes, coloptions, filter_values, q, from_export)
		
	out['colnames'] = colnames
	out['coltypes'] = coltypes
	out['coloptions'] = coloptions
	out['colwidths'] = colwidths
	out['header_html'] = header_html
	out['footer_html'] = footer_html
	out['page_template'] = page_template
	
	if style:
		out['style'] = style
	
	# just the data - return
	if ret==1:
		return res	

	out['values'] = res

	# return num of entries 
	qm = form.has_key('query_max') and form.getvalue('query_max')
	if qm:
		if qm.split()[0].lower() != 'select':
			raise Exception, 'Query (Max) must be a SELECT'
		if not form.has_key('simple_query'):
			qm = add_match_conditions(qm, tl, webnotes.user.roles, webnotes.user.defaults)

		out['n_values'] = webnotes.utils.cint(sql(qm)[0][0])

# Export to CSV
# ====================================================================

def runquery_csv():
	from webnotes.utils import getCSVelement

	# run query
	res = runquery(from_export = 1)
	
	q = form.getvalue('query')
	
	rep_name = form.getvalue('report_name')
	if not form.has_key('simple_query'):
		tl, fl= get_sql_tables(q), get_sql_fields(q)
		meta = get_sql_meta(tl)

		# Report Name
		if not rep_name:
			rep_name = get_sql_tables(q)[0]
	
	if not rep_name: rep_name = 'DataExport'
	
	# Headings
	heads = []
	for h in out['colnames']:
		heads.append(getCSVelement(h))
	if form.has_key('colnames'):
		for h in form.getvalue('colnames').split(','):
			heads.append(getCSVelement(h))

	# Output dataset
	dset = [rep_name, '']
	if heads:
		dset.append(','.join(heads))
	
	# Data
	for r in out['values']:
		dset.append(','.join([getCSVelement(i) for i in r]))
		
	txt = '\n'.join(dset)
	out['result'] = txt
	out['type'] = 'csv'
	out['doctype'] = rep_name