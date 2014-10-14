/* [INI] DDebug ----------------------------------------------------------------------------------------------------------
	Habilitar / Desabilita modo debug
	
	uso:
		HTML
			<div class="DDebug"></div>
------------------------------------------------------------------------------------------------------------------------*/
function DDebug(rm)
	{
	// Desabilita
	if(rm)
		{
		$(".DDebug_title").remove();
		$(".DDebug").removeClass("DDebug_box");
		console.log("Modo Debug Desabilitado");
		
		// remover scripts
		// include("/comum/firebug-lite/firebug-lite.js","REMOVE");
		
		return false;
		}
	
	
	// Habilita
	if ($(".DDebug_title").length == 0)
		{
		console.log("Modo Debug Habilitado");
		$("#menu_top").append("<div class='DDebug_title'>Modo Debug Habilitado <span class='DDebug_title_close' title='Fechar Debug'></span><span class='DDebug_title_expand' title='Expandir Debug Box'></span><span class='DDebug_title_burn' title='Burn Messages Debug Box'></span><span class='DDebug_title_loader' title='Remove Loaders'></span></div>");
		
		// adiciona expansao do box de debug ao clicar em expandir no titulo
		$(".DDebug_title_expand").click(function()
			{
			// $('.DDebug_box').toggleClass("DDebug_box_expanded");
			
			$(".DDebug_box").dialog(
				{ 
				title: "DDebug Box",
				draggable: true,
				resizable: true,
				width: 500,
				width: 250,
				dialogClass: "DDebug_box_modal",
				closeOnEscape: true,
				beforeClose: function( event, ui ) 
					{
					$(".DDebug_box").dialog( "destroy" );
					}
				});
				
			// $(".DDebug_box").dialog( "destroy" );
			});
			
		// desliga ddebug
		$(".DDebug_title_close").click(function(){ DDebug(1); });
		
		// burn ddebug
		$(".DDebug_title_burn").click(function(){ $(".DDebug_box").html(""); });
		
		// remove loaders
		$(".DDebug_title_loader").click(function(){ $(".DLoaders").remove(); });
		}
	$(".DDebug").addClass("DDebug_box");
	// include("/comum/firebug-lite/build/firebug-lite.js");
	}
	
/* Lista todas as propriedades de um objeto */
function DDebugObj(obj)
	{
	if(!obj)
		{
		alert("ERRO: Você deve informar um objeto");
		return false;
		}
		
	var r = "";
	$.each(obj, function(key, element) 
		{ 
		r += '['+key+']{'+element+"} <br>";
		});
		
	$(".DDebug_box").append("<hr>"+r);
	}
/* [END] DDebug ------------------------------------------------------------------------------------------------------- */
