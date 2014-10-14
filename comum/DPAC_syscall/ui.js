// document.writeln("<link rel='stylesheet' type='text/css' href='/css/comum/ui.css'>");
// document.writeln("<link rel='stylesheet' type='text/css' href='/css/ui.css'>");

var sys_nome = "Done Webcontacts"; // nome do sistema, usado nas telas de alerta #ui_sys_name. ver init.pl variavel $sys_nome
var rememberPositionedInCookie = false;
var rememberPosition_cookieName = 'ui';

inc('/comum/dragable-content.js');

messageObj = new DHTMLSuite.modalMessage();
messageObj.setWaitMessage('Carregando...');
messageObj.setShadowOffset(10);

DHTMLSuite.commonObj.setCssCacheStatus(true);



/* [INI] Modal Window Padrao  (by akgleal.com) ------------------------------------------------------------------------------------ 
	Dependencias:
		/css/comum/ui.css 
		/css/ui.css
		
	CSS necessarios:
		.ui_frame { }
		.ui_box { }
		.ui_title { }
		.ui_btn_bar { }
		.ui_msg { }
		
	Opcoes:
		this.setTitle('txt') = { titulo do modal }
		this.setBtn('btns html') = { Botoes do modal }
		this.setMsg('txt') = { mensagem de exibicao }
		this.setSize(width,height) = { largura e altura }
		
	Exemplo de uso:
		// botoes ajusta exibicao
		btns = "<div id='btn_yes' class='ui_btn' onClick='closeMsg("+yes+")'><div class='ui_btn_container'><div class='ui_btn_title'><nobr>Sim</nobr></div></div></div>";
		btns += "<div id='btn_no' class='ui_btn' onClick='closeMsg("+no+")'><div class='ui_btn_container'><div class='ui_btn_title'><nobr>Não</nobr></div></div></div>";

		// Modal, cria janela
		box = new modalWin();
		box.setTitle("Confirmação");
		box.setSize(200,100);
		box.setBtn(btns);
		box.setMsg(msg);
		box.show();
*/
function modalWin()
	{
	var title = "";
	var btn = "";
	var msg = "";
	
	this.setTitle = function(val){ title = val; }
	this.setBtn = function(val){ btn = val; }
	this.setMsg = function(val){ msg = val; }
		
	this.show = function()
		{
		box =  "<div class='dragableElement'>";
		box += "	<div class='ui_frame'>";
		box += "		<div class='ui_title'><div id='ui_sys_name'>["+sys_nome+"] "+title+"</div></div>";		
		box += "		<div class='ui_box'>";
		box += "			<div class='ui_btn_bar' align='center'>"+btn+"</div>";
		box += "			<div class='ui_msg'>"+msg+"</div>";
		box += "		</div>";
		box += "	</div>";
		box += "</div>";
		}
	}
/* [END] Modal Window Padrao  (by akgleal.com) ------------------------------------------------------------------------------------ */

/* [INI] Close, Modal  ---------------------------------------------------------------------------------------------------------- */
function closeMsg(action)
	{
	messageObj.close();
	if(action)
		{
		eval(action);
		}
	}
/* [INI] Close, Modal  ---------------------------------------------------------------------------------------------------------- */

/* [INI] Alerta, Modal  ---------------------------------------------------------------------------------------------------------- */
function alerta(msg, action)
	{
	// mensagem ajusta exibicao
	msg = msg.replace(/\n/,"<br>");
	msg = msg.replace("<nobr>","");
	msg = msg.replace("</nobr>","");
	
	// botoes ajusta exibicao
	btns = "<div id='btn_yes' class='ui_btn' onClick='closeMsg("+action+")'><div class='ui_btn_container'><div class='ui_btn_title'><nobr>OK</nobr></div></div></div>";
	
	// Modal, cria janela
	box = new modalWin();
	box.setTitle("Aviso");
	box.setBtn(btns);
	box.setMsg(msg);
	box.show();
	
	messageObj.setHtmlContent(box);
	messageObj.setSize(350,100);
	messageObj.setCssClassMessageBox('ui_alerta');
	messageObj.setSource(false);
	messageObj.setShadowDivVisible(false);	
	messageObj.display();
	// document.getElementById('btn_ui_ok').focus();
	initdragableElements();
	}

