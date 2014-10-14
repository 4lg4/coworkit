/* [INI]  MONEY field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
		price_format.js
	
	CSS necessario:
		.fieldMoney { }
		.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:
		clearPrefix(true) => R$ (mostra prefixo sempre)
	
	Exemplo de uso:
		$("campo_money").fieldMoney();
*/

// dependencias
// include("/comum/price_format/jquery.price_format.1.8.min.js"); 

(function($){
	
    $.fn.fieldMoney = function(settings, value) {
        if(isObject(settings) || !settings) { // setter
            
        	var settings = $.extend({
        		enable		 : true,
        		prefix		 : 'R$ ',
        		clearPrefix	 : false,
        		postFunction : false,
                centsSeparator : ',',
                thousandsSeparator : '.'
        	}, settings);
            
        } else { // getter / setter unico
    
    		switch(settings.lc()) {
    		    case "enable":
                    eos.template.field.unlock($(this));
                    return true;
    		    break;
            
    			case "disable":
                    eos.template.field.lock($(this));
                    return true;
    			break;
            
                // reset
                case "reset" :
                    $(this).val("");
                    return true;
                break;
                
                // retorna valor
                case "value" :
                    
                    if(value) {
                        $(this).val(value).setMask();
                    } else {
                        return $(this).val().replace(/\.|\-|\s*/g,'').replace(',','.');
                    }
                    
                    return true;
                break;
                
                // atualiza
                case "refresh" :
                    $(this).setMask();
                    
                    return true;
                break;
            }
        }
    
        /*
        // ajusta para salvar
        function unmask(f){
            var field = f.val();
            var result = "";

            for(var f in field) {
                if(!isNaN(field[f]) || field[f] == "-") result += field[f];
            }

            return result;
        }
        */
    
    	return this.each(function() {
    		$(this)
			    .attr('alt','decimal')
			    .setMask()
            /*
    			.priceFormat({ 
    				prefix             : settings.prefix,
    				clearPrefix        : settings.clearPrefix,
                    centsSeparator     : settings.centsSeparator,
                    thousandsSeparator : settings.thousandsSeparator
    			})
            */
    			.prop({
                    'autocomplete':'off'
                })
    			.focusout(function() {
    				if(settings.postFunction !== false) {
    					settings.postFunction.call(this);
                    }
    			});
                    
            eos.template.field.money($(this));
    	});
        
    };
    
})( jQuery );

/* [END]  MONEY field (by akgleal.com)  ------------------------------------------------------------------------- */
