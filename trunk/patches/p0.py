# add interests and activity fields to Profile

import webnotes.modules.import_module
webnotes.modules.import_module.import_from_files(record_list=[['System','DocType','Profile'], ['My Company','Module Def','My Company']])

# update module control

webnotes.conn.sql("update tabDocType set module='Event Updates' where name='Home Control' limit 1")
webnotes.conn.sql("update tabDocType set module='Application Internal' where name='Menu Control' limit 1")

webnotes.conn.set_value('Control Panel',None,'sync_with_gateway',1)

# update module def "icon" field

webnotes.conn.sql("update tabDocField set fieldtype='Data' and options='' where parent='Module Def' and fieldname='module_icon' limit 1")

# update module icons

webnotes.conn.sql("update `tabModule Def` set module_icon='Home.gif' where name='Event Updates'")
webnotes.conn.sql("update `tabModule Def` set module_icon='Setup.gif' where name='Setup'")
webnotes.conn.sql("update `tabModule Def` set module_icon='Projects.gif' where name='Projects'")
webnotes.conn.sql("update `tabModule Def` set module_icon='Selling.gif' where name='CRM'")
webnotes.conn.sql("update `tabModule Def` set module_icon='Buying.gif' where name='SRM'")
webnotes.conn.sql("update `tabModule Def` set module_icon='Accounts.gif' where name='Accounts'")
webnotes.conn.sql("update `tabModule Def` set module_icon='Stock.gif' where name='Material Management'")
webnotes.conn.sql("update `tabModule Def` set module_icon='HR.gif' where name='Payroll'")
webnotes.conn.sql("update `tabModule Def` set module_icon='Analysis.gif' where name='Analysis'")
webnotes.conn.sql("update `tabModule Def` set module_icon='Maintenance.gif' where name='Maintenance'")
webnotes.conn.sql("update `tabModule Def` set module_icon='Production.gif' where name='Production'")

webnotes.conn.sql("update `tabModule Def` set module_label='Support' where name='Maintenance'")

# update file system
from webnotes.utils.file_manager import convert_to_files
convert_to_files()