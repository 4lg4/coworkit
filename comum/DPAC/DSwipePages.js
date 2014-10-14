/* [INI]  DTouch field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
		Javascript:
	
		CSS:
			/css/ui.css
				.fieldEmail { }
				.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:
		Enable / Disable
		Auto Complete
		Post Function
	
	Exemplo de uso:
		Javascript:
			$("#campo_email").fieldEmail();
			$(".campo_email").fieldEmail();
			
			$("#campo_email").fieldEmail(
				{
				options:values
				});
							
		HTML:
			<input type="text" id='campo_email' name='campo_email'>			
*/

(function($){
	
$.fn.DSwipePages = function(settings) 
	{
	var settings = $.extend(
		{
		direction		: 'left',
		visible			: 'show',
		speed			: 500,
		style			: 'slide',
		delay			: false,
		postFunction	: ''
		}, settings);
	
	return this.each(function()
		{
				
		if(settings.delay === true)
			{
			// alert("delay");
			$(this).delay(500);
			}
				
		$(this).addClass("DTouchPages_transition");
		
		if(settings.visible == "hide")
			{
			$(this)
				.hide(
					settings.style, 
					{ direction: settings.direction  }, 
					settings.speed, 
					function() 
						{ 
						$(this).removeClass("DTouchPages_transition");
 
						// executa postfunction
						if(isFunction(settings.postFunction))
							settings.postFunction.call(this);
						else if(settings.postFunction != "") // mantem compatibilidade
							eval(settings.postFunction);
						} 
					);
			}
		else
			{
			$(this)
				.show(
					settings.style, 
					{ direction: settings.direction  }, 
					settings.speed, 
					function() 
						{ 
						$(this).removeClass("DTouchPages_transition");
						
						// executa postfunction
						if(isFunction(settings.postFunction))
							settings.postFunction.call(this);
						else if(settings.postFunction != "") // mantem compatibilidade
							eval(settings.postFunction);
						}
					);
			}
		});
	};

})( jQuery );



