/* [INI]  Text Editor field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
		Javascript
			/comum/tiny_mce/jquery.tinymce.js
		
		CSS
			/css/ui.css
			
		IMG
			/img/tiny_mce/

    Opcoes:
		Buttons
		Model
		Enable
		Disable
	
	Exemplo de uso:
		Javascript:
			$("#campo_TextEditor").fieldTextEditor();
			$(".campo_TextEditor").fieldTextEditor();
			
			$("#campo_email").fieldTextEditor(
				{
				options:values
				});
							
		HTML:
			<textarea id='campo_textEditor' name='campo_textEditor'></textarea>
*/

include("/comum/tiny_mce/jquery.tinymce.js"); 


(function($){
	
$.fn.fieldTextEditor = function(settings) 
	{
	var settings = $.extend(
		{
		buttons 	: "fullscreen,|,print,|,undo,redo,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,fontselect,fontsizeselect,|,search,replace,|,forecolor,backcolor,|,bullist,numlist,|,link,unlink,image",
		enable		: 'on',
		model		: '',
		}, settings);
	
	// return fields
	return this.each(function()
		{
			
		// modelo simples com botoes basicos de edicao de texto
		if(settings.model == "simple" || settings.model == "simples" || settings.model == "basic" || settings.model == "basico")
			{
			settings.buttons = "undo,redo,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,fontselect,fontsizeselect,|,search,replace,|,forecolor,backcolor,|,bullist,numlist";
			}
				
		$(this).tinymce(
			{
			// Location of TinyMCE script
			script_url : '/comum/tiny_mce/tiny_mce.js',

			// General options
			theme : "advanced",
			skin : "eos",
			skin_variant : "black",
			plugins : "inlinepopups,fullscreen,print",
			theme_advanced_buttons1 : settings.buttons,
			theme_advanced_buttons2 : "",
			theme_advanced_buttons3 : "",
			theme_advanced_toolbar_location : "top",
			theme_advanced_toolbar_align : "left",
			theme_advanced_resizing : false,

			// Example content CSS (should be your site CSS)
			content_css : "css/content.css",

			// Drop lists for link/image/media/template dialogs
			template_external_list_url : "lists/template_list.js",
			external_link_list_url : "lists/link_list.js",
			external_image_list_url : "lists/image_list.js",
			media_external_list_url : "lists/media_list.js",
		  	});
		});

	};

})( jQuery );