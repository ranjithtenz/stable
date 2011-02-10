class DocType:
	def __init__(self, doc, doclist=[]):
		self.doc = doc
		self.doclist = doclist
		
	def on_update(self):
		msgprint("here")
		return

		cp = Document('Control Panel', 'Control Panel')
		sys_man = cp.support_email or cp.system_manager_email
		if not sys_man:
			sys_man = 'support@notesandreports.com'
			
		msg = '''
A new ticket has been updated

once more

A/c: %s
Ticket Number: %s
Subject: %s
Created by: %s
Status: %s

''' % (cp.account_id, self.doc.name, self.doc.subject, self.doc.owner, self.doc.status)

		sendmail([sys_man], subject='%s: Ticket Updated: %s' % (cp.account_id, self.doc.name), parts=[['text/plain', msg]])