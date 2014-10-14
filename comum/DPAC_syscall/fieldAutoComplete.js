/* [INI]  AUTOCOMPLETE  (by akgleal.com)  ----------------------------------------------------------------------------- 

	Dependencias:
	- Arquivo "search.cgi" deve estar dentro da pasta do modulo a ser usado (melhorar, unificando em um local somente!)
	
	CSS necessario:
	.search 
		{ 
		background:#fff url("/img/search.png") top right no-repeat; 
		background-size: 16px;
		}
	.searchAdd
		{ 
		background:#fff url("/img/search_add.png") top right no-repeat; 
		background-size: 16px;
		}
	.fieldDisable { padrao de cores para campo desabilitado }

	opcoes:

	exemplo de uso:

  Search na tbl baseado na digitacao do campo e gera campos autocomplete  

--------------------------------------------------- */

function fieldAutoComplete(field,tbl,fast)
	{
	/*	modelo de uso da funcao
	field = campo que recebe o autocomplete
		<input type='text' name='contratante' id='contratante' style="width:50px;">
		<input type='text' name='contratante_descrp' id='contratante_descrp' style="width:70%;" autocomplete="off">

		// ex. uso com campos adicionais
		contratante = new autoComplete("contratante", "empresa");
		contratante.setSearchField("nome");
		contratante.show();

		// uso basico (sendo numero 1 no final atalho para mostrar obejto direto)
		cliente = new autoComplete("clientes", "empresa", 1);
	*/

	var field = field;	// campo que recebe o autocomplete
	var tbl = tbl;	// tabela de pesquisa do autocomplete
	var sfield = "descrp";	// campo de pesquisa do banco de dados
	var pfunc = "";	// Post function, funcao adicional para tratar campos de multiplo add ou de outras instrucoes em sequencia
	var sql = "";	// sql extra ex. select * from tbl where sql
	var qtd = 2;	// quantidade minima de caracteres a ser usado
	var join = ""; // instrucoes do join
	var order = "descrp"; // campo de ordenacao
	var rfield = "descrp"; // campo com o retorno do sql 
	var nfield = ""; // jump to the next field
	var notab = "";
	
	$("#"+field+"_descrp").addClass("search"); // add classe com configuracao do campo de pesquisa auto complete

	this.setField = function(val) { field = val; }
	this.setTable = function(val) { tbl = val; }
	this.setSearchField = function(val) { sfield = val; }
	this.setPostFunction = function(val) { pfunc = val; }
	this.setJoin = function(val) { join = val; }
	this.setSql = function(val,fast) 
		{ 
		sql = val; 
		if(fast)
			return this.show();
		}
	this.setOrder = function(val) { order = val; }
	this.setReturnField = function(val) { rfield = val; }
	this.setMinQtd = function(val) { qtd = val; }
	this.setJumpNextField = function(val) { nfield = val; }

	// adiciona pesquisa autocomplete no campo	
	this.show = function() 
		{
		  // if(field == "sol_responsavel")	
			// alert("search.cgi?ID="+document.forms[0].ID.value+"&tbl="+tbl+"&join="+join+"&sql="+sql+"&order="+order+"&rfield="+rfield+"&sfield="+sfield+"&sql="+sql);
		
		// source: "search.cgi?tbl="+tbl+"&join="+join+"&sql="+sql+"&order="+order+"&rfield="+rfield+"&sfield="+sfield+"&sql="+sql,
		$("#"+field+"_descrp").attr( "autocomplete", "off" ).autocomplete({
			delay: 0, // ajusta delay de pesquisa em microsegundos padrao 300
			source: "search.cgi?ID="+document.forms[0].ID.value+"&tbl="+tbl+"&join="+join+"&sql="+sql+"&order="+order+"&rfield="+rfield+"&sfield="+sfield+"&sql="+sql,
			// source: "../../cfg/DPAC/fieldAutoComplete.cgi?tbl="+tbl+"&join="+join+"&sql="+sql+"&order="+order+"&rfield="+rfield+"&sfield="+sfield+"&sql="+sql,
			// source: "search.cgi",
			// data: "?tbl="+tbl+"&join="+join+"&sql="+sql+"&order="+order+"&rfield="+rfield+"&sfield="+sfield+"&sql="+sql,
			method: "POST",
			minLength: qtd,
			change: function(){ },
			select: function(event, ui) {
				if(ui)
					{
					$("#"+field).val(ui.item.id);
					$("#"+field+"_descrp").val(ui.item.value);
					if(nfield != "")
						$("#"+nfield).focus();
					}					
			},
			close: function(event) { // limpa campos quando selecionado na lista um valor e enter pressed (multiplo include)
				if(event.which == 13)
					{
					if($("#"+field+"_descrp").val() != "")
						{
						// executa post function
						if(pfunc != "")
					 		eval(pfunc);
						}
					}
				// if(event.which == 9) // Tab pressionado do nothing
				// 	event.preventDefault();
			} 
		// quando alguma tecla é pressionada
			})
			
		.keydown(function(event) 
			{
			// Tab pressionado do nothing
			if(notab == 1)
				{
				if(event.which == 9) 
					event.preventDefault();
				}
				
			// alert(window.location.pathname.split('/'));
			// alert(window.location.pathname.replace('//','/').split('/'));
			// alert(window.location.pathname.replace('//','/').split('/').length -1);
			
			if(event.which == 13) // Enter pressionado add novos valores
				if($("#"+field).val() == "" || $("#"+field+"_descrp").val() != "")
					{
					if(pfunc != "")
				 		eval(pfunc);
			
					// $("#"+nfield).focus(); // retorna o foco work around para manter somente 1 pulo ao usar tab
			//		if(nfield != "")
			//			$("#"+nfield).focus();
					}
			// altera icone do campo de pesquisa
			if($("#"+field+"_descrp").val() != "")
				$("#"+field+"_descrp").removeClass("search").addClass("searchAdd"); // change icon for add
			else
				$("#"+field+"_descrp").removeClass("searchAdd").addClass("search"); // change icon for search	
			})
			
		.change(function()
			{
			if($("#"+field+"_descrp").val() != "")
				$("#"+field+"_descrp").removeClass("search").addClass("searchAdd"); // change icon for add
			else
				$("#"+field+"_descrp").removeClass("searchAdd").addClass("search"); // change icon for search
			})
			
		// .focusout(function(){ $("#"+field+"_descrp").autocomplete( "close" ); })
		
		.attr({'autocomplete':'off'});
		
		// $("#ui-active-menuitem").click(function(){ alert("Click Click Click!!!"); });
		};

	/*
	// controla o clique no autoselect  [funcao experimental]
	this.clickControl = function() 
		{
		// $("#adversas_descrp").children(".ui-corner-all").click(function(){ alert("teste click !"); });
		$(".ui-corner-all").click(function() { 
			if(pfunc != "")
		 		eval(pfunc);
		});
		}
	*/
	
	// desabilita campo
	this.disable = function()
		{
		var f = field+"_descrp";
		$('#'+f).autocomplete("disable");
		fieldOptDisable(f); 
		}

	// habilita campo
	this.enable = function()
		{
		var f = field+"_descrp";
		$('#'+f).autocomplete("enable");
		fieldOptEnable(f);
		}
		
	// quando sai do campo executa funcao
	this.blur = function(func){ fieldOptBlur(field,func) };
	
	// quando entra no campo executa funcao
	this.focus = function(func){ fieldOptFocus(field,func) };
	
	// Desativa tab
	this.noTab = function(){ notab = 1; };
	
	if(fast) 
		{
		alert("fast");
		return this.show();
		}
	}
	
/* [END]  AUTOCOMPLETE  (by akgleal.com)  ----------------------------------------------------------------------------- */
