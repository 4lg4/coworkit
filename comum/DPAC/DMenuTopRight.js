/**
 * 
 * Menu Top Right:
 *
 * @example $("#ID").DTouchRadio({ addItem: "[{val:value,descrp:'description',img:'image'}]" });
 * @desc Uso Básico
 * @example $("#ID").DTouchRadio({ addItem: "[{val:(valor de retorno),descrp:(descrição do item),img:(imagem do item)}]" });
 * @desc addItem, img é opcional
 * @example $('#accordion').activate(1);
 * @desc Activate the second content of the Accordion contained in &lt;div id="accordion"&gt;.
 *
 * @param addItem Array (obrigatório) Ver: Exemplo addItem
 *
 * @type jQuery
 *
 * @name DTouchRadio
 * @cat Plugins/Accordion
 * @author DONE Tecnologia - Adriano Karkow Gaiatto Leal (http://gaiattos.com/akgleal.com)
 */


(function($){
	
$.fn.DMenuTopRight = function(settings,value)
	{
	// se for um array ou estiver vazio ajusta variaveis
	if(isObject(settings) === true)
		{
		var settings = $.extend(
			{
			enable		: true,
			click		: '',
			dblclick	: '',
			uncheck		: '',
			type		: 'button',
			title		: '', 
			img			: '',
			text		: '',
			textContent : '',
			dropdownContent: '',
			dropdownContentAppend: '',
			dropdownContentPrepend: '',
			dropdownContentHtml: ''
			}, settings || {});
		}
	else
		{
		// fast switches eg. enable / disable
		switch(settings)
			{
			// Adiciona linhas ao fim
			case "dropdownContentAppend":
				$("#"+$(this).prop("id")+"_dropdown .dbox_menu_cont").append("<div class='DMenuTopRightDropdownContentItem'>"+value+"</div>");
				return true;
			break;
			
			// Adiciona linhas ao inicio
			case "dropdownContentPrepend":
				$("#"+$(this).prop("id")+"_dropdown .dbox_menu_cont").prepend("<div class='DMenuTopRightDropdownContentItem'>"+value+"</div>");
				return true;
			break;
			
			// remove conteudo e adiciona novo
			case "dropdownContentHtml":
				$("#"+$(this).prop("id")+"_dropdown .dbox_menu_cont").html("<div class='DMenuTopRightDropdownContentItem'>"+value+"</div>");
				return true;
			break;
			
			// remove conteudo e adiciona novo
			case "blink":
				$(this).fadeOut(function()
					{ 
					$(this).fadeIn(function()
						{ 
						$(this).fadeOut(function()
							{ 
							$(this).fadeIn(); 
							}); 
						}); 
					});
			break;
			}
		}
		
	// gera menu
	return this.each(function()
		{
		settings.menu = $(this);
		settings.menu_id = $(this).prop("id");
		
		// salva opcoes setadas do objeto para uso futuro
		if(isObject(settings) === true)
			$(this).data("DMenuTopRight", settings);
		
		// adiciona classe no objeto
		$(this).addClass("DMenuTopRight");
		
		// TYPE, ajusta configuracao com base no tipo
		switch(settings.type)
			{
			// button (somente botao) ---------------------------
			case "button":
				// adiciona imagem
				$(this).html("<img src='"+settings.img+"' alt='"+settings.title+"' title='"+settings.title+"'>");
                $(this).find("img").tooltip();
				
				// clique unico
				if(isFunction(settings.click) === true)
					{
					$(this).click(function(){ settings.click.call(this); });
					}
			break;
			
			// dropdown (dropdown) ---------------------------
			case "dropdown":
				// adiciona imagem
				$(this).html("<img id='sair' src='"+settings.img+"' alt='"+settings.title+"' title='"+settings.title+"'>");
				
				// controla interacao com mouse
				$(this)
					.mouseenter(function() 
						{
						if($("#"+settings.menu_id+"_dropdown").hasClass("DMenuTopRight_dropdown_open"))
							return true;
						else
							$("#"+settings.menu_id+"_dropdown").fadeIn("fast");							
						})
					.mouseleave(function() 
						{
						if($("#"+settings.menu_id+"_dropdown").hasClass("DMenuTopRight_dropdown_open"))
							return true;
						else
							$("#"+settings.menu_id+"_dropdown").fadeOut("fast");
						})
					.click(function() 
						{
						// if($(".DMenuTopRight_dropdown_open").length > 1)
						//	$(".DMenuTopRight_dropdown_open").removeClass("DMenuTopRight_dropdown_open").fadeOut("fast");
							
						if($("#"+settings.menu_id+"_dropdown").hasClass("DMenuTopRight_dropdown_open"))
							$("#"+settings.menu_id+"_dropdown").removeClass("DMenuTopRight_dropdown_open").fadeOut("fast");
						else
							$("#"+settings.menu_id+"_dropdown").addClass("DMenuTopRight_dropdown_open").fadeIn("fast");
						});

				var dropdown  = '<div id="'+settings.menu_id+'_dropdown" class="dbox_menu DMenuTopRight_dropdown">';
					dropdown += '	<div class="dbox_menu_title">';
					dropdown += '		<img src="'+settings.img+'" align="absmiddle"><span>'+settings.title+'</span>';
					dropdown += '	</div>';
					dropdown += '	<div class="dbox_menu_cont">';
					dropdown += 		settings.dropdownContent;
					dropdown += '	</div>';
					dropdown += '</div>';
			
					$("#DMenuTopRightDropDown").append(dropdown);
			break;
			
			// text (somente texto) ---------------------------
			case "text":
			
				$(this).html("<div class='DMenuTopRightText'>"+settings.textContent+"</div>");
			
			break;
			}
			
		});
	};

})( jQuery );



