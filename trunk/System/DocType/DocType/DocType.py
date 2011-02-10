class DocType:
	def __init__(self, doc, doclist):
		self.doc = doc
		self.doclist = doclist

		
	def change_modified_of_parent(self):
		parent_list = sql('SELECT parent from tabDocField where fieldtype="Table" and options="%s"' % self.doc.name)
		for p in parent_list:
			sql('UPDATE tabDocType SET modified="%s" WHERE `name`="%s"' % (now(), p[0]))

	def scrub_field_names(self):
		restricted = ('name','parent','idx','owner','creation','modified','modified_by','parentfield','parenttype')
		for d in self.doclist:
			if d.parent and d.fieldtype:
				if (not d.fieldname) and (d.fieldtype.lower() in ('data', 'select', 'int', 'float', 'currency', 'table', 'text', 'link', 'date', 'code', 'check', 'read only', 'small_text', 'time')):
					d.fieldname = d.label.strip().lower().replace(' ','_')
					if d.fieldname in restricted:
						d.fieldname = d.fieldname + '1'
					set(d, 'fieldname', d.fieldname)

	def compile_code(self):
		if self.doc.server_code or self.doc.server_code_core:
			import marshal
			try:
				code = compile(cstr(self.doc.server_code_core) + NEWLINE + cstr(self.doc.server_code), '<string>', 'exec')
				set(self.doc, 'server_code_compiled', marshal.dumps(code))
			except:
				pass
	
	def set_version(self):
		self.doc.version = cint(self.doc.version) + 1

	def validate(self):
		self.set_version()
				
	def on_update(self):
		self.scrub_field_names()
		if self.doc.server_code:
			self.doc.server_code_error = '<pre style="text-align: left;">' + check_syntax(cstr(self.doc.server_code_core) + NEWLINE + cstr(self.doc.server_code)) + '</pre>'
		self.change_modified_of_parent()
		self.compile_code()