class DocType:
  def __init__(self,d,dl):
    self.doc, self.doclist = d, dl

  def add_update(self):
    d = Document('Project Activity Update')
    d.parent = self.doc.name
    d.update = self.doc.new_update
    d.hours = self.doc.hours
    d.save(1)

    self.doc.new_update = ''
    self.doc.hours = ''