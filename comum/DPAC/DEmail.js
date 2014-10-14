/**
 * 
 * D Email:
 *
 * @example $.DEmail({ vars });
 * @desc Uso Básico
 *
 *
 * @type jQuery
 *
 * @name DEmail
 * @cat Plugins
 * @author DONE Tecnologia - Adriano Karkow Gaiatto Leal (http://gaiattos.com/akgleal.com)
 */

(function($, window){
    $.extend({
    
    	DEmail: function(settings) {
        
    		var settings = $.extend({
                type           : 'bug',    // bug / suggestion
    			message        : '',    // text
    		}, settings);
		
            // configura
    		switch(settings.type.lc()) {
    			case "bug":
                    settings.req  = "title=issue[Bug]["+eos.core.genId()+"]";
                    settings.req += "&type="+settings.type;
                    settings.req += "&message="+settings.message;
                break;
            }
        
            // envia
            $.DActionAjax({
                action : "/sys/cfg/DPAC/DEmail.cgi",
                req    : settings.req,
                postFunction : function(x){

                        try {   
                            var x = JSON.parse(x);
                        } catch(e) {
                            console.log(e);
                            var x = { 
                                status  : "error"
                            }
                        } 
                        
                    if(x.status === "error") {
                        $.DDialog({
                            type    : "error",
                            title   : "Desculpe o transtorno",
                            message : "Erro ao enviar o email por favor envie um email diretamente para sos@coworkit.com.br"
                        });
                    }   
                }
            });    
        } 
    });
})(jQuery, this);


