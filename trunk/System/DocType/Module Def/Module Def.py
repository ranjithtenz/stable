class DocType:
	def __init__(self,d,dl):
		self.doc, self.doclist = d,dl
		
	def on_update(self):
		if not getlist(self.doclist,'items') and not self.doc.widget_code:
			obj = Document(self.doc.doctype, self.doc.name)
			
			doc_type = [['DocType','name','name','Forms',"(istable is null or istable=0) and (issingle is null or issingle=0)"],['Page','name','page_name','Pages','(show_in_menu=1 or show_in_menu=0)'],['Search Criteria','doc_type','criteria_name','Reports',"(disabled is null or disabled=0)"]]
			for dt in doc_type:
				dn = [[d[0] or '', d[1] or ''] for d in sql("select %s,%s from `tab%s` where module = '%s' and %s" % (dt[1],dt[2],dt[0],self.doc.name,dt[4]))]

				if dn:
					r = addchild(obj,'items','Module Def Item',1)
					r.doc_type = 'Separator'
					r.doc_name = dt[3]
					r.save(1)

					for d in dn:
						r = addchild(obj,'items','Module Def Item',1)
						r.doc_type = dt[3]
						r.doc_name = d[0]
						r.display_name = d[1]
						r.save(1)