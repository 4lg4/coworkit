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
		click unico (usar funcao) DTouchListClick(settings.radios_id,opt);
		Editable (true / false) (opcao para remocao de opcoes)
	
	Exemplo de uso:
		Javascript:
			$("#campo_email").fieldEmail();
			$(".campo_email").fieldEmail();
			
			$("#campo_email").fieldEmail(
				{
				options:values
				});
							
		HTML:
		
			<div>
				<input type='radio' name='nome_do_radio_group' value='$DB->{codigo}' />
				<img src='$DB->{imagem}' />
				<span>$DB->{descricao}</span>
			</div>
*/

(function($){
	
$.fn.DTouchList = function(settings,value) 
	{
	// se for um array ou estiver vazio ajusta variaveis
	if(isObject(settings) === true)
		{
		var settings = $.extend(
			{
			enable			: true,
			btnmore			: '',
			vertical		: false,
			editable		: false,
			addItem			: '',
			// opcoes 
			DTouchListValue	: '',
			DTouchListGetValue	: '',
			DTouchListSetValue	: '',
			DTouchListReset	: '',
			DTouchListAddItems	: '',
			}, settings);
		}
	else
		{
		switch(settings)
			{
			// DTouchListSetValue: Seta Valor ---------------------------
			case "DTouchListSetValue":
			
				if(value == "")
					{
					alert("Devil's: valor nao pode ser vazio !!");
					return false;
					}
				
				// soma contador de vezes que foi modificado o objeto on the fly
				$(this).data("DTouchListSettings")["DTouchListSetValue"] = $(this).data("DTouchListSettings")["DTouchListSetValue"] + 1;
			
				// modifica valor do objeto low-level
				$(this).data("DTouchListSettings")["DTouchListValue"] = value;

				// altera o valor visual
				DTouchListSetValue($(this));
				return true;
				
			break;
			
			// DTouchListReset: Limpa Radio Group ---------------------------
			case "DTouchListReset":
				
				// soma contador de vezes que foi modificado o objeto on the fly
				// $(this).data("DTouchListSettings")["DTouchListSetValue"] = parseInt($(this).data("DTouchListSettings")["DTouchListSetValue"]) + 1;
				
				// modifica valor do objeto low-level
				$(this).data("DTouchListSettings")["DTouchListValue"] = "";
				
				// altera o valor visual
				DTouchListReset($(this));
				return true;
			
			break;
			
			// DTouchListGetValue: Pega valor do Radio Group ---------------------------
			case "DTouchListGetValue":
				
				// soma contador de vezes que foi modificado o objeto on the fly
				// $(this).data("DTouchListSettings")["DTouchListGetValue"] = parseInt($(this).data("DTouchListSettings")["DTouchListGetValue"]) + 1;
				
				// retorna o valor do radio grupo
				return $(this).data("DTouchListSettings")["DTouchListValue"];
			
			break;
			}
		
		
		// retorna / seta demais opcoes que nao necessitam de tratamento
		if(value == "")
			{
			return $(this).data("DTouchListSettings")[settings];
			}
		else
			{
			$(this).data("DTouchListSettings")[settings] = value;
			return true;
			}
		}


 	// retorno do objeto criado
	return this.each(function()
		{ 
		settings.lists = $(this);
		settings.lists_id = $(this).attr("id");
		
		// adicionar item
		if(settings.addItem != "")
			{
			DTouchListAddItem($(this),settings.addItem["val"],settings.addItem["descrp"],settings.addItem["img"]);
			}
		
		
		// ao selecionar
		$(this).children("div").addClass("DTouchList").click(function()
			{
			settings.lists.children("div").removeClass("DTouchList_selected");	// remove classe de todos os lists
			$(this).addClass("DTouchList_selected").find(":radio").attr("checked", true);
			
			// if(settings.postFunction != "")
			//	eval(settings.postFunction);
			DTouchListClick(settings.lists_id,$(this).find(":radio").val());
			});	
			
			
		// ajusta para vertical 
		if(settings.vertical === true)
			{
			$(this).children("div").addClass("DTouchList_vertical");
			
			// adiciona slider
			$(this).DTouchSlider();
			}
		else
			{
			$(this).children("div").addClass("DTouchList_horizontal");
			
			// adiciona slider
			$(this).DTouchSlider({ orientation:"horizontal" });
			}			
			
		// se Editable habilitado
		if(settings.editable === true)
			{
			// verifica se ja existe botao de exclusao
			$(this).children("div").each(function()
				{
				if($(this).find("span").find(".DTouchListRemoveItem").html() == undefined)
					$(this).find("span").append("<span class='DTouchListRemoveItem'>x</span>");
				});

			// Remove List Item -----------	
			$(".DTouchListRemoveItem").click(function() 
				{ 
				$(this).closest("div").remove();
				});
			}
		});
	};

})( jQuery );

