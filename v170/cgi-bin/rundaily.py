import server

cp = server.get_obj('Control Panel')

if has_attr(cp, 'run_daily'):
	cp.run_daily()