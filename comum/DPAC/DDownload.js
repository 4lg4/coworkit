/**
 * 
 * Cria Grupos de rádio para uso Touch: 
 * Suporte a organização Horizontal / Vertical
 * Suporte a Accordion
 *
 * @example $.DDownload({ action:'download.cgi', vars:$("#CAD").serializeArray() });
 * @desc Uso
 *
 * @param action text (obrigatório) url completa /exemplo/download.cgi
 *
 * @type jQuery
 *
 * @name DDownload
 * @cat Plugins / Core
 * @author DONE Tecnologia - Adriano Karkow Gaiatto Leal (http://gaiattos.com/akgleal.com)
 */

include("/comum/fileDownload/jquery.fileDownload.js");


(function($, window){
	
$.extend(
	{
	DDownload: function (settings, value) 
		{
		var settings = $.extend(
			{
			enable			: true,
			action			: "",
			vars			: ""
			}, settings || {});

		// caso de arquivos pdf
		if(settings.action.search("pdf") > 0)
			{
			$("#CAD").append("<input type='hidden' name='ID' value='"+$("#AUX input[name=ID]").val()+"'>").attr({ method:"POST", action:settings.action, target:"_blank" }).submit();
			return true;
			}

		$.fileDownload(settings.action, 
			{
			// preparingMessageHtml: "We are preparing your report, please wait...",
			// failMessageHtml: "There was a problem generating your report, please try again.",
			httpMethod: "POST",
			data: settings.vars,
			/*
			// antes de iniciar o download
			prepareCallback: function (url) 
				{
				alertaLoading("Preparando arquivo para download");
				},
			// se download ocorrer como devido
			onSuccess: function (url) 
					{
					console.log("logs");
					alertaClose();
					},
			successCallback: function (url) 
				{
				console.log("logs");
				alertaClose();
				},
			*/
			failCallback: function (responseHtml, url) 
				{
				alerta("Erro ao executar download");
				}
		    });
		}
	});
	
})(jQuery, this);
