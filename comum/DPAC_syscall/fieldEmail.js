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
				if($('#'+field).val() != "")
					if(!isMail($('#'+field).val())) 
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
