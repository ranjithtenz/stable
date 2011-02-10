class DocType:
  def __init__(self, d, dl):
    self.doc, self.doclist = d,dl

  # replace $image
  # ------------------
  def validate(self):
    import re
    p = re.compile('\$image\( (?P<name> [^)]*) \)', re.VERBOSE)
    if self.doc.content:
      self.doc.content = p.sub(self.replace_by_img, self.doc.content)
  
  def replace_by_img(self, match):
    name = match.group('name')
    return '<img src="cgi-bin/getfile.cgi?ac=%s&name=%s">' % (Document('Control Panel', 'Control Panel').account_id, name)