# -------------------
# Email class:
# Sends email via outgoing server specified in "Control Panel"
# Allows easy adding of Attachments of "File" objects
# -------------------

from webnotes import msgprint

class EMail:
	def __init__(self, sender='', recipients=[], subject=''):
		from email.mime.multipart import MIMEMultipart
		if type(recipients)==str:
			recipients.replace(';', ',')
			recipients = recipients.split(',')
			
		self.sender = sender
		self.reply_to = sender
		self.recipients = recipients
		self.subject = subject
		self.msg = MIMEMultipart()
		self.cc = []
		
	def set_message(self, message, mime_type='text/html'):
		from email.mime.text import MIMEText
		
		maintype, subtype = mime_type.split('/')
		msg = MIMEText(message, _subtype = subtype)
		self.msg.attach(msg)
		
	def attach(self, n):
		import webnotes.utils		
		res = webnotes.utils.get_file(n)
		if not res:
			self.msg.attach('Sender tried to attach an unknown file id: ' + n)
	
		from email.mime.audio import MIMEAudio
		from email.mime.base import MIMEBase
		from email.mime.image import MIMEImage
		from email.mime.text import MIMEText
			
		fname = res[0][0]
		fcontent = res[0][1]
		fmodified = res[0][2]
		
		import mimetypes

		ctype, encoding = mimetypes.guess_type(fname)
		if ctype is None or encoding is not None:
			# No guess could be made, or the file is encoded (compressed), so
			# use a generic bag-of-bits type.
			ctype = 'application/octet-stream'
		
		maintype, subtype = ctype.split('/', 1)
		if maintype == 'text':
			# Note: we should handle calculating the charset
			msg = MIMEText(fcontent, _subtype=subtype)
		elif maintype == 'image':
			msg = MIMEImage(fcontent, _subtype=subtype)
		elif maintype == 'audio':
			msg = MIMEAudio(fcontent, _subtype=subtype)
		else:
			msg = MIMEBase(maintype, subtype)
			msg.set_payload(fcontent)
			# Encode the payload using Base64
			from email import encoders
			encoders.encode_base64(msg)
		# Set the filename parameter
		msg.add_header('Content-Disposition', 'attachment', filename=fname)
		self.msg.attach(msg)
	
	def validate(self):
		from webnotes.utils import validate_email_add
		# validate ids
		if self.sender and (not validate_email_add(self.sender)):
			raise Exception, "%s is not a valid email id" % self.sender

		if self.reply_to and (not validate_email_add(self.reply_to)):
			raise Exception, "%s is not a valid email id" % reply_to

		for e in self.recipients:
			if not validate_email_add(e):
				raise Exception, "%s is not a valid email id" % e	
	
	def setup(self):
		import webnotes.model.doc
		from webnotes.utils import cint

		# get defaults from control panel
		cp = webnotes.model.doc.Document('Control Panel','Control Panel')
		self.server = cp.outgoing_mail_server and cp.outgoing_mail_server or mail_server
		self.login = cp.mail_login and cp.mail_login or mail_login
		self.port = cp.mail_port and cp.mail_port or None
		self.password = cp.mail_password and cp.mail_password or mail_password
		self.use_ssl = cint(cp.use_ssl)
	
	def send(self):
		from webnotes.utils import cint
		
		self.setup()
		self.validate()
		
		import smtplib
		sess = smtplib.SMTP(self.server, self.port or None)
		
		if self.use_ssl: 
			sess.ehlo()
			sess.starttls()
			sess.ehlo()
			
		ret = sess.login(self.login, self.password)

		# check if logged correctly
		if ret[0]!=235:
			msgprint(ret[1])
			raise Exception
		
		self.msg['Subject'] = self.subject
		self.msg['From'] = self.sender
		self.msg['To'] = ', '.join([r.strip() for r in self.recipients])
		self.msg['Reply-To'] = self.reply_to
		if self.cc:
			self.msg['CC'] = ', '.join([r.strip() for r in self.cc])
				
		sess.sendmail(self.sender, self.recipients, self.msg.as_string())
		
		try:
			sess.quit()
		except:
			pass
	
def sendmail(recipients, sender='', msg='', subject='[No Subject]', parts=[], cc=[], attach=[]):
	import webnotes	
	
	if not sender:
		sender = webnotes.conn.get_value('Control Panel',None,'auto_email_id')
	email = EMail(sender, recipients, subject)
	email.cc = cc
	if msg: email.set_message(msg)
	for p in parts:
		email.set_message(p[1])
	for a in attach:
		email.attach(a)

	c = webnotes.app_conn or webnotes.conn
	email.set_message(c.get_value('Control Panel',None,'mail_footer') or '<div style="font-family: Arial; border-top: 1px solid #888; padding-top: 8px">Powered by <a href="http://www.erpnext.com">erpnext</a></div>')
	email.send()

def get_contact_list():
	import webnotes

	cond = ['`%s` like "%s%%"' % (f, webnotes.form.getvalue('txt')) for f in webnotes.form.getvalue('where').split(',')]
	cl = webnotes.conn.sql("select `%s` from `tab%s` where %s" % (
  			 webnotes.form.getvalue('select')
			,webnotes.form.getvalue('from')
			,' OR '.join(cond)
		)
	)
	webnotes.response['cl'] = filter(None, [c[0] for c in cl])

# Send Form
# ----------
def send_form():
	import webnotes
	from webnotes.utils import cint

	form = webnotes.form

	recipients = form.getvalue('sendto')
	subject = form.getvalue('subject')
	sendfrom = form.getvalue('sendfrom')
	
	# get attachments
	al = []
	if cint(form.getvalue('with_attachments')):
		try:
			al = webnotes.conn.sql('select file_list from `tab%s` where name="%s"' % (form.getvalue('dt'), form.getvalue('dn')))
			if al:
				al = (al[0][0] or '').split('\n')
		except Exception, e:
			if e.args[0]==1146:
				pass # no attachments in single types!
			else:
				raise Exception, e
	if recipients:
		recipients = recipients.replace(';', ',')
		recipients = recipients.split(',')
		update_contacts(recipients)

		if not sendfrom:
			sendfrom = webnotes.conn.get_value('Control Panel',None,'auto_email_id')
		email = EMail(sendfrom, recipients, subject)
		email.cc = [form.getvalue('cc'),]

		if form.getvalue('message'):
			email.set_message(form.getvalue('message') or 'No text')
		email.set_message(form.getvalue('body'))
	
		# footer
		c = webnotes.app_conn or webnotes.conn
		email.set_message(c.get_value('Control Panel',None,'mail_footer') or '<div style="font-family: Arial; border-top: 1px solid #888; padding-top: 8px">Powered by <a href="http://www.erpnext.com">erpnext</a></div>')
		
		for a in al:
			if a:
				email.attach(a.split(',')[0])

		email.send()
	webnotes.msgprint('Sent')

# Add to Contacts
# ---------------

def update_contacts(recipients):
	import webnotes
	from webnotes.model.doc import Document
	
	for r in recipients:
		r = r.strip()
		try:
			if not webnotes.conn.sql("select email_id from tabContact where email_id=%s", r):
				d = Document('Contact')
				d.email_id = r
				d.save(1)
		except Exception, e:
			if e.args[0]==1146: pass # no table
			else: raise e
