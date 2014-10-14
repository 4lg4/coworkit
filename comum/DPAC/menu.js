/* [INI] MENU Actions ------------------------------------------------------------------------------------------------------------------
	
	ac_show, Gera Menu Actions


*/
// compatibilidade com syscall remover esta funcao apos toda migracao
function ac_show(x) 
	{ 
	// Mantem suporte a versao antiga da funcao
	$(".menu_btn_control").hide();
	
	for(var i in x)
		$("#"+x[i]).show();		
	}
	
	
function menu(array)
	{
	// mostra somente icone solicitado
	this.btnShow = function(icon)
		{ 
		// suporte a array para mostrar icones
		if(typeof icon == 'string')
			$("#"+icon).fadeIn('fast');
		else
			{
			// $(".menu_btn_control").hide();
			
			for(var i in icon)
				$("#"+icon[i]).fadeIn('fast');
			}
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
        /*
		// percorrer por todos id e testar se botao gerado em tempo de execucao nao conflita com outros
		$(".menu_btn").each(function()
			{ 
			if($(this).attr("id") == id)
				{
				$(this).remove();
				}
			});
        */
        
		// remove botao se existir
		if($("#"+id).length > 0){
			$("#"+id).remove();
		}
        
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
			
		$("#menu_actions").append('<div class="menu_btn menu_btn_control '+clas+'" id="'+id+'" onClick="'+func+'"><div class="menu_btn_container"><div class="menu_btn_title_sub" style="'+menu_btn_title_sub+'">'+subtitle+'</div><div class="menu_btn_title" style="'+menu_btn_title+'">'+title+'</div></div></div>');
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
	

/* menu where am i */
function menu_whereami(x,func,home)
	{ // alert(MENU_WHEREAMI[x]);
	// traducao - DPAC/translate.js
	// MENU_WHEREAMI[x];
	
	// seta o home
	if(home)
		{
		var descrp  = '<a onClick=\"'+func+'; menu_whereami();\"><img src="/img/ui/menu_home.png" align="absmiddle"></a>';
		$('#menu_top_home').html(descrp);
		func = ""; 
		x = "";
		}
	
	if(!x)
		{ 
		func = ""; 
		x = ""; 
		}
		
	var descrp  = '<a onClick=\"'+func+'\">'+x+'</a>';
	// descrp += '	<div class="menu_top_modules menu_top_modules_opt">'+x+'</div>';
					
	$('#menu_top_modules').html(descrp);
	
	return;
	
	}
	
function shmenu(x)
	{
	// if(bloqueado == true)
	//	{
	//	unblock();
	//	}
	// else
	//	{
		if(x == menu_sel)
			{
			/*
			if(menu_bloqueado == false)
				{
				clean_menu();
				return true;
				}
			*/
			}
		else
			{
			// block_menu(true);
			// $('.corpo_blk').fadeIn('fast', function() { $('.corpo').animate({top: '300px'}, 300); block_menu(false); }).animate({top: '300px'}, 300);
			// $('.head_blk').fadeIn('fast');
			$('.menu').hide();
			$('.menu_selected').removeClass();
			menu_sel = x;
			$(x).show();
			}
	//	}
	}

/* menu where am i */
function menuWhere(menu)
	{ 
	// executa menu selecionado
	MENUSER[menu].acao();
	
	
	// seta o home
	if(menu == "home")
		{
		var home  = '<a onClick="menuWhere(\'home\');"><img src="/img/ui/menu_home.png" align="absmiddle" title="'+MENUSER['home'].descrp+'"></a>';
		$('#menu_top_home').html(home);
		
		// limpa modulo se for home
		$('#menu_top_modules').html("");
		return true;
		}
		
	// seta modulo
	var modulo  = '<a onClick="menuWhere(\''+menu+'\');">'+MENUSER[menu].descrp+'</a>';				
	$('#menu_top_modules').html(modulo);
	}
		
