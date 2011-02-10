import webnotes
import webnotes.utils

class FrameworkServer:
	def __init__(self, remote_host, path, user='', password='', account='', cookies={}, opts={}, https = 0):
		# validate
		if not (remote_host and path):
			raise Exception, "Server address and path necessary"

		if not ((user and password) or (cookies)):
			raise Exception, "Either cookies or user/password necessary"
	
		self.remote_host = remote_host
		self.path = path
		self.cookies = cookies
		self.webservice_method='POST'
		self.account = account
		self.account_id = None
		self.https = https

		# login
		if not cookies:
			args = { 'usr': user, 'pwd': password, 'acx': account }
			
			for key in opts: # add additional keys
				args[key] = opts[key]
			
			res = self.http_get_response('login', args)
		
			ret = res.read()
			try:
				ret = eval(ret)
			except Exception, e:
				webnotes.msgprint(ret)
				raise Exception, e
				
			if ret.get('message') and ret.get('message')!='Logged In':
				raise Exception, ret.get('message')
				
			if ret.get('exc'):
				raise Exception, ret.get('exc')
				
			self._extract_cookies(res)

			self.account_id = cookies.get('account_id')
			self.app_id = cookies.get('app_id')
			self.sid = cookies.get('sid')
			
			self.login_response = ret
				
	def http_get_response(self, method, args):
		# get response from remote server
	
		import httplib, urllib		

		args['cmd'] = method

		headers = {}
		if self.cookies:
			headers['Cookie'] = webnotes.utils.dict_to_str(self.cookies, '; ')
	
		if self.webservice_method == 'POST':
			headers["ENCTYPE"] =  "multipart/form-data"
			headers["Accept"] = "text/plain, text/html, */*"
			headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
		
		if self.https:
			conn = httplib.HTTPSConnection(self.remote_host)	
		else:
			conn = httplib.HTTPConnection(self.remote_host)	
			
		import os
		conn.request(self.webservice_method, os.path.join(self.path, "index.cgi"), urllib.urlencode(args), headers=headers)
	
		return conn.getresponse()
	
	def _extract_cookies(self, res):
		h = res.getheader('set-cookie')
		if h:
			cl = h.split(';')
			for c in cl:
				if c:
					t = c.split('=')
					if len(t)==2:
						self.cookies[t[0].strip(', ')] = t[1].strip()

	def runserverobj(self, doctype, docname, method, arg=''):
		res = self.http_get_response('runserverobj', args = {
			'doctype':doctype
			,'docname':docname
			,'method':method
			,'arg':arg
		})
		return eval(res.read())
