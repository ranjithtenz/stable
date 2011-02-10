class DocType:
  def __init__(self, d, dl):
    self.doc, self.doclist = d,dl
    
  def validate(self):
    if not self.doc.file_list:
      msgprint("Warning: No files attached")

    # set mime type
    if not self.doc.mime_type:
      import mimetypes
      self.doc.mime_type = mimetypes.guess_type(self.doc.name)[0] or 'application/unknown'

    if not self.doc.file_name:
      fname = self.doc.file_list.split(',')[0]
      self.doc.file_name = fname