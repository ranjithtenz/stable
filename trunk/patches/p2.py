# Contact to simple

sql("update tabDocType set section_style='Simple' where name='Contact' limit 1")

import webnotes.modules.import_module
webnotes.modules.import_module.import_from_files(record_list=[['Utilities','DocType','Patch Util']])

#get_obj('Patch Util').delete_unnamed_field('Receivable Voucher', 'is_pos')
