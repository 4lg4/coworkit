/* [INI]  NUMBER field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	<script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery.meiomask.js"></script> (arquivo modificado por akgleal.com)
	
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
*/
include("/comum/DPAC_syscall/jquery/jquery.meiomask.js");

function fieldNumber(field,size) 
	{
	// ajusta o tamanho minimo de caracteres do campo
	if(!size)
		size = 1;
		// $('#'+field).size(size)
	
	// cria campo
	this.show = function()
		{
		// seta campo
		$('#'+field)
			.addClass("fieldNumber")
			.attr({
				'alt' : 'number', 
				'autocomplete' : 'off',
				'maxlength' : size 
				})
			.setMask(); 
		}

	// define tamanho
	this.size = function(s){ fieldOptSize(field,s); };
	
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
/* [END]  NUMBER field (by akgleal.com)  ------------------------------------------------------------------------- */
