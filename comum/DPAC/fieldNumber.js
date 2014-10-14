/* [INI]  NUMBER field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
		Javascript:
			/comum/jquery/jquery.meiomask.js (loaded on DPAC)
	
		CSS:
			/css/ui.css
				.fieldNumber { }
				.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:
		Enable / Disable
		Max Lenght
		Auto Complete
	
	Exemplo de uso:
		Javascript:
			$("#campo_number").fieldNumber();
			$(".campo_number").fieldNumber();
			
			$("#campo_number").fieldNumber(
				{
				options:values
				});

		HTML:
			<input type="text" id='campo_number' name='campo_number'>
*/

(function($){
	
$.fn.fieldNumber = function(settings){
    
    if(isObject(settings) || !settings) { // setter
    	var settings = $.extend({
        		maxlength		: '255',
        		autocomplete	: true,
			range           : false,   // range { min : 0, max : 999 }
			placeholder     : ''
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
            
            // reset
            case "reset" :
                $(this).val("");
                return true;
            break;
            
            // value
            case "value" :
                return $(this).val();
            break;
        }
    }
	
        
	
	return this.each(function() {
        	
		// se for dispositivos moveis
		if(isTablet() === true || isMobile() === true) {
			$(this).get(0).type = settings.type;
		}
		
		if(!settings.placeholder) {
			settings.placeholder = $(this).prop('placeholder');
		}
		
		// cria campo	
		$(this)
			.prop({
				'maxlength'	: settings.maxlength,
				'autocomplete'	: settings.autocomplete,
				'placeholder'   : settings.placeholder,
			})
			.attr('alt','number')
			.setMask()
            .focusout(function(){
                if(isObject(settings.range)){
                    if($(this).val() && ($(this).val() < settings.range.min || $(this).val() > settings.range.max)) {
                        var f = $(this);
                        $.DDialog({
                            type    : "alert",
                            message : "Fora do range válido <br> Mínimo: "+settings.range.min+" / Máximo: "+settings.range.max ,
                            btnOK   : function(){
                                f.val("").focus();
                            }
                        })
                    }
                }
            });
            
            
            
            eos.template.field.number($(this));
	});
    
};

})( jQuery );

