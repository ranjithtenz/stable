// Navigation Object

var nav_obj = {}

nav_obj.observers = [];
nav_obj.add_observer = function(o) { nav_obj.observers.push(o); }

nav_obj.ol = [];
nav_obj.open_notify = function(t, dt, dn) {
	// last should not be this (refresh)
	if(nav_obj.length) {
		var tmp = nav_obj[nav_obj.length-1];
		if(tmp[0]==t && tmp[1]==dt && tmp[2]==dn) return;
	}

	// remove from list (if exists)
	var tmp = [];
	for(var i in nav_obj.ol)
		if(!(nav_obj.ol[i][0]==t && nav_obj.ol[i][1]==dt && nav_obj.ol[i][2]==dn)) tmp.push(nav_obj.ol[i]);
	nav_obj.ol = tmp;

	// add to top
	nav_obj.ol.push([t, dt, dn])	
	
	// add to "back" history
	t = encodeURIComponent(t);
	dt = encodeURIComponent(dt);
	if(dn)dn = encodeURIComponent(dn);
	
	var id = t+'/'+ dt + (dn ? ('/'+dn): '')
	
	// option to add to analytics engine
	if(nav_obj.on_open)
		nav_obj.on_open(id);
	
	dhtmlHistory.add(id,'');
	
	// notify observers (for menu?)
	for(var i=0; i<nav_obj.observers.length; i++) {
		var o = nav_obj.observers[i];
		if(o && o.notify) o.notify(t, dt, dn);
	}
}

nav_obj.rename_notify = function(dt, oldn, newn) {
	for(var i=0;i<nav_obj.ol.length;i++) {
		var o = nav_obj.ol[i];
		if(o[1]==dt && o[2]==oldn) o[2]=newn;
	}
} 

nav_obj.show_last_open = function() {
	var l = nav_obj.ol[nav_obj.ol.length-2];
	delete nav_obj.ol[nav_obj.ol.length-1]; // delete current open

	if(!l) loadpage('_home');
	else if(l[0]=='Page') { 
		loadpage(l[1]);
	} else if(l[0]=='Report') {
		loadreport(l[1],l[2]);
	} else if(l[0]=='Form') {
		loaddoc(l[1],l[2]);
	} else if(l[0]=='DocBrowser') {
		loaddocbrowser(l[1]);
	}
}

var _history_current;

function history_get_name(t) {
	var parts = [];
	if(t.length>=3) {
		// combine all else
		for(var i=2; i<t.length; i++) {
			parts.push(t[i]);
		}
	}
	return parts.join('/')
}

function historyChange(newLocation, historyData) {
	t = newLocation.split('/');

	for(var i=0;i<t.length;i++) 
		t[i] = decodeURIComponent(t[i]);

	// re-opening the same page?
	if(nav_obj.ol.length) {
		var c = nav_obj.ol[nav_obj.ol.length-1];

		if(t.length==2)	{
			if(c[0]==t[0] && c[1]==t[1]) return;
		} else {
			if(c[0]==t[0] && c[1]==t[1] && c[2]==t[2]) return;
		}
	}
	
	if(t[2])
		var docname = history_get_name(t);
	
	if(t[0]=='Form') {
		_history_current = newLocation;
		if(docname.substr(0, 3)=='New') {
			newdoc(t[1]);
		} else {
			loaddoc(t[1], docname);
		}
	} else if(t[0]=='Report') {
		_history_current = newLocation;
		loadreport(t[1], docname);
	} else if(t[0]=='Page') {
		_history_current = newLocation;
		loadpage(t[1]);
	} else if(t[0]=='Application') {
		_history_current = newLocation;
		loadapp(t[1]);
	} else if(t[0]=='DocBrowser') {
		_history_current = newLocation;
		loaddocbrowser(t[1]);
	} 
};
