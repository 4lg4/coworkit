/**
 * 
 * D Issue:
 *
 * @example $.DIssue({ vars });
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
    
    	DIssue: function(settings) {
        
    		var settings = $.extend({
                type           : 'bug',    // bug / suggestion
                source         : 'cgi',
    			message        : '',    // text
    		}, settings);
		
            // configura
    		switch(settings.type.lc()) {
    			case "bug":
                    
                    var source = 1;
                    if(settings.source === "postgres") {
                        source = 2;
                    } else if(settings.source  === "javascript") {
                        source = 3;
                    }
                    
                    settings.req  = "type=1";
                    settings.req += "&source="+source;
                    settings.req += "&message="+settings.message;
                break;
            }
        
            // envia
            $.DActionAjax({
                action : "/sys/cfg/DPAC/DIssue.cgi",
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
                    } else {
                        $.DDialog({
                            type    : "alert",
                            title   : "Desculpe o transtorno",
                            message : "Solicitação enviada com sucesso, entraremos em contato em breve, obrigado"
                            /* btnOK   : function(){
                                eos.core.call.module.dashboard();
                            } */
                        });
                    }   
                }
            });    
        } 
    });
})(jQuery, this);


