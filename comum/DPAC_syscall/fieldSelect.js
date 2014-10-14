/* [INI]  SELECT field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	<script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery.ui.selselect.js"></script>
	
	CSS necessario:
	.fieldSelect { definicoes necessarias para uso }

    Opcoes:
	setStyle(style) => ajusta o comportamento do select
	
	Exemplo de uso: 
	  Uso com array vindo do banco:
		opt_arr = new Array (['1','Select 1'],['2','Select 2']);
		campo_select = new fieldSelect("campo_select", opt_arr);
		<select name="campo_select" id="campo_select"></select>	
	  Uso com <option> setada no html:
		campo_select = new fieldSelect("campo_select");
		<select name="campo_select" id="campo_select"><option value=1>Select 1</option><option value=2>Select 2</option></select>
		
	var campoSelect = new fieldSelect("campo_select","array_se_necessario");
	<select name="campo_select" id="campo_select"></select>
	
	Todo:
	adicionar outras opcoes de select com imagens e grupos
*/

// dependencias
include("/comum/DPAC_syscall/jquery/jquery.ui.selectmenu.js"); 

function fieldSelect(field,opt)
	{
	var stl = 'dropdown'; // estilo padrao do select
	
	// funcoes config
	this.setStyle = function(val) { stl = val; }
		
	// cria campo
	this.show = function()
		{
		// options via array (metodo novo)
		if(opt)
			{
			for(var i in opt)
				{
				$('#'+field).append("<option value='"+opt[i][0]+"'>"+opt[i][1]+"</option>");
				}
			}
			
		// cria select
		$('#'+field).selectmenu(
			{
			style:stl
			});
		}
	
	// desabilita campo
	this.disable = function(v)
		{
		$('#'+field).selectmenu("disable");
		fieldOptDisable(field);
		
		// esconde campo
		if(v)
			fieldOptHide(field);
		}
		
	// habilita campo
	this.enable = function()
		{
		$('#'+field).selectmenu("enable");
		fieldOptEnable(field);
		
		// mostra campo
		fieldOptShow(field);
		}		
	
	// troca o valor
	this.setValue = function(val)
		{
		alert(val);
		$('#'+field).selectmenu('value', val);
		}
	
	// retorna select campo pronto
	if(!opt)
		return this.show();
	}
/* [END]  SELECT field (by akgleal.com)  ------------------------------------------------------------------------- */
