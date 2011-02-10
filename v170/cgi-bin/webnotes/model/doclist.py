import webnotes
import webnotes.model
import webnotes.model.doc

def xzip(a,b):
	d = {}
	for i in range(len(a)):
		d[a[i]] = b[i]
	return d
	
def expand(docs):
	import string
	try:
		import json
	except:
		import simplejson as json # python 2.4

	docs = json.loads(docs)
	clist = []
	for d in docs['_vl']:
		doc = xzip(docs['_kl'][d[0]], d);
		clist.append(doc)
	return clist

def compress(doclist):
	if doclist and hasattr(doclist[0],'fields'):
		docs = [d.fields for d in doclist]
	else:
		docs = doclist
		
	kl, vl = {}, []
	for d in docs:
		dt = d['doctype']
		if not (dt in kl.keys()):
			fl = d.keys()
			forbidden = ['server_code_compiled']
			nl = ['doctype','localname','__oldparent','__unsaved']
			for f in fl:
				if not (f in nl) and not (f in forbidden):
					nl.append(f)
			kl[dt] = nl

		## values
		fl = kl[dt]
		nl = []
		for f in fl:
			v = d.get(f)

			if type(v)==long:
				v=int(v)
			nl.append(v)
		vl.append(nl)
	#errprint(str({'_vl':vl,'_kl':kl}))
	return {'_vl':vl,'_kl':kl}

# Get Children List (for scripts utility)
# ---------------------------------------

def getlist(doclist, field):
	l = []
	for d in doclist:
		if d.parent and (not d.parent.lower().startswith('old_parent:')) and d.parentfield == field:
			l.append(d)
	return l

# Copy doclist
# ------------

def copy_doclist(doclist, no_copy = []):
	from webnotes.model.doc import Document
	
	cl = []
	
	# main doc
	c = Document(fielddata = doclist[0].fields.copy())
	
	# clear no_copy fields
	for f in no_copy: 
		if c.fields.has_key(f):
			c.fields[f] = None
	
	c.name = None
	c.save(1)
	cl.append(c)
	
	# new parent name
	parent = c.name
	
	# children
	for d in doclist[1:]:
		c = Document(fielddata = d.fields.copy())
		c.name = None
		
		# clear no_copy fields
		for f in no_copy: 
			if c.fields.has_key(f):
				c.fields[f] = None

		c.parent = parent
		c.save(1)
		cl.append(c)

	return cl

# Validate Multiple Links
# -----------------------

def validate_links_doclist(doclist):
	ref, err_list = {}, []
	for d in doclist:
		if not ref.get(d.doctype):
			ref[d.doctype] = d.make_link_list()
			
		err_list += d.validate_links(ref[d.doctype])
	return ', '.join(err_list)
	
# Get list of field values
# ------------------------

def getvaluelist(doclist, fieldname):
	l = []
	for d in doclist:
		l.append(d.fields[fieldname])
	return l

def _make_html(doc, link_list):

	from webnotes.utils import cstr
	out = '<table class="simpletable">'
	for k in doc.fields.keys():
		if k!='server_code_compiled':		
			v = cstr(doc.fields[k])
			
			# link field
			if v and (k in link_list.keys()):
				dt = link_list[k]
				if type(dt)==str and dt.startswith('link:'):
					dt = dt[5:]
				v = '<a href="index.cgi?page=Form/%s/%s">%s</a>' % (dt, v, v) 
				
			out += '\t<tr><td>%s</td><td>%s</td></tr>\n' % (cstr(k), v)
		
	out += '</table>'
	return out

def to_html(doclist):
	out = ''
	link_lists = {}
	
	for d in doclist:
		if not link_lists.get(d.doctype):
			link_lists[d.doctype] = d.make_link_list()

		out += _make_html(d, link_lists[d.doctype])
		
	return out
	