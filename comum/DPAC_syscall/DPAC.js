/*
	- iPAC JavaScript - Vers�o Alpha 20080827 - http://codigolivre.org.br/projects/libjs/
	- 07-12-2011 - Vers�o Alpha 20111207 - http://syscall.done.com.br/iPAC/

	- DPAC (Done Packages) 
	- Data: 01-07-2012 
	- Local: http://eos.done.com.br/DPAC_syscall/ 
	- Descrp.: baseado no iPAC 
*/

/* [INI] Load jquery scripts ------------------------------------------------------------------------------------------ */	
// include JS file asynchronous 	
function include(file)
	{
	var xhrObj = new XMLHttpRequest();
	
	// open and send a synchronous request
	xhrObj.open('GET', file, false);
	xhrObj.send('');
	
	// add the returned content to a newly created script tag
	var se = document.createElement('script');
	se.type = "text/javascript";
	se.text = xhrObj.responseText;
	document.getElementsByTagName('head')[0].appendChild(se);
	}
	
// include JS file asynchronous 	
function loadJS(file)
	{
	var fileref = document.createElement('script');
	fileref.setAttribute("type","text/javascript");
	fileref.setAttribute("src", file);
	
	document.getElementsByTagName("head")[0].appendChild(fileref);
	}
	
// include CSS file asynchronous 	
function loadCSS(file)
	{
	var fileref=document.createElement("link")
		fileref.setAttribute("rel", "stylesheet")
	  	fileref.setAttribute("type", "text/css")
	  	fileref.setAttribute("href", file)
	
	document.getElementsByTagName("head")[0].appendChild(fileref);
	}
	
// dependencias para funcionamento basico do sistema
// loadCSS("/css/CSS_syscall/comum/ui.css");
loadCSS("/css/CSS_syscall/ui.css");
// include("/comum/DPAC_syscall/jquery/jquery-1.6.4.js");
include("/comum/DPAC_syscall/jquery/jquery-1.6.4.js");
include("/comum/DPAC_syscall/jquery/jquery.ui.js");
// include("/comum/DPAC_syscall/jquery/jquery-ui-1.10.0.custom.min.js");
include("/comum/DPAC_syscall/jquery/jquery.meiomask.js");

if(window.name != "main" || window.name != "main_int") // carrega funcoes se for formulario
	{
	// loadCSS("/css/CSS_syscall/comum/menu.css");
	loadCSS("/css/CSS_syscall/menu.css");
	}
/* [END] Load jquery scripts ------------------------------------------------------------------------------------------ */	


/* Primeira Letra Capital  -------------------------------------------------------------------------------------------- */
String.prototype.ucfirst = function()
	{
	return this.charAt(0).toUpperCase() + this.slice(1);
	}

/* [INI] Remove simbolos de uma string  ------------------------------------------------------------------------------- */
function srtClean(c)
	{
	var pos;
	var s = new Array(); // define uma matriz com os s�mbolos que ser�o eliminados
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
	return(c);			// retorna o valor sem os s�mbolos
	}
	
function LIMP(c) { srtClean(c); }
/* [END] Remove simbolos de uma string  ------------------------------------------------------------------ */

/* [INI] Testa se variavel NULA -------------------------------------------------------------------------- */
function isNULL(c)	
	{
	// Fun��o para verifi��o se o valor � vazio ou s� contenha espa�os
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
				return(1);			// retorna 1 (true) se apenas tiver espa�os em branco
				}
			pos++;
			}
		return(0);			// retorna 0 (false) se for um valor n�o vazio (ou n�o nulo)
		}
	}
/* [END] Testa se variavel NULA ------------------------------------------------------------------------- */

/* [INI] Testa se variavel NUMERO  ---------------------------------------------------------------------- */
// Fun��o para verifica��o de um valor num�rico v�lido 
// retorna 0 (false) se n�o for um valor num�rico v�lido
// retorna 1 (true) se for um valor num�rico v�lido
function isNUMB(c) { if(c) isNum(c); else return false; } // short cut !

