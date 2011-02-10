// Tweets
var n_tweets = {}; var last_comments = {};
function Tweets(parent) {
	
	this.tag = null; this.last_comment = '';
	this.wrapper = $a(parent, 'div', '', {padding:'8px'});
	
	// header
	var ht = make_table($a(this.wrapper,'div'),1,1,'100%',['100%'],{textAlign:'center', verticalAlign:'middle'})

	// label
	this.label = $a($td(ht,0,0),'div'); this.label.innerHTML = 'Write Something';
	
	// input
	this.inp = $a($a($td(ht,0,0),'div'),'input','',{width:'180px', margin:'4px 0px'});
	
	// send button
	var me = this;
	this.btn = $a($td(ht,0,0),'button'); this.btn.innerHTML = 'Send'; this.btn.onclick = function() {
		if(strip(me.inp.value)) {
			$c_obj('Home Control','send_tweet',(me.inp.value+'~~~'+(me.tag?me.tag:'')), 
				function(r,rt) { me.tweet_lst.run(); });
		}
		me.comment_added = 1;
		me.last_comment = me.inp.value;
		me.inp.value = ''; // clear
	}
	
	var lst = new Listing('Tweets',1,1);
	lst.opts.hide_export = 1;
	lst.opts.hide_print = 1;
	lst.opts.hide_refresh = 1;
	lst.opts.no_border = 1;
	lst.opts.hide_rec_label = 1;
	lst.opts.show_calc = 0;
	lst.opts.round_corners = 0;
	lst.opts.alt_cell_style = {};
	lst.opts.cell_style = {padding:'3px'};

	lst.page_len = 10;
	lst.colwidths = ['100%'];
	lst.coltypes = ['Data'];

	lst.get_query = function() {
		var tag_cond = '';
		if(me.tag) tag_cond = ' and t1.`tag`="' + me.tag + '" ';
		
		this.query = repl('select t1.creation, t1.by, t1.comment, t2.file_list from tabTweet t1, tabProfile t2 where t1.by = t2.name %(tag_cond)s order by t1.name desc',{tag_cond:tag_cond});
		this.query_max = repl('select count(*) from tabTweet t1 where docstatus<2 %(tag_cond)s', {tag_cond:tag_cond});
	}

	// show weet
	lst.show_cell = function(cell, ri, ci, d) {
		var div = $a(cell,'div','', {paddingBottom:'2px',marginBottom:'2px',borderBottom:'1px dashed #CCC'});
		var t = make_table(div, 1,2, '100%', ['10%','90%'],{textAlign:'left'});

		// show image
		if(d[ri][3]) {
			var img = $a($td(t,0,0),'img','',{width:'40px'});
			var img_src = d[ri][3].split(NEWLINE)[0].split(',')[0];
			img.src = repl('cgi-bin/getfile.cgi?ac=%(ac)s&name=%(fn)s&thumbnail=40',{fn:img_src, ac:session.account_name});
		} else {
			var div = make_table($td(t,0,0),1,1,'40px',['100%']);
			var np_div = $td(div,0,0);
			np_div.innerHTML = 'No Picture';
			$y(np_div, {color:'#AAA', fontSize:'11px',padding:'2px',verticalAlign:'middle',textAlign:'center',border:'1px solid #AAA'});
		}
		
		// text
		$td(t,0,1).innerHTML = repl('<div class="comment" style="font-size:11px">%(by)s: %(on)s</div><div style="font-size: 12px;">%(comment)s</div>',
			{'by':d[ri][1], 'on':dateutil.str_to_user(d[ri][0]), 'comment':d[ri][2]});
	}

	// enter
	this.inp.onkeypress = function(e) {
		if(isIE)var kc = window.event.keyCode;
		else var kc = e.keyCode;
		if(kc==13) me.btn.onclick();
	}

	lst.make(this.wrapper);
	this.tweet_lst = lst;
	
	// show message
	this.msg_area = $a(this.wrapper, 'div', '', {margin:'4px 0px'});
	lst.onrun = function() {
		if(!this.total_records) me.msg_area.innerHTML = 'No comments yet. Be the first one to comment!';
		else me.msg_area.innerHTML = '';
	}
	
	// show
	this.show = function(tag) {
		me.tag = tag;
		me.tweet_lst.run();
	}
}

var tweet_dialog;
function setup_tweets() {
	tweet_dialog = document.createElement('div');
	$y(tweet_dialog,{height:'360px', width:'240px'})

	// Tweets object
	tweet_dialog.tweets = new Tweets(tweet_dialog);
	
	// onshow
	tweet_dialog.show = function() {
		//this.title_text.innerHTML = 'Comments for ' + this.dt + ' ' + this.dn;
		this.tweets.comment_added = false;
		this.tweets.show(cur_frm.doctype+'/'+cur_frm.docname);
	}
	
	// onclose
	tweet_dialog.hide = function() {
		n_tweets[tweet_dialog.tweets.tag] = cint(tweet_dialog.tweets.tweet_lst.total_records);
		last_comments[tweet_dialog.tweets.tag] = [dateutil.full_str(),user,tweet_dialog.tweets.last_comment];
		frm_con.comments_btn.innerHTML = 'Comments (' + n_tweets[tweet_dialog.tweets.tag] + ')';
		if(tweet_dialog.tweets.comment_added)
			cur_frm.set_last_comment();
	}
}
startup_lst[startup_lst.length] = setup_tweets;
 
