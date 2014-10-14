// iPAC JavaScript - Versão Alpha 20080827 - http://codigolivre.org.br/projects/libjs/
// 07-12-2011 - Versão Alpha 20111207 - http://syscall.done.com.br/iPAC/

String.prototype.ucfirst = function()
	{
    return this.charAt(0).toUpperCase() + this.slice(1);
	}

function LIMP(c)					
	{
	// Função que retorna como resultado um valor sem símbolos auxiliares, como a barra
	var pos;
	var s = new Array();			// define uma matriz com os símbolos que serão eliminados
	s[0] = "-";
	s[1] = "/";
	s[2] = ",";
	s[3] = ".";
	s[4] = "(";
	s[5] = ")";
	s[6] = " ";
	for(var x=0; x < s.length ; x++)
		{
		while((pos=c.indexOf(s[x])) != -1)
			{
			c = c.substring(0, pos) + c.substring(pos+1);
			}
		}
	return(c);			// retorna o valor sem os símbolos
	}

function isNULL(c)	
	{
	// Função para verifição se o valor é vazio ou só contenha espaços
	if(c == "")
		{
		return(1);			// retorna 1 (true) se for vazio
		}
	else
		{
		var pos=0;
		while(c.charAt(pos) == " ")
			{
			if(pos == c.length-1)
				{
				return(1);			// retorna 1 (true) se apenas tiver espaços em branco
				}
			pos++;
			}
		return(0);			// retorna 0 (false) se for um valor não vazio (ou não nulo)
		}
	}


// Função para verificação de um valor numérico válido 
// retorna 0 (false) se não for um valor numérico válido
// retorna 1 (true) se for um valor numérico válido
function isNum(c) { if(c) isNUMB(c); else return false; } // short cut !
function isNUMB(c)
	{
	if((pos=c.indexOf(",")) != -1)
		c = c.substring(0,pos)+"."+c.substring(pos+1);

	if((parseFloat(c) / c != 1))
		{
		if(parseFloat(c) * c == 0)
			return true;
		else
			return false;
		}
	else
		return true;	
	}


// Função que converte um número com sinal decimal ponto para vírgula
// retorna 0 se não for um valor numérico válido
// retorna o valor convertido
function toNUMB(c)
	{
	if(isNUMB(c) != 1)
		return(0);			
	if((pos=c.indexOf(","))!=-1)
		c = c.substring(0,pos)+"."+c.substring(pos+1);
		
	c = parseFloat(c);
	return(c);			
	}


// Função que testa se é um email valido
// retorna 0 (false) se não for um valor numérico válido
// retorna 1 (true) se for um valor numérico válido
function isMAIL(email)
	{
	var regex = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
	if(regex.test(email))
		return true;
	else
		return false;
	}



function isCNPJ(CNPJ)
	{
	// Função que verifica se é um código de CNPJ, antigo CGC, válido
	CNPJ = LIMP(CNPJ);		// limpa o valor
	if(CNPJ.length != 14)
		{
		return(0);			// retorna como um código de CNPJ inválido
		}
	if(isNUMB(CNPJ) == -1)		// verifica se o que sobrou é um valor numérico
		{
		return(0);			// retorna como um código de CNPJ inválido
		}
	else
		{
		if(CNPJ == 0)			// verifica se for um valor numérico vazio
			{
			return(0);
			}
		else
			{
			pos=CNPJ.length-2;
			if(isCNPJ2(CNPJ,pos) == 1)			// desmembra o código e verifica se este é válido
				{
				pos=CNPJ.length-1;
				if(isCNPJ2(CNPJ,pos) == 1)
					{	
					return(1);			// retorna 1 (true) indicando que o CNPJ é válido
					}
				else
					{
					return(0);			// retorna 0 (false) indicando que o CNPJ é inválido
					}
				}
			else
				{
				return(0);			// retorna 0 (false) indicando que o CNPJ é inválido
				}
			}
		}
	}
function isCNPJ2(CNPJ, pos)
	{
	// Segunda parte da função que verifica se o código do CNPJ é válido
	var v = 0;
	var ind = 2;
	var tam;
	for(var f=pos; f > 0; f--)
		{
		v += parseInt(CNPJ.charAt(f-1))*ind;
		if(ind > 8)
			{
			ind = 2;
			}
		else
			{
			ind++;
			}
		}
		v %= 11;
		if(v == 0 || v == 1)
			{
			v = 0;
			}
		else
			{
			v = 11 - v;
			}
	if(v != parseInt(CNPJ.charAt(pos)))
		{
		return(0);			// retorna 0 (false) indicando que o trecho do CNPJ é inválido
		}
	else
		{
		return(1);			// retorna 1 (true) indicando que o trecho do CNPJ é válido
		}
	}



