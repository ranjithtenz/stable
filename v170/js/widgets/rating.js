// Class Rating Widget.
function RatingWidget(){ 
	this.marked = 0;	
}

RatingWidget.prototype.make = function(parent,template) {

	this.rating_div = $a(parent,'div','',{marginTop:'5px'});
	this.rating_head = $a(this.rating_div,'div','',{fontSize:'12px', fontWeight:'bold'});
	this.rating_head.innerHTML = 'Rating';
	
	this.star_div = $a(this.rating_div,'div','',{marginTop:'5px'});
	this.star_span = $a(this.star_div, 'span','',{marginRight:'10px'});
	this.message_span = $a(this.stardiv, 'span','',{verticalAlign:'top', fontSize:'12px'});
	
	if(template){ this.rating_template = template; }
	else{ this.rating_template = 'Standard'; }
	
}

// Set reference of doctype, docname to set or fetch rating given by current user.
RatingWidget.prototype.set_reference = function(dt,dn){
	var me = this;
	me.dt = dt; me.dn = dn;
}

// Fetch and display rating.
RatingWidget.prototype.refresh = function(dt, dn){	
	var me = this;

	if(dt && dn) {
		me.dt = dt; me.dn = dn;	
	}

	if(cur_frm.doc.owner == user){
		$dh(me.rating_div);
	}
	else{
		$ds(me.rating_div);
	}
	
	var callback = function(r,rt){
		me.star_span.innerHTML = '';
		if(me.marked){
			me.message_span.innerHTML = 'Thank you for rating';
		}
		else{
			me.message_span.innerHTML = r.message.avg_rating[0][0] + ' ratings';
		}

		total_stars = parseInt(r.message.total_stars[0][0]);
		
		// If already rated by current user.
		if(r.message.flag == 1){
			rating_det = r.message.rating_details;
			rating_stars = parseInt(rating_det[0][1]);
			
			for(i=0; i<total_stars; i++){
				if(i<rating_stars){
					img = $a(me.star_span, 'img');
					img.src = 'images/ui/star.gif';
				}
				else{
					img = $a(me.star_span, 'img');
					img.src = 'images/ui/star_plain.gif';
				}
				img.onmouseover = function(){
					//me.message_span.innerHTML = 'You have already rated it as ' + rating_det[0][2];
					this.title = 'You have already rated it as ' + rating_det[0][2];
				}
				//img.onmouseout = function(){ 
					me.message_span.innerHTML = r.message.avg_rating[0][0] + ' ratings';
				//}
			}
		}
		else{   // If rating for first time.
			img_lst = [];
			for(i=0; i<total_stars; i++){
				
				img = $a(me.star_span, 'img','',{cursor:'pointer'});
			 //   img.src = 'images/ui/star_plain.gif';
				img.idx = i+1;
				img.rating = r.message.rating_desc[i][0];
				img.desc = r.message.rating_desc[i][1];
				img.title = r.message.rating_desc[i][1];
				img_lst.push(img);
				
				if(i<r.message.avg_rating[0][1]){
					img.src = 'images/ui/star.gif';
				}
				else{
					img.src = 'images/ui/star_plain.gif';
				}

				img.onmouseover = function(){
					for(j=0; j<img_lst.length; j++){
						if(img_lst[j].idx > this.idx){
							img_lst[j].src = 'images/ui/star_plain.gif';
						}
						else{
							img_lst[j].src = 'images/ui/star.gif';
						}
					}
				  //  me.message_span.innerHTML = this.desc;
				}
				/*
				img.onmouseout = function(){
					for(j=0; j<img_lst.length; j++){
						img_lst[j].src = 'images/ui/star_plain.gif';
					}
					me.message_span.innerHTML = r.message.avg_rating[0][0] + ' ratings';
				}*/
				img.onclick = function(){ me.add_rating(this.rating, this.desc); }
			}
		}
	}
	args = {};
	args.by = user; args.dt = me.dt; args.dn = me.dn; args.template = me.rating_template;
	$c_obj('Rating Widget Control', 'show_my_rating', docstring(args), callback);
}

// Add comment on current doctype, docname.
RatingWidget.prototype.add_rating = function(rating, desc){
	var me = this;

	var callback = function(r,rt){
		me.marked = 1;
		me.refresh();
	}

	args = {}
	args.rating = rating; args.desc = desc; args.template = me.rating_template; args.rating_by = user;
	args.dt = me.dt; args.dn = me.dn;
	
	$c_obj('Rating Widget Control','add_rating',docstring(args),callback);
}