// set custom tip
CustomTooltip = function(parent,tip_content,cs){
	
	this.tip = $a(null,'div','custom_tooltip',cs);
	this.tip.innerHTML = tip_content;

	// append tip to body, to get the height and width of tip
	$(this.tip).appendTo('body');	
	
	this.parent = parent;
	$y(this.parent,{position:'relative'});
			
	// set parameters
	this.set_param();		
			
	// on hover
	this.onhover();		
}

// set parameters
CustomTooltip.prototype.set_param = function(){

	this.parent.tip = this.tip;
	
	// tip width
	this.parent.width = $(this.tip).outerWidth();

	// tip height
	this.parent.height = $(this.tip).outerHeight();
	
	// parent width
	var pw = $(this.parent).outerWidth();
	this.parent.parent_width = pw ? pw : 16;	// if parent width set before rendering(i.e. 0px)

	// parent height
	var ph = $(this.parent).outerHeight();
	this.parent.parent_height = ph ? ph : 16;	// if parent height set before rendering(i.e. 0px)

	// remove tip from body
	$(this.tip).remove();
}

// on hover
CustomTooltip.prototype.onhover = function(){
	
	// on hover	
	$(this.parent).hover(
		
		// mouseover
		function(e){
			
			// repositioning of tip to avoid striping on the corners of window if required
			this.screen_width = $(window).width();
			this.screen_bottom = $(window).scrollTop() + $(window).height();

			this.offset = $(this).offset();
			
			// append to parent
			$(this.tip).appendTo(this)
			$y(this.tip,{width:this.width + 'px'})
			
			// set position
			if(this.offset.left + this.parent_width + this.width > this.screen_width){
				this.left = - this.width;
			}
			else this.left = this.parent_width;
		
			if(this.offset.top + this.parent_height + this.height > this.screen_bottom){
				this.top = - this.height;
			}
			else this.top = this.parent_height;
			
			$(this.tip)
				.css('top', this.top + 'px')
				.css('left', this.left + 'px')
				.css('display', 'block')
		},
		
		// mouseout	
		function(e){
			$(this.tip)
				.css('display','none');
		}
	)
}
