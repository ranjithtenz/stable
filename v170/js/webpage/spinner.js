var _loading_div;
function set_loading() {
	if(page_body.wntoolbar)$ds(page_body.wntoolbar.spinner);
	$y(document.getElementsByTagName('body')[0], {cursor:'progress'});
	pending_req++;
}

function hide_loading() {
	pending_req--;
	if(page_body.wntoolbar)
		var d = page_body.wntoolbar.spinner;
	if(!d)return;
	if(!pending_req){
		$y(document.getElementsByTagName('body')[0], {cursor:'default'});
		$dh(d);
		/*if(isIE6) {
			document.body.onscroll = null;
		}*/
	}
}