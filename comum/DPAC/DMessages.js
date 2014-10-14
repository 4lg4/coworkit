/**
 * 
 * Gerencia mensagens do sistema e mostra no icone de chat do usuario
 *
 * @example $("#ID").DMessages({ addItem: "[{val:value,descrp:'description',img:'image'}]" });
 * @desc Uso Básico
 * @example $("#ID").DMessages({ addItem: "[{val:(valor de retorno),descrp:(descrição do item),img:(imagem do item)}]" });
 * @desc addItem, img é opcional
 * @example $('#accordion').activate(1);
 * @desc Activate the second content of the Accordion contained in &lt;div id="accordion"&gt;.
 *
 * @param addItem Array (obrigatório) Ver: Exemplo addItem
 *
 * @type jQuery
 *
 * @name DMessages
 * @cat Plugins/Accordion
 * @author DONE Tecnologia - Adriano Karkow Gaiatto Leal (http://gaiattos.com/akgleal.com)
 */


function DMessages(item,type)
	{
	if(!type)
		type = "SysMsg";

	// adiciona linha no menu suspenso de mensagens
	$("#DMenuTopRight_chat").DMenuTopRight("dropdownContentAppend",'<b>'+type+':</b>'+item)
	
	// pisca objeto
	$("#DMenuTopRight_chat").DMenuTopRight("blink");
	}
	
	
// $("#menu_top_right_chat").fadeOut(function(){ $(this).fadeIn(); });

