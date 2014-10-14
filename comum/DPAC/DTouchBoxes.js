/* [INI]  DTouchBoxes (by akgleal.com)  ------------------------------------------------------------------------- 

*/

(function($){
	
$.fn.DTouchBoxes = function(settings,value) 
	{
	// executa funcoes com objeto criado
	if(settings)
		{
		if(isObject(settings) === false)
			{
			switch(settings.lc())
				{
				// Title: ajusta titulo
				case "title":
                    $(this).find(".DTouchBoxes_title").html(value);
					return true;
				break;
                
				// Hide: esconde box
				case "hide":
					$(this).fadeOut("fast");
					return true;
				break;
			
				// Show: mostra box
				case "show":
					$(this).fadeIn("fast");
					return true;
				break;
				}
			}
		}
	
	var settings = $.extend(
		{
		enable		: true,
		title		: '',
		orientation	: 'top',
		width		: '',
		height		: '',
		type		: 'box', // box / bar (barra)
		removeable	: false,
		editable	: false,
        minimize    : false,
        postFunction : false
		}, settings);
	
	return this.each(function()
		{ 
		// guarda opcoes em low level
		// $(this).data("DTouchBoxesSettings", settings);
			
		var box = $(this);	
		
		// adiciona titulo
        if(settings.title != "" || $(this).find(".DTouchBoxes_title").length < 1) {
			settings.title_box = "<div class='DTouchBoxes_title'>"+settings.title+"</div>";
		}
        
		// else
		//	{
		//	console.log("DTouchBoxes generator");
		//	}
		
		// adiciona classe ao objeto principal
		$(this).addClass("DTouchBoxes");
			
			/*
			// ao clicar na caixa coloca o foco no primeiro input do DBox
			$(".DTouchBoxes").click(function()
				{ 
				$(this).find("input[type=text]:visible").focus();
				// alert($(this).attr("id"));
				// $(this).find("input:not([type=hidden]):first").focus();
				// $(this).find("input:first").focus();
				
				// alert($(this).parent().html());
				// alert($(this).html());
				// alert($(this).find("input:first").html()+" ******** "+$(this).find("input").html()+" ******** "+$(this).find("input").attr("id")+" ******* "+$(this).find("input[type=text]:visible").attr("id"));
				});
	
			*/
		
		// adicionar icone de remocao
		if(settings.removeable !== false) {
			$(this).prepend("<div class='DTouchBoxes_removeable' title='Remover'></div>");
			
			// adiciona remocao ao icone
			box.find(".DTouchBoxes_removeable")
                .tooltip()
                .off("click") // remove multiplos cliques
                .click(function() {
    				var fndel = function(){ box.remove(); };
    				$.DDialog({
                        type    : "confirm",
                        message : "Deseja realmente remover o box selecionado ? <br> essa ação é irreversível !",
                        btnYes  : function(){ 
                            box.remove();
                        },
                        postFunction : function(){
            				if(isFunction(settings.removeable)) {
            					settings.removeable.call(this,box);
                            }
                        }
                    });
    		});
		}
		
		// adicionar icone de configuracao
		if(settings.editable !== false) {
			$(this).prepend("<div class='DTouchBoxes_editable' title='Editar'><span></span></div>");
			
			// adiciona edicao do box
			box.find(".DTouchBoxes_editable")
                .tooltip()
                .click(function() {
    				if(isFunction(settings.editable)) {
    					settings.editable.call(this,box);
                    }
    			});
		}
        
		// adicionar icone de minimizar
		if(settings.minimize !== false) {
			$(this).prepend("<div class='DTouchBoxes_minimize' title='Minimizar'><span></span></div>");
			
			// adiciona edicao do box
			box.find(".DTouchBoxes_minimize")
                .tooltip()
                .click(function() {
                    box.toggleClass("DTouchBoxes_minimized");
                
    				if(isFunction(settings.minimize)) {
    					settings.minimize.call(this,box);
                    }
    			});
		}
			
		// se for barra
		if(settings.type == "bar")
			{
			$(this).addClass("DTouchBoxes_bar");
			}
			
		// ajusta a orientacao do titulo
		if(settings.title	!= '')
			{
			if(settings.orientation	== 'top')
				{
				$(this).prepend(settings.title_box);
				}
			else
				{
				$(this).append(settings.title_box);
				}
			}
            
            
		/** 
         *   post Function
         *       executa funcao apos criar objeto
         */
		if(isFunction(settings.postFunction)){
			// settings.postFunction.call(this, settings.radios.data("DTouchRadioSettings"));
            settings.postFunction.call(this);
		}
            
            
		});
	};

})( jQuery );

/*
function DTouchBoxesDelete(obj)
	{
	obj.remove();
	}
*/