function isNum(c)
	{
	if(!c)
		return false;
		
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
/* [END] Testa se variavel NUMERO  ---------------------------------------------------------------------- */

/* [INI] transforma para NUMERO  ------------------------------------------------------------------------ */
// Fun��o que converte um n�mero com sinal decimal ponto para v�rgula
// retorna 0 se n�o for um valor num�rico v�lido
// retorna o valor convertido
function toNUMB(c) {toNum(c);}

function toNum(c)
	{
	if(isNUMB(c) != 1)
		return(0);			
	if((pos=c.indexOf(","))!=-1)
		c = c.substring(0,pos)+"."+c.substring(pos+1);
		
	c = parseFloat(c);
	return(c);			
	}
/* [END] transforma para NUMERO  ------------------------------------------------------------------------ */

/* [INI] ---------------------------------------------------------------------------------------------------
	Testa E-mail
	
	- retorno: 0 (false) / 1 (true)
--------------------------------------------------------------------------------------------------------- */
function isMAIL(email) { isMail(email); }
function isMail(email)
	{
	var regex = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
	if(regex.test(email))
		return(true);
	else
		return(false);
	}
/* [END] Testa se Email  -------------------------------------------------------------------------------- */

/* [INI] Testa CNPJ  ------------------------------------------------------------------------------------ */
function isCNPJ(CNPJ)
	{
	// Fun��o que verifica se � um c�digo de CNPJ, antigo CGC, v�lido
	CNPJ = LIMP(CNPJ);		// limpa o valor
	if(CNPJ.length != 14)
		{
		return(0);			// retorna como um c�digo de CNPJ inv�lido
		}
	if(isNUMB(CNPJ) == -1)		// verifica se o que sobrou � um valor num�rico
		{
		return(0);			// retorna como um c�digo de CNPJ inv�lido
		}
	else
		{
		if(CNPJ == 0)			// verifica se for um valor num�rico vazio
			{
			return(0);
			}
		else
			{
			pos=CNPJ.length-2;
			if(isCNPJ2(CNPJ,pos) == 1)			// desmembra o c�digo e verifica se este � v�lido
				{
				pos=CNPJ.length-1;
				if(isCNPJ2(CNPJ,pos) == 1)
					{	
					return(1);			// retorna 1 (true) indicando que o CNPJ � v�lido
					}
				else
					{
					return(0);			// retorna 0 (false) indicando que o CNPJ � inv�lido
					}
				}
			else
				{
				return(0);			// retorna 0 (false) indicando que o CNPJ � inv�lido
				}
			}
		}
	}
function isCNPJ2(CNPJ, pos)
	{
	// Segunda parte da fun��o que verifica se o c�digo do CNPJ � v�lido
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
		return(0);			// retorna 0 (false) indicando que o trecho do CNPJ � inv�lido
		}
	else
		{
		return(1);			// retorna 1 (true) indicando que o trecho do CNPJ � v�lido
		}
	}
/* [END] Testa CNPJ  ------------------------------------------------------------------------------------ */

/* [INI] Testa CPF  ------------------------------------------------------------------------------------- */
function isCPF(CPF)
	{
	// Fun��o que verifica se o c�digo do CPF � v�lido;
	CPF = LIMP(CPF);			// limpa o valor
	if(isNUMB(CPF) == 0)		// verifica se o que sobrou � um valor num�rico
		{
		return(0);			// retorna como um c�digo de CPF inv�lido
		}
	else
		{
		if(CPF.length > 11)
			{
			return(0);			// retorna como um c�digo de CPF inv�lido
			}
		if(CPF == 0 || CPF == "1111111111" || CPF == "66666666666")
			{
			return(0);			// retorna 0 (falso) se for um valor vazio ou se � uma excess�o
			}
		else
			{
			var POSICAO, I, SOMA, DV, DV_INFORMADO;
			var DIGITO = new Array(10);
			DV_INFORMADO = CPF.substr(9, 2);			// retira os dois �ltimos d�gitos
			// Desemembra o n�mero do CPF na array DIGITO
			for (I=0; I<=8; I++)
				{
				DIGITO[I] = CPF.substr( I, 1);
				}
			// Calcula o valor do 10 d�gito da verifica��o
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
			// Calcula o valor do 11 d�gito da verifica��o
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
			// Verifica se os valores dos d�gitos verificadores conferem
			DV = DIGITO[9] * 10 + DIGITO[10];
			if (DV != DV_INFORMADO)
				{
				return(0);			// retorna 0 (falso) indicando que o CPF inv�lido
				} 
			}
		}
	return(1);			// retorna 1 (true) indicando que o CPF v�lido
	}
