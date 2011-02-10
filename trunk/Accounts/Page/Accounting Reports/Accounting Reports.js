pscript['onload_Accounting Reports'] = function(){
  var h = new PageHeader('accounting_reports_header','Accounting Reports');

  var callback = function(r,rt){
    report_list = r.message['Accounts'];
    cnty = r.message['Country'];
    var dv = $a('accounting_reports_body','div');

    rcount = 0;
    var j =0;
    for(i=0; i<report_list.length;i++){

      if(rcount > 1){ rcount = 0; }
      else{ rcount = rcount; }

      if(rcount == 0){
        var tab = make_table(dv,1,2,'100%',['50%','50%']);
      }
      var india_only = ['TDS Rate Chart', 'TDS Category', 'TDS Payment', 'Form 16A', 'TDS Payment Detail'];
      if((cnty != 'India' && india_only.indexOf(report_list[i][1])==-1) || cnty == 'India'){
        new HomeMenuReport($td(tab,0,Math.floor(j%2)), report_list[i][1], report_list[i][2]);
        j += 1;
        rcount += 1;        
      }
    }    
  }
  $c_obj('Report Control','get_reports','Accounts',callback);

}