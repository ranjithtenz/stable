class DocType:
  def __init__(self, doc, doclist):
    self.doc = doc
    self.doclist = doclist
  
  # Autoname
  # ---------
  def autoname(self):
    self.doc.name = make_autoname(self.doc.naming_series+'.#####')
  
  #check status of lead
  #------------------------
  def check_status(self):
    chk = sql("select status from `tabLead` where name=%s", self.doc.name)
    chk = chk and chk[0][0] or ''
    return cstr(chk)

  # Gets states belonging cto country selected
  # =====================================================================
  def check_state(self):
    return NEWLINE + NEWLINE.join([i[0] for i in sql("select state_name from `tabState` where `tabState`.country='%s' " % self.doc.country)])
  
  # Get item detail (will be removed later)
  #=======================================
  def get_item_detail(self,item_code):
    it=sql("select item_name,brand,item_group,description,stock_uom from `tabItem` where name='%s'"%item_code)
    if it:
      ret = {
      'item_name'  : it and it[0][0] or '',
      'brand'      : it and it[0][1] or '',
      'item_group' : it and it[0][2] or '',
      'description': it and it[0][3] or '',
      'uom' : it and it[0][4] or ''
      }
      return cstr(ret)
  
  def validate(self):
    import string
    # Get Address
    # ======================================================================
    if (self.doc.address_line1) or (self.doc.address_line2) or (self.doc.city) or (self.doc.state) or (self.doc.country) or (self.doc.pincode):
      address =["address_line1", "address_line2", "city", "state", "country", "pincode"]
      comp_address=''
      for d in address:
        if self.doc.fields[d]:
          comp_address += self.doc.fields[d] + NEWLINE
      if self.doc.website:
        comp_address += "Website : "+ self.doc.website
      self.doc.address = comp_address
    
    if self.doc.status == 'Lead Lost' and not self.doc.order_lost_reason:
      msgprint("Please Enter Order Lost Reason")
      raise Exception  
    
    if self.doc.source == 'Campaign' and not self.doc.campaign_name and session['user'] != 'Guest':
      msgprint("Please specify campaign name")
      raise Exception
    
    if self.doc.email_id:
      if not validate_email_add(self.doc.email_id):
        msgprint('Please enter valid email id.')
        raise Exception
    
    if session['user']!='Guest':
      self.set_last_contact_date()  
    
    
    if not self.doc.naming_series:
      if session['user'] == 'Guest':
        so = sql("select options from `tabDocField` where parent = 'Lead' and fieldname = 'naming_series'")
        #so = sql("select series_options from `tabNaming Series Options` where doc_type='Lead'")
        if so:
          sr = so[0][0].split(NEWLINE)
          set(self.doc, 'naming_series', sr[0])
      else:
        msgprint("Please specify naming series")
        raise Exception  
  
  def on_update(self):
    # Add to calendar
    # ========================================================================
    if self.doc.contact_date and self.doc.last_contact_date != self.doc.contact_date:
      if self.doc.contact_by:
        self.add_calendar_event()
    
    if session['user'] != 'Guest':
      # make feed
      obj = get_obj('Feed Control', 'Feed Control')
      if not self.doc.creation:
        obj.make_feed('created', self.doc.doctype, self.doc.name)
      else:
        obj.make_feed('modified', self.doc.doctype, self.doc.name)
    else:
      if self.doc.email_id:
        self.send_email_notification()
    
    if not self.doc.naming_series:
      if session['user'] == 'Guest':
        #so = sql("select series_options from `tabNaming Series Options` where doc_type='Lead'")
        so = sql("select options from `tabDocField` where parent = 'Lead' and fieldname = 'naming_series'")
        if so:
          sr = so[0][0].split(NEWLINE)
          set(self.doc, 'naming_series', sr[0])
      else:
        msgprint("Please specify naming series")
        raise Exception
  
  def send_email_notification(self):
    if not validate_email_add(self.doc.email_id.strip(' ')):
      msgprint('error:%s is not a valid email id' % self.doc.email_id.strip(' '))
      raise Exception
    else:
      subject = 'Thank you for interest in erpnext'
       
      sendmail([self.doc.email_id.strip(' ')], sender = sender_email[0][0], subject = subject , parts = [['text/html', self.get_notification_msg()]])
      #sendmail(cc_list, sender = sender_email[0][0], subject = subject , parts = [['text/html', message]],attach=attach_list)
      msgprint("Mail Sent")
  
  def get_notification_msg(self):
    t = """
<html>
<body>
Dear %s,<br><br>

Thank you for contacting us.<br><br>

You have left following message for us,<br>
%s
<br><br>

You will receive reply on this shortly.<br><br>

Cheers!
</body>
</html>
""" % (self.doc.lead_name, self.doc.remark)

    return t
  