function isCPF(CPF)
	{
	// Função que verifica se o código do CPF é válido;
	CPF = LIMP(CPF);			// limpa o valor
	if(isNUMB(CPF) == 0)		// verifica se o que sobrou é um valor numérico
		{
		return(0);			// retorna como um código de CPF inválido
		}
	else
		{
		if(CPF.length > 11)
			{
			return(0);			// retorna como um código de CPF inválido
			}
		if(CPF == 0 || CPF == "1111111111" || CPF == "66666666666")
			{
			return(0);			// retorna 0 (falso) se for um valor vazio ou se é uma excessão
			}
		else
			{
			var POSICAO, I, SOMA, DV, DV_INFORMADO;
			var DIGITO = new Array(10);
			DV_INFORMADO = CPF.substr(9, 2);			// retira os dois últimos dígitos
			// Desemembra o número do CPF na array DIGITO
			for (I=0; I<=8; I++)
				{
				DIGITO[I] = CPF.substr( I, 1);
				}
			// Calcula o valor do 10 dígito da verificação
			POSICAO = 10;
			SOMA = 0;
			for (I=0; I<=8; I++)
				{
				SOMA = SOMA + DIGITO[I] * POSICAO;
				POSICAO = POSICAO - 1;
				}
			DIGITO[9] = SOMA % 11;
			if (DIGITO[9] < 2)
				{
				DIGITO[9] = 0;
				}
			else
				{
				DIGITO[9] = 11 - DIGITO[9];
				}
			// Calcula o valor do 11 dígito da verificação
			POSICAO = 11;
			SOMA = 0;
			for (I=0; I<=9; I++)
				{
				SOMA = SOMA + DIGITO[I] * POSICAO;
				POSICAO = POSICAO - 1;
				}
			DIGITO[10] = SOMA % 11;
			if(DIGITO[10] < 2)
				{
				DIGITO[10] = 0;
				}
			else
				{
				DIGITO[10] = 11 - DIGITO[10];
				}
			// Verifica se os valores dos dígitos verificadores conferem
			DV = DIGITO[9] * 10 + DIGITO[10];
			if (DV != DV_INFORMADO)
				{
				return(0);			// retorna 0 (falso) indicando que o CPF inválido
				} 
			}
		}
	return(1);			// retorna 1 (true) indicando que o CPF válido
	}

function isHOUR(HORA, MIN)
	{
	// Função que verifica se é um valor de hora válido
	if(isNUMB(HORA) != 1)
		{
		return(-1);			// retorna -1 indicando que a hora não é um número
		}
	else
		{
		if(HORA < 0 || HORA > 23)
			{
			return(-1);			// retorna -1 indicando que a hora não está no intervalo de tempo correto
			}
		}
	if(isNUMB(MIN) != 1)
		{
		return(-2);			// retorna -2 indicando que o minuto não é um número
		}
	else
		{
		if(MIN < 0 || MIN > 59)
			{
			return(-2);			// retorna -2 indicando que o minuto não está no intervalo de tempo correto
			}
		}
	return(1);			// retorna 1 (true) indicando que o valor é uma hora válida
	}



function isDATE(DIA, MES, ANO)
	{
	// Função que verifica se é um valor de data válida
	if(isNUMB(DIA) != 1)
		{
		return(-2);			// retorna -2 indicando que o dia do mês não é um número
		}
	else
		{
		if(DIA < 1 || DIA > 31)
			{
			return(-2);			// retorna -2 indicando que o dia não está no intervalo de tempo correto
			}
		}
	if(isNUMB(MES) != 1)
		{
		return(-3);			// retorna -3 indicando que o mês não é um número válido
		}
	else
		{
		if(MES < 1 || MES > 12)
			{
			return(-3);			// retorna -3 indicando que o mês é inválido
			}
		}
	if(isNUMB(ANO) != 1)
		{
		return(-4);			// retorna -4 indicando que o ano não é um número válido
		}
	else
		{
		if(ANO < 0)
			{
			return(-4);			// retorna -4 indicando que o ano não é um número inteiro
			}
		}
	var c = new Date(toNUMB(ANO), (toNUMB(MES)-1), toNUMB(DIA));
	if(c.getDate() == DIA)
		{
		return(1);			// retorna 1 (true) indicando que é uma data válida
		}
	else
		{
		return(-1);			// retorna -1 indicando que é data inválida
		}
	}



function toMoney(c)
	{
	// Função que converte um número para o formato de moeda
	c += "";
	if(isNUMB(c) == 1)
		{
		if(c.indexOf(".") != -1)
			{
			cv=c.substring(0,c.indexOf("."))+","+c.substring(c.indexOf(".")+1);
			c=cv;
			}
		else
			{
			c+=",00";
			}
		if(c.indexOf(",") == c.length-2)
			{
			c+="0";
			}
		else
			{
			c = c.substring(0,c.indexOf(",")+3);
			}
		return(c);
		}
	else
		{
		return("0,00");
		}
	}