/*
(function($){
	
$.fn.DMessages = function(settings,value)
	{
	// se for um array ou estiver vazio ajusta variaveis
	if(isObject(settings) === true)
		{
		var settings = $.extend(
			{	
			enable			: true,
			addItem			: '',
			visibleItems	: 5, // padrao 5 itens se quiser mostrar tudo usar 0
			
			// opcoes 
			DMessagesClick	: '',
			DMessagesDblClick	: '',
			DMessagesValue	: '',
			DMessagesGetValue	: '',
			DMessagesSetValue	: '',
			DMessagesReset	: '',
			DMessagesAddItems	: '',
			DMessagesRefresh		: ''
			DMessagesRefresh		: ''
			}, settings || {});
		}
	else
		{
		switch(settings)
			{
			// DMessagesAddItems: adiciona item ---------------------------
			case "DMessagesAddItems":				
				
				
				
				// ajusta para criacao
				$(this).data("DMessagesSettings")["DMessagesAddItems"] = settings.addItem;
				
				DMessagesAddItems(obj)
				
			break;
			
			// DMessagesSetValue: Seta Valor ---------------------------
			case "SetVal":
			case "SetValue":
			case "DMessagesSetValue":
			
				if(value == "")
					{
					// alert("Devil's: valor nao pode ser vazio !!");
					// reseta obj
					$(this).DMessages("DMessagesReset");
					return false;
					}
				
				// soma contador de vezes que foi modificado o objeto on the fly
				$(this).data("DMessagesSettings")["DMessagesSetValue"] = $(this).data("DMessagesSettings")["DMessagesSetValue"] + 1;
			
				// modifica valor do objeto low-level
				$(this).data("DMessagesSettings")["DMessagesValue"] = value;

				// altera o valor visual
				DMessagesSetValue($(this));
				return true;
				
			break;
			
			// DMessagesReset: Limpa Radio Group ---------------------------
			case "reset":
			case "DMessagesReset":
				
				// soma contador de vezes que foi modificado o objeto on the fly
				// $(this).data("DMessagesSettings")["DMessagesSetValue"] = parseInt($(this).data("DMessagesSettings")["DMessagesSetValue"]) + 1;
				
				// remover todos os itens do radio group
				if(value == "hard")
					{
					// remove itens
					$(this).removeData("DMessagesSettings");
					
					// limpa conteudo visual
					$(this).html("");
					
					return true;
					}
				
				// altera o valor visual
				DMessagesReset($(this));
				return true;
			
			break;
			
			// DMessagesGetValue: Pega valor do Radio Group ---------------------------
			case "val":
			case "value":
			case "GetValue":
			case "DMessagesGetValue": //  || "val":
				
				// retorna o valor do radio grupo
				try 
					{ 
					return $(this).data("DMessagesSettings")["DMessagesValue"];
					} 
				catch(err) 
					{ 
					return false;
					}
					
			break;
			
			// DMessagesAccordionContent: Adiciona conteudo ao radio especifico ---------------------------
			case "DMessagesAccordionContent":
			
				// se valor for vazio
				if(value == "")
					{
					alert("Devil's: valor nao pode ser vazio !!");
					return false;
					}

				// retorna o valor do radio grupo
				$(this).data("DMessagesSettings")["DMessagesAccordionContent"] = value;
				
				// adiciona conteudo ao accordion especifico
				DMessagesAccordionContent($(this));
			
			break;
			
			// DMessagesRefresh: Refresh no grupo de radio frequente usado em tables -----------------------
			case "refresh":
			case "DMessagesRefresh":

				if($(this).data("DMessagesSettings")["type"] == "table")
					$('#'+$(this).prop("id")+'_tb').dataTable().fnDraw();
				else
					{
					console.log("Opção usada somente para TABLES");
					alerta("Devils: Opção usada somente para TABLES");
					}
				
			break;
			}
		
		
		// retorna / seta demais opcoes que nao necessitam de tratamento
		if(value == "")
			{
			return $(this).data("DMessagesSettings")[settings];
			}
		else
			{
			$(this).data("DMessagesSettings")[settings] = value;
			return true;
			}
		}
	
	return this.each(function()
		{
		settings.radios = $(this);
		settings.radios_id = $(this).attr("id");
		settings.radios_qtd = $(this).children("div").length; // quantidade de itens do radio
		
		
		
		
		
		
		/*
		// salva opcoes setadas do objeto para uso futuro
		if(isObject(settings) === true)
			$(this).data("DMessagesSettings", settings);
		
		// adicionar item / items
		if(settings.addItem != "")
			{
			// limpa DRadio para atualizar conteudo 
			$(this).html("");
			
			// se for um accordion destroy objeto
			if($(this).hasClass('ui-accordion')) 
			    $(this).accordion('destroy');
			
			// ajusta para criacao
			$(this).data("DMessagesSettings")["DMessagesAddItems"] = settings.addItem;
			
			// limpa variavel de adicao de itens
			$(this).data("DMessagesSettings")["addItem"] = "";
			
			// adiciona itens
			DMessagesAddItems($(this));
			
			// aguarda o retorno da criacao para gerar o objeto
			return true;
			}
		
		});
	};

})( jQuery );


// [INI] DMessagesSetValue: Seta valor do grupo de radio ----------------------------------------------------------------
function DMessagesSetValue(obj)
	{
	var settings = obj.data("DMessagesSettings"); // acesso as configuracoes atuais do objeto
	var val = obj.data("DMessagesSettings")["DMessagesValue"]; // acesso as configuracoes atuais do objeto
	
	// remove marcacao 
	obj.children("div").removeClass("DMessages_selected");	
	
	// verifica qual objeto sera marcado
	obj.find("input").each(function()
		{ 
		if($(this).val() == val)
			{
			$(this).attr("checked", true);
			
			// marca o selecionado
			if(settings.type != "accordion")
				$(this).parent("div").addClass("DMessages_selected");
			}
		});	
	}
// [END] DMessagesSetValue: ---------------------------------------------------------------------------------------------


// [INI] DMessagesGetValue: Pega valor atual do grupo -------------------------------------------------------------------
function DMessagesGetValue(obj)
	{
	return $("input:radio[name='"+obj.prop("id")+"_radios']:checked").val();
	}
// [END] DMessagesGetValue: ---------------------------------------------------------------------------------------------


// [INI] DMessagesReset: Reseta valor do objeto -------------------------------------------------------------------------
function DMessagesReset(obj)
	{
	var settings = obj.data("DMessagesSettings"); // acesso as configuracoes atuais do objeto
	
	// modifica valor do objeto low-level
	obj.data("DMessagesSettings")["DMessagesValue"] = "";
	
	// remove marcacao 
	obj.children("div").removeClass("DMessages_selected");
	
	// remove checked do grupo
	$("input:radio[name='"+obj.prop("id")+"_radios']:checked").prop("checked",false);
	}
// [END] DMessagesReset: ------------------------------------------------------------------------------------------------



// [INI] DMessagesAddItem: Adiciona itens no radio group ----------------------------------------------------------------
function DMessagesAddItems(obj)
	{
	var showVal = ""; 
	var showImg = "";
	var settings = obj.data("DMessagesSettings"); // acesso as configuracoes atuais do objeto
	var items = settings.DMessagesAddItems; 
	
	// variaveis para opcao tabela
	var table_count = 1; // controle para header e footer da tabela
	var table_content = "";
	var table_line = "";
	
	// monta itens e adiciona no objeto
	for(var f in items)
		{ 
		// ajusta se nao tiver descricao
		if(items[f]['descrp'] == "")
			items[f]['descrp'] = items[f]['val'];
			
		// mostra valor impresso (ex. Chamado Cards)
		if(settings.showVal === true)
			showVal = "<span class='DMessages_showVal'>"+items[f]['val']+"</span>";

		// ajusta se tem imagem
		if(items[f]['img'])
			showImg = "<img src='"+items[f]['img']+"' />";
			
		// adiciona objeto no radio on the fly
		// TYPE, ajusta configuracao com base no tipo
		switch(settings.type)
			{
			// Vazio: Adiciona Slider ---------------------------
			case "":
				obj.append("<div><input type='radio' name='"+obj.attr("id")+"_radios' value='"+items[f]['val']+"' />"+showVal+" "+showImg+"<span class='DMessages_descrp'>"+items[f]['descrp']+"</span></div>");
			break;
			
			// Accordion: adiciona accordion ---------------------------
			case "accordion":
				obj.append("<h3><div><input type='radio' name='"+obj.attr("id")+"_radios' value='"+items[f]['val']+"' />"+showVal+" "+showImg+"<span class='DMessages_descrp'>"+items[f]['descrp']+"</span></div></h3>");
				obj.append("<div id='"+obj.attr("id")+"_radios_accordion_content_"+items[f]['val']+"'></div>");
			break;
			
			// Table: adiciona tabela ---------------------------
			case "table":
			
				// ajusta array para laco
				var i = items[f]['descrp'];
				
				// inicia tabela
				if(table_count == 1)
					{
					table_line += "<table id='"+settings.radios_id+"_tb' class='DMessages_table'><thead><tr><th class='DMessages_table_first_cell'>cod</th>";
					
					// monta headers
					for(var ff in i)
						{					
						table_line += "<th>"+ff+"</th>";
						}
					
					table_line += "</tr></thead><tbody>";
					}
				
				
				// monta radio group
				table_content += "<input type='radio' name='"+obj.attr("id")+"_radios' value='"+items[f]['val']+"' class='DMessages_table_radios' />";
				
				// monta linha da tabela
				table_content += "<tr><td class='DMessages_table_first_cell'>"+items[f]['val']+"</td>";
				for(var ff in i)
					{					
					table_content += "<td>"+i[ff]+"</td>";
					}
				table_content += "</tr>";
				
				
				// finaliza tabela
				if(table_count == items.length)
					{
					table_line += table_content+"</tbody></table>";
					
					// adiciona tabela no objeto
					obj.append(table_line);
					}
										
				// soma variavel de controle de adicao de itens
				table_count++;
			break;
			}
		}
		
	// atualiza radio
	obj.DMessages(settings);
	}
// [END] DMessagesAddItem: ----------------------------------------------------------------------------------------------


// [INI] DMessagesAccordionContent: Adiciona valor ao conteudo do accordion ---------------------------------------------
function DMessagesAccordionContent(obj)
	{
	var settings = obj.data("DMessagesSettings"); // acesso as configuracoes atuais do objeto
	var obj_id = obj.prop("id")+"_radios_accordion_content_"+DMessagesGetValue(obj); // monta id do conteudo
	
	$("#"+obj_id).html(settings.DMessagesAccordionContent);
	}
// [END] DMessagesAccordionContent: -------------------------------------------------------------------------------------
*/
