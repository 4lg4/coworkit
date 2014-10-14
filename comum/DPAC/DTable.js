/* [INI]  DTouch field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
		Javascript:
			jquery
			jquery-ui
			DGrid
				include("/comum/jquery/jquery.dataTables.js");
				include("/comum/jquery/jquery.dataTables.rowGrouping.js");
				loadCSS("/css/dataTable.css");
				
	
		CSS:
			/css/DPAC/DPAC.css
				.DTable { }

    Opcoes:
		Enable / Disable
		addItem
	
	Exemplo de uso:
		Javascript:
			$("#tabela_container").DTable();
			
			$("#tabela_container").DTable(
				{
				options:values
				});
							
		HTML:
		
*/

(function($){
	
$.fn.DTable = function(settings,value) 
	{
	// se for um array ou estiver vazio ajusta variaveis
	if(isObject(settings) === true)
		{
		var settings = $.extend(
			{
			enable		: true,
			addItem		: ''
			// opcoes 
			DTableAddItems	: '',
			}, settings);
		}
	else
		{
		console.log("DTable Getter");
		}
	
	return this.each(function()
		{
		// settings.title_box = "<div class='DTable_title'>"+settings.title+"</div>";
		
		// adicionar item / items
		if(settings.addItem != "")
			{
			// limpa Dtable para atualizar conteudo 
			$(this).html("");

			// ajusta para criacao
			$(this).data("DTableSettings")["DTableAddItems"] = settings.addItem;
			
			// limpa variavel de adicao de itens
			$(this).data("DTableSettings")["addItem"] = "";
			
			// adiciona itens
			DTableAddItems($(this));
			
			// aguarda o retorno da criacao para gerar o objeto
			return true;
			}
				
		/*
		// linha
		R += "<tr><td style='display:none;'>$chamados->{codigo}</td><td>$chamados->{codigo}</td><td> $chamados->{data} </td><td> $chamados->{usuario_logado} - $chamados->{cliente_endereco} - $chamados->{dtag} - $chamados->{usuario} - $chamados->{descrp}</td></tr>";
		*/
		
		$(this).addClass("DTable");
		});
	};

})( jQuery );


// [INI] DTableAddItem: Adiciona itens no radio group ----------------------------------------------------------------
function DTableAddItems(obj)
	{
	var settings = obj.data("DTableSettings"); // acesso as configuracoes atuais do objeto
	var items = settings.DTableAddItems; 
	
	// monta itens e adiciona no objeto
	for(var f in items)
		{ 
		// ajusta se nao tiver descricao
		if(items[f]['descrp'] == "")
			items[f]['descrp'] = items[f]['val'];
			
		// mostra valor impresso (ex. Chamado Cards)
		if(settings.showVal === true)
			showVal = "<span class='DTable_showVal'>"+items[f]['val']+"</span>";

		// ajusta se tem imagem
		if(items[f]['img'])
			showImg = "<img src='"+items[f]['img']+"' />";
			
		// adiciona objeto no radio on the fly
		// TYPE, ajusta configuracao com base no tipo
		obj.append("<div><input type='radio' name='"+obj.attr("id")+"_radios' value='"+items[f]['val']+"' />"+showVal+" "+showImg+"<span class='DTable_descrp'>"+items[f]['descrp']+"</span></div>");
		
		
		// tabela
		var Table  = "<table id='list_container_tbl'>";
			Table += "<thead>";
			Table += "		<tr>";
			Table += "			<th style='display:none;'>Cod</th>";
			Table += "			<th>Cod</th>";
			Table += "			<th>Data</th>";
			Table += "			<th>Descrp</th>";
			Table += "		</tr>";
			Table += "</thead>";
			Table += "<tbody>";
			Table += 		$R;
			Table += "</tbody>";
			Table += "</table>";
		
		}
		
	// atualiza radio
	obj.DTable(settings);
	}
// [END] DTableAddItem: ----------------------------------------------------------------------------------------------