function makeRequest(sUrl, oParams)
	{
	var httpRequest;
	var sParm="";	
	if(window.XMLHttpRequest)
		{ // Mozilla, Safari, ...
		httpRequest = new XMLHttpRequest();
		if(httpRequest.overrideMimeType)
			{
			//httpRequest.overrideMimeType('text/xml');
			httpRequest.overrideMimeType('text/javascript');
			// See note below about this line
			}
		}
	else if(window.ActiveXObject)
		{ // IE
		try
			{
			httpRequest = new ActiveXObject("Msxml2.XMLHTTP");
			}
		catch(e)
			{
			try
				{
				httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
				}
			catch(e)
				{
				
				}
			}
		}
	for(sName in oParams)
		{
		sParm += encodeURIComponent(sName) + "=" + encodeURIComponent(oParams[sName]);
		sParm += "&";
		}
	if(!httpRequest)
		{
		for(sName in oParams)
			{
			if(sUrl.indexOf("?") > -1)
				{
				sUrl += "&";
				}
			else
				{
				sUrl += "?";
				}
			}
		sUrl+sParm;
		var oScript = document.createElement("script");
		oScript.src = sUrl;
		document.body.appendChild(oScript);
		}
	else
		{
		httpRequest.onreadystatechange = function() { showContents(httpRequest); };
		httpRequest.open('POST', sUrl, true);
		httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		httpRequest.send(sParm);
		}
	}

function showContents(httpRequest)
	{
	if(httpRequest.readyState == 4)
		{
		if(httpRequest.status == 200)
			{
			eval(httpRequest.responseText);
			}
		}
	}
	
// pega todos elementos de uma classe expecifica no documento ------------------------------------------------------------------------
function getElementsByClass(searchClass,node,tag)
		{
		var classElements = new Array();
		if ( node == null )
			{
			node = document;
			}
		if ( tag == null )
			{
			tag = '*';
			}
		var els = node.getElementsByTagName(tag);
		var elsLen = els.length;
		var pattern = new RegExp('(^|\\\\s)'+searchClass+'(\\\\s|$)');
		for (i = 0, j = 0; i < elsLen; i++)
			{
			if ( pattern.test(els[i].className) )
				{
				classElements[j] = els[i];
				j++;
				}
			}
		return classElements;
		}	
		
// erros ajax  ----------------------------------------------------------------------------------------------------------------------------
	function errojx(XMLHttpRequest, textStatus, errorThrown)
		{
		top.unLoading();
		top.alerta("ERRO!<br><br>"+XMLHttpRequest+" "+textStatus+" "+errorThrown);
		}
		
// define bordar vermelhas e foco no campo que esta com erro ------------------------------------------------------------------------------
	function erro(x,y)
		{
		if(y.indexOf('[') > 0)
			{
			// alert(y);
			el = y.substring(0,y.indexOf('['));
			pos = y.substring(y.indexOf('[')+1, y.indexOf(']'));
			document.getElementsByName(el)[pos].style.borderColor = 'red';
			top.alerta(x,"main.document.getElementsByName(\""+el+"\")["+pos+"].focus()");
			}
		else
			{
			// alert("*** "+y);
			// document.getElementsByName(y)[0].style.borderColor = 'red';
			// top.alerta(x,"main.document.forms[0]."+y+".focus()");
			top.alerta(x,"main.document.forms[0]."+y+".focus()");
			}
		}
		
// limpa bordas vermelhas quando campo eh modificado
	function limpa(y)
		{
		if(y)
			{
			document.getElementsByName(y)[0].style.borderColor = '';
			}
		}
	
// limpa bordas vermelhas de todos elementos do documento
	function frmCleanAll() 
		{
		parent.block(true);
		linhas = document.body.getElementsByTagName('INPUT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			if(linhas[ln].getAttribute("name").indexOf("contato_") != 0) 
				{
				linhas[ln].setAttribute('onchange', 'limpa(this.name)');
				}
			}
		}
		