function alertaCheck(msg, action)
	{
	if(msg.indexOf("\n"))
		{
		msg = msg.replace(/\n/,"<br>");
		}

	box = "<div class='dragableElement' style='top:-10%'><div class='ui_frame'><div class='ui_title'>Multiplos Cadastros</div>";
	box += "<div class='ui_box'>";
	box += "<div style='width: 80%;'><table border=0 style='min-width: 10%; max-width: 100%;' align=center><tr><td align=left style='padding-right: 10px'>";
	box += msg;
	box += "</td></tr></table></div><br clear=both><div class='ui_buttons'>";
	box += "<center><div id='btn_default'><input type='button' id='btn_ui_ok' value='Cancelar' onClick='closeMsg("+action+")'></div></center>"; 
	box += "</div></div></div>";
	
	messageObj.setHtmlContent(box);
	messageObj.setSize(350,100);
	messageObj.setCssClassMessageBox('ui_alerta');
	messageObj.setSource(false);
	messageObj.setShadowDivVisible(false);	
	messageObj.display();
	
	// document.getElementById('btn_ui_ok').focus();
	
	initdragableElements();
	}
/* [END] Alerta, Modal  ---------------------------------------------------------------------------------------------------------- */

/* [INI] Confirmacao, Modal  (by akgleal.com) ---------------------------------------------------------------------------------------
	Dependencias:
	CSS necessarios:
	Opcoes:
	Exemplo de uso:
*/
function confirma(msg, yes, no)
	{
	// modo de compatibilidade com antigo modal
	if(msg)
		{
		if(!yes){ yes = ""; }
		if(!no){ no = ""; }
		confirma_old(msg, yes, no);
		return false;
		}
		
	/*
	var modal  = '<div id="dialog-confirm" title="Empty the recycle bin?">';
		modal += '<p><span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 20px 0;"></span>These items will be permanently deleted and cannot be recovered. Are you sure?</p>';
		modal += '</div>';
	*/
	box =  "<div id='dialog-confirm' title='Confirmação'>";
	// box += "	<div class='ui_frame'>";
	// box += "		<div class='ui_title'><span id='ui_sys_name'>"+sys_nome+":</span> </div>";		
	box += "		<div class='ui_box'>";
	box += "			<div class='ui_btn_bar' align='center'>";
	box += "				<div id='btn_yes' class='ui_btn' onClick='$(\"#dialog-confirm\").dialog(\"destroy\");'><div class='ui_btn_container'><div class='ui_btn_title'><nobr>OK</nobr></div></div></div>";
	box += "			</div>";
	box += "			<div class='ui_msg'> TESTE";
 	box += "			</div>";
	box += "		</div>";
	// box += "	</div>";
	box += "</div>";
		
	$("body" ).append(box);
	
		// $( "#dialog-confirm:ui-dialog #dialog-confirm:ui_btn_bar #dialog-confirm:ui_msg" ).dialog( "destroy" );
		$("#dialog-confirm:ui-dialog").dialog( "destroy" );
		
				$( "#dialog-confirm" ).dialog({
					resizable: false,
					height:180,
					width:450,
					modal: true,
					buttons: false
				});
				
		$( "#dialog-confirm" ).removeClass("ui-widget-header");
	
	}

