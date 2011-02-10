/* adapted from: Timothy Groves - http://www.brandspankingnew.net */
var cur_autosug;
function hide_autosuggest() { if(cur_autosug)cur_autosug.clearSuggestions(); } 

function AutoSuggest(id, param) {

	this.fld = $i(id);
	if (!this.fld) {return 0; alert('AutoSuggest: No ID');}

	// init variables
	this.init();

	// parameters object
	this.oP = param ? param : {};
	
	// defaults	
	var k, def = {
		minchars:1, meth:"get", varname:"input", className:"autosuggest", timeout:4000
		,delay:1000, offsety:-5, shownoresults: true, noresults: "No results!", maxheight: 250
		,cache: false, maxentries: 25, fixed_options: false, xdelta: 0, ydelta: 5
	}
	
	for (k in def)
	{
		if (typeof(this.oP[k]) != typeof(def[k]))
			this.oP[k] = def[k];
	}
		
	// set keyup handler for field
	// and prevent autocomplete from client
	var p = this;
	
	// NOTE: not using addEventListener because UpArrow fired twice in Safari
	//DOM.addEvent( this.fld, 'keyup', function(ev){ return me.onKeyPress(ev); } );
		
	this.fld.onkeypress 	= function(ev){ if(!(selector && selector.display)) return p.onKeyPress(ev); };
	this.fld.onkeyup 		= function(ev){ if(!(selector && selector.display)) return p.onKeyUp(ev); };
	
	this.fld.setAttribute("autocomplete","off");
};

AutoSuggest.prototype.init = function() {

	this.sInp 	= "";
	this.nInpC 	= 0;
	this.aSug 	= [];
	this.iHigh 	= 0;

}

AutoSuggest.prototype.onKeyPress = function(ev)
{
	
	var key = (window.event) ? window.event.keyCode : ev.keyCode;
	//var ev = (window.event) ? window.event : ev;
	//var key = ev.keyCode ? ev.keyCode : ev.charCode;

	// set responses to keydown events in the field
	// this allows the user to use the arrow keys to scroll through the results
	// ESCAPE clears the list
	// TAB sets the current highlighted value
	//
	var RETURN = 13;
	var TAB = 9;
	var ESC = 27;
		
	var bubble = 1;

	switch(key)
	{
		case TAB:
			this.setHighlightedValue();
			bubble = 0; 
			break;
		case RETURN:
			this.setHighlightedValue();
			bubble = 0; 
			break;
		case ESC:
			this.clearSuggestions(); 
			break;

	}

	return bubble;
}

AutoSuggest.prototype.onKeyUp = function(ev)
{
	
	var key = (window.event) ? window.event.keyCode : ev.keyCode;
	//var ev = (window.event) ? window.event : ev;
	//var key = ev.keyCode ? ev.keyCode : ev.charCode;

	var ARRUP = 38; var ARRDN = 40;
	var bubble = 1;
		
	switch(key) {
		case ARRUP:
			this.changeHighlight(key);
			bubble = 0; 
			break;
			
		case ARRDN:
			this.changeHighlight(key);
			bubble = 0; 
			break;
		default:
			if(key!=13) {
				if(this.oP.fixed_options)
					this.find_nearest(key);
				else
					this.getSuggestions(this.fld.value);
			}
	}
	
	return bubble;
}

AutoSuggest.prototype.clear_user_inp = function() {
	this.user_inp = '';	
}

AutoSuggest.prototype.find_nearest = function (key) {
	var list = this.ul;
	var same_key = 0;

	// make the list
	if (!list) {
		if(this.aSug) {
			this.createList(this.aSug);
		} if(this.aSug[0].value.substr(0,this.user_inp.length).toLowerCase()==String.fromCharCode(key)) {
			this.resetTimeout();
			return;
		}
	}

	// values for multiple keystrokes
	if((this.user_inp.length==1) && this.user_inp == String.fromCharCode(key).toLowerCase()) {
		same_key = 1;
	} else {
		this.user_inp += String.fromCharCode(key).toLowerCase();
	}

	// clear user keys
	window.clearTimeout(this.clear_timer);

	// loop over the next after the current
	var st = this.iHigh;
	
	// continuation of typing, also check the current value
	if(!same_key) st--;
	
	for(var i = st; i<this.aSug.length; i++) {
		if(this.aSug[i].value.substr(0,this.user_inp.length).toLowerCase()==this.user_inp) {
			this.setHighlight(i+1);
			this.resetTimeout();
			return;
		}
	}

	this.clear_timer = window.setTimeout('if(cur_autosug)cur_autosug.clear_user_inp()', 3000);
	
	// begin at the top
	for(var i = 0; i<st; i++) {
		if(this.aSug[i].value.substr(0,this.user_inp.length).toLowerCase()==this.user_inp) {
			this.setHighlight(i+1);
			this.resetTimeout();
			return;
		}
	}
}