// desabilita todos os campos do documento e simula READONLY --------------------------------------------------------------------------
	function frmReadOnly() 
		{
		linhas = document.body.getElementsByTagName('SELECT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			//linhas[ln].disabled=true;
			linhas[ln].setAttribute('onchange', 'document.forms[0].reset()');
			linhas[ln].style.backgroundColor='#cdcdcd';
			}
			
		linhas = document.body.getElementsByTagName('INPUT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			if(linhas[ln].type.toLowerCase() != 'hidden')
				{
				//linhas[ln].disabled=true;
				linhas[ln].setAttribute('onchange', 'document.forms[0].reset()');
				if(linhas[ln].type.toLowerCase() != 'radio')
					{
					linhas[ln].style.backgroundColor='#cdcdcd';
					/*  mudar para uso de classes para padronizar entre diferentes CSS
					linhas[ln].style.className += "Nome_da_Classe_para_Read_Only";
					*/
					}
				}
			}
			
		linhas = document.body.getElementsByTagName('TEXTAREA');
		for(var ln=0;ln<linhas.length;ln++)
			{
			//linhas[ln].disabled=true;
			linhas[ln].setAttribute('onchange', 'document.forms[0].reset()');
			linhas[ln].style.backgroundColor='#cdcdcd';
			}	
		}

// quando tecla enter eh pressionada em algum campo do formulario chama funcao para adicionar novo	---------------------------------------
	function keyEnterAdd(e,funcao)
		{
		var keycode;
		// testa evento por browser ----
		if(window.event)
			keycode = window.event.keyCode;
		else if(e)
			keycode = e.which;
		else
			return true;
		
		if(keycode == 13)
			{
			eval(funcao); // chama funcao
			}
		}
		
// mostra  elementos  ---------------------------------------------------------------------------------------------------------------------
function show(object)
	{
	$('#'+object).show();
	}
	
// esconde elementos  ---------------------------------------------------------------------------------------------------------------------
function hide(object)
	{
	$('#'+object).hide();
	}
	

// quando clica no botao imprimir ---------------------------------------------------------------------------------------------------------
	function imprimir()
		{
		top.alerta('Não implementado!');
		return;
		}	

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

  Search na tbl baseado na digitacao do campo e gera campos autocomplete  --------------------------------------------------- */

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
	
	$("#"+field+"_descrp").addClass("search"); // add classe com configuracao do campo de pesquisa auto complete

	this.setField = function(val) { field = val; }
	this.setTable = function(val) { tbl = val; }
	this.setSearchField = function(val) { sfield = val; }
	this.setPostFunction = function(val) { pfunc = val; }
	this.setJoin = function(val) { join = val; }
	this.setSql = function(val) { sql = val; }
	this.setOrder = function(val) { order = val; }
	this.setReturnField = function(val) { rfield = val; }
	this.setMinQtd = function(val) { qtd = val; }
	this.setJumpNextField = function(val) { nfield = val; }

	// adiciona pesquisa autocomplete no campo	
	this.show = function() 
		{
		// alert("search.cgi?tbl="+tbl+"&join="+join+"&sql="+sql+"&order="+order+"&sfield="+sfield+"&sql="+sql);
		// source: "search.cgi?tbl="+tbl+"&join="+join+"&sql="+sql+"&order="+order+"&rfield="+rfield+"&sfield="+sfield+"&sql="+sql,
		$("#"+field+"_descrp").attr( "autocomplete", "off" ).autocomplete({
			delay: 0, // ajusta delay de pesquisa em microsegundos padrao 300
			source: "search.cgi?tbl="+tbl+"&join="+join+"&sql="+sql+"&order="+order+"&rfield="+rfield+"&sfield="+sfield+"&sql="+sql,
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
		}).keydown(function(event) {
			if(event.which == 9) // Tab pressionado do nothing
				event.preventDefault();
			
			if(event.which == 13) // Enter pressionado add novos valores
				if($("#"+field).val() == "" || $("#"+field+"_descrp").val() != "")
					{
					if(pfunc != "")
				 		eval(pfunc);
			
					// $("#"+nfield).focus(); // retorna o foco work around para manter somente 1 pulo ao usar tab
					if(nfield != "")
						$("#"+nfield).focus();
					}
		// altera icone do campo de pesquisa
			if($("#"+field+"_descrp").val() != "")
				$("#"+field+"_descrp").removeClass("search").addClass("searchAdd"); // change icon for add
			else
				$("#"+field+"_descrp").removeClass("searchAdd").addClass("search"); // change icon for search	
		}).change(function(){
			if($("#"+field+"_descrp").val() != "")
				$("#"+field+"_descrp").removeClass("search").addClass("searchAdd"); // change icon for add
			else
				$("#"+field+"_descrp").removeClass("searchAdd").addClass("search"); // change icon for search
		}).focusout(function(){ $("#"+field+"_descrp").autocomplete( "close" ); 
		}).attr({'autocomplete':'off'});

		};

	// controla o clique no autoselect  [funcao experimental]
	this.clickControl = function() 
		{
		// $("#adversas_descrp").children(".ui-corner-all").click(function(){ alert("teste click !"); });
		$(".ui-corner-all").click(function() { 
			if(pfunc != "")
		 		eval(pfunc);
		});
		}
	
	// desabilita campo
	this.disable = function()
		{
		$('#'+field)
		.addClass("fieldDisable")
		.attr("readonly", true)
		}
		
	// habilita campo
	this.enable = function()
		{
		$('#'+field)
		.removeClass("fieldDisable")
		.attr("readonly", false)
		}
		
	if(fast) 
		return this.show();
	}
