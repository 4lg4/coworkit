/**
 * 
 * D-Action Ajax:
 *
 * @example $.DActionAjax({ vars });
 * @desc Uso Básico
 *
 * @param addItem Array (obrigatório) Ver: Exemplo addItem
 *
 * @type jQuery
 *
 * @name DActionAjax
 * @cat Plugins/Accordion
 * @author DONE Tecnologia - Adriano Karkow Gaiatto Leal (http://gaiattos.com/akgleal.com)
 */

(function($, window){
	
$.extend({
    
	DActionAjax: function(settings) {
        
		var settings = $.extend({
            // type           : '',    // tipo de ajax (download / node)
			action         : '',    // arquivo para executar
			req            : '',    // variaveis adicionais
			loader         : true,  // full loader ( false = no loader / id obj = )
			serializeForm  : true,  // serializa formulario #CAD
			async          : true,  // ajax asyncrono
			target         : '#resultado', // informa a DIV que o resultado deve ser enviado
			postFunction   : false,  // executa funcao apos criar,
            type           : ''     // (download === forca download arquivo)
		}, settings);
		            
		// action verifica
		if(settings.action == "") {
			console.log("$.DActionAjax: action não definido");
			return false;
		}
    	
        // passa variaveis adicionais
    	if(settings.req) {
    	    settings.req = "&"+settings.req;
        } 
        
		// loader, se vazio adiciona loader completo
        /*
		if(isObject(settings.loader)) {
			if(settings.loader.prop("id"))
				settings.loader = settings.loader.prop("id");
			else
				settings.loader = true;
		}
        */
			
    	// se for carregamento dos menus actions do modulo deixa syncrono o carregamento
    	if(settings.action.indexOf("menu") !== -1 || settings.action.indexOf("contatos") !== -1) {
    		async = false;
    	}
        
		// serializa formulario 
    	if(settings.serializeForm) { 
    		settings.req += "&"+$('#CAD').serialize();
        }
        
    	settings.path = "";
    	// se Nao for endereco absoluto
    	if(settings.action.indexOf("/sys/") !== 0) {
    		settings.path = $('#AUX input[name="MODULO_PATH"]').val()+"/";		
        }
        
        // node apps
        if(settings.action.search("https://") !== -1 || settings.action.search("http://") !== -1) { 
            settings.path = "";
            console.log(settings.action);
        }
        
        			
    	// se arquivo nao setado
    	if(!settings.action) {
    		$.DDialog("Devils: A função: \n\n    DActionAjax() \n\nacessa o arquivo desejado via ajax e retorna o resultado dentro da div resultado dentro do modulo. \n\n *** verficar logs no console");		
    		return false;
    	}
        
        // ajusta variaveis
        settings.req = "&ID="+$('#AUX input[name="ID"]').val()+settings.req;
        
    	// executa
    	$.ajax({
    		type: "POST",
    		url: settings.path+settings.action,
    		dataType: "html",
    		data: settings.req,
    		async: settings.async,
    		beforeSend : function() {
                    // adiciona loader
        			if(settings.loader === true) {
        				Loading();
        			} else {
        				loadingObj(settings.loader);
    			}
    		},
    		success: function(data, status, request) {
                
                // se for download  
                if(settings.action.search('.xls') !== -1 || settings.action.search('.pdf') !== -1 || settings.action.search('.doc') !== -1 || settings.type === "download") {
                    // formulario de download
                    var form = document.createElement("form");
                        form.id     = "DOWNLOAD";
                        form.name   = "DOWNLOAD";
                        form.method = "POST";
                        form.target = "DOWNLOADFRAME"; //"_blank";
                        form.action = settings.path+settings.action;
                    $.each(settings.req.split('&'), function(k, v) { // form fields
                        // campos
                        var field = document.createElement("input");
                            field.type  = "hidden";
                            field.name  = v.split('=')[0];
                            field.value = v.split('=')[1];
                            
                        form.appendChild(field); // adiciona campo
                    });
                    
                    // iframe de download
                    var downframe = document.createElement("iframe");
                        downframe.id   = "DOWNLOADFRAME"; 
                        downframe.name = "DOWNLOADFRAME"; 
                        downframe.src  = "about:blank";
                    document.querySelector("body").appendChild(downframe);
                    
                    
                    $('body').append(form); // adiciona formulario ao documento
                    form.submit();          // envia download
                    delete form;            // remove formulario de download
                    // remove iframe depois de carregado
                    $("#DOWNLOADFRAME").ready(function (){
                        delete downframe; 
                    });
                } else {
                    $(settings.target).html(data);
                }
                                  
                // executa post functions
                if(isFunction(settings.postFunction)){
                    settings.postFunction.call(this,data);
                }
                
    			return true;
    		},
    		error: function(data) {
                
                if(!$(".DDialog_box").is(":visible")){ // se ja houver uma janela de erro nao mostra
                
                    var msg  = "<div class='DDialog_box_middle'> Estamos trabalhando pra MUDAR a  <br> TI do Brasil !!  </div>";
                        msg += "<div class='DDialog_box_img'><img src='/img/bugs/construction.png'></div>";
                        msg += "<div class='DDialog_box_bottom'> um email com erro será enviado para o suporte Obrigado.</div>";
                    
                    var dados  = "Formulario CAD: <hr>"+$("#CAD").serialize();
                        dados += "<br><br><br>Formulario AUX: "+$("#AUX").serialize();
                        dados += "<br><br><br>Retorno: <hr>"+data.statusText;
                        dados += data.responseText;
                    
                    $.DDialog({
                        type    : "error",
                        title   : "Desculpe o transtorno",
                        message : msg,
                        btnOK   : function(){
                            $.DIssue({
                                type    : "bug",
                                message : dados
                            });
                            /*
                            $.DEmail({
                                type    : "bug",
                                message : data
                            });
                            */
                        }
                    });
                }
            
    			return false;
    		},
            complete : function(data) {
    			
                // remove loader
    			if(settings.loader === true) {
    				unLoading();
    			} else {
    				unLoadingObj(settings.loader);
                }
            }
    	});	
    }
    
});
	
})(jQuery, this);


/* [INI] DActionAjax -----------------------------------------------------------------------------------------------------
*
*	old daction ajax
*
*	remover assim que todo o sistema usar o daction ajax do jquery
----------------------------------------------------------------------------------------------------------------------- */

function DActionAjax(page,req,obj,noserialize) { 
	if(!obj) {
		var obj = true;
	}
    
	if(!async) {
		var async = true;
	} else {
	    var async = false;
	}
    
    if(!req) {
        var req = "";
    }
    
    // serializa cad
	if(!noserialize){
		var serialize = true;
	} else {
	    var serialize = false;
	}
						
                        
	// call new function
    $.DActionAjax({
       action        : page,
       req           : req,
       serializeForm : serialize,
       loader        : obj,
       async         : async
    });
}
/* [END] DActionAjax --------------------------------------------------------------------------------------------------- */