AutoSuggest.prototype.getSuggestions = function (val)
{
	// if input stays the same, do nothing
	if (val == this.sInp) return 0;
	
	// kill list
	if(this.body && this.body.parentNode)
		this.body.parentNode.removeChild(this.body);

	this.sInp = val;

	// input length is less than the min required to trigger a request
	// do nothing
	if (val.length < this.oP.minchars)
	{
		this.aSug = [];
		this.nInpC = val.length;
		return 0;
	}
	
	var ol = this.nInpC; // old length
	this.nInpC = val.length ? val.length : 0;

	// if caching enabled, and user is typing (ie. length of input is increasing)
	// filter results out of aSuggestions from last request
	var l = this.aSug.length;
	if (this.nInpC > ol && l && l<this.oP.maxentries && this.oP.cache)
	{
		var arr = [];
		for (var i=0;i<l;i++)
		{
			if (this.aSug[i].value.substr(0,val.length).toLowerCase() == val.toLowerCase())
				arr.push( this.aSug[i] );
		}
		this.aSug = arr;
		
		this.createList(this.aSug);
		return false;
	}
	else
	// do new request
	{
		var me = this;
		var input = this.sInp;
		clearTimeout(this.ajID);
		this.ajID = setTimeout( function() { me.doAjaxRequest(input) }, this.oP.delay );
	}

	return false;
};

AutoSuggest.prototype.doAjaxRequest = function (input)
{
	// check that saved input is still the value of the field
	if (input != this.fld.value)
		return false;

	var me = this;
	
	var q = '';

	this.oP.link_field.set_get_query();
	if(this.oP.link_field.get_query) {
		if(cur_frm)var doc = locals[cur_frm.doctype][cur_frm.docname];
		q = this.oP.link_field.get_query(doc, this.oP.link_field.doctype, this.oP.link_field.docname);
	}
	
	// do ajax request
	this.fld.old_bg = this.fld.style.backgroundColor;
	$y(this.fld, {backgroundColor:'#FFD'});
	$c('webnotes.widgets.search.search_link', args={
		'txt': this.fld.value, 
		'dt':this.oP.link_field.df.options,
		'query':q  }
		, function(r,rt) {
		$y(me.fld, {backgroundColor:(me.fld.old_bg ? me.fld.old_bg : '#FFF')});
		me.setSuggestions(r, rt, input);
	});
	
	return;
};


AutoSuggest.prototype.setSuggestions = function (r, rt, input)
{
	// if field input no longer matches what was passed to the request
	// don't show the suggestions
	if (input != this.fld.value)
		return false;
		
	this.aSug = [];
	
	if (this.oP.json) {
		//var jsondata = eval('(' + req.responseText + ')');
		var jsondata = eval('(' + rt + ')');
		
		for (var i=0;i<jsondata.results.length;i++) {
			this.aSug.push(  { 'id':jsondata.results[i].id, 'value':jsondata.results[i].value, 'info':jsondata.results[i].info }  );
		}
	}
	
	this.createList(this.aSug);
};

