/*
*	- DPAC (Done Packages) 
*	- Data: 01-07-2012 
*	- Local: http://eos.done.com.br/DPAC/ 
*/

/* [INI] Main ------------------------------------------------------------------------------------------------------------
	Variaveis Globais
*/
// namespace
var eos = new EOS();    
    
var dpac = {};
dpac.test = function() { 
	console.log("test");
	alert("test");
};

var MAIN = new Array();
	MAIN["iframe"] = '<iframe src="about:blank" onLoad="history.forward();" name="main" id="main" allowtransparency="true" framespacing="0" frameborder="0" scrolling="auto"></iframe>';
	MAIN["div"]    = '<div name="main_div" id="main_div"></div>';

	
// [INI] validar ???? 
var DModules = new Array();
	DModules["path"] = [
		{
		secretaria: "secretaria",
		chamado: "chamado",
		empresa: "cad/empresa"
		}];
// [END] validar ????

// Menu usuario
var MENUSER = [];

// Menu actions
var MENACT = [];

// empresa
var COMPANY = [];
COMPANY["address"] = "Av. São Pedro, 1001, Porto Alegre - Rio Grande do Sul, Brasil";
COMPANY["name"] = "Done Tecnologia da Informação LTDA";
COMPANY["icon_maps"] = "/img/ui/maps.png";
		
// guarda Geo Localizacao
var GPS = new Array();

// Cache para selects vindo de tabelas auxiliares
var DListCache = new Array();

// Arquivos de config dos modulos
var MODULE = new Array();

// Cache de elementos radio padrao ex. users
var DTouchRadioCache = new Array();

// guarda chamada dos loaders
var LOADERS = 0;

// Cache para quotes
var cacheQuote = false;
// var DLoadCache = {};
// var cacheDUploadInterval = {};
// var cacheDUploadControl  = {};

// esquema fullscreen do eos
// var FULLSCREEN = false;

/* [END] Main ------------------------------------------------------------------------------------------------------------ */

/* [INI] flushCache ---------------------------------------------------------------------------------------------------------
*
* Função de limpeza de Cache de diversas partes do sistema 
*
* DList
* CSS dos modulos
* funções action
* 
-------------------------------------------------------------------------------------------------------------------------- */
function flushCache()
	{
	// esvazia variaveis globais
	// DListCache = new Array();
	
	// limpa DTouchPages
	// $(".DTouchPages_corner").DTouchPages("destroy");
	$(".DTouchPages_corner").remove();
    
	$("#deagle_talk_content").hide();
    
	// mostra o menu de ações
	eos.menu.action.appear();
	
	/* remove todos css dos modulos */
	for(var f in MODULE) {
		for(var c in MODULE[f]["CSS"]) {
			$('link[rel=stylesheet][href="'+MODULE[f]["CSS"][c]+'"]').remove();
        }
	}
	
    
    // limpa formulario guacamole
    document.querySelectorAll("form[name=guacamole] input").forEach(function(f){
        f.value = "";
    });
    
    
    	
	// remove funcoes action	
	try
		{
		
		delete DActionSave;
		delete DActionDelete;
		delete DActionAdd;
		delete DActionCancel;
		delete DActionResize;
		/*
		delete voltar;
		delete excluir;
		delete adicionar;
		delete cancelar;
		delete regrid;
		*/
		window['DActionSave']=null;
		window['DActionDelete']=null;
		window['DActionAdd']=null;
		window['DActionCancel']=null;
		window['DActionResize']=null;
		/*
		window['voltar']=null;
		window['excluir']=null;
		window['adicionar']=null;
		window['cancelar']=null;
		window['regrid']=null;
		*/
		// compatibilidade com modulos syscall
		/*
		if(window.main)
			{
			window.main['voltar']=null;
			window.main['excluir']=null;
			window.main['adicionar']=null;
			window.main['cancelar']=null;
			window.main['regrid']=null;
			}
		*/
		}
	catch(err)
		{
		alerta("Erro ao limpar funções actions. \n"+err);
		}
	}
/* [END] flushCache ------------------------------------------------------------------------------------------------------ */

/* [INI] Mobile ------------------------------------------------------------------------------------------------------------
	get mobile features
*/
// variavel global testa dispositivo
var DEVICE = deviceCheck(); // vazio = PC

// test if mobile
function deviceCheck()
	{ 
	var uagent = navigator.userAgent.toLowerCase();
	
	if (uagent.search("iphone") > -1)
    	return "mobile";
	else if (uagent.search("ipod") > -1)
		return "mobile";
	/*
	else if (uagent.search("android") > -1)
		{
		if($(window).width() < 700)
			return "mobile";
		}
	*/
	else if (uagent.search("ipad") > -1)
    	return "tablet";
	/*
	else if (uagent.search("android") > -1)
		{
		if($(window).width() > 700)
			return "tablet"; 
		}
	*/
	else
		return "";
	}

// retorna true se for tablet
function isTablet()
	{
	if(DEVICE == "tablet")
		return true;
	else
		return false;
	}
	
// retorna true se for mobile
function isMobile()
	{
	if(DEVICE == "mobile")
		return true;
	else
		return false;
	}

// retorna true se for PC
function isPC()
	{
	if(DEVICE == "")
		return true;
	else
		return false;
	}
/* [END] Mobile ---------------------------------------------------------------------------------------------------------- */
	

// include JS file synchronous 	
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
	fileref.async = true;
	
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
	
// verificar essa funcao pois faz parte de compatibilidade do core do SYSCALL
function included()
	{
	console.log(document.getElementsByTagName("script")[0].src);
	console.log(document.getElementsByTagName("script").length);
	
	// var scripts = document.getElementsByTagName("script");

	var a = "";
	for (i=0; i<document.getElementsByTagName("script").length; i++)
		{
		/*
		if(scripts[i].src == "something.js")
			{
			scripts[i].src = "this.js";
			}
		*/
		a += document.getElementsByTagName("script")[i].src+", "; 
		}
	
	console.log(a);
	
	console.log(document.getElementsByTagName("script"));
	}

// atualiza carregamento inicial do core
function DLibsLoader(c,s) {
	count = Math.round((c*100) / DLIBS.length);
	// step = s+" / 2";
	
	if(document.getElementById("DLIBSLOADER")) {
		document.getElementById("DLIBSLOADERCOUNT").innerHTML = count+"%";
		// document.getElementById("DLIBSLOADERCOUNTSTEP").innerHTML = step;
		document.getElementById("DLIBSLOADERCOUNTCONTAINER").style.width = (count)+"%";
	}
}

// adicionar css usado por padrao em todo o sistema
var DLIBSCSS = [
	"/css/menu.css",
	"/css/ui.css",
	"/css/loader.css",
	"/css/DPAC/DPAC.css", // css das funcoes dpac
	"/css/DPAC/DTouchSlider.css", // css do modulo de slider
	"/css/DPAC/field.css", // css dos campos
    "/css/EOS.css"
];

if(eos.device.get() === "mobile"){
    DLIBSCSS.push("/css/ui_mobile.css");
}

// bibliotecas basicas do core
// carregamento syncrono
var DLIBS = [
    // "/comum/modernizr/modernizr.custom.77791.js",
	"/comum/DPAC/DLoad.js",
	"/comum/DPAC/DMessages.js",
	
	// jquery 
	"/comum/jquery/jquery-1.8.3.js",
	// "/comum/jquery/jquery-1.10.1.min.js",  	=> apos mudanca para core v2 substituir para novo jquery
	// "/comum/jquery/jquery-migrate-1.2.1.min.js", => foram identificados problemas com cad empresa.
	"/comum/jquery/jquery-ui-1.9.2.custom.min.js",
	// async -> "/comum/jquery/jquery.ui.touch-punch.js", // melhorias para funcionamento em telas touch
	
	"/comum/DPAC/DUI.js", // ui basica (alertas)
	"/comum/DPAC/menu.js", // menus EYE / actions / where
	"/comum/DPAC/Call.js", //funcoes call / callgrid / callregrid
	"/comum/DPAC/relogin.js",
    "/comum/DPAC/DIssue.js", // bugtracker
    // "/comum/DPAC/DEmail.js", // envio de emails
	
	// async -> "/comum/fastclick/lib/fastclick.js",
	// async -> "/comum/touch/TouchSwipe/jquery.touchSwipe.min.js",
	// async -> "/comum/jquery/jquery.meiomask.js",
	"/comum/DPAC/DMenuTopRight.js", // Menu Top Right (sair e outros)
	// "/comum/DPAC/fieldOpt.js", // carrega opcoes dos campos
	// async -> "/comum/DPAC/fieldOpt2.js", // carrega opcoes dos campos
	// "/comum/DPAC/translate.js",
	"/comum/DPAC/fieldSelect.js", // refazer esse plugin pois esta muito pesado
	// "/comum/DPAC/grid.js",
	// "/comum/DPAC/DSwipePages.js", // parte do DPAGES, controla a troca de paginas
	// async -> "/comum/DPAC/DGrid.js", // novo grid
	// async -> "/comum/DPAC/DSearch.js", // pesquisa dentro de boxes
	// async -> "/comum/DPAC/DDebug.js", // modulo para degub do sistema
	// async -> "/comum/DPAC/DDownload.js", // plugin para executar download de arquivos
	// async -> "/comum/DPAC/DGeoLocation.js", // plugin para pegar geolocalizacao
	
	// Objects Core
	"/comum/DPAC/fieldNumber.js", // campos Numero
	"/comum/DPAC/fieldMoney.js", // campos Money
	"/comum/DPAC/fieldEmail.js", // campos Email
	"/comum/DPAC/fieldDateTime.js", // campos Data / Hora
	// "/comum/DPAC/fieldDateTime2.js", // campos Data / Hora
	"/comum/DPAC/fieldAutoComplete.js", // campos autocomplete
	"/comum/DPAC/fieldTextEditor.js", // campos Rich text editor
	"/comum/DPAC/DList.js", // gera listas para selects
	
	// "/comum/DPAC/fieldCheck.js", // converter para jquery plugin
    "/comum/DPAC/fieldCheckbox.js", // converter para jquery plugin
	// "/comum/DPAC/fieldPassword.js", // converter para jquery plugin
	// "/comum/DPAC/fieldUser.js", // converter para jquery plugin
	
	//Upload
	// "/comum/jquery-upload/js/vendor/jquery.ui.widget.js",
	// "/comum/jquery-upload/js/jquery.iframe-transport.js",
	// "/comum/jquery-upload/js/jquery.fileupload.js",
	// "/comum/DPAC/fieldUpload.js",
	
	// "/comum/DPAC/dbox.js", // converter para jquery plugin

	// Objects Touch Core
	"/comum/DPAC/DTouchPages.js",
	"/comum/DPAC/DTouchBoxes.js",
	"/comum/DPAC/DTouchRadio.js",
	"/comum/DPAC/DTouchList.js",
	// "/comum/DPAC/DTouchSlider.js",
    
    "/comum/DPAC/DActionAjax.js", // action ajax jquery plugin
	
	// maps usado em conjunto a gmaps library que carrega dentro do DPAC asyncronamente
    "/comum/DPAC/DMaps.js"
	];
	
	// requirimento for maps works, **** nao remover deste local de carregamento ****
    loadJS("https://maps.googleapis.com/maps/api/js?sensor=false");
	
