# Event
# -------------

def get_cal_events(m_st, m_end):
	import webnotes
	import webnotes.model.doc
	
	sql = webnotes.conn.sql

	# load owned events
	res1 = sql("select name from `tabEvent` WHERE event_date >= '%s' and event_date <= '%s' and owner = '%s' and event_type != 'Public' and event_type != 'Cancel'" % (m_st, m_end, webnotes.user.name))

	# load individual events
	res2 = sql("select t1.name from `tabEvent` t1, `tabEvent User` t2 where t1.event_date >= '%s' and t1.event_date <= '%s' and t2.person = '%s' and t1.name = t2.parent and t1.event_type != 'Cancel'" % (m_st, m_end, webnotes.user.name))

	# load role events
	roles = webnotes.user.get_roles()
	myroles = ['t2.role = "%s"' % r for r in roles]
	myroles = '(' + (' OR '.join(myroles)) + ')'
	res3 = sql("select t1.name from `tabEvent` t1, `tabEvent Role` t2  where t1.event_date >= '%s' and t1.event_date <= '%s' and t1.name = t2.parent and t1.event_type != 'Cancel' and %s" % (m_st, m_end, myroles))
	
	# load public events
	res4 = sql("select name from `tabEvent` where event_date >= '%s' and event_date <= '%s' and event_type='Public'" % (m_st, m_end))
	
	doclist, rl = [], []
	for r in res1 + res2 + res3 + res4:
		if not r in rl:
			doclist += webnotes.model.doc.get('Event', r[0])
			rl.append(r)
	
	return doclist


# Load Month Events
# -----------------

def load_month_events():
	import webnotes
	
	form = webnotes.form

	mm = form.getvalue('month')
	yy = form.getvalue('year')
	m_st = str(yy) + '-' + str(mm) + '-01'
	m_end = str(yy) + '-' + str(mm) + '-31'

	webnotes.response['docs'] = get_cal_events(m_st, m_end)