AutoSuggest.prototype.createList = function(arr) {
	
	if(cur_autosug && cur_autosug!= this)
		cur_autosug.clearSuggestions();

	this.aSug = arr;
	this.user_inp = '';
	
	var me = this;
	
	var pos = objpos(this.fld); pos.y += this.oP.ydelta; pos.x += this.oP.xdelta;
	if(pos.x <= 0 || pos.y <= 0) return; // field hidden
	
	// get rid of old list and clear the list removal timeout
	if(this.body && this.body.parentNode)
		this.body.parentNode.removeChild(this.body);
		
	this.killTimeout();
	
	// if no results, and shownoresults is false, do nothing
	if (arr.length == 0 && !this.oP.shownoresults)
		return false;
		
	// create holding div
	var div = $ce("div", {className:this.oP.className});
	top_index++;
	div.style.zIndex = 1100;
	div.isactive = 1;

	// create and populate ul
	this.ul = $ce("ul", {id:"as_ul"}); var ul = this.ul;

	// loop throught arr of suggestionscreating an LI element for each suggestion
	for (var i=0;i<arr.length;i++) {
		// format output with the input enclosed in a EM element
		// (as HTML, not DOM)
		//
		var val = arr[i].value;
		
		if(this.oP.fixed_options) {
			var output = val;
		} else {
			var st = val.toLowerCase().indexOf( this.sInp.toLowerCase() );
			var output = val.substring(0,st) + "<em>" + val.substring(st, st+this.sInp.length) + "</em>" + val.substring(st+this.sInp.length);
		}
		var span = $ce("span", {}, output, true);
		span.isactive = 1;
		if (arr[i].info != "")
		{
			var small = $ce("small", {}, arr[i].info);
			span.appendChild(small);
			small.isactive = 1
		}
		
		
		var a = $ce("a", { href:"#" });
		
		a.appendChild(span);
		
		a.name = i+1;
		a.onclick = function (e) { 
			me.setHighlightedValue(); return false; 
		};
		a.onmouseover = function () { me.setHighlight(this.name); };
		a.isactive = 1;
		
		var li = $ce(  "li", {}, a  );

		// empty option
		if(!val) {
			$y(span,{height:'12px'});
		}
		
		ul.appendChild( li );
	}
	
	// no results
	//
	if (arr.length == 0 && this.oP.shownoresults) {
		var li = $ce(  "li", {className:"as_warning"}, this.oP.noresults);
		ul.appendChild( li );
	}
	div.appendChild( ul );
	// get position of target textfield
	// set width of holding div to width of field
	//
	
	var mywid = cint(this.fld.offsetWidth);
	if(this.oP.fixed_options) {
		mywid += 20;
	}
	
	if(cint(mywid) < 100) mywid = 100;
	var left = pos.x - ((mywid - this.fld.offsetWidth)/2);
	if(left<0) {
		mywid = mywid + (left/2); left = 0;
	}
	
	div.style.left 		= left + "px";
	div.style.top 		= ( pos.y + this.fld.offsetHeight + this.oP.offsety ) + "px";
	div.style.width 	= mywid + 'px';

	// set mouseover functions for div
	// when mouse me leaves div, set a timeout to remove the list after an interval
	// when mouse enters div, kill the timeout so the list won't be removed
	//
	div.onmouseover 	= function(){ me.killTimeout() };
	div.onmouseout 		= function(){ me.resetTimeout() };

	// add DIV to document
	//
	//document.getElementsByTagName("body")[0].appendChild(div);	
	popup_cont.appendChild(div);
	
	//height
	if(cint(div.clientHeight) >= this.oP.maxheight) {
		div.original_height = cint(div.clientHeight);
		$y(div,{height: this.oP.maxheight+'px', overflowY:'auto'});
		div.scrollbars = true;
	}

	this.body = div;
	
	if(isIE) {
		$y(div,{border:'1px solid #444'});
	}
	
	// currently no item is highlighted
	//
	
	// if value, then hilight value
	this.iHigh = 0;
	if(this.oP.fixed_options && this.fld.value) {
		for(var i=0; i<this.aSug.length; i++) {
			if(this.aSug[i].value == this.fld.value) {
				this.iHigh = i;
				break;
			}
		}
	}
		
		
	if(!this.iHigh)
		this.changeHighlight(40); // hilight first
	
	// remove list after an interval
	//
	this.resetTimeout();
};

AutoSuggest.prototype.changeHighlight = function(key)
{	
	var list = this.ul;

	if (!list) {
		if(this.aSug) 
			this.createList(this.aSug);
		return false;
	}

	var n;
	if (key == 40)
		n = this.iHigh + 1;
	else if (key == 38)
		n = this.iHigh - 1;

	if (n > list.childNodes.length)
		n = list.childNodes.length;
	if (n < 1)
		n = 1;
	this.setHighlight(n);
};