// Confirma, modal antigo  ------------------------------------------------------------------------- 
function confirma_old(msg, yes, no)
	{
	// mensagem ajusta exibicao
	msg = msg.replace(/\n/,"<br>");
	msg = msg.replace("<nobr>","");
	msg = msg.replace("</nobr>","");
	
	// botoes ajusta exibicao
	btns = "<div id='btn_yes' class='ui_btn' onClick='closeMsg("+yes+")'><div class='ui_btn_container'><div class='ui_btn_title'><nobr>Sim</nobr></div></div></div>";
	btns += "<div id='btn_no' class='ui_btn' onClick='closeMsg("+no+")'><div class='ui_btn_container'><div class='ui_btn_title'><nobr>Não</nobr></div></div></div>";
	
	// Modal, cria janela
	box = new modalWin();
	box.setTitle("Confirmação");
	box.setBtn(btns);
	box.setMsg(msg);
	box.show();
		
	messageObj.setHtmlContent(box);
	messageObj.setSize(400,100);
	messageObj.setCssClassMessageBox('ui_alerta');
	messageObj.setSource(false);
	messageObj.setShadowDivVisible(false);	
	messageObj.display();
	// document.getElementById('btn_no').focus();
	initdragableElements();
	}
/* [END] Confirmacao, Modal  (by akgleal.com) --------------------------------------------------------------------------------------- */

function abre(title, msg, width, height)
	{
	var rememberPositionedInCookie = true;
	var rememberPosition_cookieName = 'ui_abre';
	
	if(msg.indexOf("\n"))
		{
		msg = msg.replace(/\n/,"<br>");
		}

	box  = "<div id='dragMe' class='dragableElement' style='width:"+width+"px; height:"+height+"px;'><div class='ui_frame'>";
	box += "  <div class='ui_title'>"+title;
	box += "    <div style='float: right; margin-top: -5px;'><a href='javascript:closeMsg()'><img src='/img/ui/close.png' border=0></a></div>";
	box += "  </div>";
	box += "  <div class='ui_box2'>";
	box +=      msg;	
	box += "  </div>";
	box += "</div></div>";
		
	messageObj.setHtmlContent(box);
	messageObj.setSize(width,height);
	messageObj.setCssClassMessageBox('ui_alerta');
	messageObj.setSource(false);
	messageObj.setShadowDivVisible(false);
	messageObj.display();
	initdragableElements();
	}
	
function login_run(dest)
	{
	req = $("#logon").serialize();
	top.main.login_run(dest, req);
	}
	
function login(title, msg, dest, width, height)
	{
	if(msg.indexOf("\n"))
		{
		msg = msg.replace(/\n/,"<br>");
		}

	msg = "<form name='logon' id='logon' method='post' onSubmit='login_run(\""+dest+"\"); return false;'>"+msg+"</form>";

	box = "<div id='dragMe' class='dragableElement' style='width: "+width+"px; height: "+height+";'><div class='ui_frame' style='height: 340px'><div class='ui_title'>Relogin</div>";
	box += "<div class='ui_box' style='height: 320px'>";
	box += "<div style='width: 100%'><table border=0 style='min-width: 10%; max-width: 100%;' align=center><tr><td align=left>";
	box += msg;
	box += "</td></tr></table></div><br clear=both>";
	box += "</div></div>";	
	
		
	messageObj.setHtmlContent(box);
	messageObj.setSize(width,height);
	messageObj.setCssClassMessageBox('ui_alerta');
	messageObj.setSource(false);
	messageObj.setShadowDivVisible(false);
	messageObj.display();
	initdragableElements();
	if(document.getElementById('USUARIO').value != '')
		{
		try
			{
			document.getElementById('SENHA').focus();
			}
		catch(err)
			{
			// ignora erro
			}
		}
	else
		{
		try
			{
			document.getElementById('USUARIO').focus();
			}
		catch(err)
			{
			// ignora erro
			}
		}
	}

function carrega(pag, width, height)
	{
	messageObj.setSize(width,height);
	messageObj.setSource(pag);
	messageObj.setShadowDivVisible(false);
	messageObj.display();
	initdragableElements();
	}

function inc(arquivo)
	{
	//By Anônimo e Micox - http://elmicox.blogspot.com
	var novo = document.createElement("script");
	novo.setAttribute('type', 'text/javascript');
	novo.setAttribute('src', arquivo);
	document.getElementsByTagName('head')[0].appendChild(novo);
	//apos a linha acima o navegador inicia o carregamento do arquivo
	//portanto aguarde um pouco até o navegador baixá-lo. :)
	}
