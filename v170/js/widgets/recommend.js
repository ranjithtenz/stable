// Requires: 
// 
// Recommendation Control
// Recommendation
//
// Usage: create a new recommendation object
// For a new instance: pass dt, dn, call refresh
// ==============================================

Recommendation = function() { }

Recommendation.prototype.make = function(parent, dt, dn){
	var me = this;	
	this.allow_guest = 1;
	
	this.wrapper = $a(parent,'div','',{width:'140px'});
	
	var tbl = make_table(this.wrapper,1,2,'100%',['20px','120px'], {verticalAlign:'middle'});
	
	this.img_span = $a($td(tbl,0,0),'img');
	this.img_span.src = 'images/icons/icon-recommend.gif';
	
	this.rec = $a($td(tbl,0,1),'span','',{textDecoration:'underline', cursor:'pointer', width:'120px'});
	this.rec.onclick = function(){
		if(me.allow){ me.recommend(); }
	}
	
	if(dt && dn) {
		this.dt = dt; 
		this.dn = dn;
		this.refresh();
	}
}

// set reference of doctype, page.
Recommendation.prototype.set_reference = function(dt,dn){
	this.dt = dt; this.dn = dn;
}

// get recommendation count.
Recommendation.prototype.refresh = function(dt, dn){
	if(dt && dn) {
		this.dt = dt; 
		this.dn = dn;
	}

	var me = this;
	var args = {};
	args.dt = me.dt; args.dn = me.dn; args.user = user;

	var callback = function(r,rt){
		var count = cint(r.message.count) ? cint(r.message.count) : 0;
		me.reco_count = count;
		me.rec.innerHTML = 'Recommend' + ' (' + me.reco_count + ')';
		
		if(r.message.flag){ me.set_title(1, r.message.owner); }else{ me.set_title(0, r.message.owner); }
	}
	$c_obj('Recommendation Control','get_reco_count', docstring(args), callback);
}

// set onmouseover title.
Recommendation.prototype.set_title = function(unrecommended, is_owner){

	var me = this;
	if((!this.allow_guest) && user == 'Guest'){
		me._blur();
		me.rec.title = 'You need to login to recommend';
		me.allow = 0;
	}
	else{
		if(unrecommended){
			me._activate();
			me.rec.title = 'Recommend';
			me.allow = 1;
		}
		else{
			me._blur();
			me.rec.title = (is_owner ? 'Owner cannot recommend.' : 'Recommended');
			me.allow = 0;
		}
	}
}

Recommendation.prototype._blur = function() {
	$y(this.rec, {cursor:'auto', textDecoration:'none', color:'#888'});
}

Recommendation.prototype._activate = function() {
	$y(this.rec, {cursor:'pointer', textDecoration:'underline', color:'#000'});
}

// add recommendation.
Recommendation.prototype.recommend = function(){

	var me = this;
	var args = {}
	args.dt = me.dt; args.dn = me.dn; args.user = user;
	
	var callback = function(r,rt){
		if(r.message){ me.reco_count += 1; me.rec.innerHTML = 'Recommend (' + me.reco_count + ')'; me.set_title(0,0); }
	}
	$c_obj('Recommendation Control','recommend', docstring(args),callback);
}
