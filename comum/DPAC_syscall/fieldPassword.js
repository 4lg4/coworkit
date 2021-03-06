/* [INI]  Password field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	
	CSS necessario:
	.fieldPassword { }
	.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:
	
	Exemplo de uso:
	var campoNumber = new fieldNumber("campo_number");
	campoNumber.setSize(10);
	<input type="text" id='campo_number' name='campo_number'>
	
	var campoNumber = new fieldNumber("campo_number","10");
	<input type="text" id='campo_number' name='campo_number'>
*/

function fieldPassword(field) 
	{
	// cria campo
	this.show = function()
		{		
		// seta campo
		$('#'+field)
			.addClass("fieldPassword")
			.attr({
				'type' : 'password',
				'alt' : 'password', 
				'autocomplete' : 'off'})
			.addClass("fieldPassword")
			.setMask(); 
		}
	
	// define tamanho
	this.size = function(size){ fieldOptSize(field,size); };
	
	// desabilita campo
	this.disable = function(){ fieldOptDisable(field); };

	// habilita campo
	this.enable = function(){ fieldOptEnable(field); };
	
	// quando sai do campo executa funcao
	this.blur = function(func){ fieldOptBlur(field,func) };
	
	// auto complete do navegador
	this.autoComplete = function(opt)
		{
		if(!opt) opt = 'off';
		fieldAutoComplete(field,opt) 
		};
		
	// retorna campo pronto
	return this.show();
	}
/* [END]  Password field (by akgleal.com)  ------------------------------------------------------------------------- */
