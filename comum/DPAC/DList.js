/**
 * 
 * Gera lista apartir de uma tabela no banco de dados
 *
 * @example $("#ID").DList({ addItem: "[{val:value,descrp:'description',img:'image'}]" });
 * @desc Uso Básico
 *
 * @param addItem Array (obrigatório) Ver: Exemplo addItem
 *
 * @type jQuery
 *
 * @name DList
 * @cat Plugins / Core
 * @author DONE Tecnologia - Adriano Karkow Gaiatto Leal (http://gaiattos.com/akgleal.com)
 */


(function($){
	
$.fn.DList = function(settings,value)
	{
	// se for um array ou estiver vazio ajusta variaveis
	if(isObject(settings) === true)
		{
		var settings = $.extend(
			{
			table			: "",
			sql_codigo		: "",
			sql_descrp		: "",
			sql_order		: "",
			sql_limit		: "",
			orientation		: "vertical",
			type			: "select",
			multiple		: false,
			loader			: false,
			// opcoes 
			click		: '',
			dblClick	: '',
		}, settings || {});
		}
	else
		{
		switch(settings)
			{
			// DListSetValue: Seta Valor ---------------------------
			case "val":
		
				// DListSetValue($(this));
				// return true;
				
			break;
			
			// DListReset: Limpa Radio Group ---------------------------
			case "reset":

				// DListReset($(this));
				// return true;
			
			break;			
			}
		}
	
	return this.each(function()
		{
		settings.list = $(this);
		settings.list_id = $(this).attr("id");
		
		// salva opcoes setadas do objeto para uso futuro
		if(isObject(settings) === true)
			$(this).data("DListSettings", settings);

		// Adiciona classe DListContainer na div PAI
		// $(this).addClass("DListContainer");


		// TYPE, ajusta configuracao com base no tipo
		switch(settings.type)
			{
			case "select":
			
			// adiciona loader
			if(settings.loader === true)
				LoadingObj(settings.list_id)
				
			// se cache referente a listagem ja estiver criado retorna objeto usando ele
			if(DListCache[settings.table])
				{
				DListReturn(settings.list);
				
				return true;
				}	

			
				// adiciona loader
				if(settings.loader === true)
					LoadingObj(settings.list_id);
			
				$.ajax({
					async:false,
					type: "POST",
					url: "/sys/cfg/DPAC/DListGet.cgi",
					// dataType: "html",
					dataType : "json",
					data: "&ID="+$('#AUX input[name="ID"]').val()+"&T="+settings.table+"&D="+settings.sql_descrp+"&C="+settings.sql_codigo+"&L="+settings.sql_limit+"&O="+settings.sql_order,
					success: function(data)
						{
						// pega json obj
						var LIST = data;
						
						// gera select
						var sel = "";
						var sel_in = "";
						for(var f in LIST)
							{
							sel_in += "<option value=\""+LIST[f]["codigo"]+"\">"+LIST[f]["descrp"]+"</option>";
							}
							
						// salva cache
						DListCache[settings.table] = sel_in;
						
						// retorna objeto
						DListReturn(settings.list);
						},
					error: function(data)
						{
						// se erro em todas as tentativas retorna tip + mensagem de erro
						console.log(data);
						alerta("Devils: O Plugin: \n\n    DList \n\né usada em conjunto com /cfg/DListGet. \n\n *** verficar logs no console");
						unLoadingObj();

						return false;
						}
					});
					
			//	}
			break;
			}
		});
	};

})( jQuery );

// [INI] DListReturn: retorna objeto montado ------------------------------------------------------------------------
function DListReturn(obj)
	{
	var settings = obj.data("DListSettings");
	
	sel_in = DListCache[settings.table];
	
	// ajusta id e nome do objeto que sera gerado
	var sel_id = "";
	var sel_name = "";
	
	if(obj.prop("id") != "")	
		sel_id = obj.prop("id");
	else if(obj.prop("name") != "")
		sel_id = obj.prop("name");
	else
		console.log("Devils: ID e NAME não definidos !!");
	
	if(obj.prop("name") == "")
		if(obj.prop("id") != "")	
			sel_name = obj.prop("id");
		else
			console.log("Devils: ID e NAME não definidos !!");
	else
		sel_name = obj.prop("name");

	// ajusta id unico
	var aleatorio = new Date().getUTCMilliseconds();
	sel_id = sel_id +"_"+ aleatorio;
	
	// select, cria select
	sel = "<select id='"+sel_id+"' name='"+sel_name+"' class='"+obj.prop("class")+"'>"+sel_in+"</select>";
	
	// adiciona novo no lugar com mesmo nome
	obj.replaceWith(sel);
	
	// se vier ja selecionado marca !
	if(settings.value != "")
		$("#"+sel_id).val(settings.value);
	
	// remove loader
	if(settings.loader === true)
		unLoadingObj(settings.list_id);
	}
// [END] DListReturn: retorna objeto montado ------------------------------------------------------------------------



// [INI] DListSetValue: Seta valor do grupo de radio ----------------------------------------------------------------
function DListSetValue()
	{
	}
// [END] DListSetValue: ---------------------------------------------------------------------------------------------


// [INI] DListGetValue: Pega valor atual do grupo -------------------------------------------------------------------
function DListGetValue(obj)
	{
	}
// [END] DListGetValue: ---------------------------------------------------------------------------------------------


// [INI] DListReset: Reseta valor do objeto -------------------------------------------------------------------------
function DListReset(obj)
	{
	var settings = obj.data("DListSettings"); // acesso as configuracoes atuais do objeto
	
	// modifica valor do objeto low-level
	obj.data("DListSettings")["DListValue"] = "";
	
	}
// [END] DListReset: ------------------------------------------------------------------------------------------------


