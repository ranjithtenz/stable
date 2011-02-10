class DocType:
  def __init__(self, d, dl):
    self.doc, self.doclist = d, dl

  def get_module_list(self):
    from webnotes.modules.module_manager import get_modules_from_filesystem
    return get_modules_from_filesystem()

  def get_module_details(self, arg=''):
    from webnotes.modules.module_manager import get_module_details
    return get_module_details(arg)

  # modules ------------------------
  def import_module(self, arg):
    from webnotes.modules.import_module import import_from_files
    return import_from_files([arg])

  # import attachments
  def import_attach_module(self, arg):
    from webnotes.modules.import_module import import_attachments
    return import_attachments(arg)

  def export_module(self, arg):
    from webnotes.modules.export_module import export_to_files
    return export_to_files([arg], record_module = arg)

  # items ------------------------
  def import_item(self, arg):
    from webnotes.modules.import_module import import_from_files
    return import_from_files(record_list = [eval(arg)])

  def export_item(self, arg):
    from webnotes.modules.export_module import export_to_files
    return export_to_files(record_list = [eval(arg)[0]], record_module = eval(arg)[1])

  # cp -------------
  def update_cp(self, arg=''):
    from webnotes.modules.import_module import import_control_panel
    import_control_panel()
