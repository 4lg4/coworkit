(function($, window){
	
$.extend(
	{
	DDialog: function(settings)
		{
		var settings = $.extend(
			{
			type         : 'alerta',    // tipos de  alerta / alert / confirma / confirm 
			title        : false,       // titulo da janela
			message      : 'Teste: Janela de Dialogo',
			modal        : true,        // Screen Block
			focusBack    : false,       // objeto que criou o modal para retorno do foco
			postFunction : false,       // executa funcao apos o fechamento do botao
			minWidth     : "300",       // tamanho minimo do dialog
			minHeight    : "200",       // tamanho minimo do dialog
			btnOK        : false,       // funcao do botao OK
			btnYes       : false,       // funcao do botao Yes
			btnNo        : false,       // funcao do botao No
			img          : false,       // mostra imagem de fundo (usado em campanhas)
			closeEsc     : false,       // fecha box com esc
			resizable    : true,
			draggable    : true,
			/*
			btnCustom : [
						{ text: "OK", click: function() { alert("OK"); }},
						{ text: "NO", click: function() { alert("NO"); }}
						],
			*/
			}, settings);		
				
		settings.id = "DDialog_"+$(".DDialog_box").length+1; //id unico
		// settings.id = "DDialog";
		
		// mensagem ajusta exibicao
		// msg = msg.replace(/\n/,"<br>");
		// msg = msg.replace("<nobr>","");
		// msg = msg.replace("</nobr>","");
		switch(settings.type.lc())
			{
			case "alerta":
			case "alert":
            case "error":
            case "erro":
                
				// titulo do dialog
				if(settings.title === false && (settings.type.lc() === "alert" || settings.type.lc() === "alerta")) {
					settings.title = 'Aviso';
				} else if(settings.title === false) {
				    settings.title = 'Erro';
				}
					
				// botoes 
				settings.buttons = [
					// botao OK
					{ 
					text: "OK", 
					click: function() 
						{
						// funcao OK executa
						if(isFunction(settings.btnOK)) {
							settings.btnOK.call(this);
                        }
						
						// post Function, executa
						if(isFunction(settings.postFunction)){
							settings.postFunction.call(this);
                        }
							
						// remove dialog
						$("#"+settings.id).remove();
							
						// ajusta foco no campo desejado
						if(settings.focusBack !== false)
							settings.focusBack.focus();
						}
					}
				];					
			break;
			
			case "confirm":
			case "confirma":
				// titulo do dialog
				if(settings.title === false)
					settings.title = 'Confirma';
					
				// botoes
				settings.buttons = 
					[
					// botao YES
						{ 
						text: "SIM", 
						click: function() 
							{
							// funcao Yes executa
							if(isFunction(settings.btnYes))
								settings.btnYes.call(this);
							
							// remove dialog
							$("#"+settings.id).remove();
							
							// post Function, executa
							if(isFunction(settings.postFunction))
								settings.postFunction.call(this);
								
							// ajusta foco no campo desejado
							if(settings.focusBack !== false)
								settings.focusBack.focus();
							}
						},
					// botao NO
						{ 
						text: "NÃO", 
						click: function() 
							{
							// funcao NO executa
							if(isFunction(settings.btnNo))
								settings.btnNo.call(this);
								
							// remove dialog
							$("#"+settings.id).remove();
							
							// post Function, executa
							if(isFunction(settings.postFunction))
								settings.postFunction.call(this);
								
							// ajusta foco no campo desejado
							if(settings.focusBack !== false)
								settings.focusBack.focus();
							}
						}
					];
			break;
			}
		
		
		
		// remove modal se for reescrever
		// $(".DDialog_box").remove(); 
		$("#"+settings.id).remove();
		
		// imagem
		if(settings.img !== false)
			{
			settings.message = "<div class='DDialog_img' style='width:100%; height:"+($(window).height()-100)+"px; overflow:auto;'><img src='"+settings.img+"'></div>";
			}
		
		// caixa de dialogo
		settings.dialog  = "<div id='"+settings.id+"' title='"+settings.title+"' class='DDialog_box'>";
		settings.dialog += "		<div class='DDialog_box'>"+settings.message+"</div>";
		settings.dialog += "</div>";
		
		// adiciona html da caixa de dialogo
		$("body").append(settings.dialog);
		
		
		// imagem
		if(settings.img !== false)
			{
			settings.minWidth = $(".DDialog_img").width() - settings.minWidth;
			settings.minHeight = $(window).height()-50;
			settings.closeEsc = true;
			settings.resizable = false;
			settings.draggable = false;
			}
			
		// adiciona dialogo
		$("#"+settings.id).dialog(
			{
			modal: settings.modal,
			closeOnEscape: settings.closeEsc,
			buttons: settings.buttons,
			minWidth: settings.minWidth,
			minHeight: settings.minHeight,
			maxHeight: $(window).height(),
			resizable: settings.resizable,
			draggable: settings.draggable,
			// width: 'auto',
			open: function( event, ui ) 
				{
				var e = $(this);
				/*
				var e = $(this);
				
				console.log(event);
				console.log(ui);
				console.log($(this));
				console.log($(this).prop("id"));
				console.log($(this).html());
				console.log($(this).parent().html());
				*/
				// imagem
				if(settings.img !== false)
					{
					$(".ui-dialog-buttonpane").hide();
					e.css("width","100%");
					// $("#"+settings.id).removeClass(".ui-dialog .ui-dialog-content");
					// e.css("width","100% !important");
					// $(".DDialog_box .ui-dialog-content").css("height","100% !important");
					// $(".DDialog_box .ui-dialog-content").css("overflow","auto");
					
					// close on click anywhere
					$('.ui-widget-overlay').click(function()
						{
						e.dialog('close');
						});
					}
				}
			});
		}
		
	// funcao after click
	/*
	DDialogAfterClick: function(settings)
		{
		// remove dialog
		obj.remove();
	
		// post Function, executa
		if(isFunction(settings.postFunction))
			settings.postFunction.call(this);
		
		// ajusta foco no campo desejado
		if(settings.focusBack !== false)
			settings.focusBack.focus();
		};
	*/
	});
	
})(jQuery, this);


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
	var loader = "";
	
	// remove modal
	this.close = function()
		{ 
		$("#warning_box").remove();
		}
	
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
				
				// esconde easter egg eos
				// $('#loader_eos').hide();
				};
			}
		else
			{
			btn[descrp] = function() 
				{ 
				if(isFunction(act))
					act.call(this);
				else
					eval(act);
					
				$("#warning_box").remove();
				
				// esconde easter egg eos
				// $('#loader_eos').hide();
				};
			}
		}
		
	// mensagem
	this.setMsg = function(val)
		{ 
		msg = val; 
		}
	
	// loader, adiciona barra de carregamento
	this.setLoader = function()
		{
		loader = "";
		// loader = "<div id='warning_box_loader' style='border:1px solid red; width:80%;  height:30px;'></di>";
		}
		
	// exibe modal	
	this.show = function()
		{
		// mostra easter egg eos
		// $('#loader_eos').show();
		
		// remove modal se for reescrever
		$("#warning_box").remove(); 
		
		box = "	<div id='warning_box' title='EOS - "+title+"'>";
		box += "	<div class='ui_msg'>"+msg+"</div>";
		box += loader;
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
			
		// loader
		// if(loader != "")
			// $("#warning_box_loader").progressbar({ value: false });
		}
	}

// remove modal
function modalWinClose()
	{ 
	$("#warning_box").remove();
	}
/* [END] Modal Window Padrao  (by akgleal.com) ------------------------------------------------------------------------------------ */


/* [INI] Alerta, Modal  ---------------------------------------------------------------------------------------------------------- 
*
*	
-------------------------------------------------------------------------------------------------------------------------------- */

function alertaClose()
	{
	modalWinClose();
	}
// adiciona barra de carregamento ao alerta
function alertaLoading(msg, act)
	{
	if(!act)
		act = "";
		
	alerta(msg,act,1);
	}
	
function alerta(msg, act, loader)
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
	if(loader)
		box.setLoader();
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

function confirmaClose()
	{
	modalWinClose();
	}
/* [END] Confirmacao, Modal  (by akgleal.com) --------------------------------------------------------------------------------------- */

