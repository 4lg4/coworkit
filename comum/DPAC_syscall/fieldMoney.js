
/* [INI]  MONEY field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
		price_format.js
	
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

// dependencias
include("/comum/DPAC_syscall/jquery/price_format.js"); 

function fieldMoney(field,fast) 
	{
	var prefix_show = false; // mostra ou nao prefixo
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
	this.enable = function(v)
		{
		$('#'+field)
		.removeClass("fieldDisable")
		.attr("readonly", false);
		
		// set focus
		// if(v)
		// $('#'+field)
		//	a.focus();
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
