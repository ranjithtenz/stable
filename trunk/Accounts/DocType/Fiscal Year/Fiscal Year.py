class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d,dl
		
	def repost(self):
		if not in_transaction:
			sql("start transaction")
				
		self.clear_account_balances()
		self.create_account_balances()
		self.update_opening()	
		self.post_entries()
		sql("commit")
		msgprint("Account balance reposted")

	def clear_account_balances(self):
		# balances clear - `tabAccount Balance` for fiscal year
		sql("update `tabAccount Balance` set opening=0, balance=0, debit=0, credit=0 where fiscal_year=%s", self.doc.name)

	def create_account_balances(self):
		# get periods
		period_list = self.get_period_list()
		cnt = 0
		
		# get accounts
		al = sql("select name from tabAccount")
		
		for a in al:
			# check
			if sql("select count(*) from `tabAccount Balance` where fiscal_year=%s and parent=%s", (self.doc.name, a[0]))[0][0] < 13:
				for p in period_list:
					# check if missing
					if not sql("select name from `tabAccount Balance` where period=%s and parent=%s and fiscal_year=%s", (p[0], a[0], self.doc.name)):
						d = Document('Account Balance')
						d.parent = a[0]
						d.parentfield = 'account_balances'
						d.parenttype = 'Account'
						d.period = p[0]
						d.start_date = p[1].strftime('%Y-%m-%d')
						d.end_date = p[2].strftime('%Y-%m-%d')
						d.fiscal_year = p[3]
						d.debit = 0
						d.credit = 0
						d.opening = 0
						d.balance = 0
						ac.save(1)
						cnt += 1
		return cnt
				
	# Get periods(month and year)
	def get_period_list(self):
		periods = []
		pl = sql("SELECT name, start_date, end_date, fiscal_year FROM tabPeriod WHERE fiscal_year = '%s' and period_type in ('Month', 'Year') order by start_date ASC, end_date DESC" % self.doc.name)
		for p in pl:
			periods.append([p[0], p[1], p[2], p[3]])
		return periods

	# ====================================================================================
	def update_opening(self):
		# set opening from last year closing
		abl = sql("select t1.parent, t1.balance from `tabAccount Balance` t1, tabAccount t2 where t1.period=%s and t2.company=%s and ifnull(t2.is_pl_account, 'No') = 'No' and t1.parent = t2.name", (self.doc.past_year, self.doc.company))
		
		cnt = 0
		for ab in abl:
			if cnt % 100 == 0: 
				sql("commit")
				sql("start transaction")
				
			sql("update `tabAccount Balance` set opening=%s where period=%s and parent=%s", (ab[1], self.doc.name, ab[0]))
			sql("update `tabAccount Balance` set balance=%s where fiscal_year=%s and parent=%s", (ab[1], self.doc.name, ab[0]))
			cnt += 1
		
		return cnt
			
	def get_account_details(self, account):
		return sql("select debit_or_credit, lft, rgt, is_pl_account from tabAccount where name=%s", account)[0]

	# ====================================================================================
	def post_entries(self):
	
		# post each gl entry (batch or complete)
		gle = sql("select name, account, debit, credit, is_opening, posting_date from `tabGL Entry` where fiscal_year=%s and ifnull(is_cancelled,'No')='No' and company=%s", (self.doc.name, self.doc.company))
		account_details = {}

		cnt = 0
		for entry in gle:
			# commit in batches of 100
			if cnt % 100 == 0: 
				sql("commit")
				sql("start transaction")
			cnt += 1
			#print cnt

			if not account_details.has_key(entry[1]):
				account_details[entry[1]] = self.get_account_details(entry[1])
			
			det = account_details[entry[1]]
			diff = flt(entry[2])-flt(entry[3])
			if det[0]=='Credit': diff = -diff

			# build dict
			p = {
				'debit': flt(entry[2])
				,'credit':flt(entry[3])
				,'opening': entry[4]=='Yes' and diff or 0
				
				# end date conditino only if it is not opening
				,'end_date_condition':(entry[4]!='Yes' and ("and ab.end_date >= '"+entry[5].strftime('%Y-%m-%d')+"'") or '')
				,'diff': diff
				,'lft': det[1]
				,'rgt': det[2]
				,'posting_date': entry[5]
				,'fiscal_year': self.doc.name
			}
		
			sql("""update `tabAccount Balance` ab, `tabAccount` a 
					set 
						ab.debit = ifnull(ab.debit,0) + %(debit)s
						,ab.credit = ifnull(ab.credit,0) + %(credit)s
						,ab.opening = ifnull(ab.opening,0) + %(opening)s
						,ab.balance = ifnull(ab.balance,0) + %(diff)s
					where
						a.lft <= %(lft)s
						and a.rgt >= %(rgt)s
						and ab.parent = a.name
						%(end_date_condition)s
						and ab.fiscal_year = '%(fiscal_year)s' """ % p)



	# ====================================================================================
	# Clear PV/RV outstanding
	def clear_outstanding(self):
		# clear o/s of current year
		sql("update `tabPayable Voucher` set outstanding_amount = 0 where fiscal_year=%s and company=%s", (self.doc.name, self.doc.company))
		sql("update `tabReceivable Voucher` set outstanding_amount = 0 where fiscal_year=%s and company=%s", (self.doc.name, self.doc.company))

	# Update Voucher Outstanding
	def update_voucher_outstanding(self):
		# Clear outstanding
		self.clear_outstanding()

		against_voucher = sql("select against_voucher, against_voucher_type from `tabGL Entry` where fiscal_year=%s and is_cancelled='No' and company=%s group by against_voucher, against_voucher_type", (self.doc.name, self.doc.company))
		for d in against_voucher:
			# get voucher balance
			bal = sql("select sum(debit)-sum(credit) from `tabGL Entry` where against_voucher=%s and against_voucher_type=%s", (d[0], d[1]))
			bal = bal and flt(bal[0][0]) or 0.0
			if d[1] == 'Payable Voucher':
				bal = -bal
			# set voucher balance
			sql("update `tab%s` set outstanding_amount=%s where name='%s'"% (d[1], bal, d[0]))

	# ====================================================================================
	# Generate periods
	def create_periods(self):
		get_obj('Period Control').generate_periods(self.doc.name)

	# on update
	def on_update(self):
		if not self.doc.is_fiscal_year_closed:
			self.is_fiscal_year_closed = 'No'
			self.doc.save()
		self.create_periods()