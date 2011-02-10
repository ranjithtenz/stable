class DocType:
	def __init__(self,d,dl):
		self.doc, self.doclist = d,dl

	# add social badge points
	def add_badge_points(self,dt,status=0):
		# get points
		det = sql("select create_points as `0`, submit_points as `1`, cancel_points as `2` from `tabBadge Settings Detail` where transaction=%s", dt, as_dict=1)
		if det:
			det = det[0]
		else:
			det = {'0':1, '1':1, '2':0 }
			
		# get user points
		user_points = sql("select social_points from tabProfile where name=%s", session['user'])[0][0] or 0
		
		# add points
		sql("update tabProfile set social_points = ifnull(social_points,0) + %s where name=%s", (det[str(status)], session['user']))
		
		# see if badge is changed
		badge = sql("select name from `tabSocial Badge` where badge_points between %s and %s", (user_points, user_points + cint(det[str(status)])))

		if badge:
			self.add_badge_feed(badge[0][0])
					
	# Add badge feed
	def add_badge_feed(self,badge):
		f = Document('Feed')
		f.feed = '<b>News Flash:</b> %s is now a <b>%s</b>! Congrats!' % (session['user'], badge)
		f.feed_owner = session['user']
		f.creation_date = nowdate()
		f.save(1)
		
	def get_badge_details(self):
		my_info = convert_to_lists(sql("select name, concat_ws(' ', first_name, last_name), ifnull(social_points,0), ifnull(social_badge,'White Belt') from tabProfile where name=%s", session['user']))

		top_player = convert_to_lists(sql("select name, concat_ws(' ', first_name, last_name), social_points, social_badge from tabProfile order by social_points desc limit 3"))

		badge_det = convert_to_lists(sql("select name, badge_name, badge_points, badge_image, badge_description from `tabSocial Badge` order by badge_points asc"))

		for b in badge_det:
			if b[0] == 'White Belt':
				condn = "social_badge = 'White Belt' or social_badge is null or social_badge = ''"
			else:
				condn = "social_badge = '%s'" % b[0]

			count = sql("select count(name) from tabProfile where %s" % condn)
			count = count and count[0][0] or ''
	
			b.append(count)
			
		return my_info, top_player, badge_det
