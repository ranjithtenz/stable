# to generate sitemaps

frame_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s
</urlset>"""

# generate the sitemap XML
def generate_xml(conn, site_prefix):
	global frame_xml
	import urllib

	# settings
	max_doctypes = 10
	max_items = 1000
	
	site_map = ''
	
	if site_prefix:
		# list of all Guest pages (static content)
		for r in conn.sql("SELECT tabPage.name, tabPage.modified FROM `tabPage Role`, tabPage WHERE `tabPage Role`.role='Guest' AND `tabPage Role`.parent = tabPage.name ORDER BY tabPage.modified DESC"):
			site_map += '\n<url><loc>%s?page=Page/%s</loc><lastmod>%s</lastmod></url>' % (site_prefix, urllib.quote(r[0]), r[1].strftime('%Y-%m-%d'))
		
		# list of all Records that are viewable by guests (Blogs, Articles etc)
		for dt in conn.sql("SELECT DISTINCT tabDocPerm.parent FROM `tabDocPerm`, tabDocType WHERE tabDocPerm.role='Guest' AND IFNULL(tabDocPerm.`read`,0) = 1 AND IFNULL(tabDocPerm.`permlevel`,0) = 0 AND tabDocType.name = tabDocPerm.parent and IFNULL(tabDocType.issingle,0) != 1 LIMIT %s" % max_doctypes):
			
			for d in conn.sql("SELECT name, modified FROM `tab%s` WHERE docstatus != 2 ORDER BY modified DESC LIMIT %s" % (dt[0], max_items)):
			
				site_map += '\n<url><loc>%s?page=Form/%s/%s</loc><lastmod>%s</lastmod></url>' % (site_prefix, dt[0], urllib.quote(d[0]), d[1].strftime('%Y-%m-%d'))

	return frame_xml % site_map