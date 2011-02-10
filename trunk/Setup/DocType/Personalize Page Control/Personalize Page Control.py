class DocType:
	def __init__(self,d,dl):
		self.doc, self.doclist = d,dl

	#---upload image----
	def save_file(self, fdata, fname, compress=0):
		import webnotes.utils.file_manager
		
		blob = fdata.file.read()

		#create thumbnails
		if compress:
			blob = self.create_thumbnail(60,blob)

		return webnotes.utils.file_manager.save_file(fname, blob)

	# upload files
	def upload_many(self,form):
	
		# get for details
		host = form.getvalue('host')
		acx = form.getvalue('acx')
		is_banner = form.getvalue('form_name') == 'banner_options'
		fname = is_banner and 'pp_banner_60.gif' or 'pp_letter_head.gif' 

		# save
		if form.getvalue('filedata'):
			self.save_file(form['filedata'], fname, is_banner)
			html = '<div><img src="cgi-bin/getfile.cgi?name=' + fname + '&acx=' + acx + (is_banner and '" height="60px"/>' or '"') + '</div>'
			webnotes.conn.set_value('Control Panel', None, (is_banner and 'client_name' or 'letter_head'), html)
			return 'File uploaded successfully'
		else:
			return 'No file found'

	def upload_callback(self):
		return 'alert("Done")'

	def create_thumbnail(self,tn,blob):
		from PIL import Image
		import cStringIO

		fobj = cStringIO.StringIO(blob)
		image = Image.open(fobj)
		image.thumbnail((600,tn), Image.ANTIALIAS)
		outfile = cStringIO.StringIO()
		image.save(outfile, 'GIF')
		outfile.seek(0)
		fcontent = outfile.read()
		return fcontent

	# set banner
	def set_banner(self,html=''):
		webnotes.conn.set_value('Control Panel', None, 'client_name', html)

	# set letter head
	def set_letter_head(self,html):
		webnotes.conn.set_value('Control Panel', None, 'letter_head', html)
	
	def update_cp(self,arg):
		arg = eval(arg)
		cp = Document('Control Panel','Control Panel')
		for k in arg:
			cp.fields[k] = arg[k];
		cp.save()

	def remove_banner(self):
		cp = Document('Control Panel','Control Panel')
		if sql("select name from `tabFile Data` where file_name = %s", cp.client_logo):
			sql("delete from `tabFile Data` where file_name = %s", cp.client_logo)

		cp.fields['client_logo'] = ''
		cp.save()

	def get_banner(self):
		cp = Document('Control Panel', 'Control Panel')
		return cp.fields['client_name']

	def get_letter_head(self):
		cp = Document('Control Panel', 'Control Panel')
		return cp.fields['letter_head']