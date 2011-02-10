class DocType:
	def __init__(self,d,dl):
		self.doc, self.doclist = d, dl

	def add_comment(self,args):
		import time
		args = eval(args)
		if(args['cmt']):
			cmt = Document('Comment Widget Record')
			cmt.comment = args['cmt']
			cmt.comment_by = args['cmt_by']
			cmt.comment_doctype = args['dt']
			cmt.comment_docname = args['dn']
			cmt.comment_date = nowdate()
			cmt.comment_time = time.strftime('%H:%M')
			cmt.save(1)
		else:
			raise Exception

	def remove_comment(self,cmt_id):
		sql("delete from `tabComment Widget Record` where name=%s",cmt_id)