// carrega library 2
// carregamento de bibliotecas Asyncrono
var DLIBSASYNC = [
	"/comum/fastclick/lib/fastclick.js", // remove o delay em dispositivos touch
	// "/comum/touch/TouchSwipe/jquery.touchSwipe.min.js", // controle de swipe em dispositivos touch
	"/comum/jquery/jquery.meiomask.js", // mascaramento de campos
	// "/comum/DPAC/fieldOpt2.js",
	"/comum/DPAC/fieldTextEditor.js", // campos Rich text editor
	"/comum/jquery/jquery.ui.touch-punch.js", // melhorias para funcionamento em telas touch
	"/comum/DPAC/DSearch.js",  // pesquisa dentro de boxes
    "/comum/DPAC/DUpload.js"  // upload padrao v2
	// "/comum/DPAC/DDownload.js", // plugin para executar download de arquivos
	// "/comum/DPAC/DGeoLocation.js", // plugin para pegar geolocalizacao
	// "/comum/DPAC/DDebug.js", // modulo para degub do sistema
	// "/comum/DPAC/DGrid.js", // novo grid
	// "/comum/DPAC/DActionAjax.js", // action ajax jquery plugin
	// "/comum/DPAC/DCEP.js", // action ajax jquery plugin
	// "/comum/keynav/javascript/jquery.keynav.js", // action ajax jquery plugin
];
	
	
// se for PC ativa hover (verificar se existe mouse ???)
if(isPC() === true) {
	loadCSS("/css/DPAC/DPAC_hover.css");
}

// carrega funcoes especificas para tablets
if(isTablet() === true) {
	// include("/comum/touch/fastclick/lib/fastclick.js");
	loadCSS("/css/ui_tablet.css");
	loadCSS("/css/DPAC/DPAC_tablet.css");
}

// carrega css DBLIBS
for(var i in DLIBSCSS) {	
	DLibsLoader(i,1); // loader das LIBS iniciais	
	loadCSS(DLIBSCSS[i]);
}
DLibsLoader(DLIBSCSS.length,1); // finaliza carregamento

// carrega js DBLIBS
for(var i in DLIBS) {	
	DLibsLoader(i,2); // loader das LIBS iniciais
	include(DLIBS[i]);
}
DLibsLoader(DLIBS.length,2); // finaliza carregamento

// carrega js DBLIBSASYNC
for(var i in DLIBSASYNC) {	
	loadJS(DLIBSASYNC[i]);
}

// remove loader inicial das bibliotecas, deixar esse codigo apos o caregamento da biblioteca jquery
$("#DLIBSLOADER").remove();

/* [END] Load jquery scripts ------------------------------------------------------------------------------------------ */	



/* [INI] Loader ------------------------------------------------------------------------------------------------------------------------
	Funcoes para mostrar e esconder o loading
------------------------------------------------------------------------------------------------------------------------------------- */
/*
(function($, window){ $.extend(
	{
	DLoader: function (settings, value) 
		{
		var settings = $.extend(
			{
			descrp	: "",
			}, settings || {});
		}
			
	
	}); })(jQuery, this);	
*/
	
// mostra Loader
function Loading(descrp) {
	// adiciona fundo (easter egg)
	// $("#loader_eos").addClass('body_central');
	
	// adiciona descritivo ao loader
	console.log("Loading: "+descrp);
	if(descrp) {
		// se for modulo chamado pelo call
		if(descrp.search("edit.cgi") != -1 || descrp.search("start.cgi") != -1) {
            var filter = descrp.match(/([^\/]+)(?=\/+\w+\.\w+$)/)[0];    
		} else if(descrp.search(".cgi") != -1) {
            var filter = descrp.match(/([^\/]+)(?=\.\w+$)/)[0];
		} else {
            var filter = descrp;
		};
			
		// translate para modulo 
		// *** verificar console.log para ver o modulo que nao esta sendo filtrado	
		var filtert  = {
			"enderecos"             : "endereços",
			"edit_list"             : "lista de itens",
			"dados_ti"              : "dados de ti",
            "dados_pc"              : "inventário de máquinas",
            "dados_users"           : "inventário de usuários",
			"usuario"               : "usuários",
			"usuario_tipo"          : "tipo de usuários",
			"contato_dados"         : "contatos",
			"tipo_relacionamento"   : "grupos empresa",
			"quotes"                : "daily quotes",
            "edit_acoes"            : "interações",
            "edit_submit"           : "salvando dados",
            "edit_submit_finalizar" : "finalizando chamado",
            "chamado_relatorio_prod": "relatório de produção",
            "chamado_relatorio"     : "financeiro service desk",
            "users"                 : "usuários",
            "procede"               : "procedimentos",
            "agrupo"                : "agrupamentos",
            "grupo"                 : "grupos",
            "tipo_grupo_item"       : "atributos",
            "tipo_doc"              : "tipo de documentos",
            "tipo_contato"          : "tipo de contatos",
            "prod_unidade"          : "tipo de unidade",
            "orc"                   : "orçamento",
            "verify"                : "ativação"
        };
			
		if(filtert[filter])
			filter = filtert[filter];
			
		$("#loader_descrp").html(filter);
		}
	else
		$("#loader_descrp").html("carregando... ");
	
	
	$('#loading, #loading_container').show();
	$('#loader_eos').show();
	
	// soma loaders
	LOADERS ++;
	// console.log(LOADERS);
};

// esconde Loader
function unLoading(v)
	{
	// ajusta loaders
	LOADERS --;	
	// console.log(LOADERS);
	if(LOADERS > 1)
		return false;
	else
		LOADERS = 0;
		
	// velocidade do fade in
	if(v == undefined)
		{
		v = "slow";
		}
		
	// mostra pagina apos ser carregada carregada
	if($("#main").is(":visible"))
		{
		$("#main").fadeIn("slow");
		}
		
	// remove fundo (easter egg)
	// $("#loader_eos").removeClass('body_central');
	
	// esconde loaders
	$('#loading, #loading_container').hide();
	$('#loader_eos').fadeOut(v); 
	}

/**
 *  Loader Obj
 */
function LoadingObj(obj)
	{
	loadingObj(obj);
	}
	
function loadingObj(obj) {
    
	if(isObject(obj)) { // se for objeto e nao o id
        var id = obj.prop("id");
        
        if(id === ""){ // adiciona id para funcionamento
            id = "temp_"+eos.core.genId();
            obj.prop("id",id);
        }
		obj = id;
	}
    
	if($('#loading').is(":visible")) { // se loader principal estiver ativo nao executa loader por objeto
		return true;
    }
    
    /* Cria Loader, usando template em /menu/start.cgi */
    var loaderObj = $(".eos_template_loader_obj").clone()
        .prop("id", "loader_obj_"+obj)
        .removeClass("eos_template_loader_obj")
        .addClass("loader_obj_container_full")
        .show();        
    
	var obj_full = "";
	
	if($("#main").is(":visible")) {
		obj_full = $("#main").contents().find("#"+obj);
	} else {
		obj_full = $("#"+obj);
	}
    
	// adiciona posicao relativa ao pai e adiciona o loader OBJ
	obj_full
        .css("position","relative")
        .append(loaderObj);
	
	// ajusta loader obj conforme tamanho do objeto
	var h = obj_full.css("height");
	if(h) {
		h.match(/\d+/g);
		if(h < 90) {
			$("#loader_obj_"+obj+" .loader_obj_container")
                .css({
    				"height": (h-10)+"px", 
    				"margin-top": "4px"
				});
		}
	}
}
	
    
// un loader por objeto
function unLoadingObj(obj) {
	// ajusta id pela opcao
	if(!obj) {
		obj = ".loader_obj_container_full";
	} else if(isObject(obj)) {
		obj = "#loader_obj_"+obj.prop("id");
	} else {
		obj = "#loader_obj_"+obj;
    }
		
	if($("#main").is(":visible")) {
		$("#main").contents().find(obj).remove();
	} else {
		$(obj).remove(); // remove todos os loaders de OBJs
    }
}
/* [END] Loader --------------------------------------------------------------------------------------------------------------------- */

