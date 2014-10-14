/* [INI]  DTouchAccordion (by http://gaiattos.com/akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
		Javascript:
	
		CSS:
			/css/DPAC/DPAC.css
			/css/DPAC/DTouchAccordion.css

    Opcoes:
		Enable			(Habilita / Desabilita)
		Button More		(Mostra botao mais)
		Orientation		(Horizontal / Vertical)
		Editable  		(opcao de icone de remocao de item)
		add Item 		(adiciona item /items and reload obj)
		Visible Items 	(0 = todos)
	
	Exemplo de uso:
		Javascript:
			$("#ID").DTouchAccordion();
			$(".Class").DTouchAccordion();
			
			$("#ID")..DTouchAccordion(
				{
				options:values
				});
							
		HTML:
			<div id=ID class=Class></div>
*/

(function($){
	
$.fn.DTouchAccordion = function(settings,value) 
	{
	// se for um array ou estiver vazio ajusta variaveis
	if(isObject(settings) === true)
		{
		var settings = $.extend(
			{
			enable			: true,
			orientation		: "vertical",
			addItem			: '',
			// opcoes 
			DTouchAccordionValue	 : '',
			DTouchAccordionGetValue	 : '',
			DTouchAccordionSetValue	 : '',
			DTouchAccordionAddItems	 : '',
			DTouchAccordionExpandAll : '',
			}, settings || {});
		}
	else
		{
		switch(settings)
			{
			// DTouchAccordionSetValue: Seta Valor ---------------------------
			case "DTouchAccordionSetValue":
			
				if(value == "")
					{
					alert("Devil's: valor nao pode ser vazio !!");
					return false;
					}
				
				// soma contador de vezes que foi modificado o objeto on the fly
				$(this).data("DTouchAccordionSettings")["DTouchAccordionSetValue"] = $(this).data("DTouchAccordionSettings")["DTouchAccordionSetValue"] + 1;
			
				// modifica valor do objeto low-level
				$(this).data("DTouchAccordionSettings")["DTouchAccordionValue"] = value;

				// altera o valor visual
				DTouchAccordionSetValue($(this));
				return true;
				
			break;
			
			// DTouchAccordionReset: Limpa Radio Group ---------------------------
			case "DTouchAccordionReset":
				
				// soma contador de vezes que foi modificado o objeto on the fly
				// $(this).data("DTouchAccordionSettings")["DTouchAccordionSetValue"] = parseInt($(this).data("DTouchAccordionSettings")["DTouchAccordionSetValue"]) + 1;
				
				// remover todos os itens do radio group
				if(value == "hard")
					{
					// remove itens
					$(this).removeData("DTouchAccordionSettings");
					
					// limpa conteudo visual
					$(this).html("");
					
					return true;
					}
				
				
				// modifica valor do objeto low-level
				$(this).data("DTouchAccordionSettings")["DTouchAccordionValue"] = "";
				
				// altera o valor visual
				DTouchAccordionReset($(this));
				return true;
			
			break;
			
			// DTouchAccordionGetValue: Pega valor do Radio Group ---------------------------
			case "DTouchAccordionGetValue":
				
				// soma contador de vezes que foi modificado o objeto on the fly
				// $(this).data("DTouchAccordionSettings")["DTouchAccordionGetValue"] = parseInt($(this).data("DTouchAccordionSettings")["DTouchAccordionGetValue"]) + 1;
				
				// retorna o valor do radio grupo
				return $(this).data("DTouchAccordionSettings")["DTouchAccordionValue"];
			
			break;
			}
		
		
		// retorna / seta demais opcoes que nao necessitam de tratamento
		if(value == "")
			{
			return $(this).data("DTouchAccordionSettings")[settings];
			}
		else
			{
			$(this).data("DTouchAccordionSettings")[settings] = value;
			return true;
			}
		}
	
	return this.each(function()
		{
		settings.radios = $(this);
		settings.radios_id = $(this).attr("id");
		settings.radios_qtd = $(this).children("div").length; // quantidade de itens do radio
		
		// salva opcoes setadas do objeto para uso futuro
		if(isObject(settings) === true)
			$(this).data("DTouchAccordionSettings", settings);
		
		// adicionar item / items
		if(settings.addItem != "")
			{
			// limpa DRadio para atualizar conteudo 
			$(this).html("");

			// ajusta para criacao
			$(this).data("DTouchAccordionSettings")["DTouchAccordionAddItems"] = settings.addItem;
			
			// limpa variavel de adicao de itens
			$(this).data("DTouchAccordionSettings")["addItem"] = "";
			
			// adiciona itens
			DTouchAccordionAddItems($(this));
			
			// aguarda o retorno da criacao para gerar o objeto
			return true;
			}
		
		
		// corrige largura do container ao iniciar (bug: conhecido quando regera o objeto que ja foi setado com largura maxima)
		$(this).css("width","auto");
		
		// se habilitado botao mais
		if(isFunction(settings.buttonMore) === true)
			{
			$(this)
				.append("<div class='DTouchAccordionButtonMore'>Limpar Seleção</div>")
				.show();
			
			settings.buttonMore.call(this);
			}
			
		// Adiciona classe DTouchAccordionContainer na div PAI
		$(this).addClass("DTouchAccordionContainer");
		
		// Ajuste da orientacao do objeto
		$(this).children("div").addClass(" DTouchAccordion_"+settings.orientation);
		
		// pega a largura do item para rolagem horizontal
		settings.radios_item_width = $(this).children("div:first-child").width();	
		
		// ao selecionar
		$(this).children("div").addClass("DTouchAccordion").click(function()
			{ 	
			settings.radios.children("div").removeClass("DTouchAccordion_selected");	// remove classe de todos os radios
			$(this).addClass("DTouchAccordion_selected").find(":radio").attr("checked", true);
			
			if(settings.click === true)
				DTouchAccordionClick(settings.radios, DTouchAccordionGetValue(settings.radios));
			// DTouchAccordionClick(settings.radios_id,$(this).find(":radio").val());
			});	
		
		// ajuste da largura do radio se for horizontal
		if(settings.orientation == "horizontal")
			{
			// se a quantidade de itens for maior que o padrao visivel
			if(settings.visibleItems > 0)
				if(settings.radios_qtd > settings.visibleItems)
					$(this).css("width",(settings.radios_item_width * settings.visibleItems)+"px");
			}
			
		// se Editable habilitado
		if(settings.editable === true)
			{
			// verifica se ja existe botao de exclusao
			$(this).children("div").each(function()
				{
				if($(this).find("span").find(".DTouchAccordionRemoveItem").html() == undefined)
					$(this).find("span").append("<span class='DTouchAccordionRemoveItem'>x</span>");
				});

			// Remove Radio Item 
			$(".DTouchAccordionRemoveItem").click(function() 
				{ 
				$(this).closest("div").remove();
				});
			}

		// Adiciona Slider
		$(this).DTouchSlider({ orientation: settings.orientation });
		});
	};

})( jQuery );


