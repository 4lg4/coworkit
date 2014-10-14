/* [INI]  Call (by akgleal.com)  ------------------------------------------------------------------------- 
	
*/

/* [INI] Call D-Grid --------------------------------------------------------------------------------------------------------------------
	Funcao Grid padrao usando novo grid
------------------------------------------------------------------------------------------------------------------------------------- */
function callDGrid(x, g)
	{
	flushCache();
	// Grava a função e os parâmetros para uso em caso de relogin
	lastcall(arguments.callee.name, arguments);
	
	// loader
	Loading(x);

	// ?????
	$('#menu_actions').show();
	
	if(g)
		{
		document.forms[0].FILTRO.value = g;
		}
	else
		{
		document.forms[0].FILTRO.value = '';
		}

	document.forms[0].TABLE.value = x;
	document.forms[0].FROM.value = 'menu';
	document.forms[0].target = 'main';
	document.forms[0].action = "/sys/grid/dstart.cgi";
	document.forms[0].submit();
	}
/* [END] Call D-Grid ------------------------------------------------------------------------------------------------------------------ */

	
/* [INI] Last Call ---------------------------------------------------------------------------------------------------------------------
	Guarda ultima funcao executada para reload se necessario
------------------------------------------------------------------------------------------------------------------------------------- */
function lastcall(x, a)
	{
	flushCache();
	// if( == false)
	//	{
		slastcall = x+"(";
		for(var i = 0, j = a.length; i < j; i++) slastcall += a[i]+", ";
		slastcall = slastcall.replace(/, $/, ")");
	//	}
	}
/* [END] Last Call ----------------------------------------------------------------------------------------------------------------------- */

/* [INI] Call --------------------------------------------------------------------------------------------------------------------------
	Carrega modulo
	
	vars
		x = local + arquivo que sera carregado do modulo
		jqdiv = usa div para carregamento do modulo ao inves do iframe (remover assim que o core passar todo para EOS)
------------------------------------------------------------------------------------------------------------------------------------- */	
function call(x,jqdiv,other)
	{
    $("#main_div").empty();
    $("#main").remove();
    
    
	// Grava a função e os parâmetros para uso em caso de relogin
	lastcall(arguments.callee.name, arguments);
	
	// Loader
	Loading(x);
	
	// limpa Caches
	flushCache();
	
	// controla fullscreen
	DFullscreen();
	
	
	
	// esconde botoes
	$(".menu_btn").hide(); 
		
	// esconde bird view
	$("#DTouchPages_layout, #DTouchPages_bird_view").hide();
	
	// [INI] remover apos correcao -------
	// ajusta path
	// rever o init.pl para ajustes na variavel dir e apos remover aqui.
	if(x.indexOf("/sys/") != 0)
		x = "/sys/"+x;
	// [END] remover apos correcao -------
	
	// se for carregar em divs
	if(jqdiv)
		{
		// adiciona Div
		DMainDiv();
		
		// carrega modulo na div
		if(isObject(jqdiv) === true) {
			// adiciona campos default para carregamento
			jqdiv.ID = $('#AUX [name="ID"]').val();
			
			// se modo for vazio pega valor do formulario AUX
			if(jqdiv.MODO == "")
				jqdiv.MODO = $('#AUX [name="MODO"]').val();

			// carrega modulo
			$("#main_div").load(x, jqdiv, function(){ 
                unLoading(); 
            });
            
		} else {
			// adiciona div
			DMainDiv();
			
			//Ao usar o call sem objeto zera as variaveis do auxiliar
			$('#AUX [name=COD]').val('');
			$('#AUX [name=MODO]').val('');
            
			$("#main_div").load(x, { ID: $('#AUX [name="ID"]').val(), EXTRA:jqdiv }, function(){ 
                unLoading(); 
            });
		}
	
		
		/*
		 * codigo para uso quando nao houver mais IFRAMES no MAIN do sistema
		 *
		$("#main_div").load("/sys/"+x, { ID: $("#ID").val(), "outras_vars": "outras_vars" }, function() 
			{
		    $("#ajaxLoader2").remove();
			});
		*/
		
		// sai da funcao
		return false;
		}
	
	// ajusta divs
	DMainDiv(false);	
	
	// ajusta variaveis do formulario principal
	$('#AUX input[name="SHOW"]').val(x);
	// $('#AUX input[name="COD"]').val(cod);
	// $('#AUX input[name="MODO"]').val(modo);
		
	$("#AUX")
		.prop(
			{
			target: 'main',
			action: x
			})
		.submit();
	}
