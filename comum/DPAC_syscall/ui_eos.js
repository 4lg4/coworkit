var sys_nome = "EOS"; // nome do sistema, usado nas telas de alerta #ui_sys_name. ver init.pl variavel $sys_nome

/* [INI] Modal Window Padrao  (by akgleal.com) ------------------------------------------------------------------------------------ 
	Dependencias:
		/css/comum/ui.css 
		/css/ui.css
		/comum/DPAC.js
		
	CSS necessarios:
		.ui_frame { }
		.ui_box { }
		.ui_title { }
		.ui_btn_bar { }
		.ui_msg { }
		
	Opcoes:
		setTitle('txt') = { titulo do modal }
		setBtn('btns html') = { Botoes do modal }
		setMsg('txt') = { mensagem de exibicao }
		setSize(width,height) = { largura e altura }
		show(); // mostra obj
		
	Exemplo de uso:

		// Modal, cria janela
		box = new modalWin();
		box.setTitle("Confirmação");
		box.setSize(200,100);
		box.setBtn("Sim",funcao);
		box.setMsg(msg);
		box.show();
*/
function modalWin()
	{
	// variaveis
	var title = "";
	var Width = "300";
	var Height = "200";
	var btn = {};
	var msg = "";
	
	// titulo
	this.setTitle = function(val)
		{ 
		title = val; 
		}
	
	// tamanho 
	this.setSize = function(w,h)
		{
		Width = w;
		Height = h;
		}
	
	// botoes, adiciona
	this.setBtn = function(descrp,act)
		{
		// se acao vier vazio adiciona Botao somente com dialog remove
		if(!act)
			{
			btn[descrp] = function() 
				{
				$("#warning_box").remove(); 
				};
			}
		else
			{
			btn[descrp] = function() 
				{ 
				eval(act); 
				$("#warning_box").remove(); 
				};
			}
		}
		
	// mensagem
	this.setMsg = function(val)
		{ 
		msg = val; 
		}
	
	// exibe modal	
	this.show = function()
		{		
		box = "	<div id='warning_box' title='"+sys_nome+" - "+title+"'>";
		box += "	<div class='ui_msg'>"+msg+"</div>";
		box += "</div>";
		
		$("body").append(box);
		
		$("#warning_box").dialog(
			{
			modal: true,
			closeOnEscape: false,
			buttons: btn,
			minWidth: Width,
			minHeight: Height
			});			
		}
	}
/* [END] Modal Window Padrao  (by akgleal.com) ------------------------------------------------------------------------------------ */


/* [INI] Alerta, Modal  ---------------------------------------------------------------------------------------------------------- */
function alerta(msg, act)
	{
	if(!act)
		act = "";

	// mensagem ajusta exibicao
	msg = msg.replace(/\n/,"<br>");
	msg = msg.replace("<nobr>","");
	msg = msg.replace("</nobr>","");
	
	// Modal, cria janela
	box = new modalWin();
	box.setTitle("Aviso");
	box.setBtn("OK",act);
	box.setMsg(msg);
	box.show();	
	}
/* [END] Alerta, Modal  ---------------------------------------------------------------------------------------------------------- */

/* [INI] Confirmacao, Modal  (by akgleal.com) ------------------------------------------------------------------------------------ */
function confirma(msg, yes, no)
	{
	if(!yes)
		yes = "";
	if(!no)
		no = "";
		
	// Modal, cria janela
	box = new modalWin();
	box.setTitle("Confirmação");
	if(yes)
		box.setBtn("Sim",yes);
	box.setBtn("Não",no);
	box.setMsg(msg);
	box.show();
	}
/* [END] Confirmacao, Modal  (by akgleal.com) --------------------------------------------------------------------------------------- */

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

	// Modal, cria janela
	box = new modalWin();
	box.setTitle("Relogin");
	box.setBtn("Login","");
	box.setMsg(msg);
	box.show();
		
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
