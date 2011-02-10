// Container
var cur_cont = '';
var containers = [];

function Container(name) { }

Container.prototype.init = function() {
	this.wrapper = $a(cont_area, 'div', 'container_div');
	if(isFF) {
		$dh(this.wrapper);
		$y(this.wrapper,{overflow:'hidden'});
	}
	this.head = $a(this.wrapper, 'div', 'container_head');
	this.body = $a(this.wrapper, 'div', 'container_body');
	if(this.oninit)this.oninit();
}

Container.prototype.show = function() {
	if(this.onshow)	this.onshow();
	if(cur_cont)cur_cont.hide();
	cur_cont = this;
	if(this.wrapper.style.display.toLowerCase()=='none') {
		$ds(this.wrapper);
		return;
	}
	//$ds(this.wrapper);
	if(isFF && this.has_frame) {
		$y(this.wrapper,{height:null})
	} else {
		$ds(this.wrapper); 
	}
}

Container.prototype.hide = function() { 
	if(this.onhide)	this.onhide();
	if(isFF && this.has_frame) {
		$y(this.wrapper,{height:'0px'})
	} else {
		$dh(this.wrapper); 
	}
	
	// hide autosuggest
	hide_autosuggest();
	cur_cont = ''; 
}

