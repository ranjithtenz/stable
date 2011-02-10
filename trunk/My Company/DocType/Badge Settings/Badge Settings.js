cur_frm.fields_dict['badge_settings_detail'].grid.get_field("transaction").get_query = function(doc, cdt, cdn) {
	return "SELECT `tabDocType`.name FROM tabDocType WHERE (tabDocType.document_type = 'Transaction' or tabDocType.document_type = 'Master' or tabDocType.document_type is null or tabDocType.document_type = '') AND tabDocType.name Like '%s' LIMIT 50";
}
