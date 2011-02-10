# Notification control
class DocType:
	def __init__(self,d,dl):
		self.doc, self.doclist = d,dl

	# get message to load in custom text
	# ----------------------------------
	def get_message(self, arg):
		fn = arg.lower().replace(' ', '_') + '_message'
		v = sql("select value from tabSingles where field=%s and doctype=%s", (fn, 'Notification Control'))
		return v and v[0][0] or ''

	# set custom text
	# ---------------
	def set_message(self, arg=''):
		fn = self.doc.select_transaction.lower().replace(' ', '_') + '_message'
		set(self.doc, fn, self.doc.custom_message)
		msgprint("Custom Message for %s updated!" % self.doc.select_transaction)

	# notify contact
	# --------------
	def notify_contact(self, key, dt, dn, contact_email, contact_nm):

		if contact_email:
			dt_small = dt.replace(' ','_').lower()

			if cint(self.doc.fields.get(dt_small)):
				self.send_notification(key, dt, dn, contact_email, contact_nm)
			
	# send notification
	def send_notification(self, key, dt, dn, contact_email, contact_nm):
		import webnotes.utils.encrypt
		import os
		
		cp = Document('Control Panel', 'Control Panel')
		
		banner = cp.client_name

		sender_nm = sql("select concat_ws(' ', first_name, last_name) from tabProfile where name = %s", session['user'])[0][0] or ''
		
		if contact_nm:
			contact_nm = ' ' + contact_nm
		else:
			contact_nm = ''
		
		msg = '''
					<div style="padding:16px; border:8px solid #eef; width:580px;">
						<div style="border-bottom:2px solid #eef">%(company_banner)s</div>
						<div style="margin-top:16px;">
							<p>Hi%(contact)s,</p><br>
							<p>%(message)s</p><br>
							<p><a href="http://%(domain)s/?page=Form/%(dt)s/%(dn)s&ac_name=%(account)s&akey=%(akey)s">Click here to see the document.</a></p><br>
							<p>Thanks, <br><br>%(sent_by)s<br>%(company_name)s</p>
						</div>
					</div>
		''' % {
			'company_banner': banner, 
			'contact': contact_nm, 
			'message': self.doc.fields[key.lower().replace(' ','_')+'_message'],
			'sent_by': sender_nm, 
			'company_name':cp.company_name,
			'dt': dt.replace(' ', '%20'),
			'dn': dn.replace('/', '%2F'),
			'domain': os.environ.get('HTTP_HOST'),
			'account': cp.account_id,
			'akey': webnotes.utils.encrypt.encrypt(dn)
		}

		if not validate_email_add(session['user']):
			sender = "automail@webnotestech.com"
		else:
			sender = session['user']
		
		rec_lst = [contact_email, sender]
		subject = cp.company_name + ' - ' + dt

		sendmail(rec_lst, sender, msg, subject)