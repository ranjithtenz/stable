// ABOUT

var about_dialog;

function show_about() {
	if(!about_dialog) {
		var d = new Dialog(360,480, 'About')
	
		d.make_body([
			['HTML', 'info']
		]);
		
		d.rows['info'].innerHTML = "<div style='padding: 16px;'><center>"
			+"<div style='text-align: center'><img src = 'images/ui/webnotes30x120.gif'></div>"
			+"<br><br>&copy; 2007-08 Web Notes Technologies Pvt. Ltd."
			+"<p><span style='color: #888'>Customized Web Based Solutions and Products</span>"
			+"<br>50/2386, Vijaydeep C.H.S,<br>Gandhi Nagar,<br>Opp MIG Cricket Club,<br>Bandra (East),<br>Mumbai 51</p>"
			+"<p>Phone: +91-22-6526-5364 (M-F 9-6)"
			+"<br>Email: info@webnotestech.com"
			+"<br><b>Customer Support: support@webnotestech.com</b></p>"
			+"<p><a href='http://www.webnotestech.com'>www.webnotestech.com</a></p></center>"
			+"</div>";
	
		about_dialog = d;
	}
	about_dialog.show();
}