/* [END] Call ----------------------------------------------------------------------------------------------------------------------- */

/* [INI] Call Grid ---------------------------------------------------------------------------------------------------------------------
	Funcao para carregamento do GRID antigo do 
	core do syscall
------------------------------------------------------------------------------------------------------------------------------------- */	
function callGrid(x, g)
	{
	eos.menu.action.appear();
	
  	// Grava a função e os parâmetros para uso em caso de relogin
	lastcall(arguments.callee.name, arguments);

	// carregamento
	Loading(x);
	
	// limpa Caches
	flushCache();
	
	// controla fullscreen
	DFullscreen();
	
	// ajusta divs
	DMainDiv();
	
	if(g)
		{
		$("#AUX input[name=GRUPO]").val(g);
		}
	else
		{
		$("#AUX input[name=GRUPO]").val('');
		}
		
	$("#AUX input[name=SHOW]").val(x);
	$("#AUX input[name=FROM]").val("menu");
	
	// Para não ficar sujeira no AUX
	// $("#AUX input[name=COD]").val("");
	$("#AUX input[name=MODO]").val("");
    
	// carrega pagina
	$("#main_div").load("/sys/done/grid/start.cgi", $("#AUX").serializeArray(), function(){
        unLoading(); 
     });
    
    $("#AUX input[name=COD]").val("");
	}

/* [INI] Call Re Grid ------------------------------------------------------------------------------------------------------------------
	Funcao para carregamento do Re GRID antigo do 
	core do syscall
------------------------------------------------------------------------------------------------------------------------------------- */		
function callRegrid(x, g)
	{
	// Grava a função e os parâmetros para uso em caso de relogin
	lastcall(arguments.callee.name, arguments);
	
	// carregamento
	Loading(x);
	
	// limpa Caches
	flushCache();
	
	// controla fullscreen
	DFullscreen();
	
	// ajusta divs
	DMainDiv();
	
	
	if(g)
		{
		$("#AUX input[name=GRUPO]").val(g);
		}
	else
		{
		$("#AUX input[name=GRUPO]").val('');
		}
		
	$("#AUX input[name=SHOW]").val(x);
	$("#AUX input[name=FROM]").val("menu");
	
	// carrega pagina
	$("#main_div").load("/sys/done/grid/start.cgi", $("#AUX").serializeArray(), function(){ unLoading(); });
	
	// Para não ficar sujeira no AUX
	$("#AUX input[name=COD]").val("");
	$("#AUX input[name=MODO]").val("");
	}
	
/* [INI] CallExt  ----------------------------------------------------------------------------------------------------------------------
	Funcao para carregamento de modulos externos
------------------------------------------------------------------------------------------------------------------------------------- */		
function callExt(x, notfull)
	{	
	// esconde e mostra iframe somente
	DMainDiv(false);
	
	// se for fullscreen total esconde todos os menus
	if(!notfull)
		{
		// arruma variavel global do controle de fullscreen 
		// FULLSCREEN = true;
		
		DFullscreen(true);
		}
	
	// esconde bird view
	$("#DTouchPages_layout, #DTouchPages_bird_view").hide();	
		
	$("#AUX")
		.prop(
			{
			target: "main",
			action: x
			})
		.submit();
	}
/* [END] CallExt  ------------------------------------------------------------------------------------------------------------------- */	
	

function DFullscreen(x)
	{
	if(x === true)
		{
		$("#menu_actions").hide();
		$("#main_container").addClass("main_container_fullscreen");
		$("#main").addClass("main_fullscreen");
		}
	else
		{
		// FULLSCREEN = false;
		
		$("#menu_actions").show();
		$("#main_container").removeClass("main_container_fullscreen");
		$("#main").removeClass("main_fullscreen");
		}
	}
	
// esconde e remove mostra e inclui (div e iframe)
function DMainDiv(div)
	{ 
	$("#main_div").hide();
	$("#main").remove();
	
	if(div === false)
		{	
		$("#main_container").append(MAIN["iframe"]);
		return true;
		}
		
	$("#main_div").show();
	}