AutoSuggest.prototype.setHighlight = function(n)
{
	this.resetTimeout();
	var list = this.ul;
	if (!list)
		return false;
	
	if (this.iHigh > 0)
		this.clearHighlight();
	
	this.iHigh = Number(n);
	
	var ele = list.childNodes[this.iHigh-1];
	ele.className = "as_highlight";

	// set scroll
	if(this.body.scrollbars) {
		var cur_y = 0;
		for(var i=0; i<this.iHigh-1; i++)
			cur_y += (isIE ? list.childNodes[i].offsetHeight : list.childNodes[i].clientHeight);
		
		// scroll up
		if(cur_y < this.body.scrollTop)
			this.body.scrollTop = cur_y;
			
		// scroll down
		ff_delta = (isFF ? cint(this.iHigh/2) : 0);
		var h = (isIE ? ele.offsetHeight : ele.clientHeight);
		if(cur_y >= (this.body.scrollTop + this.oP.maxheight - h))
			this.body.scrollTop = cur_y - this.oP.maxheight + h + ff_delta;
	}

	// set it the field (but do not call onchange as this field still has focus)
	if(this.oP.fixed_options) {
		this.fld.value = this.aSug[this.iHigh-1 ].value;
	}
	
};


AutoSuggest.prototype.clearHighlight = function()
{
	var list = this.ul;
	if (!list)
		return false;
	if (this.iHigh > 0) {
		list.childNodes[this.iHigh-1].className = "";
		this.iHigh = 0;
	}
};

AutoSuggest.prototype.setHighlightedValue = function ()
{
	if (this.iHigh) {
		if(this.custom_select)
			this.sInp = this.custom_select(this.fld.value, this.aSug[ this.iHigh-1 ].value);
		else
			this.sInp = this.aSug[ this.iHigh-1 ].value;
		
		// move cursor to end of input (safari)
		//
		try {
			this.fld.focus();
			if (this.fld.selectionStart)
				this.fld.setSelectionRange(this.sInp.length, this.sInp.length);
		} catch(e) { 
			return; // pass
		}

		this.fld.value = this.sInp;

		this.clearSuggestions();
		this.killTimeout();
		
		// pass selected object to callback function, if exists
		//
		if (typeof(this.oP.callback) == "function")
			this.oP.callback( this.aSug[this.iHigh-1] );			
	}
};

AutoSuggest.prototype.killTimeout = function() {
	cur_autosug = this;
	clearTimeout(this.toID);
	clearTimeout(this.clear_timer);
};

AutoSuggest.prototype.resetTimeout = function() {
	cur_autosug = this;
	clearTimeout(this.toID);
	clearTimeout(this.clear_timer);
	this.toID = setTimeout(function () { if(cur_autosug)cur_autosug.clearSuggestions(); }, this.oP.timeout);
};

AutoSuggest.prototype.clearSuggestions = function () {
	this.killTimeout();
	cur_autosug = null;
	var me = this;
	if (this.body) { $dh(this.body); delete this.body; }
	if(this.ul)
		delete this.ul;
	this.iHigh = 0;
	
	// refresh field value (in case not seleted and the suggestions timeout)
	if(this.oP.fixed_options) {
		if(this.fld.field_object && this.fld.field_object.docname) {
			var d = locals[this.fld.field_object.doctype][this.fld.field_object.docname];

			if(this.fld.fieldname) {
				this.fld.value = d[this.fld.fieldname]; // refresh the value
			}
		} else {

		}
	}
	
	// accept the value
	if(this.fld.field_object && !this.oP.fixed_options) {
		// call onchange
		// we do not call onchange from the link field if autosuggest options are open
		this.fld.onchange();
	}
}


/* create element */
$ce = function ( type, attr, cont, html )
{
	var ne = document.createElement( type );
	if (!ne) return 0;

	for (var a in attr) ne[a] = attr[a];
	
	var t = typeof(cont);
	
	if (t == "string" && !html) ne.appendChild( document.createTextNode(cont) );
	else if (t == "string" && html) ne.innerHTML = cont;
	else if (t == "object") ne.appendChild( cont );

	return ne;
};