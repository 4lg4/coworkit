/**
 * 
 * D-CEP:
 *
 * @example $.DCEP({ vars });
 * @desc Uso Básico
 *
 * @param addItem Array (obrigatório) Ver: Exemplo addItem
 *
 * @type jQuery
 *
 * @name DCEP
 * @cat Plugins/Accordion
 * @author DONE Tecnologia - Adriano Karkow Gaiatto Leal (http://gaiattos.com/akgleal.com)
 */

(function($, window){
	
$.extend(
	{
	DCEP: function(settings)
		{
		var settings = $.extend(
			{
			CEP	: '',
			logradouro : ''
			}, settings);
			
		// testa cep
		if(! /^\d{5}\-?\d{3}$/.test(settings.CEP))
			{
			console.log("$.DCEP: CEP inválido");
			return false;
			}
		
		// Busca CEP
		$.getScript("http://cep.republicavirtual.com.br/web_cep.php?formato=javascript&cep="+settings.CEP, function(cep)
			{	});
		}
	});
	
})(jQuery, this);


