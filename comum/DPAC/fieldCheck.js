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