/* [END] Testa CPF  ------------------------------------------------------------------------------------- */

function isHOUR(HORA, MIN)
	{
	// Fun��o que verifica se � um valor de hora v�lido
	if(isNUMB(HORA) != 1)
		{
		return(-1);			// retorna -1 indicando que a hora n�o � um n�mero
		}
	else
		{
		if(HORA < 0 || HORA > 23)
			{
			return(-1);			// retorna -1 indicando que a hora n�o est� no intervalo de tempo correto
			}
		}
	if(isNUMB(MIN) != 1)
		{
		return(-2);			// retorna -2 indicando que o minuto n�o � um n�mero
		}
	else
		{
		if(MIN < 0 || MIN > 59)
			{
			return(-2);			// retorna -2 indicando que o minuto n�o est� no intervalo de tempo correto
			}
		}
	return(1);			// retorna 1 (true) indicando que o valor � uma hora v�lida
	}



function isDATE(DIA, MES, ANO)
	{
	// Fun��o que verifica se � um valor de data v�lida
	if(isNUMB(DIA) != 1)
		{
		return(-2);			// retorna -2 indicando que o dia do m�s n�o � um n�mero
		}
	else
		{
		if(DIA < 1 || DIA > 31)
			{
			return(-2);			// retorna -2 indicando que o dia n�o est� no intervalo de tempo correto
			}
		}
	if(isNUMB(MES) != 1)
		{
		return(-3);			// retorna -3 indicando que o m�s n�o � um n�mero v�lido
		}
	else
		{
		if(MES < 1 || MES > 12)
			{
			return(-3);			// retorna -3 indicando que o m�s � inv�lido
			}
		}
	if(isNUMB(ANO) != 1)
		{
		return(-4);			// retorna -4 indicando que o ano n�o � um n�mero v�lido
		}
	else
		{
		if(ANO < 0)
			{
			return(-4);			// retorna -4 indicando que o ano n�o � um n�mero inteiro
			}
		}
	var c = new Date(toNUMB(ANO), (toNUMB(MES)-1), toNUMB(DIA));
	if(c.getDate() == DIA)
		{
		return(1);			// retorna 1 (true) indicando que � uma data v�lida
		}
	else
		{
		return(-1);			// retorna -1 indicando que � data inv�lida
		}
	}

/* [INI] to Money (by akgleal.com) ----------------------------------------------------------------------------------------------------
 	Ajusta n�mero para o formato de moeda, substitute of Luciano function toMoney
	
	future: Implementar a colocacao do separador de milhar

*/
function money(val,calc)
	{
	// ajusta money para calculos
	if(calc)
		{
		// testa se campo nao vazio
		if(isNaN(parseFloat(val))) 
			{
			val = 0;
			}
		else
			{
			val = val.replace(/^.*[R\$]/i,""); // remove R$
			val = val.replace(/[.]/g,""); // remove pontos
			val = val.replace(",","."); // troca ponto por virgula
			}
			
		// ajusta variavel para retorno
		retorno = parseFloat(val);
		}
	// ajuste money para mostrar em campos
	else
		{
		retorno = val.toFixed(2).replace(".",",");
		}
		
	// retorno
	return retorno; 
	}
	
