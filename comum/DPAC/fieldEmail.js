/* [INI]  EMAIL field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
		Javascript:
	
		CSS:
			/css/ui.css
				.fieldEmail { }
				.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:
		Enable / Disable
		Auto Complete
		Post Function
	
	Exemplo de uso:
		Javascript:
			$("#campo_email").fieldEmail();
			$(".campo_email").fieldEmail();
			
			$("#campo_email").fieldEmail(
				{
				options:values
				});
							
		HTML:
			<input type="text" id='campo_email' name='campo_email'>			
*/

(function($) {
    
    $.fn.fieldEmail = function(settings) {
        
        if(isObject(settings) || !settings) { // setter
            
        	var settings = $.extend({
            		autocomplete	: 'off',
            		disable			: false,
            		postFunction	: false,
            		type			: 'email'
        		}, settings);
                
        } else { // getter / setter unico
        
    		switch(settings.lc()) {
			    case "enable":
                    // $(this).prop("readonly",false);
                    eos.template.field.unlock($(this));
                    return true;
			    break;
                
    			case "disable":
                    // $(this).prop("readonly",true);
                    eos.template.field.lock($(this));
                    return true;
    			break;
                
    			case "reset":
                    // $(this).prop("readonly",true);
                    $(this).val("");
                    return true;
    			break;
                
    		    case "trigger":
                    // $(this).prop("readonly",true);
                    // $(this).val("");
                    check($(this));
                    return true;
        		break;
            }
        }
	
    
        // var obj = $(this);
        
        function check(obj) {
            var settings = obj.data("DTouchRadioSettings");
            
			// gera um alerta e coloca o foco no campo especifico
			if(obj.val()) {
				if(!isMail(obj.val())) {
					$.DDialog({
						message   : "<nobr>Email inválido !!</nobr>",
						focusBack : obj
					});
				
					return false;
				}
				
				// executa funcao post se setado
				if(isFunction(settings.postFunction)) {
				    settings.postFunction.call(this,obj.val());
				}
			}
        }
    
    	return this.each(function() { 
            
            // salva low level as opcoes do objeto
            $(this).data("DTouchRadioSettings", settings);
            
            $(this).addClass('DFields'); // adiciona identificador para campos EOS DFields
        
    		// se for dispositivos moveis
    		if(isTablet() === true || isMobile() === true) {
    			$(this).get(0).type = settings.type;
    		}
		
    		// cria campo	
    		$(this)
    			.prop(
    				{
    				'autocomplete'	: settings.autocomplete,
    				'disabled'		: settings.disable
    				})
    			.keydown(function(event)  {
    				// segura propagacao do enter
    				if(event.which == 13)
    					event.preventDefault();
							
    				// on enter or tab
    				if(event.which == 13 || event.which == 9) {
    					check($(this));
    				}
    			});
                    
            eos.template.field.email($(this)); // mostra na tela
    	});
    };
    
})( jQuery );


