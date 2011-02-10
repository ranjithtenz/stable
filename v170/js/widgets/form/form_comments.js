// Comment Listing
// ===============
CommentList = function(parent, dt, dn) {
  this.wrapper = $a(parent, 'div', '', {margin:'16px'});
  this.input_area = $a(this.wrapper, 'div', '', {margin:'2px'});
  this.lst_area = $a(this.wrapper, 'div', '', {margin:'2px'});
  
  this.make_input();
  this.make_lst();
  this.dt;
  this.dn;
}

CommentList.prototype.run = function() {
  this.lst.run();
}

CommentList.prototype.make_input = function() {
  var me = this;
  // make the input text area and button
  this.input = $a(this.input_area, 'textarea', '', {height:'60px', width:'300px', fontSize:'14px'});
  this.btn = $a($a(this.input_area,'div','',{marginTop:'8px'}), 'button')
  $(this.btn).html('Post').click(function() {me.add_comment();}).button();  
}

// Add comment listing
// --------------------
CommentList.prototype.add_comment = function() {
  //to be called from button
  var me = this;
  var args = {};
  args.comment = this.input.value;
  args.comment_by = user;
  args.comment_doctype = this.dt;
  args.comment_docname = this.dn;
  $c_obj('Widget Control', 'add_comment', docstring(args), function(r,rt){
    me.lst.run();
    // clean up the text area
    me.input.value = '';
    cur_frm.no_of_comments += 1;
    cur_frm.frm_head.refresh_comments();
  });
}

// Make comment listing
// --------------------
CommentList.prototype.make_lst = function() {
  if(!this.lst) {
    var l = new Listing('Comments', 1);
    var me = this;
    // define the columns etc
    l.colwidths = ['100%'];

    // define options
    l.opts.hide_export = 1;     l.opts.hide_print = 1;    l.opts.hide_refresh = 1;    l.opts.no_border = 1;
    l.opts.hide_rec_label = 0;    l.opts.show_calc = 0;    l.opts.round_corners = 0;
    l.opts.alt_cell_style = {};
    l.opts.cell_style = {padding:'3px'};
    l.no_rec_message = 'No comments yet. Be the first one to comment!';
    
    l.get_query = function(){
      //----------------------     0         1             2               3             4                5                   6                                                                   7                                            8             9                      10                     11                 12                 13                 14
      this.query = repl("select t1.name, t1.comment, t1.comment_by, '', t1.creation, t1.comment_doctype, t1.comment_docname, ifnull(concat_ws(' ',ifnull(t2.first_name,''),ifnull(t2.middle_name,''),ifnull(t2.last_name,'')),''), '', DAYOFMONTH(t1.creation), MONTHNAME(t1.creation), YEAR(t1.creation), hour(t1.creation), minute(t1.creation), second(t1.creation) from `tabComment Widget Record` t1, `tabProfile` t2 where t1.comment_doctype = '%(dt)s' and t1.comment_docname = '%(dn)s' and t1.comment_by = t2.name order by t1.creation desc",{dt:me.dt, dn:me.dn});
      this.query_max = repl("select count(name) from `tabComment Widget Record` where comment_doctype='%(dt)s' and comment_docname='%(dn)s'",{'dt': me.dt, 'dn': me.dn});
    }

    l.show_cell = function(cell, ri, ci, d){
      new CommentItem(cell, ri, ci, d, me)
    }
    this.lst = l;
    this.lst.make(this.lst_area);

  }
}

// Comment Item
//=============
CommentItem = function(cell, ri, ci, d, comment) {
  this.comment = comment;
  $y(cell, {borderBottom:'1px solid #AAA', padding:'4px 0px'})
  var t = make_table(cell, 1, 3, '100%', ['15%', '65%', '20%'], {padding:'4px'});
  
  // image
  this.img = $a($td(t,0,0), 'img', '', {width:'40px'});
  this.cmt_by = $a($td(t,0,0), 'div');
  this.set_picture(d, ri);

  // comment
  this.cmt_dtl = $a($td(t,0,1), 'div', 'comment', {fontSize:'11px'});
  this.cmt = $a($td(t,0,1), 'div','',{fontSize:'14px'});
  this.show_cmt($td(t,0,1), ri, ci, d);

  this.cmt_delete($td(t,0,2), ri, ci, d);
}
  
// Set picture
// -----------
CommentItem.prototype.set_picture = function(d, ri){
	set_user_img(this.img, user)
	this.cmt_by.innerHTML = d[ri][7] ? d[ri][7] : d[ri][2];
}

// Set comment details
// -------------------
CommentItem.prototype.show_cmt = function(cell, ri, ci, d) {
  //time  and date of comment
  if(d[ri][4]){
    hr = d[ri][12]; min = d[ri][13]; sec = d[ri][14];
    if(parseInt(hr) > 12) { time = (parseInt(hr)-12) + ':' + min + ' PM' }
    else{ time = hr + ':' + min + ' AM'}
  }
  this.cmt_dtl.innerHTML = 'On ' + d[ri][10].substring(0,3) + ' ' + d[ri][9] + ', ' + d[ri][11] + ' at ' + time;
  this.cmt.innerHTML = replace_newlines(d[ri][1]);
}

// Set delete button
// -----------------
CommentItem.prototype.cmt_delete = function(cell, ri, ci, d) {
  var me = this;
  if(d[ri][2] == user || d[ri][3] == user) {
    del = $a(cell,'div','wn-icon ic-trash',{cursor:'pointer'});
    del.cmt_id = d[ri][0];
    del.onclick = function(){ 
      $c_obj('Widget Control','remove_comment',this.cmt_id,function(r,rt){
      	cur_frm.no_of_comments = cur_frm.no_of_comments - 1;
      	cur_frm.frm_head.refresh_comments();
        me.comment.lst.run();
      });
    }
  }
}