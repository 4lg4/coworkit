/* [INI]  Grid (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	<script type="text/javascript" src="/comum/jquery/jquery.tablesorter.js"></script> 
		
	CSS necessario:
	

    Opcoes:
	
	Exemplo de uso:
	var campoNumber = new fieldNumber("campo_number");
	campoNumber.setSize(10);
	<input type="text" id='campo_number' name='campo_number'>
	
	
	Criar funcoes para click e 2 clicks
	function DGridClick(x)
		{
		alert("Click - "+x);
		}

	function DGridDblClick(x)
		{
		alert("DBL Click - "+x);
		}
		
	
	// agrupamento	
	grid.group();
	habilita agrupamento, criar 2 tds hidden adicionais
	<td>group_cod</td> = codigo numerico crescente
	<td>group_descrp</td> = descricao que aparecera no agrupamento
	
*/
include("/comum/jquery/jquery.dataTables.js");
include("/comum/jquery/jquery.dataTables.rowGrouping.js");
loadCSS("/css/dataTable.css");
// include("/comum/jquery/jquery.tablesorter.js");
// include("/comum/jquery/jquery.tablesorter.pager.js");
(function($){
	
$.fn.DGrid = function(settings) 
	{
	var settings = $.extend(
		{
		height			: '100%', 								// altura 
		qtd 			: -1, 								// quantidade de linhas que sera mostrado
		footer 			: 'rt<"dataTables_bottom"flpi>', 	// 'rt<"dataTables_bottom"flpi>'; // ajusta rodape
		group 			: 1, 								// agrupamento, <td> usada para
		tdorder 		: 3, 								// agrupamento, <td> usada para
		enable			: 'on',
		postFunction	: '',
		linha_action	:false,
		icon		:'',
		type		: ""
		}, settings);
	
	
	// ajusta altura da pagina
	function getGridHeight()
		{
		if(settings.height == "")
			return Math.round($(this).parent().height()-25); // return Math.round($(tipo+''+table).parent().height()-70);	// return Math.round($(window).height()-70);
		else
			return settings.height;
		}
	// Verifica se o grid é simples o completo - Simples: para divs pequenas. - Completo: Grid de resultados	
	if(settings.type=="simple")
			{
			$(".dataTables_wrapper").css("display","none !important");
			settings.footer=""; // remove paginacao
			}
	
	return this.each(function()
		{
		
		//alert($(this));
		
		
		//alert(settings.footer);
	/*
	this.group = function() 
		{ 
		group = "";
		
		// se grupo for usado por padrao define 4 <td> para ordenacao crescente 
		if(tdorder == 1)
			tdorder = 3; 
		}
		*/
		var oTable = $(this);
		
		oTable // antigo $(this)
			.dataTable(
				{
				// "bJQueryUI": true,
				// "sPaginationType": "full_numbers",
				"bDestroy": settings.destroy,
				"sDom": settings.footer,
				"sScrollY": getGridHeight(),
				"iDisplayLength": settings.qtd, // sem paginacao
				// "aLengthMenu": [[150, 100, 50, 25 , -1], [150, 100, 50, 25, "All"]],
				// "aaSortingFixed": [[tdorder,'asc']]
				// "aaSorting": [[tdorder,'asc']],
				
				// "bLengthChange": false, 
				// "bPaginate": false
				// "sScrollX": "100%"
				// "bScrollInfinite": true
				// "bScrollCollapse": true
				})
			
			.click(function(event) 
				{
				if($(event.target.parentNode)[0].tagName != "TABLE" && $(event.target.parentNode)[0].tagName != "DIV") // Verifica se nao for elemento errado e marca
					{ 
					// desmarca todos da tabela	
					// marca elemento clicado / executa funcao clique simples
					// se nao for titulo de agrupamento
					if($(event.target.parentNode).find("td:first").hasClass("group") === false)
						{
						/*Para fazer a marcação da linha tive que substituir o $(this) acima
						pela variável oTable pois se eu refeciasse o $(this) ele pegava o elemento
						atual e não entendia a função aoData - Kelvyn C. */
						$(oTable.fnSettings().aoData).each(function ()
							{
							// Verifica se o plugin está a opção de exibir ícone na linha
							if(settings.linha_action===true)
								{
								$(this.nTr).find(settings.icon).fadeOut("fast");
								}
							//Remove a cor da linha	
							$(this.nTr).removeClass('row_selected');
							});
						// Verifica se o plugin está a opção de exibir ícone na linha
						if(settings.linha_action===true)
							{
							$(event.target.parentNode).find(settings.icon).fadeIn("fast");
							}
						//Adiciona a cor da linha
						$(event.target.parentNode).addClass('row_selected');
						
						// se nao houver codigo passa toda a linha para a funcao
						if($(event.target.parentNode).find("td:first").html() == "")
							DGridClick($(this),$(event.target.parentNode).find("td:first").closest("tr").html());
						else
							DGridClick($(this),$(event.target.parentNode).find("td:first").html());
						}
					}
				})
			
			// Duplo Clique
			.dblclick(function(event) 
				{
				// executa funcao duplo clique
				// se nao for titulo de agrupamento
				if($(event.target.parentNode).find("td:first").hasClass("group") === false)
					{
					// se nao houver codigo passa toda a linha para a funcao
					if($(event.target.parentNode).find("td:first").html() == "")
						DGridDblClick($(this),$(event.target.parentNode).find("td:first").closest("tr").html());
					else
						DGridDblClick($(this),$(event.target.parentNode).find("td:first").html());
					}
				});		
			
		});
				
		/*
		// agrupamento, agrupa por campos hidden
		if(group == "")
			{
			$(this).rowGrouping(
				{
				iGroupingColumnIndex: 2, // terceiro <td>group_descrp</td>
				sGroupingColumnSortDirection: "asc",
				iGroupingOrderByColumnIndex: 1, // segundo <td>group_cod</td>
				// bExpandableGrouping: true,
				// bExpandSingleGroup: true,
				// asExpandedGroups: ["TOP 10","Empresas"]
				});
			}
		*/
		
		// seta campo
		/*
		$(tipo+''+table)
			.addClass("tablesorter")
			.tablesorter(
				{ */
				// widthFixed: true, 
				// widgets: ['zebra'], // ,'repeatHeaders']
				/* sortList: 
					[
					[1,0]
					//,[0,1]
					] */
				
				// });
			/*
			.tablesorterPager(
				{
				container: $("#"+table)
				});
			*/
			
		// alert(tipo+''+table);
		
		//Setup the quickSearch plugin with on onAfter event that first checks to see how
	    //many rows are visible in the body of the table. If there are rows still visible
	    //call tableSorter functions to update the sorting and then hide the tables footer. 
	    //Else show the tables footer  
	
		
		// ajusta largura
		// oTable.fnAdjustColumnSizing();
		/*
		if(fast == "simple")
			{
			// this.setFooter(""); // remove paginacao
			// $("#"+table).css("width","100% !important"); // ajusta 100% a largura
			// $("#"+table).closest("thead").css("display","none"); // remove header do grid
			// this.show(); // monta obj
			// oTable.addClass("grid_simple"); // ajustes grid simple em ui.css
			$(".dataTables_wrapper").css("display","none");
			}
		
		}
	
	// define tamanho
	// this.size = function(size){ fieldOptSize(field,size); };
	
	// desabilita 
	// this.disable = function(){ fieldOptDisable(field); };

	// habilita 
	// this.enable = function(){ fieldOptEnable(field); };
	
	
	// testa se for simple grid, cria grid sem padinacao e sem header
	if(fast == "simple")
		{
		this.setFooter(""); // remove paginacao
		// $("#"+table).css("width","100% !important"); // ajusta 100% a largura
		// $("#"+table).closest("thead").css("display","none"); // remove header do grid
		this.show(); // monta obj
		}
	
	// retorna obj pronto
	if(!fast)
		return this.show();
		
		*/
	};
	
})( jQuery );