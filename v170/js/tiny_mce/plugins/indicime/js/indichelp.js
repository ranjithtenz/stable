tinyMCEPopup.requireLangPack();

var IndicHelpDialog = {
	init : function(ed) {
		tinyMCEPopup.resizeToInnerSize();
	}
};

tinyMCEPopup.onInit.add(IndicHelpDialog.init, IndicHelpDialog);
