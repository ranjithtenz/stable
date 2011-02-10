pscript['onload_Login Page'] = function(){
    keypress_observers.push(new function() {
      this.notify_keypress = function(kc) { if(kc==13 && $i("password").value) pscript.doLogin(); }
    }
  );
}


// Login Callback
pscript.onLoginReply = function(r, rtext) {
    if(r.message=="Logged In"){
        window.location.href='index.cgi' + (get_url_arg('page') ? ('?page='+get_url_arg('page')) : '');
    } else {
        $i('login_message').innerHTML = '<span style="color: RED;">'+eval(r.message)+'</span>';
        //if(r.exc)alert(r.exc);
    }
}


// Login
pscript.doLogin = function(){

    var args = {};
    args['usr']=$i("login_id").value;
    args['pwd']=$i("password").value;
    if($i('remember_me').checked) 
      args['remember_me'] = 1;

    $c("login", args, pscript.onLoginReply);
}


pscript.show_forgot_password = function(){
    // create dialog
    var d = new Dialog(400, 400, 'Reset Password')
    d.make_body([['HTML','Title','Enter your email id to reset the password'], ['Data','Email Id'], ['Button','Reset']]);

    var callback = function(r,rt) { 
        if(!r.exc) pscript.forgot_dialog.hide();
    }

    d.widgets['Reset'].onclick = function() {
      $c('reset_password', {user: pscript.forgot_dialog.widgets['Email Id'].value}, callback)
    }
    d.show();
    pscript.forgot_dialog = d;
}