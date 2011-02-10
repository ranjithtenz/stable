function Layout(parent, width) { 
	if(parent&&parent.substr) { parent = $i(parent); }

	this.wrapper = $a(parent, 'div', '', {display:'none'});


	if(width) {
		this.width = this.wrapper.style.width;
	}
	
	this.myrows = [];
}

Layout.prototype.addrow = function() {
	this.cur_row = new LayoutRow(this, this.wrapper);
	this.myrows[this.myrows.length] = this.cur_row;
	return this.cur_row
}

Layout.prototype.addsubrow = function() {
	this.cur_row = new LayoutRow(this, this.cur_row.wrapper);
	this.myrows[this.myrows.length] = this.cur_row;
	return this.cur_row
}

Layout.prototype.addcell = function(width) {
	return this.cur_row.addCell(width);
}

Layout.prototype.setcolour = function(col) { $bg(cc,col); }

Layout.prototype.show = function() { $ds(this.wrapper); }
Layout.prototype.hide = function() { $dh(this.wrapper); }
Layout.prototype.close_borders = function() {
	if(this.with_border) {
		this.myrows[this.myrows.length-1].wrapper.style.borderBottom = '1px solid #000';
	}
}

function LayoutRow(layout, parent) {
	this.layout = layout;
	this.wrapper = $a(parent,'div');
	
	// for sub rows
	this.sub_wrapper = $a(this.wrapper,'div');

	if(layout.with_border) {
		this.wrapper.style.border = '1px solid #000';
		this.wrapper.style.borderBottom = '0px';
	}
	
	this.header = $a(this.sub_wrapper, 'div','',{padding:(layout.with_border ? '0px 8px' : '0px')});
	this.body = $a(this.sub_wrapper,'div');
	this.table = $a(this.body, 'table', '', {width:'100%', borderCollapse: 'collapse'});
	this.row = this.table.insertRow(0);
	
	this.mycells = [];
}

LayoutRow.prototype.hide = function() { $dh(this.wrapper); }
LayoutRow.prototype.show = function() { $ds(this.wrapper); }

LayoutRow.prototype.addCell = function(wid) {
	var lc = new LayoutCell(this.layout, this, wid);
	this.mycells[this.mycells.length] = lc;
	return lc;
}

function LayoutCell(layout, layoutRow, width) {
	if(width) { // add '%' if user has forgotten
		var w = width + '';
		if(w.substr(w.length-2, 2) != 'px') {
			if(w.substr(w.length-1, 1) != "%") {width = width + '%'};
		}
	}

	this.width = width;
	this.layout = layout;
	var cidx = layoutRow.row.cells.length;
	this.cell = layoutRow.row.insertCell(cidx);

	this.cell.style.verticalAlign = 'top';
	if(width)
		this.cell.style.width = width;
	
	var h = $a(this.cell, 'div','',{padding:(layout.with_border ? '0px 8px' : '0px')});	

	this.wrapper = $a(this.cell, 'div','',{padding:(layout.with_border ? '8px' : '8px 0px')}); 

	layout.cur_cell = this.wrapper;
	layout.cur_cell.header = h;
}

LayoutCell.prototype.show = function() { $ds(this.wrapper); }
LayoutCell.prototype.hide = function() { $dh(this.wrapper); }

