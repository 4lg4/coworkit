/* [INI]  Menu Actions (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	
		
	CSS necessario:
	

    Opcoes:
	
	
	
	Exemplo de uso:
	var menu = new menu("campo_number");
	campoNumber.setSize(10);
	<input type="text" id='campo_number' name='campo_number'>
	
	
	Criar funcoes para click e 2 clicks
	function gridClick(x)
		{
		alert("Click - "+x);
		}

	function gridDblClick(x)
		{
		alert("DBL Click - "+x);
		}
	
*/

function ac_show(x) 
	{ 
	// Mantem suporte a versao antiga da funcao
	$(".menu_btn_control").hide();
	
	for(var i in icon)
		$("#"+icon[i]).show();
		
	console.log(x);
	}
function menu(array)
	{
	// mostra somente icone solicitado
	this.btnShow = function(icon)
		{
		// suporte a array para mostrar icones
		if(typeof icon == 'string')
			$("#"+icon).show();
		else
			for(var i in icon)
				$("#"+icon[i]).show();
		return;
		}
	// mostra todos icones
	this.btnShowAll = function()
		{
		$(".menu_btn_control").show();
		return;
		}	
	// esconde somente icone solicitado
	this.btnHide = function(icon)
		{
		// suporte a array para esconder icones
		if(typeof icon == 'string')
			$("#"+icon).hide();
		else
			for(var i in icon)
				$("#"+icon[i]).hide();
		return;
		}
	// esconde todos icones
	this.btnHideAll = function()
		{
		$(".menu_btn_control").hide();
		return;
		}
	
	// cria icone
	this.btnNew = function(id,title,func,subtitle,clas)
		{
		// percorrer por todos id e testar se botao gerado em tempo de execucao nao conflita com outros
		// $(".menu_btn").each() 
		// if(this.id == id)
		menu_btn_title = "";
		menu_btn_title_sub = "";
		
		if(!subtitle) 
			subtitle = "";
		if(!clas)
			clas = "";
			
		// ajusta tamanho fonte na descricao principal	
		if(title.length >= 7 && title.length <= 8)
			menu_btn_title = 'font-size:10px; margin-bottom:1px;';
		else if(title.length >= 9)
			menu_btn_title = 'font-size:9px; margin-bottom:1px;';
			
		// ajusta borda da sub descricao
		if(subtitle == "")
			menu_btn_title_sub = 'border:none; ';
			
		// ajusta tamanho fonte na descricao principal
		if(subtitle.length > 8)
			menu_btn_title_sub += 'font-size:9px;';
			
		$("#menu_actions").append('<div class="menu_btn menu_btn_control '+clas+'" id="'+id+'" onClick="'+func+'"><div class="menu_btn_container"><div class="menu_btn_title_sub" style="'+menu_btn_title_sub+'"><nobr>'+subtitle+'</nobr></div><div class="menu_btn_title" style="'+menu_btn_title+'"><nobr>'+title+'</nobr></div></div></div>');
		return;
		}
	
	// Mantem suporte a versao antiga da funcao
	$(".menu_btn_control").hide();

	if(array)
		{
		// suporte a array para montar menu
		if(typeof icon == 'string')
			$("#"+icon).show();
		else
			for(var f in array)
				$("#"+array[f]).show();
		}
	}