#--------------Validation For Last Contact Date-----------------
  def set_last_contact_date(self):
    if not self.doc.contact_date_ref:
      self.doc.contact_date_ref=self.doc.contact_date
      #self.doc.last_contact_date=self.doc.contact_date_ref
    if self.doc.contact_date_ref != self.doc.contact_date:
      if getdate(self.doc.contact_date_ref) < getdate(self.doc.contact_date):
        self.doc.last_contact_date=self.doc.contact_date_ref
      else:
        msgprint("Contact Date Cannot be before Last Contact Date")
        raise Exception
      set(self.doc, 'contact_date_ref',self.doc.contact_date)

  # Add to Calendar
  # ===========================================================================
  def add_calendar_event(self):
    # delete any earlier event by this lead
    sql("delete from tabEvent where ref_type='Lead' and ref_name=%s", self.doc.name)
  
    ev = Document('Event')
    ev.description = 'Contact ' + cstr(self.doc.lead_name) + '.By : ' + cstr(self.doc.contact_by) + '.To Discuss : ' + cstr(self.doc.to_discuss)
    ev.event_date = self.doc.contact_date
    ev.event_hour = '10:00'
    ev.event_type = 'Private'
    ev.ref_type = 'Lead'
    ev.ref_name = self.doc.name
    ev.save(1)
    
    ch = addchild(ev, 'event_individuals', 'Event User', 0)
    ch.person = self.doc.lead_owner
    ch.save()

#-----------------Email-------------------------------------------- 
  def send_emails(self, email=[], subject='', message=''):    

    if email:
      sender_email= sql("Select email from `tabProfile` where name='%s'"%session['user'])
      
      if sender_email and sender_email[0][0]:
        attach_list=[ at.select_file for at in getlist(self.doclist,'lead_attachment_detail') if at.select_file ]
        
        cc_list= self.doc.cc_to and self.doc.cc_to.split(',') or []

        for cl in cc_list:
          if not validate_email_add(cl.strip(' ')):
            msgprint('error:%s is not a valid email id' % cl.strip(' '))
            raise Exception
        
        sendmail(email, sender = sender_email[0][0], subject = subject , parts = [['text/html', message]],cc=cc_list,attach=attach_list)
        #sendmail(cc_list, sender = sender_email[0][0], subject = subject , parts = [['text/html', message]],attach=attach_list)
        msgprint("Mail Sent")
        self.add_in_follow_up(message,'Email')
      else:
        msgprint("Please enter your mail id in Profile")
        raise Exception

#-------------------------Checking Sent Mails Details----------------------------------------------        
  def send_mail(self):
    if not self.doc.subject or not self.doc.message:
      msgprint("Please enter subject & message in their respective fields.")
    elif not self.doc.email_id:
      msgprint("Recipient not specified. Please add email id of lead in 'Email id' field provided in 'Basic Info' section.")
      raise Exception
    else :
      if not validate_email_add(self.doc.email_id.strip(' ')):
        msgprint('error:%s is not a valid email id' % self.doc.email_id)
      else:
        self.send_emails([self.doc.email_id.strip(' ')], subject = self.doc.subject ,message = self.doc.message)

#---------------------- Add details in follow up table----------------
  def add_in_follow_up(self,message,type):
    import datetime
    child = addchild( self.doc, 'follow_up', 'Follow up', 1, self.doclist)
    child.date = datetime.datetime.now().date().strftime('%Y-%m-%d')
    child.notes = message
    child.follow_up_type = type
    child.save()

#-------------------SMS----------------------------------------------
  def send_sms(self):
    if not self.doc.sms_message or not self.doc.mobile_no:
      msgprint("Please enter mobile number in Basic Info Section and message in SMS Section ")
      raise Exception
    else:
      receiver_list = []
      if self.doc.mobile_no:
        receiver_list.append(self.doc.mobile_no)
      for d in getlist(self.doclist,'lead_sms_detail'):
        if d.other_mobile_no:
          receiver_list.append(d.other_mobile_no)
    
    if receiver_list:
      msgprint(get_obj('SMS Control', 'SMS Control').send_sms(receiver_list, self.doc.sms_message))
      self.add_in_follow_up(self.doc.sms_message,'SMS')