// Add List Item --
function DTouchListAddItem(obj,val,descrp,img)
	{
	// se minimo requerido nao preenchido
	if(!val || !obj)
		{
		alert("ERRO: Função deve receber no mínimo o objeto e o valor do item. \n Uso: \n\n DTouchListAddItem(obj,val,descrp,img)");
		return false
		}
		
	// ajusta descricao
	if(!descrp)
		descrp = val;

	// adiciona objeto no radio on the fly
	if(!img)
		obj.append("<div><input type='text' name='DTouchList_"+obj.attr("id")+"' value='"+val+"' /><span>"+descrp+"</span></div>");
	else
		obj.append("<div><input type='text' name='DTouchList_"+obj.attr("id")+"' value='"+val+"' /><img src='"+img+"' /><span>"+descrp+"</span></div>");	
	}

// Change List -----------
function DTouchListChange(obj,val)
	{
	// remove marcacao 
	obj.children("div").removeClass("DTouchList_selected");	
	
	// verifica qual objeto sera marcado
	obj.find("input").each(function()
		{ 
		if($(this).val() == val)
			{
			$(this).attr("checked", true);
			
			// marca o selecionado
			$(this).parent("div").addClass("DTouchList_selected");
			}
		});
	}
	
	
// [INI] DTouchListSetValue: Seta valor do grupo de radio ----------------------------------------------------------------
function DTouchListSetValue(obj)
	{
	var val = obj.data("DTouchListSettings")["DTouchListValue"]; // acesso as configuracoes atuais do objeto
	
	// remove marcacao 
	obj.children("div").removeClass("DTouchList_selected");	
	
	// verifica qual objeto sera marcado
	obj.find("input").each(function()
		{ 
		if($(this).val() == val)
			{
			$(this).attr("checked", true);
			
			// marca o selecionado
			$(this).parent("div").addClass("DTouchList_selected");
			}
		});	
	}
// [END] DTouchListSetValue: ---------------------------------------------------------------------------------------------


// [INI] DTouchListGetValue: Pega valor atual do grupo -------------------------------------------------------------------
function DTouchListGetValue(obj)
	{
	return $("input:radio[name='"+obj.prop("id")+"_radios']:checked").val();
	}
// [END] DTouchListGetValue: ---------------------------------------------------------------------------------------------



// [INI] DTouchListReset: Reseta valor do objeto -------------------------------------------------------------------------
function DTouchListReset(obj)
	{
	var settings = obj.data("DTouchListSettings"); // acesso as configuracoes atuais do objeto
	
	// remove marcacao 
	obj.children("div").removeClass("DTouchList_selected");
	
	// remove checked do grupo
	$("input:radio[name='"+obj.prop("id")+"_radios']:checked").prop("checked",false);
	}
// [END] DTouchListReset: ------------------------------------------------------------------------------------------------



// [INI] DTouchListAddItem: Adiciona itens no radio group ----------------------------------------------------------------
function DTouchListAddItems(obj)
	{
	var showVal = ""; 
	var showImg = "";
	var settings = obj.data("DTouchListSettings"); // acesso as configuracoes atuais do objeto
	var items = settings.DTouchListAddItems; 
	
	// monta itens e adiciona no objeto
	for(var f in items)
		{ 
		// ajusta se nao tiver descricao
		if(items[f]['descrp'] == "")
			items[f]['descrp'] = items[f]['val'];
			
		// mostra valor impresso (ex. Chamado Cards)
		if(settings.showVal === true)
			showVal = "<span class='DTouchList_showVal'>"+items[f]['val']+"</span>";

		// ajusta se tem imagem
		if(items[f]['img'] != "")
			showImg = "<img src='"+items[f]['img']+"' />";
			
		// adiciona objeto no radio on the fly
		obj.append("<div><input type='radio' name='"+obj.attr("id")+"_radios' value='"+items[f]['val']+"' />"+showVal+" "+showImg+"<span class='DTouchList_descrp'>"+items[f]['descrp']+"</span></div>");
		}
		
	// atualiza radio
	obj.DTouchList(settings);
	}
// [END] DTouchListAddItem: ----------------------------------------------------------------------------------------------