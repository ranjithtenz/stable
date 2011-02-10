import webnotes
import webnotes.model.doc
import webnotes.model.code

conn = webnotes.app_conn or webnotes.conn

class Page:
	def __init__(self, name):
		self.name = name

	def _page_import(self, match):
		name = match.group('name')

		content = conn.sql('select script from `tabPage` where name=%s', name)
		return content and content[0][0] or ''

	def get_script(self, script):
		import re
		if not script:
			return ''
	
		p = re.compile('\$import\( (?P<name> [^)]*) \)', re.VERBOSE)
		return p.sub(self._page_import, script)

	def load(self):	
		doclist = webnotes.model.doc.get('Page', self.name)
		doc = doclist[0]

		doc.__script = self.get_script(doc.script)
		if doc.fields.get('content') and doc.content.startswith('#python'):
			doc.__content = webnotes.model.code.execute(doc.content)
		return doclist

def get(name):
	return Page(name).load()

def getpage():
	webnotes.response['docs'] = get(webnotes.form.getvalue('name'))