/* [END]  AUTOCOMPLETE  (by akgleal.com)  ----------------------------------------------------------------------------- */


/* [INI]  DATE / TIME field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	<script type="text/javascript" src="/comum/jquery/jquery.meiomask.js"></script> (arquivo modificado por akgleal.com)
	<script type="text/javascript" src="/comum/jquery/jquery.ui.datepicker-pt-BR.js"></script>
	<script type="text/javascript" src="/comum/jquery/jquery.ui.timepicker.js"></script>

	CSS necessarios
	.fieldDate { field_date.png }
	.fieldDateTime { field_datetime.png }
	.fieldTime { field_time.png }
	.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:
	just_date_time = "date" => dd/mm/YYYY 
	just_date_time = "date-time" => dd/mm/YYYY hh:mm
	just_date_time = "time" => hh:mm
	fast = 0 / 1
	
	Exemplo de uso:
	var data = new fieldDateTime("campo_data",just_date_time,fast);
	<input type="text" id='campo_data_completa' name='campo_data_completa' alt="date-time">
*/
function y2k(number) { return (number < 1000) ? number + 1900 : number; }
 
function fieldDateTime(field,just_date_time,fast) 
	{
	// retorno automatico ativado
	if(!fast)
		fast = 1;
		
	// se nao for setado opt ou for errado ajusta para padrao
	if(!just_date_time) //  != "date" || just_date_time != "date-time" || just_date_time != "time")
		just_date_time = "date";
		
	// cria campo
	this.show = function()
		{
		if(just_date_time == "date")
			{
			$('#'+field).datepicker(
				{
				// showOn: "button",
				// buttonImage: "/img/calendar.png",
				buttonImageOnly: false,
				showButtonPanel:  true
				})
				.addClass("fieldDate");
			}
		else if(just_date_time == "date-time")
			{
			$('#'+field).datetimepicker(
				{
				hourGrid: 4,
				minuteGrid: 15,
				// showOn: "button",
				// buttonImage: "/img/calendar.png",
				buttonImageOnly: false,
				showButtonPanel:  true
				})
				.addClass("fieldDateTime");
			}
		else
			{ // campo de tempo
			$('#'+field).timepicker(
				{
				hourGrid: 4,
				minuteGrid: 15,
				// showOn: "button",
				// buttonImage: "/img/calendar.png",
				buttonImageOnly: false,
				showButtonPanel:  true
				})
			.addClass("fieldTime");
			}
		
		// ajusta atributos e inicia mascaramento
		$('#'+field).attr({'alt':just_date_time, 'autocomplete':'off'}).setMask(); 
		
		// se NAO for campo time somente data controla entrada
		if(just_date_time != "time")
			{	
			$('#'+field).change(function() 
				{
		        var f = $(this).val();
				f = f.replace(/\//g,''); // remove barras
				f = f.replace(/:/g,''); // remove dois pontos
				
				if(f.length < 8 && f.length > 0)
					{
					top.erro("<nobr>Data Errada !!</nobr>",$(this).attr('id'));
					}
				else if(f.length > 7)
					{
					year = f.substr(4,4); 
					month = f.substr(2,2); 
					day = f.substr(0,2);
										
				    var test = new Date(year,month,day);
				    if ( (y2k(test.getYear()) == year) && (month == test.getMonth()) && (day == test.getDate()) )
						a = "ok";
				    else
						if(day != 31)
							top.erro("<nobr>Data Errada !!</nobr>",$(this).attr('id'));
					}
				
				});
			}
		}
		
	// desabilita campo
	this.disable = function()
		{
		$('#'+field)
		.datepicker("disable")
		.addClass("fieldDisable")
		.attr("readonly", true);
		}

	// habilita campo
	this.enable = function()
		{
		$('#'+field)
		.datepicker("enable")
		.removeClass("fieldDisable")
		.attr("readonly", false);
		}
		
	// retorna campo pronto
	if(fast == 1)
		return this.show();
	}
/* [END]  DATE / TIME field (by akgleal.com)  ------------------------------------------------------------------------- */


/* [INI]  MONEY field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	<script type="text/javascript" src="/comum/jquery/price_format.js"></script>
	
	CSS necessario:
	.fieldMoney { }
	.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:
	setPrefixClear(true) => R$ (mostra prefixo sempre)
	fast = 0 / 1 (para usar setPrefixShow, fast deve ser desligado)
	
	Exemplo de uso:
	var campoMoney = new fieldMoney("campo_money",0);
	campoMoney.setPrefixShow(1);
	<input type="text" id='campo_money' name='campo_money'>
	
	var campoMoney = new fieldMoney("campo_money");
	<input type="text" id='campo_money' name='campo_money'>
*/

function fieldMoney(field,fast) 
	{
	var prefix_show = true; // mostra ou nao prefixo
	var prefix = "R$"; // prefixo padrao
	
	// retorno automatico ativado
	if(!fast)
		fast = 1;
	
	// funcoes de funcionamento
	// this.setPrefixClear = function(val) { prefix_show = val; this.show(); }
	// this.setPrefix = function(val) { prefix = val; }
		
	// cria campo
	this.show = function()
		{
		$('#'+field)
		.priceFormat(
			{ 
			prefix: "",
			clearPrefix: false
			})
		.addClass("fieldMoney")
		.attr({'autocomplete':'off'});
		}
	
	// desabilita campo
	this.disable = function()
		{
		$('#'+field)
		.addClass("fieldDisable")
		.attr("readonly", true);
		}

	// habilita campo
	this.enable = function()
		{
		$('#'+field)
		.removeClass("fieldDisable")
		.attr("readonly", false);
		}
	
	// quando sai do campo executa funcao
	this.blur = function(f)
		{
		$('#'+field)
		.focusout(function() 
			{
			eval(f);
			});
		}
		
	// retorna campo pronto
	if(fast == 1)
		return this.show();
	}
/* [END]  MONEY field (by akgleal.com)  ------------------------------------------------------------------------- */

/* [INI]  NUMBER field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	
	CSS necessario:
	.fieldNumber { }
	.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:
	
	Exemplo de uso:
	var campoNumber = new fieldNumber("campo_number");
	campoNumber.setSize(10);
	<input type="text" id='campo_number' name='campo_number'>
	
	var campoNumber = new fieldNumber("campo_number","10");
	<input type="text" id='campo_number' name='campo_number'>
/

function fieldNumber(field,size) 
	{
	// ajusta o tamanho minimo de caracteres do campo
	if(!size)
		var num = 1;
	else
		var num = size;
		
	// cria campo
	this.show = function()
		{
		// seta mascara
		var num_length = "";
		for(i=0; i<num; i++)
			num_length = num_length+'9';		
		$.mask.masks.number = {mask: num_length};
		
		// seta campo
		$('#'+field)
			.addClass("fieldNumber")
			.attr({
				'alt' : 'number', 
				'autocomplete' : 'off'})
			.setMask(); 
		}
	
	// desabilita campo
	this.disable = function()
		{
		$('#'+field)
			.addClass("fieldDisable")
			.attr("readonly", true);
		}

	// habilita campo
	this.enable = function()
		{
		$('#'+field)
			.removeClass("fieldDisable")
			.attr("readonly", false);
		}
	
	// quando sai do campo executa funcao
	this.blur = function(f)
		{
		$('#'+field)
		.focusout(function() 
			{
			eval(f);
			});
		}
		
	// retorna campo pronto
	if(size)
		return this.show();
	}
/ [END]  NUMBER field (by akgleal.com)  ------------------------------------------------------------------------- */

/* [INI]  EMAIL field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	
	CSS necessario:
	.fieldEmail { }
	.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:
	
	Exemplo de uso:
	var campoMoney = new fieldMoney("campo_money",0);
	campoMoney.setPrefixShow(1);
	<input type="text" id='campo_money' name='campo_money'>
	
	var campoMoney = new fieldMoney("campo_money");
	<input type="text" id='campo_money' name='campo_money'>
*/

function fieldEmail(field) 
	{
	// cria campo
	this.show = function()
		{
		$('#'+field)
			.addClass("fieldEmail")
			.attr({'autocomplete' : 'off'})
			.blur(function(){ 
				// testa email
				if($('#'+field).val().length > 0)
					if(!isMAIL($('#'+field).val())) 
						top.erro("<nobr>Email invalido !!</nobr>",$(this).attr('id'));
				});
		}
	
	// desabilita campo
	this.disable = function()
		{
		$('#'+field)
		.addClass("fieldDisable")
		.attr("readonly", true);
		}

	// habilita campo
	this.enable = function()
		{
		$('#'+field)
		.removeClass("fieldDisable")
		.attr("readonly", false);
		}
	/*
	// quando sai do campo executa funcao
	this.blur = function(f)
		{
		$('#'+field)
		.focusout(function() 
			{
			eval(f);
			});
		}
	*/	
	// retorna campo pronto
	return this.show();
	}
/* [END]  EMAIL field (by akgleal.com)  ------------------------------------------------------------------------- */

/* [INI]  CHECK.BOX field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	
	CSS necessario:
	.fieldCheck { }
	.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:
	
	Exemplo de uso:
	var campoCheck = new fieldCheck("campo_checkbox");
	<input type="checkbox" id='campo_checkbox' name='campo_checkbox'>
	
	Todo
	- adicionar suporte a array para criacao de multiplos checks ??
		$( "#format" ).buttonset();
		<div id="format">
			<input type="checkbox" id="check1" /><label for="check1">B</label>
			<input type="checkbox" id="check2" /><label for="check2">I</label>
			<input type="checkbox" id="check3" /><label for="check3">U</label>
		</div>
*/

function fieldCheck(field,fast) 
	{
	// retorno automatico ativado
	if(!fast)
		fast = 1;
	
	// cria campo
	this.show = function()
		{
		/*
		$('#'+field)
		.button(
			{ 
			icons: 
				{
				primary: "ui-icon-bullet",
				secondary: "ui-icon-check"
				}
			});
		// .closest('label').text("AAAAAAAA");
		// .addClass("fieldCheck");
		}
		*/
		
		$('#'+field)
		.button(
			{
			text: false,
			icons: { primary: "ui-icon-bullet" }
			})
		.click(function() 
			{
			if($(this).is(':checked'))
				{
				options = { icons: { primary: "ui-icon-bullet" } };
				} 
			else 
				{
				options = { icons: { primary: "ui-icon-radio-on" } };
				}
			$(this).button("option", options);
			});
			
		// remove bordas com erro	
		$(".ui-state-default, .ui-state-active").css({ border: "none" });
		}
		
	// desabilita campo
	this.disable = function()
		{
		$('#'+field)
		.button("disable");
		}

	// habilita campo
	this.enable = function()
		{
		$('#'+field)
		.button("enable");
		}
		
	// retorna campo pronto
	if(fast == 1)
		return this.show();
	}
/* [END]  CHECK.BOX field (by akgleal.com)  ------------------------------------------------------------------------- */

/* [INI]  SELECT field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	<script type="text/javascript" src="/comum/jquery/jquery.ui.selselect.js"></script>
	
	CSS necessario:
	.fieldSelect { definicoes necessarias para uso }

    Opcoes:
	setStyle(style) => ajusta o comportamento do select
	
	Exemplo de uso: 
	  Uso com array vindo do banco:
		opt_arr = new Array (['1','Select 1'],['2','Select 2']);
		campo_select = new fieldSelect("campo_select", opt_arr);
		<select name="campo_select" id="campo_select"></select>	
	  Uso com <option> setada no html:
		campo_select = new fieldSelect("campo_select");
		<select name="campo_select" id="campo_select"><option value=1>Select 1</option><option value=2>Select 2</option></select>
		
	var campoSelect = new fieldSelect("campo_select","array_se_necessario");
	<select name="campo_select" id="campo_select"></select>
	
	Todo:
	adicionar outras opcoes de select com imagens e grupos
*/

function fieldSelect(field,opt)
	{
	var stl = 'dropdown'; // estilo padrao do select
	
	// funcoes config
	this.setStyle = function(val) { stl = val; }
		
	// cria campo
	this.show = function()
		{
		// options via array (metodo novo)
		if(opt)
			{
			for(var i in opt)
				{
				$('#'+field).append("<option value='"+opt[i][0]+"'>"+opt[i][1]+"</option>");
				}
			}
			
		// cria select
		$('#'+field).selectmenu(
			{
			style:stl
			});
		}
		
	// retorna select campo pronto
	return this.show();
	}
/* [END]  SELECT field (by akgleal.com)  ------------------------------------------------------------------------- */


function scrolify(tblAsJQueryObject, height)
	{
	var oTbl = tblAsJQueryObject;
	if(oTbl.height() > height)
		{
		// for very large tables you can remove the four lines below
		// and wrap the table with <div> in the mark-up and assign
		// height and overflow property
		var oTblDiv = $("<div/>");
		oTblDiv.css('width', oTbl.width());
		oTblDiv.css('height', height);
		oTblDiv.css('overflow-y','scroll'); 
		oTblDiv.css('position','absolute');
		oTblDiv.css('top','13px');
		oTbl.wrap(oTblDiv);

		// save original width
		oTbl.attr("data-item-original-width", oTbl.width());
		oTbl.find('thead tr th').each(function(){
			$(this).attr("data-item-original-width",$(this).width());
			}); 
		//oTbl.find('tbody tr:eq(0) td').each(function(){
		//	$(this).attr("data-item-original-width",$(this).width());
		//	});                 


		// clone the original table
		var newTbl = oTbl.clone();

		// remove table header from original table
		//oTbl.find('thead tr').remove();                 
		oTbl.find('thead tr th').html('');                 
		// remove table body from new table
		newTbl.find('tbody tr').remove();   

		oTbl.parent().parent().prepend(newTbl);
		var newTblDiv = $("<div/>");
		newTblDiv.css('overflow-y','auto');               
		newTblDiv.css('position','absolute');
		newTblDiv.css('top','0px');
		newTblDiv.css('z-index','100');
		newTbl.wrap(newTblDiv);

		// replace ORIGINAL COLUMN width                
		newTbl.attr('width', newTbl.attr('data-item-original-width'));
		newTbl.find('thead tr th').each(function(){
			$(this).attr('style', 'width:'+$(this).attr("data-item-original-width")+'px');
			});     
		oTbl.attr('width', oTbl.attr('data-item-original-width'));      
		oTbl.find('thead tr th').each(function(){
			$(this).attr('style', 'width:'+$(this).attr("data-item-original-width")+'px');
			});
		}
	}


/*
// gera select ja selecionando ----------------------------
	function selSelect(field,cod)
		{
		// alert(field+" - "+cod);
		var select = '<select name="'+field+'" id="'+field+'" style="width:80%;">';
		for(i=0; i<eval(field+"_cod").length; i++) 
			{
			// alert(eval(field)[i]);
			select += "<option value='"+eval(field+"_cod")[i]+"'";
			if(eval(field+"_cod")[i] == cod)
				{
				select +="selected";
				}
			select += ">"+eval(field)[i]+"</option>";
			}
		select += '</select>';
		$("#"+field).html(select);
		}	

				 
//	icone Voltar Actions quando clicado ---------------------------------------------------------------------------------------------------
	function voltar(modulo)
		{
		alert(modulo);
		top.regrid(modulo);
		}

// funcao quando o botao voltar eh pressionado
	function voltar()
		{
			// ex.
			// url = "$dir{empresas}edit.cgi?&ID=$ID&COD=$cod_emp&MODO=editar"
			// top.regrid.location.href = url;
			
			
		$.ajax({
			type: "POST",
			url: voltar_action,
			dataType: "html",
			data: voltar_data,
			success: function(data) {},
			error: function() { alert }
			});
		}
*/		

/* Upload  ------------------------------------------------------------------------------------  
	interval = null;

	function uploadFetch(uuid,task)
		{
		req = new XMLHttpRequest();
		req.open("GET", "/progress", 1);
		req.setRequestHeader("X-Progress-ID", uuid);
		req.onreadystatechange = function()
			{
			if(req.readyState == 4)
				{
				if(req.status == 200)
					{
					// poor-man JSON parser 
					var upload = eval('new Object(' + req.responseText + ')');
					// change the width if the inner progress-bar 
					if(upload.state == 'done' || upload.state == 'uploading')
						{
						bar = document.getElementById('progressbar');
						w = (upload.received*99)/upload.size;
						bar.style.width = w + '%';
						document.getElementById('progressbar_perc').innerHTML = parseInt(w) + '%';
						}
					// we are done, stop the interval 
					if(upload.state == 'done')
						{
						bar = document.getElementById('progressbar');
						bar.style.width = '100%';
						document.getElementById('progressbar_perc').innerHTML = '100%';
						window.clearTimeout(interval);						
						$("#progress_status").hide(); // esconde barra de progressao
						$("#progress_form").show(); // esconde barra de progressao						
						$(".button").text('Escolha o Arquivo'); // limpa o formulario						
						$(".file-holder").text(''); // limpa o formulario
						$("#doc_add").hide(); // esconde o botao de upload
						task_show(task, '','', $("#doc_descrp").val()+' - '+$("#doc_file").val()); // atualiza tela
						alert(task+" - "+$("#doc_descrp").val()+' - '+$("#doc_file").val());
						// task_show(task, '','', document.getElementById('doc_descrp').value+' - '+document.getElementById('doc_file').value); // atualiza tela
						}
					}
				}
			}
		req.send(null);
		}

	function uploadProgressBar(event,task)
		{
		document.getElementById('progress').innerHTML = '<div id="progressbar_perc" style="text-align: left; position: absolute; left: 49%; margin-top: 2px;">0%</div><div id="progressbar" style="width: 100%; background-color: #00cc00; width: 0%; height: 100%; float: left;"></div>';

		// generate random progress-id 
		uuid = "";
		for(i = 0; i < 32; i++)
			{
			uuid += Math.floor(Math.random() * 16).toString(16);
			}		
		// call the progress-updater every 1000ms 
		interval = window.setInterval(function(){ uploadFetch(uuid,task); }, 1000);
		$("#progress_form").hide();
		$("#progress").show();
		
		$("#CAD").attr('action','/sys/upload/task.cgi?X-Progress-ID='+uuid);
		$("#CAD").attr('target', 'uploadframe');
		$("#CAD").submit();
		return false;
		}
*/			