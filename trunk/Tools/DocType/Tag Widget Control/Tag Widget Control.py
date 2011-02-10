class DocType:
    def __init__(self,d,dl):
        self.doc = d
        self.doclist = dl
        
    def add_tag(self,arg):
        arg = eval(arg)
        main_lst = []
        tag_lst = arg['tag'].split(',')

        for t in tag_lst:
            t = t.strip(' ').title()
            if t:
                name = sql("select name from tabTag where name = %s", t)
                name = name and name[0][0] or ''
                if name:
                    parent = name
                else:
                    nt = Document('Tag')
                    nt.tag_name = t
                    nt.save(1)
                    parent = nt.name
                
                if(sql("select name from `tabTag Detail` where tag_doctype = %s and tag_docname = %s  and parent = %s",(arg['dt'], arg['dn'], parent))):
                    pass
                else:
                    td = Document('Tag Detail')
                    td.tag_doctype = arg['dt']
                    td.tag_docname = arg['dn']
                    td.tag_by = arg['tag_by']
                    td.parent = parent
                    td.parenttype = 'Tag'
                    td.parentfield = 'tag_details'
                    td.save(1)
        
    def get_tags(self,arg):
        arg = eval(arg)
        ret = {}
        ret['tag_lst'] = convert_to_lists(sql("select parent, tag_by from `tabTag Detail` where tag_doctype = %s and tag_docname = %s",(arg['dt'], arg['dn'])))
        return ret
        
    def get_my_tags(self,arg):
        arg = eval(arg)
        ret = {}
        ret['tag_lst'] = convert_to_lists(sql("select distinct t1.parent from `tabTag Detail` t1, `tabTag` t2 where (t1.tag_by = %s) or (t2.owner = %s and t1.parent = t2.name)", (arg['tag_by'], arg['tag_by'])))
        return ret
        
    def delete_tag(self,arg):
        arg = eval(arg)
        sql("delete from `tabTag Detail` where parent = %s and tag_by = %s and tag_doctype = %s and tag_docname = %s",(arg['tag'],arg['tag_by'],arg['dt'],arg['dn']))
        
    def get_all_tags(self,arg):
        arg = eval(arg)
        res = sql("select name from tabTag where name not in (select distinct parent from `tabTag Detail` where tag_doctype='%s' and tag_docname ='%s' and parent like '%s%%') and name like '%s%%'" % (arg['dt'], arg['dn'], arg['last_txt'], arg['last_txt']))
        res = [{'id':r[0], 'value':r[0], 'info':''} for r in res]
        return {'results':res}