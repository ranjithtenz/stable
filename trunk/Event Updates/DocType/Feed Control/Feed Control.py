class DocType:
	def __init__(self,d,dl):
		self.doc, self.doclist = d,dl

	def make_feed(self,action, doc_name, doc_no):
		feed_name = ''
		
		if action != 'cancelled':
			doc_label = sql("select dt_label from `tabDocType Label` where dt = %s", doc_name)
			doc_label = doc_label and doc_label[0][0] or doc_name
	
			feed = sql("select name, doc_label, doc_no from tabFeed where creation_date=%s and doc_name=%s and action =%s and feed_owner=%s",(getdate(nowdate()), doc_name, action, session['user']), as_dict=1)
		
			if feed:
				if not has_common(feed[0]['doc_no'].split(','), [doc_no]):
					f = Document('Feed', feed[0]['name'])
					f.doc_no = feed[0]['doc_no'] + ',' + doc_no
					if not f.doc_label:
						f.doc_label = doc_label
					f.save(0)
				
					feed_name = f.name
			else:
				role = sql("select distinct role from tabDocPerm where parent=%s", doc_name)
				role_list = [r[0] for r in role]

				f = Document('Feed')
				f.feed_owner = session['user']
				f.doc_name = doc_name
				f.doc_label = doc_label
				f.doc_no = doc_no
				f.action = action
				f.creation_date = getdate(nowdate())
				f.can_view = ','.join(role_list)
				f.save(1)
			
				feed_name = f.name
			
			if feed_name:
				self.delete_prev_feeds(feed_name, doc_no)
			
			self.control_feed()

			# add badge points
			b_dict = {'created':0, 'submitted':1, 'cancelled':2}
			if b_dict.has_key(action):
				get_obj('Badge Settings').add_badge_points(doc_name,b_dict[action])

	# delete previous feeds
	def delete_prev_feeds(self,feed_name,doc_no):
		prev_feeds = sql("select name from tabFeed where doc_no like %s and name != %s" , ('%' + doc_no + '%', feed_name))
		fl = [p[0] for p in prev_feeds]
		if fl:
			for f in fl:
				d = Document('Feed',f)
				l = d.doc_no.split(',')

				if doc_no in l:
					if len(l) == 1:
						sql("delete from tabFeed where name = %s", f)
					else:
						l.remove(doc_no)
						d.doc_no = ','.join(l)
						d.save(0)
		
	def add_comment(self,args):
		import time
		args = eval(args)
		count = 0
		if(args['cmt']):
			cmt = Document('Comment Widget Record')
			cmt.comment = args['cmt']
			cmt.comment_by = args['cmt_by']
			cmt.comment_by_fullname = args['cmt_by_fullname']
			cmt.comment_doctype = args['dt']
			cmt.comment_docname = args['dn']
			cmt.comment_date = getdate(nowdate())
			cmt.comment_time = now().split(' ')[-1][:5]
			cmt.save(1)
			
			# update comment count
			if args['dt'] == 'Feed':
				d = Document(args['dt'], args['dn'])
				d.total_comments = cint(d.total_comments) + 1
				d.modified = now()
				d.save(0)
			
				count = d.total_comments
			
			# update latest comments
			self.update_latest_comments(args)
			ret = self.return_latest_comment(cmt.name)
			return ret, count
		else:
			raise Exception
			
	# update latest comments		
	def update_latest_comments(self,args):
		cl = convert_to_lists(sql("select ifnull(t1.name,''), ifnull(t1.comment,''), ifnull(t1.comment_by,''), ifnull(t1.comment_by_fullname,''), ifnull(t1.comment_date,''), ifnull(t1.comment_time,''), ifnull(t1.comment_doctype,''), ifnull(t1.comment_docname,''), ifnull(concat_ws(' ', t2.first_name, t2.last_name),''), ifnull(t2.file_list,''), ifnull(t2.gender,'') from `tabComment Widget Record` t1, `tabProfile` t2 where t1.comment_doctype = %s and t1.comment_docname = %s and t1.comment_by = t2.name order by t1.creation desc limit 2",(args['dt'],args['dn'])))

		f = Document(args['dt'],args['dn'])
		f.latest_comments = cstr(cl) or ''
		f.save()

	# return latest comment
	def return_latest_comment(self,cmt_name):
		res = convert_to_lists(sql("select ifnull(t1.name,''), ifnull(t1.comment,''), ifnull(t1.comment_by,''), ifnull(t1.comment_by_fullname,''), ifnull(t1.comment_date,''), ifnull(t1.comment_time,''), ifnull(t1.comment_doctype,''), ifnull(t1.comment_docname,''), ifnull(concat_ws(' ', t2.first_name, t2.last_name),''), ifnull(t2.file_list,''), ifnull(t2.gender,'') from `tabComment Widget Record` t1, `tabProfile` t2 where t1.name=%s and t1.comment_by = t2.name order by t1.creation desc", cmt_name))
		return res
		
	# Add feed
	def add_feed(self,feed):
		f = Document('Feed')
		f.feed = feed
		f.feed_owner = session['user']
		f.creation_date = getdate(nowdate())
		f.can_view = 'All'
		f.save(1)
		sql("update tabProfile set messanger_status=%s where name=%s", (feed, session['user']))
		self.control_feed()

		
	# control feed - keep max 300 feeds
	def control_feed(self):
		t = sql("select count(name) from tabFeed")
		t = t[0][0] or 0
		
		if t and t>300:
			sql("delete from tabFeed order by modified asc limit 1")

	# show all comments
	def show_all_comments(self,feed_id):
		cl = convert_to_lists(sql("select t1.name, t1.comment, t1.comment_by, t1.comment_by_fullname, t1.comment_date, t1.comment_time, t1.comment_doctype, t1.comment_docname, concat_ws(' ', t2.first_name, t2.last_name), t2.file_list, t2.gender from `tabComment Widget Record` t1, `tabProfile` t2 where t1.comment_doctype = 'Feed' and t1.comment_docname = %s and t1.comment_by = t2.name order by t1.creation desc",feed_id))
		return cl
		
	# delete comment
	def delete_comment(self,args):
		args = eval(args)
		count = 0
		if args['dt'] == 'Feed':
			d = Document(args['dt'],args['dn'])
			d.total_comments = cint(d.total_comments) - 1
			d.save(0)
			
			count = d.total_comments
		
		sql("delete from `tabComment Widget Record` where name=%s",args['id'])
		self.update_latest_comments(args)
		
		return count
		
	# delete feed
	def delete_feed(self,id):
		sql("delete from `tabFeed` where name=%s",id)
		sql("delete from `tabComment Widget Record` where comment_doctype='Feed' and comment_docname = %s",id)
		
	def get_latest_comments(self, id):
		cmt = sql("select latest_comments from tabFeed where name=%s", id)
		cmt = cmt and cmt[0][0] or ''
		return cmt
		
	def get_auto_feed(self):
		if cint(get_defaults().get('auto_feed_off')):
			return 1
		else:
			return 0
			
	def set_auto_feed(self,status):
		set_default('auto_feed_off',status)
		
	def get_social_badge(self):
		sb = [[r[0],r[1],r[2]] for r in sql("select name,social_badge,social_points from tabProfile")]
		ret = {}
		for s in sb:
			ret[s[0]] = [s[1],s[2]]
		return ret