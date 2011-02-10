#!/usr/bin/python

import cgi
import datetime
import os

try:

	# Traceback
	# ---------
	def getTraceback():
		import sys, traceback, string
		type, value, tb = sys.exc_info()
		body = "Traceback (innermost last):\n"
		list = traceback.format_tb(tb, None) \
			+ traceback.format_exception_only(type, value)
		body = body + "%-20s %s" % (string.join(list[:-1], ""), list[-1])
		return body
	
	
	form = cgi.FieldStorage()
			
	plugins = form.getvalue("plugins", "").split(",")
	languages = form.getvalue("languages", "").split(",")
	themes = form.getvalue("themes", "").split(",")
	isJS = form.getvalue("js", "") == "true"
	compress = form.getvalue("compress", "true") == "true"
	suffix = form.getvalue("suffix", "") == "_src" and "_src" or ""
	
	# headers and content
	# -------------------
	headers = []
	content = []
	
	headers.append("Content-Type: text/javascript")
	
	# file content
	# ------------
	def get_file_contents(filename):
		try:
			f = open(os.path.join('', filename))
			try:
				return f.read()
			finally:
				f.close()
		except IOError,e:
			return ""
			
	# Compress String
	# ---------------
	def compress_string(buf):
		import gzip, cStringIO
		zbuf = cStringIO.StringIO()
		zfile = gzip.GzipFile(mode = 'wb',  fileobj = zbuf, compresslevel = 5)
		zfile.write(buf)
		zfile.close()
		return zbuf.getvalue()
	
	# Add core, with baseURL added
	content.append(get_file_contents("tiny_mce%s.js" % suffix).replace(
	            "tinymce._init();", "tinymce.baseURL='js/tiny_mce';tinymce._init();"))
	
	# Patch loading functions
	content.append("tinyMCE_GZ.start();")
	
	# Add core languages
	for lang in languages:
		content.append(get_file_contents("langs/%s.js" % lang))
	
	# Add themes
	for theme in themes:
		content.append(get_file_contents("themes/%s/editor_template%s.js" % (theme, suffix)))
	
		for lang in languages:
			content.append(get_file_contents("themes/%s/langs/%s.js" % (theme, lang)))
	
	# Add plugins
	for plugin in plugins:
		content.append(get_file_contents("plugins/%s/editor_plugin%s.js" % (plugin, suffix)))
	
		for lang in languages:
			content.append(get_file_contents("plugins/%s/langs/%s.js" % (plugin, lang)))
	
	
	# Restore loading functions
	content.append("tinyMCE_GZ.end();")
	
	# Compress
	# --------
	if compress:
		content = compress_string(''.join(content))
		headers.append('Content-Encoding: gzip')
		headers.append('Content-Length: ' + str(len(content)))
	
	# Print Everything
	# ----------------
	for t in headers:
		print t
	
	print
	
	print content

except Exception, e:
	print "Content-Type: text/html"
	try:
		out = {'message':'', 'exc':getTraceback().replace('\n','<br>')}
	except:
		out = {'exc': e}
	print
	print str(out)