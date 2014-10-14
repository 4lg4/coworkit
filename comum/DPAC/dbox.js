/* [INI]  Dbox (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	
	
	CSS necessario:
 	.dbox {	box principal }
	.dbox_title { titulo do dbox }
	.dbox_title span { descricao interna do titulo }
	.dbox_cont { conteudo do dbox }

    Opcoes:

	Exemplo de uso minimo:	
	BOX = new dbox("elemento_id","titulo desejado");
	BOX.show();
	<div id="elemento_id">conteudo desejado</div>
*/

function dbox(id,titulo) 
	{	
	var W = "100%"; // largura
	var H = "100%"; // altura
	var STYLE = ""; // stilo se necessario
	
	// Ajusta tamanho do quadro	
	this.setSize = function(width,height)
		{
		W = width;
		H = height;
		}
	
	// adiciona stilo 
	this.setStyle = function(val) { STYLE = val; }
	
	// gera elemento
	this.show = function()
		{
		// gera dbox
		var cont  = '<div id="dbox_'+id+'" class="dbox" '+STYLE+'>'
			cont +=	'	<div id="dbox_title_'+id+'" class="dbox_title"> <span>'+titulo+'</span></div>';
			cont += '	<div id="dbox_cont_'+id+'" class="dbox_cont"></div>';
			cont += '</div>';
			// &nbsp;&nbsp; &bull;
		$($('#'+id)).before(cont);
		
		// move conteudo para dbox
		$('#'+id).detach().prependTo($('#dbox_cont_'+id));
		
		// DBOX minimiza / maximiza
		$("#dbox_title_"+id).click(function()
			{
			// $("#"+$(this).parent().attr("id")).toggleClass("dbox_min","fast");
			$("#dbox_"+id).toggleClass("dbox_min","fast");
			});
			
		// ajusta Altura e largura css
		$("#dbox_"+id).css({ "width":W, "height":H });
		}
	
	// retorna
	// return this.show();
	}
/* [END]  Dbox (by akgleal.com)  ------------------------------------------------------------------------- */