/* [INI] Remove simbolos de uma string  ------------------------------------------------------------------------------- */
function srtClean(c) {
	return c.replace(/(\/|\-|\:|\,|\.|\(|\)|\ )/g,'');
}

function LIMP(c) { return srtClean(c); }
/* [END] Remove simbolos de uma string  ------------------------------------------------------------------ */

/* [INI] Testa se variavel NULA -------------------------------------------------------------------------- */
function isNULL(c) {
	// Função para verifição se o valor é vazio ou só contenha espaços
	if(c == "") {
		return(1);			// retorna 1 (true) se for vazio
	} else {
		var pos=0;
		while(c.charAt(pos) == " ") {
			if(pos == c.length-1) {
				return(1);			// retorna 1 (true) se apenas tiver espaços em branco
			}
			pos++;
		}
		return(0);			// retorna 0 (false) se for um valor não vazio (ou não nulo)
	}
}
/* [END] Testa se variavel NULA ------------------------------------------------------------------------- */

/* [INI] Testa se variavel NUMERO  ---------------------------------------------------------------------- */
// Função para verificação de um valor numérico válido 
// retorna 0 (false) se não for um valor numérico válido
// retorna 1 (true) se for um valor numérico válido
function isNUMB(c) { 
    if(c) return isNum(c); else return false; 
} // short cut !

function isNum(c) {
	if(!c) {
		return false;
    }
		
	if((pos=c.indexOf(",")) != -1) {
		c = c.substring(0,pos)+"."+c.substring(pos+1);
    }

	if((parseFloat(c) / c != 1)) {
		if(parseFloat(c) * c == 0) {
			return true;
		} else {
			return false;
        }
	} else {
		return true;
    }
}

/**
 *  To Num
 *      Função que converte um número com sinal decimal ponto para vírgula
 *          retorna false se não for um valor numérico válido
 *          retorna o valor convertido
 */

function toNUMB(c) { // compatibilidade com core syscall (remover)
    console.log("toNUMB() core syscall, substituir por toNum()");
    return toNum(c); 
}  

function toNum(c) {
	if(isNum(c) != 1) {
		return false;
    }		
		
	if((pos = c.indexOf(",")) !=-1 ) {
		c = c.substring(0,pos)+"."+c.substring(pos+1);
    }
    
	return parseFloat(c);
}

/**
 *  Testa Tipo do OBJETO
 *      isArray(obj)    - array
 *      isFunction(obj) - funcao
 *      isObject(obj)   - objeto
 */
function isArray(obj) {
	if(Object.prototype.toString.call(obj) === '[object Array]') {
		return true;
	}
	return false;
}

function isObject(obj) {
	if(Object.prototype.toString.call(obj) === '[object Object]') {
		return true;
	}
	return false;
}
	
function isFunction(obj) {
	if(typeof obj == 'function') {
		return true;
	}
	return false;
}

/* [INI] ---------------------------------------------------------------------------------------------------
	Testa E-mail
	
	- retorno: 0 (false) / 1 (true)
--------------------------------------------------------------------------------------------------------- */
function isMail(email) {
	var regex = new RegExp(/^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i);
	
	if(regex.test(email)) {
		return true;
	} else {
		return false;
    }
}
/* [END] Testa se Email  -------------------------------------------------------------------------------- */

/* [INI] isDoc ------------------------------------------------------------------------------------
*	Testa DOCS  
* 		CNPJ / CPF
------------------------------------------------------------------------------------------------ */
function isDoc(doc)
	{
	// se valor vazio
	if(!doc)
		var doc = "";
	
	// limpa o valor
	doc = srtClean(doc);
	
	// verifica se numero
	if(!isNum(doc) && doc != "")
		return "Não é um numero";
		
	// cnpj
	if(doc.length == 14)
		{
		if(isCNPJ(doc) == 1)
			return true;
		else
			return "CNPJ inválido !";
		}
	// cpf
	else if(doc.length == 11)
		{
		if(isCPF(doc) == 1)
			return true;
		else
			return "CPF inválido !";
		}
	else
		return false;
	}
/* [END] isDoc  -------------------------------------------------------------------------------- */

/* [INI] Testa CNPJ  ------------------------------------------------------------------------------------ */
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
/* [END] Testa CNPJ  ------------------------------------------------------------------------------------ */

/* [INI] Testa CPF  ------------------------------------------------------------------------------------- */
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
/* [END] Testa CPF  ------------------------------------------------------------------------------------- */

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
	var c = new Date(toNum(ANO), (toNum(MES)-1), toNum(DIA));
	if(c.getDate() == DIA)
		{
		return(1);			// retorna 1 (true) indicando que é uma data válida
		}
	else
		{
		return(-1);			// retorna -1 indicando que é data inválida
		}
	}

/* [INI] to Money (by gaiattos.com/akgleal) ----------------------------------------------------------------------------------------------------
 	Ajusta número para o formato de moeda, substitute of Luciano function toMoney
	
	future: Implementar a colocacao do separador de milhar
------------------------------------------------------------------------------------------------------------------------------------ */
function money(val,calc) {
	// ajusta money para calculos
	if(calc) {
        
		// testa se campo nao vazio
		if(isNaN(parseFloat(val))) {
			val = 0;
		} else {
			val = val.replace(/^.*[R$]/i,""); // remove R$
            
            
            if(/(\..*,|\,.*\.)+/.test(val)) {
            // if(/(\,)+/.test(val) && /(\.)+/.test(val)) {
                val = val.replace(/[.]/g,""); // remove pontos   
            }
            
            val = val.replace(",","."); // troca ponto por virgula
		}
        
		retorno = parseFloat(val);
        
	} else { // ajuste money para mostrar em campos
        val = parseFloat(val);
		retorno = val.toFixed(2).replace(".",",");
	}
		
	// retorno
	return retorno; 
}
	