// [INI] DTouchAccordionSetValue: Seta valor do grupo de radio ----------------------------------------------------------------
function DTouchAccordionSetValue(obj)
	{
	var val = obj.data("DTouchAccordionSettings")["DTouchAccordionValue"]; // acesso as configuracoes atuais do objeto
	
	// remove marcacao 
	obj.children("div").removeClass("DTouchAccordion_selected");	
	
	// verifica qual objeto sera marcado
	obj.find("input").each(function()
		{ 
		if($(this).val() == val)
			{
			$(this).attr("checked", true);
			
			// marca o selecionado
			$(this).parent("div").addClass("DTouchAccordion_selected");
			}
		});	
	}
// [END] DTouchAccordionSetValue: ---------------------------------------------------------------------------------------------


// [INI] DTouchAccordionGetValue: Pega valor atual do grupo -------------------------------------------------------------------
function DTouchAccordionGetValue(obj)
	{
	return $("input:radio[name='"+obj.prop("id")+"_radios']:checked").val();
	}
// [END] DTouchAccordionGetValue: ---------------------------------------------------------------------------------------------



// [INI] DTouchAccordionReset: Reseta valor do objeto -------------------------------------------------------------------------
function DTouchAccordionReset(obj)
	{
	var settings = obj.data("DTouchAccordionSettings"); // acesso as configuracoes atuais do objeto
	
	// remove marcacao 
	obj.children("div").removeClass("DTouchAccordion_selected");
	
	// remove checked do grupo
	$("input:radio[name='"+obj.prop("id")+"_radios']:checked").prop("checked",false);
	}
// [END] DTouchAccordionReset: ------------------------------------------------------------------------------------------------



// [INI] DTouchAccordionAddItem: Adiciona itens no radio group ----------------------------------------------------------------
function DTouchAccordionAddItems(obj)
	{
	var showVal = ""; 
	var showImg = "";
	var settings = obj.data("DTouchAccordionSettings"); // acesso as configuracoes atuais do objeto
	var items = settings.DTouchAccordionAddItems; 
	
	// monta itens e adiciona no objeto
	for(var f in items)
		{ 
		// ajusta se nao tiver descricao
		if(items[f]['descrp'] == "")
			items[f]['descrp'] = items[f]['val'];
			
		// mostra valor impresso (ex. Chamado Cards)
		if(settings.showVal === true)
			showVal = "<span class='DTouchAccordion_showVal'>"+items[f]['val']+"</span>";

		// ajusta se tem imagem
		if(items[f]['img'])
			showImg = "<img src='"+items[f]['img']+"' />";
			
		// adiciona objeto no radio on the fly
		obj.append("<div><input type='radio' name='"+obj.attr("id")+"_radios' value='"+items[f]['val']+"' />"+showVal+" "+showImg+"<span class='DTouchAccordion_descrp'>"+items[f]['descrp']+"</span></div>");
		}
		
	// atualiza radio
	obj.DTouchAccordion(settings);
	}
// [END] DTouchAccordionAddItem: ----------------------------------------------------------------------------------------------