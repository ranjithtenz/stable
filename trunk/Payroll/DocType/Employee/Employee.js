//Add Employee Profile Button click function : redirect to Employee Profile new record & add some values
cur_frm.cscript['Employee Profile']=function(doc,cdt,cdn){
  if(doc.__islocal!=1){
    
    var ep = LocalDB.create('Employee Profile');
    ep = locals['Employee Profile'][ep];
    ep.employee = doc.name;
    ep.employee_name=doc.employee_name;
    ep.date_of_joining=doc.date_of_joining;
    loaddoc('Employee Profile', ep.name); 
     
  }
  else{
    alert("Please first save employee.");
  }
}

//Make Salary Structure Button click function : redirect to Salary Structure new record & add some values
//========================================================
cur_frm.cscript['Salary Structure']=function(doc,cdt,cdn){
  $c_obj(make_doclist (doc.doctype,doc.name),'sal_struct_exist','',function(r, rt) {
      if(r.message){
        alert("You have already created Active salary structure.\nIf you want to create new one, please ensure that no active salary structure exist.\nTo inactive salary structure select 'Is Active' as 'No'.");

      }
      else {
        var st = LocalDB.create('Salary Structure');
        st = locals['Salary Structure'][st];
        st.employee = doc.name;
        st.employee_name = doc.employee_name;
        st.branch=doc.branch;
        st.designation=doc.designation;
        st.department=doc.department;
        st.fiscal_year = doc.fiscal_year
        st.grade=doc.grade;
        loaddoc('Salary Structure', st.name);
      }
    }
  );
 
}


//========================================================
cur_frm.cscript.date_of_birth = function(doc, cdt, cdn) {
  get_server_fields('retirement_date','','',doc,cdt,cdn,1);
}

//========================================================
cur_frm.cscript.salutation = function(doc,cdt,cdn) {
  if(doc.salutation){
    if(doc.salutation=='Mr')
      doc.gender='Male';
    else if(doc.salutation=='Ms')
      doc.gender='Female';
    refresh_field('gender');
  }
}

//========================================================
cur_frm.cscript.refresh = function(doc, cdt, cdn) {

  if(doc.__islocal!=1){

    $c_obj(make_doclist(doc.doctype,doc.name),'emp_prof_exist','',function(r, rt) {
        if(r.message){
          hide_field('Employee Profile');
          unhide_field('EmpProfile HTML');
          if(!cur_frm.emp_prof && !cur_frm.ep){
            cur_frm.emp_prof = $a(cur_frm.fields_dict['EmpProfile HTML'].wrapper,'span')
            cur_frm.ep =$a(cur_frm.fields_dict['EmpProfile HTML'].wrapper,'span','link_type')          
          }
          cur_frm.emp_prof.innerHTML = "Employee Profile : ";
          cur_frm.ep.innerHTML = r.message;
            
          cur_frm.ep.onclick = function(doc,cdt,cdn){
            loaddoc('Employee Profile', r.message);
          }
        }
        else{
          unhide_field('Employee Profile');
          hide_field('EmpProfile HTML');
        }
      }
    );
    unhide_field(['Salary Structure','Payroll Rule']);
  }
  else hide_field(['Salary Structure','Payroll Rule']);
  
}