function toMoney(c)
	{
	// link para nova funcao
	money(c);

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

/* [END] to Money (by gaiattos.com/akgleal) ---------------------------------------------------------------------------------------------------- */


/* [INI] uc / ucfirst / ucfisrtall / lc (by gaiattos.com/akgleal) ---------------------------------------------------------------------
 	uc = Uper Case = Transforma toda string em MAIUSCULAS
	ucfisrt = Uper Case First = Transforma somente a primeira letra da string em MAIUSCULA
	ucfirstall = Uper Case all First = Transforma todas as primeiras letras da string em MAIUSCULAS
	lc = Lower Case = Transforma toda string em MINUSCULAS
------------------------------------------------------------------------------------------------------------------------------------ */

/* adiciona funcoes ao objeto string */
String.prototype.lc = function(){
	return this.toLowerCase();
};

String.prototype.uc = function(){
	return this.toUpperCase();
};
	
String.prototype.ucFirst = function(){
	return this.charAt(0).toUpperCase() + this.slice(1);
};
	
String.prototype.ucFirstAll = function(){
	return this.toLowerCase().replace(/(^| |\-)(\w)/g, String.toUpperCase)
};

String.prototype.strClean = function(){
	return this.replace(/(\/|\-|\:|\,|\.|\(|\)|\ )/g,'');
};


function uc(str){
	return str.toUpperCase();
};

function ucfirst(str){ 
    return ucFirst(str); 
};
function ucFirst(str){
	str = str.slice(0,1).toUpperCase() + str.slice(1).toLowerCase();
	return str;
};
	
function ucfirstall(str) { return ucFirstAll(str); }
function ucFirstAll(str)
	{
	str = str.toLowerCase().replace(/\b[a-z]/g, function(letter) 
		{
    	return letter.toUpperCase();
		});
	return str;
	}
	
function lc(str)
	{
	return str.toLowerCase();
	}
/* [END] uc / ucfirst / ucallfisrt / lc (by gaiattos.com/akgleal) ------------------------------------------------------------------ */


	
// erros ajax  ----------------------------------------------------------------------------------------------------------------------------
	function errojx(XMLHttpRequest, textStatus, errorThrown)
		{
		unLoading();
		alerta("ERRO!<br><br>"+XMLHttpRequest+" "+textStatus+" "+errorThrown);
		}
		

/* [INI] Temporizador -------------------------------------------------------------------------- 

	window.onload = CreateTimer('timer', 30);
	<div id='timer'></div>

*/
function DTimer(id,tempo)
	{
	var Timer;
	var TotalSeconds;

	this.tick = function() 
		{
		if (TotalSeconds <= 0) 
			{
			// adicionar as funcoes aqui !!
			alert('Times up!')
			return;
			}
		
		TotalSeconds -= 1;
		UpdateTimer();
		window.setTimeout('Tick()', 1000);
		}

	this.update = function() 
		{
		Timer.innerHTML = TotalSeconds;
		}
	
	this.show = function(TimerID, Time) 
		{
		Timer = document.getElementById(TimerID);
		TotalSeconds = Time;

		UpdateTimer()
	    window.setTimeout('Tick()', 1000);
		}
	}

/* [INI] D-Grid -------------------------------------------------------------------------- 
	Funcoes de Clique e Clique Duplo


// Grid Click 
function gridClick()
	{
	try
	    {
	    main.gridClick();
	    }
	catch(err)
	    {
	    return;
	    }
	}

// Grid DBL Click 
function gridDblClick()
	{
	try
	    {
	    main.gridDblClick();
	    }
	catch(err)
	    {
	    return;
	    }
	}	
 [END] D-Grid -------------------------------------------------------------------------- */

/* [INI] Alerta ----------------------------------------------------------------------------- 
	Modal Alerta
	atalho para funcao alerta em ui_eos.js
---------------------------------------------------------------------------------------- */
function alerta(msg, act)
	{ var act, msg;
	if(!act)
		act = "";
		
	// testa se funcao existe senao executa sem modal
	try
	    {
	    alerta(msg, act);
	    }
	catch(err)
	    {
	    alert(msg);
	
		if(!act)
			eval(act);
	    }
	}
/* [END] Alerta -------------------------------------------------------------------------- */

// ajuste da funcao salvar para funcionamento com antigo core do syscall e novo do eos
function procede()
	{
	try
		{
		main.procede();
		}
	catch(err)
		{
		try
			{
			procede();
			}
		catch(err)
			{
			console.log("Devils: A função: \n\n    procede() ou main.procede \n\ndeve ser criada no documento que está sendo executado. \n\n "+err);
			}
		}
	}

// ajuste da funcao salvar para funcionamento com antigo core do syscall e novo do eos
// retro compatibilidade EOS v1
function salvar(){
	try {
	    eos.DAction.save();
	} catch(err) {
        
    	try {
    	    main.salvar();
    	} catch(err) {
    		console.log(err);
    		DActionSave();
    	}	
	}
}


// ajuste da funcao voltar para funcionamento com antigo core do syscall e novo do eos
function voltar()
	{
	try
	    {
	    main.voltar();
	    }
	catch(err)
		{
		try
		    {
			DActionBack();
			console.log("funcao voltar: "+err);
		    }
		catch(err)
		    {
			console.log("Devils: A função: \n\n    DActionBack() \n\ndeve ser criada no documento que está sendo executado. \n\n "+err);
			}
		}
	}
	
// inserir, ajuste da funcao para funcionamento com antigo core do syscall e novo do eos
function incluir() {
	try {
	    eos.DAction.new();
	} catch(err) {
        
    	try {
    	    main.incluir();
    	} catch(err) {
    		console.log(err);
    		DActionAdd();
    	}	
	}
}
	
// editar, ajuste da funcao para funcionamento com antigo core do syscall e novo do eos
function editar()
	{
	try
	    {
		main.editar();
	    }
	catch(err)
	    {
		console.log(err);
		
		DActionEdit();
		}
	}


	
// Actions Default
// busca dados do banco para preenchimento do formulario
function DActionEditDB(req)
	{
	Loading(" formulário");
	
	if(!req)
		req = "";
	else
		req = "&"+req;
	
	$.ajax({
		type: "POST",
		url: $('#AUX input[name="MODULO_PATH"]').val()+"/edit_db.cgi",
		dataType: "html",
		data: "&ID="+$('#AUX input[name="ID"]').val()+"&COD="+$('#CAD input[name="COD"]').val()+"&MODO="+$('#CAD input[name="MODO"]').val()+req,
		success: function(data)
			{
			$("#resultado").html(data);
			unLoading();
			},
		error: errojx
		});	
		
	}

/* [INI] Delete ----------------------------------------------------------------------------------------------------------
*
*	Funcoes de Delete / Exclusao padrao
*	function excluir() para manter suporte ao core do syscall
*	function DActionDelete() novo padrao do EOS, ainda mantem compatibilidade com o core do syscall testando a funcao 
*		main.excluir antes de continuar.
*	function DActionDeleteDefault() executa funcoes de delecao padrao se funcao function DActionDelete() nao existir 
*		no modulo carregado
*
----------------------------------------------------------------------------------------------------------------------- */
// padrao delete novo
function cancelar()
	{
	try // testa excluir do core do syscall para manter compatibilidade
	    {
	    main.cancelar();
	    }
	catch(err)
	    {
	    DActionCancel();
	    }
	}
	

/* [END] Delete ------------------------------------------------------------------------------------------------------- */
	


/* [INI] DListGet --------------------------------------------------------------------------------------------------------
*
*	Funcoes para gerar listas de select
*
*	DListGetUser()
*	DListGet()
*
*
----------------------------------------------------------------------------------------------------------------------- */
function DListGet(table,obj)
	{
	$.ajax({
		async:false,
		type: "POST",
		url: "/sys/cfg/DPAC/DListGet.cgi",
		dataType: "html",
		data: "&ID="+$('#AUX input[name="ID"]').val()+"&T="+table,
		success: function(data)
			{
			DListGetVar = data;
			// console.log("sucesso");
			// console.log(DListGetVar);
			
			return DListGetVar;
				
			// return data;
			// var lista = data;
			// return lista;
			// return data;
			// return "aaaaaa";
			/*
			console.log(data);
			
			var aa = "";
			for(var f in lista)
				{
				aa += "cod: "+lista[f]["codigo"];
				aa += "descrp: "+lista[f]["descrp"];
				}
			
			console.log(aa);
			return aa;
			*/
			},
		error: function(data)
			{
			// se erro em todas as tentativas retorna tip + mensagem de erro
			console.log(data);
			alerta("Devils: A função: \n\n    DListGet() \n\né usada em conjunto com /cfg/DListGet. \n\n *** verficar logs no console");
			unLoading();
			
			return false;
			}
		});
	}

/* [END] DListGet ----------------------------------------------------------------------------------------------------- */

	
/* [INI] DActionForm -----------------------------------------------------------------------------------------------------
*
*	Ajusta visualizacao do formulario
*
*	ver (deixa todos os forms em html)
*
----------------------------------------------------------------------------------------------------------------------- */
function DActionForm(modo)
	{ 
	// normaliza variavel	
	modo = lc(modo)
	
	switch(modo)
		{
		// Modo Visualizar ----------------------------
		case "ver":
		
		if($("#CAD").find(".DActionForm").length > 0)
			{
			$("#CAD").find(".DActionForm").remove();
			$("#CAD").find("input[type='text'], textarea, select").show();
			
			return true;
			}
		
		// esconde todos inputs
		$("#CAD").find("input[type='text'], textarea, select").hide().each(function()
			{
			$(this).parent().append("<span class='DActionForm'>"+$(this).val()+$(this).find('option').filter(':selected').text()+"</span>");
			
			// $(this).parent().text($(this).val());
			});

		break;
		}

	}
/* [END] DActionForm --------------------------------------------------------------------------------------------------- */

/* [INI] DMenuAction -----------------------------------------------------------------------------------------------------
*
*	Ajusta menus action
*
----------------------------------------------------------------------------------------------------------------------- */
function DMenuAction(x)
	{
	if(!x)
		x = "";
	// console.log($('#AUX input[name="MODULO_PATH"]').val());
	// console.log($('#AUX input[name="SHOW"]').val());
	
	DActionAjax("menu.cgi",x);
	}
/* [END] DMenuForm --------------------------------------------------------------------------------------------------- */
	
// remover esta funcao apos finalizar importacao dos modulos do syscall para core do eos
function block(x)
	{
	return true;
	}
	
    
    
    
    
/** 
 *  EOS APP 
 *      estrutura EOS para core v3 +
 */
function EOS(){
    var eoscore = this;
    
    /**
     *   Logout
     */
    this.company = {
        db : {
          name    : "Done Tecnologia da Informação Ltda",
          address : "Av. São Pedro, 1001, Porto Alegre - Rio Grande do Sul, Brasil",
          img     : {
              logo : "/img/ui/maps.png",
              maps : "/img/ui/maps.png"
          }   
        },
        name : function(x){
            if(!x){
                return this.db.name;
            }
        },
        address : function(x){
            if(!x){
                return this.db.address;
            }
        },
    };
    
    
    
    /**
     *   Logout
     */
    this.logout = function(){
        Loading("Encerrando Sistema");
        
        var f = document.createElement("form");
            f.target = "_top";
            f.action = "/sys/logon/logout.cgi";
            
        document.getElementById("BODYEOS").appendChild(f);
        f.submit();
    };
    
    /**
     *   Tools
     */
    this.tools = {
        idGen: function(){
            return Math.random().toString().substr(2);
        }
    };
        
    /**
     *   Templates
     */
    this.template = {
        chamado : {
            
        },
        field : {
            // right click
            right : {
                click : function(obj){
                    
                },
                class : function(obj,c){
                    
                }
            },
            // mostra campo
            show : function(f){
                console.log("EOS.template.field.show");
                
                f.parents(".EOS_template_field").show();
                f.parent().find(".EOS_template_field").show(); // se caso autocomplete
            },
            // esconde campo
            hide : function(f){
                console.log("EOS.template.field.hide");
                
                f.parents(".EOS_template_field").hide();
                f.parent().find(".EOS_template_field").hide(); // se caso autocomplete
            },
            // clique no campo
            click : function(){
                $(".EOS_template_field_img").off("click").click(function(event){
                    // $(this).parent().find(".EOS_template_field_field [input|select]").focus();
                    console.log("click dentro campo");
                    // se campo desabilitado
                    if($(this).closest(".EOS_template_field").hasClass("EOS_template_lock")){
                        return false;
                    }
                    
                    // starta campo quando clicado na imagem
                    if($(this).parent().find(".EOS_template_field_field .fieldSelect").length > 0){
                        $(this).parent().find(".EOS_template_field_field .fieldSelect").fieldSelect("open");
                    } else { console.log("input");
                        $(this).parent().find(".EOS_template_field_field input").focus();
                    }
                });
            },
            // read only campo
            readonly: function(f){
                console.log("EOS.template.field.lock");
                
                f.prop("readonly", true)
                    .addClass("EOS_template_field_lock");
                /*    
                f.closest(".EOS_template_field")
                    .addClass("EOS_template_lock")
                    .find(".EOS_template_field_img")
                    .addClass("EOS_template_field_img_lock");
                */
            },
            // desabilitar campo
            lock: function(f){
                console.log("EOS.template.field.lock");
                
                f.prop("readonly", true)
                    .addClass("EOS_template_field_lock");
                    
                f.closest(".EOS_template_field")
                    .addClass("EOS_template_lock");
                    /*
                    .find(".EOS_template_field_img")
                    .addClass("EOS_template_field_img_lock");
                    */
            },
            // habilitar campo
            unlock: function(f){
                console.log("EOS.template.field.unlock");
                
                f.prop("readonly", false)
                    .removeClass("EOS_template_field_lock");
                    
                f.closest(".EOS_template_field")
                    .removeClass("EOS_template_lock");
                    /*
                    .find(".EOS_template_field_img")
                    .removeClass("EOS_template_field_img_lock");
                    */
            },
            getId: function(){
                return "EOS_template_field_input_place_"+Math.random().toString().substr(2);
            },
            text: function(f){
                var id    = this.getId()
                ,   field = document.createElement("div");
                    field.id = id;
                    field.className = "EOS_template_field EOS_template_field_text";
                    
                f.parent().append(field);
                f.appendTo(field);
            },
            password: function(f){
                var id    = this.getId()
                ,   field = document.createElement("div");
                    field.id = id;
                    field.className = "EOS_template_field EOS_template_field_password";
                    
                f.parent().append(field);
                f.appendTo(field);
            },
            number: function(f){
                var id    = this.getId()
                ,   field = document.createElement("div");
                    field.id = id;
                    field.className = "EOS_template_field EOS_template_field_number";
                    
                f.parent().append(field);
                f.appendTo(field);
            },
            money: function(f){
                var id    = this.getId()
                ,   field = document.createElement("div");
                    field.id = id;
                    field.className = "EOS_template_field EOS_template_field_money";
                    
                f.parent().append(field);
                f.appendTo(field);
            },
            autocomplete: function(f){
                // this.search(f,1);
                var field  = "<div class='EOS_template_field EOS_template_field_autocomplete'>";
                    // field += "  <div class='EOS_template_field_img'></div>";
                    // field += "  <div class='EOS_template_field_field'>"+ f +"</div>";
                    field += f;
                    field += "</div>";
                return field;
            },
            search: function(f,right){
                var id = this.getId();
                
                var field  = "<div class='EOS_template_field EOS_template_field_search' id='"+id+"'>";
                
                if(right){ // adiciona campo direito
                    field += "  <div class='EOS_template_field_search_right'>"+right+"</div>";
                }
                    field += "</div>";
                    
                // adiciona campo
                f.parent().append(field);
                f.appendTo($('#'+ id));
                
                if(right){ // adiciona classe 
                    f.addClass("EOS_template_field_search_right_padding");
                }
                                
                this.click();
            },
            date: function(f){
                var id = this.getId();
                var field  = "<div class='EOS_template_field EOS_template_field_date' id='"+ id +"'>";
                    field += "</div>";
                                        
                f.parent().append(field);
                f.appendTo($('#'+ id));
            },
            datetime: function(f){
                var id = this.getId();
                var field  = "<div class='EOS_template_field EOS_template_field_datetime' id='"+ id +"'>";
                    // field += "  <div class='EOS_template_field_img'></div>";
                    // field += "  <div class='EOS_template_field_field' id='"+ id +"'></div>";
                    field += "</div>";
                    
                f.parent().append(field);
                f.appendTo($('#'+ id));
                
                this.click();
            },
            time: function(f){
                var id = this.getId();
                var field  = "<div class='EOS_template_field EOS_template_field_time' id='"+ id +"'>";
                    // field += "  <div class='EOS_template_field_img'></div>";
                    // field += "  <div class='EOS_template_field_field' id='"+ id +"'></div>";
                    field += "</div>";
                    
                f.parent().append(field);
                f.appendTo($('#'+ id));
                
                this.click();
            },
            email: function(f){
                var id = this.getId();
                var field  = "<div class='EOS_template_field EOS_template_field_email' id='"+ id +"'>";
                    // field += "  <div class='EOS_template_field_img'></div>";
                    // field += "  <div class='EOS_template_field_field' id='"+ id +"'></div>";
                    field += "</div>";
                    
                f.parent().append(field);
                f.appendTo($('#'+ id));
                
                this.click();
            },
            select: function(f){
                var id = this.getId();
                var field  = "<div class='EOS_template_field EOS_template_field_select'>";
                    field += "  <div class='EOS_template_field_img'></div>";
                    field += "  <div class='EOS_template_field_field' id='"+ id +"'></div>";
                    field += "</div>";
                    
                f.parent().append(field);
                f.appendTo($('#'+ id));
                
                this.click();
            },
            file: function(f){
                var id = this.getId();
                var field  = "<div class='EOS_template_field EOS_template_field_file' id='"+ id +"'>";
                    field += "</div>";

                f.parent().append(field);
                f.appendTo($('#'+ id));
            }
        }
    };
    
    /*
    *   Device
    *       wich device ?
    */
    
    this.device = {
        is : function(device){
            if(this.get(1) === device.toLowerCase()) {
                return true;
            } else {
                return false;
            };
        },
        get : function(x){
        	var ua = navigator.userAgent.toLowerCase(); // pega agente
	        
            if(!x){
                if( /Android|webOS|iPhone|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
                    return "mobile";
                } else {
                    return "desktop";
                }
            }
            
            if(x) {
            	if (ua.search("iphone") > -1) {
                	return "mobile";
            	} else if (ua.search("ipod") > -1) {
            		return "mobile";
                } else if (ua.search("ipad") > -1) {
                	return "tablet";
            	} else if (ua.search("android") > -1) {
                    console.log("ver melhor filtro para identificar se eh tablet ou phone");
                	return "android";
                } else {
                    return "pc";
                };
            } else {
                return ua;
            };
        }
    };
    
    
    // chamado FAST
    this.chamadoFast = function(){
        $.DDialog("TEST");
    };
    
    
    // deagle / monitoramento
    this.deagle = function(dat) {
        
        var content = "";
        if(eos.core.is.array(dat)) {
            dat.forEach(function(i){
                content += i+" <br>";
            });
        }
        
        if($("#deagle_").hasClass("deagle_down") || dat === false) {
            // $("#deagle_").hide();
            $("#deagle_").removeClass("deagle_down");
            $("#deagle_talk").removeClass("deagle_talks");
            $("#deagle_talk_content").hide();
        } else {
            $("#deagle_").addClass("deagle_down");
            $("#deagle_talk").addClass("deagle_talks");
            $("#deagle_talk_content").show().html(content);
        }
    };
    
    
    /*
    *   Menu
    *       funcoes do menu 
    */
    this.menu = {
        
        // eye, menu
        eye : function(menu){
            var m = this; // objeto menu
            
        	if($("#lightsoff").is(":visible")) {
                $("#menu_float").removeClass("menu_float_down"); // esconde menu principal
                
        		$("#user_menu_float").slideUp(300, function() { // esconde menu user
        			$("#lightsoff").fadeOut(100, function() { 
                        $("#eye").removeClass("eye_down"); // esconde menu eye
                        
        				// se for para entrar em algum modulo
        				if(menu) {
        					m.where(menu);
                        }
        			});
        		});
        	} else {
                $("#eye").addClass("eye_down"); // mostra menu eye
                		
        		$("#lightsoff").fadeIn(200, function() {
                    $("#menu_float").addClass("menu_float_down"); // mostra menu principal
        			$("#user_menu_float").slideDown(300); // mostra menu user
        	    });
        	}
        },
        
        // where, menu
        where : function(menu,no) { 
            
            if(!no){
    	        // executa menu selecionado
        	    MENUSER[menu].acao();
            }
	
        	// seta o home
        	if(menu == "home") {
        		var home  = '<a onClick="eos.menu.where(\'home\');"><img src="/img/ui/menu_home.png" align="absmiddle" title="'+MENUSER['home'].descrp+'"></a>';
        		$('#menu_top_home').html(home);
		
        		// limpa modulo se for home
        		$('#menu_top_modules').html("");
        		return true;
        	}
		
        	// seta modulo
        	var modulo  = '<a onClick="eos.menu.where(\''+menu+'\');">'+MENUSER[menu].descrp+'</a>';				
        	$('#menu_top_modules').html(modulo);
        },
        
        // action, menu
        action : {
            new : function(settings) {
                console.log("EOS.menu.action.new");
                
        		var settings = $.extend({
        			id       : "btn_"+$(".menu_btn").length,    // id do item
        			title    : "new btn",   // titulo inferior
                    subtitle : "",          // titulo superior
        			click    : false,       // ao clicar executa funcao
                    class    : "",          // adiciona classe especifica para botao
                    group    : false,       // agrupa icones com outros do mesmo grupo
                    super    : false        // ajusta botao para aparecer absolute desatachado do grupo action menu
        		}, settings || {});
                
                var menu_btn_title_sub;
                
        		// remove botao se existir
    			if($("#"+settings.id).length > 0){
    				$("#"+settings.id).remove();
    			}

        		// ajusta borda da sub descricao
        		if(!settings.subtitle){
        			menu_btn_title_sub = 'border:none; ';
                }
                
                // ajusta grupo do icone
                if(settings.group === false) {
                    settings.group = "";
                }
                   
                /* mostra icone */
                if(settings.super){ // icone super
                    $("body").append('<div class="menu_btn menu_btn_control '+settings.class+' '+settings.group+' DMenu_action_super" id="'+settings.id+'"><div class="menu_btn_container"><div class="menu_btn_title_sub" style="'+menu_btn_title_sub+'">'+settings.subtitle+'</div><div class="menu_btn_title">'+settings.title+'</div></div></div>');
                } else { // icone normal
        		    $("#menu_actions").append('<div class="menu_btn menu_btn_control '+settings.class+' '+settings.group+'" id="'+settings.id+'"><div class="menu_btn_container"><div class="menu_btn_title_sub" style="'+menu_btn_title_sub+'">'+settings.subtitle+'</div><div class="menu_btn_title">'+settings.title+'</div></div></div>');
                }
                
        		$("#"+settings.id).click(function(){
                    if(settings.click){
        		        settings.click.call();
                    } else {
                        console.log("EOS.menu.action.new: definir a acao do click");
                    }
        		});
            },
            show : function(icon) {
        		if(isArray(icon)){ // array
        			for(var i in icon) {
        				$("#"+icon[i]).fadeIn('fast');
                    }
        		} else {
        			$("#"+icon).fadeIn('fast');
                }
            },
            hide : function(icon) {
        		if(isArray(icon)){ // array
        			for(var i in icon) {
                        $("#"+icon[i]).hide();
                    }
        		} else {
                    $("#"+icon).hide();
                }
            },
            // hide all esconde todos icones
            hideAll : function() {
        		$(".menu_btn_control").hide();
            },
            // desaparecer o menu inteiro
            disappear : function() {
                $("#menu_actions").addClass("menu_actions_vanish");
            },
            // aparecer o menu inteiro
            appear : function() {
                $("#menu_actions").removeClass("menu_actions_vanish");
            },
            // remove permanentemente item
            destroy : function(icon) {
        		if(isArray(icon)){ // array
        			for(var i in icon) {
                        $("#"+icon[i]).remove();
                    }
        		} else {
                    $("#"+icon).remove();
                }
            }
        }
        // user menus
        // user : MENUSER;
        // this.menu.user = MENUSER;
    };
    
    /*
    *   DAction
    *       all actions from app
    */
    this.DAction = {
        
        /*
        *   Ajax
        *       executa ajax
        */
        ajax : function(s){
            console.log("EOS.DAction.ajax");
        
    		var s = $.extend({
                type           : '',
    			action         : '',
    			req            : '',
    			loader         : true, // full loader ( false = no loader / id obj = )
    			serializeForm  : true, // serializa formulario #CAD
    			async          : true,
                postFunction   : false
    		}, s);
        
            // shortcut para funcao real, 
            // transferir para este local no core V3
            $.DActionAjax({
                type          : s.type,
    			action        : s.action,
    			req           : s.req,
    			loader        : s.loader,
    			serializeForm : s.serializeForm,
    			async         : s.async,
                postFunction  : s.postFunction
            });
        },
            
        /*
        *   New
        *       Botao incluir do sistema
        */
        new : function(){
            console.log("EOS.DAction.new");
            
        	try { // se for modulos iframe
                main.incluir();
            } catch(err) {
        		console.log("Not IFRAME: "+err);
                
            	try { // core v2
                    DActionAdd(); // executa save do modulo
                } catch(err) {
                    console.log("Not CORE v2: "+err);
                    
                    try { // core v3
                        form.new();
                    } catch(err) {
                        console.log("Not CORE v3: "+err);
                        console.log("objeto form deve ser criado para funcionamento com core v3");
                    }
                }
            }            
        },
        // shortcut for New DAction
        add : function(){
            this.new();
        }, 
        /*
        *   Save
        *       Botao salvar do sistema
        */
        save : function(){
            console.log("EOS.DAction.save");
            
        	try { // se for modulos iframe
                main.salvar();
            } catch(err) {
        		console.log("Not IFRAME: "+err);
                
            	try { // core v2
                    DActionSave(); // executa save do modulo
                } catch(err) {
                    console.log("Not CORE v2: "+err);
                    
                    try { // core v3
                        form.save()
                    } catch(err) {
                        console.log("Not CORE v3: "+err);
                        console.log("objeto form deve ser criado para funcionamento com core v3");
                    }
                }
            }
        },
        
        /*
        *   Delete
        *       acao do botao de delete
        */
        delete : function(){
            console.log("EOS.DAction.delete");
            
            try { // se for modulos iframe
                main.excluir();
            } catch(err) {
                console.log("Not IFRAME: "+err);
                
		        try { // testa se funcao delete do modulo existe
            	    DActionDelete();
                } catch(err) { // delete default
                    try {
                        $.DDialog({
                            type    : "confirma",
                            message : "Deseja realmente excluir ?",
                            btnYes  : function(){
                            	// verifica se ID esta setado no modulo 
                            	if(!$('#AUX input[name="ID"]').val()) {
                            		console.log("ID do formulario CAD nao populado verificar campo no modulo");
                            		console.log($('#AUX input[name="ID"]'));
                            		return false;
                            	}

                            	// verifica se ID esta setado no modulo 
                            	if(!$('#AUX input[name="MODULO_PATH"]').val()) {
                            		console.log("MODULO_PATH, Caminho do modulo no formulario AUX nao populado verificar campo");
                            		console.log($('#AUX input[name="MODULO_PATH"]'));
                            		return false;
                            	}

                            	// executa arquivo de exclusao
                            	Loading("processo de exclusão");
                            	$.ajax({
                            		type: "POST",
                            		url: $('#AUX input[name="MODULO_PATH"]').val()+"/edit_submit_delete.cgi",
                            		dataType: "html",
                            		data: "&ID="+$('#AUX input[name="ID"]').val()+"&"+$('#CAD').serialize(),
                            		success: function(data) {
                            			$("#resultado").html(data);
                            			unLoading();
                            		},
                            		error: function(data) {
                            			// se erro em todas as tentativas retorna tip + mensagem de erro
                            			console.log(data);
                            			unLoading();
                            		}
                            	});
                            }
                        });
                        
                    } catch(err) {
                        console.log(err);
                    }
                }
            }
        },
            
        /*
        *   Resize
        *       controla o redimensionamento do sistema
        */
        resize : function(){
            
            console.log("EOS.DAction.resize");
            // console.log($("#menu_float").height());
            
            // DTouchRadioContainer Controller
        	if($(".DTouchRadioContainer").length > 0){
        		$(".DTouchRadioContainer").each(function()
        			{
        			console.log($(this));
        			$(this).DTouchRadio("resize");
        			});
        		}
            
            /*  
            // executa 
        	try
        	    {
        		DActionResize();
        	    }
        	catch(err)
        		{
        		// console.log(err);
        		return false;
        		}
            */
            
            // Timer EOS ver o funcionamento
        	// eos.ticker && clearTimeout(eos.ticker);
        	// eos.ticker = setTimeout(DActionResizeDefault, 100);
        }
    };
    
    
    
    // ticker do sistema implementar
    this.ticker = "";
    
    
    /*
    this.company = [];
        company["address"]   = "Av. São Pedro, 1001, Porto Alegre - Rio Grande do Sul, Brasil";
        company["name"]      = "Done Tecnologia da Informação LTDA";
        company["icon_maps"] = "/img/ui/maps.png";
     */  
        
    this.core = {
        
        /**
         *   Imagem (logo sistema)
         */
        img: function(size){
            if(!size) {
                size = 300;
            }
            
            var img = [];
                img[300] = "data:image/jpeg;base64,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";
                
            return img[size];
        },
        
        /**
         *   Gen Id
         *       gera id unico
         */
        genId: function(){
            return Math.round(Math.random().toString().substr(2));
        },
        
        
        /**
         *   Upload
         *       funcoes do upload
         */
        upload : {
            
            /* done, apos concluido script de upload */
            done : function(uuid,cod) {
                console.log("EOS.core.upload.done "+uuid);
                         
                if(!cacheDUploadObj[uuid]){
                    console.log("erro desconhecido ao fazer upload");
                    return false;
                }
                
                var obj = cacheDUploadObj[uuid]
                ,   s   = cacheDUploadObj[uuid].data("DUploadSettings"); 
                
                /* post Function */
                if(isFunction(s.postFunction)) {
            
                    var r = {
                        codigo : cod,
                        descrp : obj.parent().find("input[type=text]").val(),
                        name   : obj[0].files.item(0).name,
                        size   : obj[0].files.item(0).size,
                        type   : obj[0].files.item(0).type
                    };
            
                    s.postFunction.call(this,r);
                }
                
                /* remove controles e objetos */
                delete cacheDUploadControl[uuid];
                delete cacheDUploadObj[uuid];
                
                /* remove controles de upload */
                document.getElementById("uploadframe_"+uuid).remove();
                document.getElementById("uploadform_"+uuid).remove();
                
                // atualiza disco
                eoscore.disk.update();
                
                if(eoscore.core.is.function(postFunction)){
                    postFunction.call(this);
                }
            },
            
            /* delete, deleta arquivo */
            delete : function(cod,postFunction){
                console.log("EOS.core.upload.delete");
                
                $.DActionAjax({
                    action : "/sys/upload/DUpload.cgi",
                    req    : "codigo="+cod,
                    serializeForm : false,
                    postFunction: function(x){
                        
                        var r = JSON.parse(x);
                        if(r.type === "error"){
                            $.DDialog({
                                type    : "error",
                                message : r.message
                            });
                            
                        } else {
                            // console.log(r.message);
                            
                            // atualiza disco
                            eoscore.disk.update();
                        }
                        
                        
                        if(eoscore.core.is.function(postFunction)){
                            postFunction.call(this);
                        }
                    }
                });   
            },
            
            /* download */
            download : function(x){
                $.DActionAjax({
                    action : "/sys/upload/DUpload.cgi",
                    req    : "download="+x,
                    type   : "download"
                    // target : "_blank",
                });
            }
        },
        
        /**
         *   Call
         *       carrega modulos
         */
        call : {
            // carrega modulo pelo nome
            module   : {
                // console.log("EOS.core.call.module.mod");
                
                tkt : function(x){
                    console.log("EOS.core.call.module.tkt");
                    
                    if(!x){
                        var x = 1;
                    } else {
                        x = { COD : x };
                    }
                    
                    call("chamado/edit.cgi",x); // carrega modulo
                    DLoad("chamado"); // carrega libs
                },
                tkt_rel : function(x){
                    console.log("EOS.core.call.module.tkt_rel");
                    
                    eos.core.call.exec({
                        action : '/sys/chamado/rel/relatorio.cgi',
                        dload  : 'chamado_relatorio',
                        vars   : '', 
                        postFunction : function(){
                            
                        }
                    });                    
                },
                tkt_rel_prod : function(x){
                    console.log("EOS.core.call.module.tkt_rel_prod");
                    /*
                    if(!x){
                        var x = 1;
                    } else {
                        x = { COD : x };
                    }
                    */
                    eos.core.call.exec({
                        action : '/sys/chamado/rel/relatorio_prod.cgi',
                        dload  : 'chamado_relatorio_prod',
                        vars   : '', 
                        postFunction : function(){
                            
                        }
                    });
                    
                    // call('/chamado/rel/relatorio_prod.cgi', x) // carrega modulo
                    // DLoad("chamado_relatorio"); // carrega libs
                },
                dashboard : function(x){
                    console.log("EOS.core.call.module.dashboard");
                    /*
                    if(!x){
                        var x = 1;
                    } else {
                      //   x = { COD : x };
                    }
                    */
                    
                    eos.core.call.exec({
                        action : '/sys/dashboard/edit.cgi',
                        dload  : 'dashboard',
                        vars   : '',
                        loader : false,
                        postFunction : function(){
                            
                        }
                    });
                    // DLoad("dashboard"); // carrega libs
                    // name='CAD' id='CAD' class="dashboard_form"
                },
                users : function(x){
                    
                    if(x || x === 0){
                        x = { COD : x }
                    } else {
                        var x = '';
                    }
                    
                    eos.core.call.exec({
                        action : '/sys/users/edit.cgi',
                        dload  : 'users',
                        vars   : x,
                        postFunction : function(){
                            
                        }
                    });
                },
                files : function(){
                    eos.core.call.exec({
                        action : '/sys/files/edit.cgi',
                        dload  : 'files',
                        postFunction : function(){
                            
                        }
                    });
                },
                contatos : function(){
                    eos.core.call.exec({
                        action : '/sys/contatos/edit.cgi',
                        dload  : 'contatos',
                        postFunction : function(){
                            
                        }
                    });
                },
                planos : function(x){

                    if(!x){
                        var x = '';
                    } else {
                        x = { COD : x };
                    }
                    
                    eos.core.call.exec({
                        action : '/sys/planos/edit.cgi',
                        dload  : 'planos',
                        vars   : x,
                        postFunction : function(){
                            
                        }
                    });
                },
                produtos : function(x){

                    if(!x){
                        var x = '';
                    } else {
                        x = { COD : x };
                    }
                    
                    eos.core.call.exec({
                        action : '/sys/produtos/edit.cgi',
                        dload  : 'produtos',
                        vars   : x,
                        postFunction : function(){
                            
                        }
                    });
                },
                servicos : function(x){

                    if(!x){
                        var x = '';
                    } else {
                        x = { COD : x };
                    }
                    
                    eos.core.call.exec({
                        action : '/sys/servicos/edit.cgi',
                        dload  : 'servicos',
                        vars   : x,
                        postFunction : function(){
                            
                        }
                    });
                },
                orc : function(x){

                    if(!x){
                        var x = '';
                    } else {
                        x = { COD : x };
                    }
                    
                    eos.core.call.exec({
                        action : '/sys/orc/start.cgi',
                        dload  : 'orc',
                        vars   : x,
                        postFunction : function(){
                            
                        }
                    });
                },
                orc_rel : function(x){

                    if(!x){
                        var x = '';
                    } else {
                        x = { COD : x };
                    }
                    
                    eos.core.call.exec({
                        action : '/sys/orc/rel/start.cgi',
                        dload  : 'orc_rel',
                        vars   : x,
                        postFunction : function(){
                            
                        }
                    });
                },
                checklist : function(x){

                    if(!x){
                        var x = '';
                    } else {
                        x = { COD : x };
                    }
                    
                    eos.core.call.exec({
                        action : '/sys/checklist/edit.cgi',
                        dload  : 'checklist',
                        vars   : x,
                        postFunction : function(){
                            
                        }
                    });
                },
                dadosti : function(x){
                    console.log("EOS.core.call.module.dadosti");
                    
                    if(!x) {
                        x = '';
                    } 
                    
                    eos.core.call.exec({
                        action : '/sys/dadosti/edit.cgi',
                        dload  : 'dadosti',
                        vars   : x,
                        loader : false,
                        postFunction : function(){
                            
                        }
                    });
                },
                default : function(x){
                    console.log("EOS.core.call.module.default");
                    
                    eos.core.call.exec({
                        action : '/sys/default/edit.cgi',
                        dload  : 'default',
                        vars   : { TBL : x },
                        postFunction : function(){
                            // ajusta descricao menu where
                            if(x === "prod_unidade") { console.log(x);
                                eos.menu.where("77",true);
                            } else if(x === "prod_marca") { console.log(x);
                                eos.menu.where("78",true);
                            }
                        }
                    });
                },
                // pagamentos
                pagamento : function(x){
                    console.log("EOS.core.call.module.pagamento");
                    
                    if(!x){
                        x = "";
                    }
                    
                    eos.core.call.exec({
                        action : '/sys/done/pagamento/start.cgi',
                        dload  : 'pagamento',
                        vars   : { empresa : x },
                        postFunction : function(){
                        }
                    });
                },
                verify : function(x){
                    console.log("EOS.core.call.module.verify");
                    
                    eos.core.call.exec({
                        action : '/sys/users/verify.cgi',
                        dload  : 'verify',
                        vars   : '',
                        loader : true,
                        postFunction : function(){
                            
                        }
                    });
                },
                
            }, 
            // carrega modulo por path
            internal : function(){
                console.log("EOS.core.call.module.external");
            },
            // carrega url externa
            external : function(){
                console.log("EOS.core.call.module.external");
            },
            
            /* executa */
            exec : function(settings) { 
                
                // zera conteudos
                $("#main_div").empty();
                $("#main").remove();
                
                flushCache(); // limpa caches
                
                // ajusta variaveis
        		var settings = $.extend({
                    vars   : '',
        			action : '',
        			dload  : '',
                    loader : true,
                    postFunction : false
        		}, settings);

                if(settings.loader) {
                    Loading(settings.dload); // adiciona loader
                }
                
                eos.menu.action.hideAll(); // remove menus
                
        		DMainDiv(); // adiciona Div
		
                // variaveis 
    			settings.vars.ID = $('#AUX [name="ID"]').val();
    			if(!settings.vars.MODO){
    				settings.vars.MODO = $('#AUX [name="MODO"]').val();
                }
                
                DLoad(settings.dload); // carrega libs do modulo
                
    			// carrega modulo
    			$("#main_div").load(settings.action, settings.vars, function(){     
                    // ajusta formulario se nao existir
                    if($("#CAD").length === 0){
                        
                        // $("form").each(function(){ console.log($(this)); console.log($(this).html());
                            
                            // ajusta formulario
                            var form = $("form:first");
                            
                            if(!form.prop("id") && !form.prop("name")){
                                form
                                    .prop({
                                        id     : "CAD",
                                        name   : "CAD",
                                        method : "POST"
                                    })
                                    .addClass(settings.dload+"_form");
                                
                                // cria div para retorno dos ajax (<div id='resultado' class="DDebug"></div>)
                                $("#resultado").remove(); // remove div se existir
                                var resultado = document.createElement("div");
                                    resultado.id = "resultado";
                                    resultado.className = "DDebug";
                                    
                                form.append(resultado); // adiciona ao formulario do modulo
                            }
                            // });
                    }
                    
                    
                    // executa postfunction se for o caso
                    if(eoscore.core.is.function(settings.postFunction)){
                        settings.postFunction.call(this);
                    }
                    
                    unLoading(); // remove loader
                    
                    eoscore.DAction.resize(); // ajusta objetos na tela
                });
            }
        },
        
        
        /**
         *   getList
         *       gera lista key : value from a table
         *       cria cache para uso futuro
         *
         *       **** rever a variavel DListCache para futuro core v3 usando EOS.app
         *
         */
        getList: function(t){
            console.log("EOS.core.getList");
            
            var file = '/sys/cfg/DPAC/DListGet.cgi';
            
            // se gerar apartir de um arquivo
            if(isObject(t)){
                file = document.querySelector('#AUX input[name="MODULO_PATH"]').value+"/"+t.file; // path + file from module
                t    = t.key;
            }
            
            // pega lista do cache
			if(DListCache[t]){
			    return DListCache[t];
			}	
            
            console.log(" no cache ");
            
            // gera cache e lista
            var d = new FormData();
            d.append('ID', $('#AUX input[name="ID"]').val());
            d.append('T', t);
            
            req = new XMLHttpRequest();
            req.open('POST', file, false); 
            req.setRequestHeader('Accept-Encoding', 'application/json');
            req.setRequestHeader('Accept-Charset', 'utf-8');
            req.send(d);
                        
            if(req.status == 200){ // console.log(req.responseText);
                DListCache[t] = JSON.parse(req.responseText);
			    return JSON.parse(req.responseText);
            } else {
				console.log(req);
				return false; 
            }
        },
        
        /**
         *   Time
         *      toSum: converte tempo para calculo
         *      toShow: converte tempo para exibicao (retorna objeto h+m)
         */
        time : {
            toSum : function(t){
                return ( (Number(t.split(':')[0]) * 60) + Number(t.split(':')[1])  );
            },
            toShow : function(t){
                var ct = (t/60).toString();
                
                var m = Number(ct.split('.')[1]) * 0.6;
                if(!m){
                    m = "00";
                } else if(m < 10) {
                    m = m*10;
                }
                
                return {
                    h : Number(ct.split('.')[0]),
                    m : m
                }
            }
        },
        
        /*
        sel : function(x) {
            return document.querySelector(x);
        },
        */
        sel : function(x) {
            return document.querySelectorAll(x);
        },
        selEach : function(q,f,c) {
            [].forEach.call(document.querySelectorAll(q), f, c);
        },
        cache : {
            DUpload : {}
        },
        
        
        /*
        *   Math
        *       funcoes matematicas usadas no eos
        */
        math : {
            /* converte para MB */
            toMB : function(x){
        		var s = $.extend({
                    decimal : 0,
                    value   : x,
        		}, x);
                
                return parseFloat(s.value / 1048576).toFixed(s.decimal);
                // return Math.round(x / 1048576)
                // return Math.round(42715453 / 1048576)
                // parseFloat(42715453 / 1048576).toFixed(2);
            }
        },
        
        /*
        *   IS
        *       testa tipos ex. array / obj / function
        */
        is : {
            /* is Array */
            array : function(obj) {
        	    if(Object.prototype.toString.call(obj) === '[object Array]') {
        		    return true;
        	    }
        	    return false;
            },
            
            /* is Object */
            object : function(obj) {
                if(Object.prototype.toString.call(obj) === '[object Object]') {
                    return true;
                }
                return false;
            },
            
            /* is Function */
            "function" : function(obj) {
                if(typeof obj == 'function') {
                    return true;
                }
                return false;
            },
            
            /* is Number */
            num : function(n) {
                n = parseFloat(toString().replace(/(\,|\.|\ )/g,''));
                
                return !isNaN(parseFloat(n)) && isFinite(n);
            }
            
        },
        
        
        /**
         *   Limit
         *       controle de limites
         */
        limit : {
            
            /**
             *   User
             */
            user : {
                /* inicializa */
                initialize : function(){
                    this.get();            
                },
            
                /* get space total */
                get : function(postFunction){
                    var userlimit = this;
                    
                    $.DActionAjax({
                        action : "/sys/cfg/DPAC/user_limit.cgi",
                        req    : "acao=get",
                        loader : false,
                        serializeForm : false,
                        postFunction: function(x){
                            userlimit.cache = JSON.parse(x);
                            
                            if(eos.core.is.function(postFunction)){
                                postFunction.call(this,userlimit.stats());
                            }
                        }
                    });
                },
        
                /* verifica podera ser adicionado */
                verify : function(x){
            
                    if(this.cache.used >= this.cache.total) { // full
                        return false;
                    }
            
                    return true;  // avaliable
                },
        
                /* atualiza */
                update : function(f){
                    this.initialize();
                },
        
                /* quantidade disponivel */
                stats : function(f){
            
                    /* calculos */
                    var total   = this.cache.total
                      , used    = this.cache.used
                      , percent = parseFloat((used * 100) / total).toFixed(3);
              
                    /* mostra totais */
                    return " usado "+used+" de "+total+" usuários ("+percent+"%) ";
                },    
            
                /* cache */
                cache : {
                    total : "",
                    used  : ""
                }
            },
            
            /**
             *   Empresa
             */
            empresa : {
                /* inicializa */
                initialize : function(){
                    this.get();            
                },
            
                /* get space total */
                get : function(postFunction){
                    var emplimit = this;
                    
                    $.DActionAjax({
                        action : "/sys/cfg/DPAC/emp_limit.cgi",
                        req    : "acao=get",
                        loader : false,
                        serializeForm : false,
                        postFunction: function(x){
                            emplimit.cache = JSON.parse(x);
                            
                            if(eos.core.is.function(postFunction)){
                                postFunction.call(this,emplimit.stats());
                            }
                        }
                    });
                },
        
                /* verifica podera ser adicionado */
                verify : function(x){
            
                    if(this.cache.used >= this.cache.total) { // full
                        return false;
                    }
            
                    return true;  // avaliable
                },
        
                /* atualiza */
                update : function(f){
                    this.initialize();
                },
        
                /* quantidade disponivel */
                stats : function(f){
            
                    /* calculos */
                    var total   = this.cache.total
                      , used    = this.cache.used
                      , percent = parseFloat((used * 100) / total).toFixed(3);
              
                    /* mostra totais */
                    return " usado "+used+" de "+total+" empresas ("+percent+"%) ";
                },    
            
                /* cache */
                cache : {
                    total : "",
                    used  : ""
                }
            }
        }
    };    
    
    
    /*
    *   Disk
    *       funcoes funcionamento do armazenamento
    */
    this.disk = {
        /* inicializa */
        initialize : function(){
            this.get();
            
            $("#eos_disk").click(function(){
                $("#eos_disk_stats").toggleClass("eos_disk_stats_show");
            });
        },
            
        /* get disk space total */
        get : function(){
            var eosdisk = this;
            $.DActionAjax({
                action : "/sys/cfg/DPAC/disk.cgi",
                req    : "acao=get",
                loader : false,
                serializeForm : false,
                postFunction: function(x){
                    eosdisk.cache = JSON.parse(x);
                    eosdisk.stats();
                }
            });
        },
        
        /* verifica se arquivo adicionado podera ser adicionado */
        verify : function(x){
            
            if(this.cache.used >= this.cache.total) {             // disk full 
                return false;
            } else if((this.cache.used + x) > this.cache.total) { // disk not full but no space avaliable
                return (this.cache.total - this.cache.used);
            }
            
            return true;  // space avaliable
    
            
            /* calculos 
            var total   = eoscore.core.math.toMB(this.cache.total)
              , used    = eoscore.core.math.toMB(this.cache.used);
              */
            /*
            $.DActionAjax({
                action : "/cfg/DPAC/disk.cgi",
                req    : "acao=get",
                postFunction: function(x){
                    return x;
                }
            })
            */
        },
        
        /* atualiza */
        update : function(f){
            this.initialize();
        },
        
        /* quantidade de disco disponivel */
        stats : function(f){
            
            /* calculos */
            var total   = eoscore.core.math.toMB(this.cache.total)
              , used    = eoscore.core.math.toMB(this.cache.used)
              , percent = Math.round((used * 100) / total)
              , total_show
              , used_show;
              
            /* ajusta tamanho do uso */
            if(!percent){
                percent = 0;
            }
            $("#eos_disk_total span").text(percent+"%");
            if(percent >= 100){
                percent += 10;
            }
            $("#eos_disk_used").css("width",percent+"%");
            
            /* mostra totais */
            if(used < 1024){
                used_show = used+"MB";
            } else {
                used_show = used / 1024;
                used_show += "GB";    
            }
            
            if(total < 1024){
                total_show = total+"MB";
            } else {
                total_show = total / 1024;
                total_show += "GB";
            }
            
            $("#eos_disk_stats").html("<span> "+used_show+" ("+total_show+")</span>");
            
            /* ajusta cor pelo uso */
            $("#eos_disk_used, #eos_disk_stats").removeClass("eos_disk_used_mid eos_disk_used_heavy");
            if(percent > 75) {
                $("#eos_disk_used, #eos_disk_stats").addClass("eos_disk_used_heavy");
            } else if(percent > 30 && percent <= 75) {
                $("#eos_disk_used, #eos_disk_stats").addClass("eos_disk_used_mid");
            }                     
        },    
            
        /* cache do disco */
        cache : {
            total : "",
            used  : ""
        }
    };
};

// add for each para objetos vindo do querySelector
NodeList.prototype.forEach = function (fn, scope) {
    'use strict';
    var i, len;
    for (i = 0, len = this.length; i < len; ++i) {
        if (i in this) {
            fn.call(scope, this[i], i, this);
        }
    }
};

/*
    [].forEach.call(document.querySelectorAll('.awsome'), function(el){
        console.log(el);
    });
*/
// add for each para objetos arrays
Array.prototype.forEach = function (fn, scope) {
        'use strict';
        var i, len;
        for (i = 0, len = this.length; i < len; ++i) {
            if (i in this) {
                fn.call(scope, this[i], i, this);
            }
        }
    };