function toMoney(c)
	{
	// link para nova funcao
	money(c);

	// Fun��o que converte um n�mero para o formato de moeda
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

/* [END] to Money (by akgleal.com) ---------------------------------------------------------------------------------------------------- */

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
					//  mudar para uso de classes para padronizar entre diferentes CSS
					// linhas[ln].style.className += "Nome_da_Classe_para_Read_Only";
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

/* Glow, Marca item selecionado na lista ------------------------------------------------------------------------------ */
function glow(id,classe) 
	{
	if(!classe)
		{
		classe = "glow";
		}
	$('.'+classe).removeClass(classe);
	$('#'+id+' td').addClass(classe);

	// $('#'+id).toggleClass("glow")
	}
	
/* [INI] Field Options (by akgleal.com) ----------------------------------------------------------------------------------------------------
	Opcoes padrao dos campos field
*/
function fieldOptions()
	{
	// define tamanho
	this.size = function(size){ fieldOptSize(field,size); };
	// desabilita campo
	this.disable = function(){ fieldOptDisable(field); };
	// habilita campo
	this.enable = function(){ fieldOptEnable(field); };
	// quando sai do campo executa funcao
	this.blur = function(func){ fieldOptBlur(field,func) };
	}

// define quantidade de caracteres maximo
function fieldOptSize(field,size)
	{
	$('#'+field).attr('maxlength',size);
	$('#'+field).css('width',(size*5)+'px');
	}
	
// on exit propriedade
function fieldOptBlur(field,func)
	{
	$('#'+field).focusout(function(){ eval(func); });
	}

// on focus propriedade
function fieldOptFocus(field,func)
	{
	$('#'+field).focus(function(){ eval(func); });
	}

// auto complete do navegador (on / off)
function fieldBrowserAutoComplete(opt)
	{
	$('#'+field).attr({ 'autocomplete' : opt });
	}	
	
// desabilita campo
function fieldOptDisable(field)
	{
	$('#'+field)
		.addClass("fieldDisable")
		.attr("readonly", true);
	}
	
// habilita campo
function fieldOptEnable(field)
	{		
	$('#'+field)
		.removeClass("fieldDisable")
		.attr("readonly", false);
	}

// Mostra campo
function fieldOptShow(field)
	{		
	$("#"+field).show();
	$('label[for="'+field+'"]').show();
	}

// Esconde campo
function fieldOptHide(field)
	{		
	$("#"+field).hide();
	$('label[for="'+field+'"]').hide();
	}

	
/* [END] Field Options (by akgleal.com) ---------------------------------------------------------------------------------------------------- */
if(window.name == "main") // carrega funcoes se for formulario
	{
	include("/comum/DPAC_syscall/fieldAutoComplete.js");
	include("/comum/DPAC_syscall/fieldCheck.js");
	include("/comum/DPAC_syscall/fieldDateTime.js");
	include("/comum/DPAC_syscall/fieldEmail.js");
	include("/comum/DPAC_syscall/fieldMoney.js");
	include("/comum/DPAC_syscall/fieldNumber.js");
	include("/comum/DPAC_syscall/fieldPassword.js");
	include("/comum/DPAC_syscall/fieldSelect.js");
	include("/comum/DPAC_syscall/fieldTextEditor.js");
	include("/comum/DPAC_syscall/fieldUpload.js");
	include("/comum/DPAC_syscall/fieldUser.js");
	include("/comum/DPAC_syscall/grid.js");
	 
	$(document).ready(function() 
		{	
		// DBOX minimiza / maximiza
		$(".dbox_title").click(function()
			{
			// $("#"+$(this).parent().attr("id")).addClass("dbox_min");
			
			$("#"+$(this).parent().attr("id")).toggleClass("dbox_min","fast");
			// $("#"+$(this).parent().attr("id")).toggleClass("dbox_full","fast");
			// $("#"+$(this).attr("id")+"_content").fadeToggle("slow");
			// alert();
			});
		});
	}