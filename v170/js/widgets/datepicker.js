//----------------------------------------------------------------------------
// Author: Matt Kruse <matt@mattkruse.com>
// WWW: http://www.mattkruse.com/

_c.popup_list = [];
_c.cal_displayed = 0;

_c.MONTH_NAMES=new Array('January','February','March','April','May','June','July','August','September','October','November','December','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
_c.DAY_NAMES=new Array('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sun','Mon','Tue','Wed','Thu','Fri','Sat');
_c.LZ = function(x) {return(x<0||x>9?"":"0")+x}

// _c.formatDate (date_object, format)
// ------------------------------------------------------------------
_c.formatDate = function(date,format) {
	format=format+"";
	var result="";
	var i_format=0;
	var c="";
	var token="";
	var y=date.getYear()+"";
	var M=date.getMonth()+1;
	var d=date.getDate();
	var E=date.getDay();
	var H=date.getHours();
	var m=date.getMinutes();
	var s=date.getSeconds();
	var yyyy,yy,MMM,MM,dd,hh,h,mm,ss,ampm,HH,H,KK,K,kk,k;
	// Convert real date parts into formatted versions
	var value=new Object();
	if (y.length < 4) {y=""+(y-0+1900);}
	value["y"]=""+y;
	value["yyyy"]=y;
	value["yy"]=y.substring(2,4);
	value["M"]=M;
	value["MM"]=_c.LZ(M);
	value["MMM"]=_c.MONTH_NAMES[M-1];
	value["NNN"]=_c.MONTH_NAMES[M+11];
	value["d"]=d;
	value["dd"]=_c.LZ(d);
	while (i_format < format.length) {
		c=format.charAt(i_format);
		token="";
		while ((format.charAt(i_format)==c) && (i_format < format.length)) {
			token += format.charAt(i_format++);
			}
		if (value[token] != null) { result=result + value[token]; }
		else { result=result + token; }
		}
	return result;
	}
	
// Utility functions for parsing in _c.getDateFromFormat()
// ------------------------------------------------------------------

_c._getInt = function(str,i,minlength,maxlength) {
	function _isInteger(val) {
		var digits="1234567890";
		for (var i=0; i < val.length; i++) {
			if (digits.indexOf(val.charAt(i))==-1) { return false; }
			}
		return true;
	}	

	for (var x=maxlength; x>=minlength; x--) {
		var token=str.substring(i,i+x);
		if (token.length < minlength) { return null; }
		if (_isInteger(token)) { return token; }
		}
	return null;
	}

_c.getDateFromFormat = function(val,format) {
	val=val+"";
	format=format+"";
	var i_val=0;
	var i_format=0;
	var c="";
	var token="";
	var token2="";
	var x,y;
	var now=new Date();
	var year=now.getYear();
	var month=now.getMonth()+1;
	var date=1;
	var hh=now.getHours();
	var mm=now.getMinutes();
	var ss=now.getSeconds();
	var ampm="";
	
	while (i_format < format.length) {
		// Get next token from format string
		c=format.charAt(i_format);
		token="";
		while ((format.charAt(i_format)==c) && (i_format < format.length)) {
			token += format.charAt(i_format++);
			}
		// Extract contents of value based on format token
		if (token=="yyyy" || token=="yy" || token=="y") {
			if (token=="yyyy") { x=4;y=4; }
			if (token=="yy")   { x=2;y=2; }
			if (token=="y")    { x=2;y=4; }
			year=_c._getInt(val,i_val,x,y);
			if (year==null) { return 0; }
			i_val += year.length;
			if (year.length==2) {
				if (year > 70) { year=1900+(year-0); }
				else { year=2000+(year-0); }
				}
			}
		else if (token=="MM"||token=="M") {
			month=_c._getInt(val,i_val,token.length,2);
			if(month==null||(month<1)||(month>12)){return 0;}
			i_val+=month.length;}
		else if (token=="dd"||token=="d") {
			date=_c._getInt(val,i_val,token.length,2);
			if(date==null||(date<1)||(date>31)){return 0;}
			i_val+=date.length;}
		else if (token=="mm"||token=="m") {
			mm=_c._getInt(val,i_val,token.length,2);
			if(mm==null||(mm<0)||(mm>59)){return 0;}
			i_val+=mm.length;}
		else {
			if (val.substring(i_val,i_val+token.length)!=token) {return 0;}
			else {i_val+=token.length;}
			}
		}
	// If there are any trailing characters left in the value, it doesn't match
	if (i_val != val.length) { return 0; }
	// Is date valid for month?
	if (month==2) {
		// Check for leap year
		if ( ( (year%4==0)&&(year%100 != 0) ) || (year%400==0) ) { // leap year
			if (date > 29){ return 0; }
			}
		else { if (date > 28) { return 0; } }
		}
	if ((month==4)||(month==6)||(month==9)||(month==11)) {
		if (date > 30) { return 0; }
		}
	// Correct hours value
	if (hh<12 && ampm=="PM") { hh=hh-0+12; }
	else if (hh>11 && ampm=="AM") { hh-=12; }
	var newdate=new Date(year,month-1,date,hh,mm,ss);
	return newdate.getTime();
	}

_c.parseDate = function(val) {
	var preferEuro=(arguments.length==2)?arguments[1]:false;
	generalFormats=new Array('y-M-d','MMM d, y','MMM d,y','y-MMM-d','d-MMM-y','MMM d');
	monthFirst=new Array('M/d/y','M-d-y','M.d.y','MMM-d','M/d','M-d');
	dateFirst =new Array('d/M/y','d-M-y','d.M.y','d-MMM','d/M','d-M');
	var checkList=new Array('generalFormats',preferEuro?'dateFirst':'monthFirst',preferEuro?'monthFirst':'dateFirst');
	var d=null;
	for (var i=0; i<checkList.length; i++) {
		var l=window[checkList[i]];
		for (var j=0; j<l.length; j++) {
			d=_c.getDateFromFormat(val,l[j]);
			if (d!=0) { return new Date(d); }
			}
		}
	return null;
	}


// Position and show the popup, relative to an anchor object
_c.PopupWindow_showPopup = function(anchorname, inputobj) {
	var p = objpos(inputobj);
	this.x = p.x + this.offsetX;
	this.y = p.y + this.offsetY;
		
	if (!this.populated && (this.contents != "")) {
		this.populated = true;
		this.refresh();
		}
	if (this.divObj != null) {
		// Show the DIV object
		this.divObj.style.left = this.x + "px";
		this.divObj.style.top = this.y + "px";
		this.divObj.style.visibility = "visible";
		_c.cal_displayed = 1;
		}
		
	click_observers.push(this);
	this.click_index = click_observers.length - 1;
}
// Hide the popup
_c.PopupWindow_hidePopup = function() {
	if (this.divObj) {
		this.divObj.style.visibility = "hidden";
		_c.cal_displayed = 0;
	}
	else {
		if (this.popupWindow && !this.popupWindow.closed) {
			this.popupWindow.close();
			this.popupWindow = null;
			_c.cal_displayed = 0;			
		}
	}
	if(this.click_index != -1) {
		delete click_observers[this.click_index];
		this.click_index = -1;
	}
}


// Run this immediately to attach the event listener
// CONSTRUCTOR for the PopupWindow object
// Pass it a DIV name to use a DHTML popup, otherwise will default to window popup
_c.PopupWindow = function(parent) {
	//attachListener();
	this.index = _c.popup_list.length;
	_c.popup_list[_c.popup_list.length] = this;
	this.divObj = parent;
	this.popupWindow = null;
	this.width=0;
	this.height=0;
	this.populated = false;
	this.visible = false;
	
	this.contents = "";
	this.url="";
	this.type="DIV";

	this.use_byId = true;
	this.use_css = false;
	this.use_layers = false;
	this.offsetX = 0;
	this.offsetY = 0;
	// Method mappings
	this.populate = function(contents) {
		this.contents = contents;
		this.populated = false;
	};
	this.setUrl = function(url) {
		this.url = url;
	}
	this.refresh = function() {
		if(this.divObj) {
			this.divObj.innerHTML = this.contents;
			this.divObj.style.visibility = "visible";
			_c.cal_displayed = 1;
		}
	}
	this.showPopup = _c.PopupWindow_showPopup;
	this.hidePopup = _c.PopupWindow_hidePopup;
	
	this.setSize =function(width,height) {
		this.width = width;
		this.height = height;
	}
	
	this.hideIfNotClicked = function(e) { this.hidePopup(); };
	
	this.notify_click = function(e, target) {
		if(target.className.substr(0,2)!='cp') {
			this.hidePopup();
		}
	}
	
}

/* SOURCE FILE: CalendarPopup.js */

/* 
DESCRIPTION: This object implements a popup calendar to allow the user to
select a date, month, quarter, or year.
*/ 

// CONSTRUCTOR for the CalendarPopup Object
_c.CalendarPopup = function() {
	var body = document.getElementsByTagName('body')[0]

	var parent = $a(body, 'div', 'caldiv');
	
	var c = new _c.PopupWindow(parent);
	c.setSize(150,175);

	c.offsetX = 0;
	c.offsetY = 25;
	// Calendar-specific properties
	c.monthNames = new Array("January","February","March","April","May","June","July","August","September","October","November","December");
	c.monthAbbreviations = new Array("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");
	c.dayHeaders = new Array("S","M","T","W","T","F","S");
	c.returnFunction = "_c.CP_tmpReturnFunction";
	c.returnMonthFunction = "_c.CP_tmpReturnMonthFunction";
	c.returnQuarterFunction = "_c.CP_tmpReturnQuarterFunction";
	c.returnYearFunction = "_c.CP_tmpReturnYearFunction";
	c.weekStartDay = 0;
	c.isShowYearNavigation = false;
	c.displayType = "date";
	c.disabledDatesExpression = "";
	c.yearSelectStartOffset = 2;
	c.currentDate = null;
	c.todayText="Today";
	c.cssPrefix="";
	window._c.CP_calendarObject = null;
	window._c.CP_targetInput = null;
	window._c.CP_dateFormat = "MM/dd/yyyy";
	// Method mappings
	c.copyMonthNamesToWindow = _c.CP_copyMonthNamesToWindow;
	c.setReturnFunction = _c.CP_setReturnFunction;
	c.setReturnMonthFunction = _c.CP_setReturnMonthFunction;
	c.setReturnQuarterFunction = _c.CP_setReturnQuarterFunction;
	c.setReturnYearFunction = _c.CP_setReturnYearFunction;
	c.setMonthNames = _c.CP_setMonthNames;
	c.setMonthAbbreviations = _c.CP_setMonthAbbreviations;
	c.setDayHeaders = _c.CP_setDayHeaders;
	c.setWeekStartDay = _c.CP_setWeekStartDay;
	c.setDisplayType = _c.CP_setDisplayType;
	c.setYearSelectStartOffset = _c.CP_setYearSelectStartOffset;
	c.setTodayText = _c.CP_setTodayText;
	c.showYearNavigation = _c.CP_showYearNavigation;
	c.showCalendar = _c.CP_showCalendar;
	c.hideCalendar = _c.CP_hideCalendar;
	c.refreshCalendar = _c.CP_refreshCalendar;
	c.getCalendar = _c.CP_getCalendar;
	c.select = _c.CP_select;
	c.setCssPrefix = _c.CP_setCssPrefix;
	c.copyMonthNamesToWindow();
	// Return the object
	return c;
	}
_c.CP_copyMonthNamesToWindow = function() {
	// Copy these values over to the date.js 
	if (typeof(window._c.MONTH_NAMES)!="undefined" && window._c.MONTH_NAMES!=null) {
		window._c.MONTH_NAMES = new Array();
		for (var i=0; i<this.monthNames.length; i++) {
			window._c.MONTH_NAMES[window._c.MONTH_NAMES.length] = this.monthNames[i];
		}
		for (var i=0; i<this.monthAbbreviations.length; i++) {
			window._c.MONTH_NAMES[window._c.MONTH_NAMES.length] = this.monthAbbreviations[i];
		}
	}
}
// Temporary default functions to be called when items clicked, so no error is thrown
var cal_clicked = 0;
_c.CP_tmpReturnFunction = function(y,m,d) { 
	cal_clicked = 1;
	if (window._c.CP_targetInput!=null) {
		var dt = new Date(y,m-1,d,0,0,0);
		if (window._c.CP_calendarObject!=null) { window._c.CP_calendarObject.copyMonthNamesToWindow(); }
		window._c.CP_targetInput.value = _c.formatDate(dt,window._c.CP_dateFormat);
		window._c.CP_targetInput.onchange() // RM - call onchange function
		}
	}

// Set the name of the functions to call to get the clicked item
_c.CP_setReturnFunction = function(name) { this.returnFunction = name; }
_c.CP_setReturnMonthFunction = function(name) { this.returnMonthFunction = name; }
_c.CP_setReturnQuarterFunction = function(name) { this.returnQuarterFunction = name; }
_c.CP_setReturnYearFunction = function(name) { this.returnYearFunction = name; }

// Over-ride the built-in month names
_c.CP_setMonthNames = function() {
	for (var i=0; i<arguments.length; i++) { this.monthNames[i] = arguments[i]; }
	this.copyMonthNamesToWindow();}

// Over-ride the built-in month abbreviations
_c.CP_setMonthAbbreviations = function() {
	for (var i=0; i<arguments.length; i++) { this.monthAbbreviations[i] = arguments[i]; }
	this.copyMonthNamesToWindow();}

// Over-ride the built-in column headers for each day
_c.CP_setDayHeaders = function() {
	for (var i=0; i<arguments.length; i++) { this.dayHeaders[i] = arguments[i]; }
	}

// Set the day of the week (0-7) that the calendar display starts on
// This is for countries other than the US whose calendar displays start on Monday(1), for example
_c.CP_setWeekStartDay = function(day) { this.weekStartDay = day; }

// Show next/last year navigation links
_c.CP_showYearNavigation = function() { this.isShowYearNavigation = (arguments.length>0)?arguments[0]:true; }

// Which type of calendar to display
_c.CP_setDisplayType = function(type) {
	if (type!="date"&&type!="week-end"&&type!="month"&&type!="quarter"&&type!="year") { alert("Invalid display type! Must be one of: date,week-end,month,quarter,year"); return false; }
	this.displayType=type;
	}

// How many years back to start by default for year display
_c.CP_setYearSelectStartOffset = function(num) { this.yearSelectStartOffset=num; }
		
// Set the text to use for the "Today" link
_c.CP_setTodayText = function(text) {this.todayText = text;}

// Set the prefix to be added to all CSS classes when writing output
_c.CP_setCssPrefix = function(val) { this.cssPrefix = val; }

// Hide a calendar object
_c.CP_hideCalendar = function() {
	if (arguments.length > 0) { window._c.popup_list[arguments[0]].hidePopup(); }
	else { this.hidePopup(); }
	}

// Refresh the contents of the calendar display
_c.CP_refreshCalendar = function(index) {
	var calObject = window._c.popup_list[index];
	if (arguments.length>1) { 
		calObject.populate(calObject.getCalendar(arguments[1],arguments[2],arguments[3],arguments[4],arguments[5]));
		}
	else {calObject.populate(calObject.getCalendar());}
	calObject.refresh();
	}

// Populate the calendar and display it
_c.CP_showCalendar = function(anchorname, inputobj) {
	//if (arguments.length>1) {
	//	if (arguments[1]==null||arguments[1]=="") {this.currentDate=new Date();}
	//	else { this.currentDate=new Date(_c.parseDate(arguments[1])); }
	//}
	this.populate(this.getCalendar());
	this.showPopup(anchorname, inputobj); }

// Simple method to interface popup calendar with a text-entry box
_c.CP_select = function(inputobj, linkname, format) {
	var selectedDate=(arguments.length>3)?arguments[3]:null;
	if (inputobj.disabled) { return; } // Can't use calendar input on disabled form input!
	window._c.CP_targetInput = inputobj;window._c.CP_calendarObject = this;
	this.currentDate=null; var time=0;
	if (selectedDate!=null) { time = _c.getDateFromFormat(selectedDate,format) }
	else if (inputobj.value!="") { time = _c.getDateFromFormat(inputobj.value,format); }
	if (selectedDate!=null || inputobj.value!="") {
		if (time==0) { this.currentDate=null; }
		else { this.currentDate=new Date(time); }
	}
	window._c.CP_dateFormat = format;
	
	this.showCalendar(linkname, inputobj); }

// Return a string containing all the calendar code to be displayed
_c.CP_getCalendar = function() {
	var now = new Date();
	// Reference to window
	var windowref = "";
	var result = "";
	// If POPUP, write entire HTML document
	
	result += '<TABLE CLASS="cpBorder" WIDTH=144 BORDER=1 BORDERWIDTH=1 CELLSPACING=0 CELLPADDING=1>\n';
	result += '<TR><TD ALIGN=CENTER><CENTER>\n';
	
	// Code for DATE display (default)
	// -------------------------------
	if (this.displayType=="date" || this.displayType=="week-end") {
		if (this.currentDate==null) { this.currentDate = now; }
		if (arguments.length > 0) { var month = arguments[0]; }
			else { var month = this.currentDate.getMonth()+1; }
		if (arguments.length > 1 && arguments[1]>0 && arguments[1]-0==arguments[1]) { var year = arguments[1]; }
			else { var year = this.currentDate.getFullYear(); }
		var daysinmonth= new Array(0,31,28,31,30,31,30,31,31,30,31,30,31);
		if ( ( (year%4 == 0)&&(year%100 != 0) ) || (year%400 == 0) ) {
			daysinmonth[2] = 29;
			}
		var current_month = new Date(year,month-1,1);
		var display_year = year;
		var display_month = month;
		var display_date = 1;
		var weekday= current_month.getDay();
		var offset = 0;
		
		offset = (weekday >= this.weekStartDay) ? weekday-this.weekStartDay : 7-this.weekStartDay+weekday ;
		if (offset > 0) {
			display_month--;
			if (display_month < 1) { display_month = 12; display_year--; }
			display_date = daysinmonth[display_month]-offset+1;
			}
		var next_month = month+1;
		var next_month_year = year;
		if (next_month > 12) { next_month=1; next_month_year++; }
		var last_month = month-1;
		var last_month_year = year;
		if (last_month < 1) { last_month=12; last_month_year--; }
		var date_class;
		result += "<TABLE WIDTH=144 BORDER=0 BORDERWIDTH=0 CELLSPACING=0 CELLPADDING=0>";
		result += '<TR>\n';
		var refresh = windowref+'_c.CP_refreshCalendar';
		var refreshLink = 'javascript:' + refresh;
		result += '<TD CLASS="cpMonthNavigation" WIDTH="22"><A CLASS="cpMonthNavigation" HREF="'+refreshLink+'('+this.index+','+last_month+','+last_month_year+');">&lt;&lt;</A></TD>\n';
		result += '<TD CLASS="cpMonthNavigation" WIDTH="100"><SPAN CLASS="cpMonthNavigation">'+this.monthNames[month-1]+' '+year+'</SPAN></TD>\n';
		result += '<TD CLASS="cpMonthNavigation" WIDTH="22"><A CLASS="cpMonthNavigation" HREF="'+refreshLink+'('+this.index+','+next_month+','+next_month_year+');">&gt;&gt;</A></TD>\n';

		result += '</TR></TABLE>\n';
		result += '<TABLE style="width:120px" BORDER=0 CELLSPACING=0 CELLPADDING=1 ALIGN=CENTER>\n';
		result += '<TR>\n';
		for (var j=0; j<7; j++) {
			result += '<TD CLASS="cpDayColumnHeader" WIDTH="14%"><SPAN CLASS="cpDayColumnHeader">'+this.dayHeaders[(this.weekStartDay+j)%7]+'</TD>\n';
			}
		result += '</TR>\n';
		for (var row=1; row<=6; row++) {
			result += '<TR>\n';
			for (var col=1; col<=7; col++) {
				var disabled=false;
				var dateClass = "";
				if ((display_month == this.currentDate.getMonth()+1) && (display_date==this.currentDate.getDate()) && (display_year==this.currentDate.getFullYear())) {
					dateClass = "cpCurrentDate";
					}
				else if (display_month == month) {dateClass = "cpCurrentMonthDate";}
				else {dateClass = "cpOtherMonthDate";}
				var selected_date = display_date;
				var selected_month = display_month;
				var selected_year = display_year;
				result += '	<TD CLASS="'+this.cssPrefix+dateClass+'"><A HREF="javascript:'+windowref+this.returnFunction+'('+selected_year+','+selected_month+','+selected_date+');'+windowref+'_c.CP_hideCalendar(\''+this.index+'\');" CLASS="'+this.cssPrefix+dateClass+'">'+display_date+'</A></TD>\n';
				display_date++;
				if (display_date > daysinmonth[display_month]) {display_date=1;display_month++;}
				if (display_month > 12) {display_month=1;display_year++;}
				}
			result += '</TR>';
			}
		var current_weekday = now.getDay() - this.weekStartDay;
		if (current_weekday < 0) {current_weekday += 7;}
		result += '<TR>\n<TD COLSPAN=7 ALIGN=CENTER CLASS="cpTodayText">\n<A CLASS="cpTodayText" HREF="javascript:'+windowref+this.returnFunction+'(\''+now.getFullYear()+'\',\''+(now.getMonth()+1)+'\',\''+now.getDate()+'\');'+windowref+'_c.CP_hideCalendar(\''+this.index+'\');">'+this.todayText+'</A>\n';
		result += '<BR></TD></TR></TABLE></CENTER></TD></TR></TABLE>\n';
	}
	return result;
}
