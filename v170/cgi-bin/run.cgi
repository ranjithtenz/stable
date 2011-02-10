#!/usr/bin/python

try:

	import sys, os
	
	sys.path.append(os.getcwd()+'/cgi-bin')

	def getTraceback():
		import sys, traceback, string
		type, value, tb = sys.exc_info()
		body = "Traceback (innermost last):\n"
		list = traceback.format_tb(tb, None) \
			+ traceback.format_exception_only(type, value)
		body = body + "%-20s %s" % (string.join(list[:-1], ""), list[-1])
		return body
		
	import webnotes.handler
		
except Exception, e:
	print "Content-Type: text/html"
	try:
		out = {'message':'', 'exc':getTraceback().replace('\n','<br>')}
	except:
		out = {'exc': e}
	print
	print str(out)