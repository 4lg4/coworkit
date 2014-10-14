/** 
 *  @author: Adriano Leal (http://adriano.gaiattos.com)
 *  
 *  Dependencias:
 *  	Javascript:
 *  		DSwipePages (/comum/DPAC/DSwipePages.js) // troca de paginas
 *  		
 *  	CSS:
 *  		/css/DPAC/DPAC.css
 *  
 *  Exemplo de uso							
 *  	HTML:
 *  		<div id="DTouchPages_MODULO">
 *  			<div id="center"> Pagina principal </div>
 *  			<div id="left"> Pagina com Listagem vinda do banco </div>
 *  			<div id="right"> Pagina com conteudo complementar </div>
 *  		</div>
 *  
 *      JS:
 *  		\$("#DTouchPages_MODULOe").DTouchPages({
 *              pageChange: "center",
 *              pageCenter : \$("#center"),
 *              pageRight  : \$("#right"),
 *              pageLeft   : \$("#left"),
 *  			postFunctionCenter : function() {
 *                  ... JS code ...
 *              },
 *  			postFunctionRight : function() {
 *                  ... JS code ...
 *              },
 *  			postFunctionLeft : function() {
 *                  ... JS code ...
 *              },
 *              onChange : function() {    
 *                  ... JS code ...
 *              },
 *  			onCreate : function() {    
 *                  ... JS code ...
 *              }
 *          });
*/


(function($){
	
$.fn.DTouchPages = function(settings, value) {
    
	// executa funcoes com objeto criado
	if(settings && isObject(settings) === false) {
        
			switch(settings.lc()) {
				// Page Change: troca de pagina
				case "page":
                case "change":
				case "pageChange":
				case "changePage":
                    if(value) {
                        DTouchPagesChange($(this),value);
                        return true;
                    } else {
                        return $(this).data("DTouchPagesSettings")["pageChange"]
                    }
				break;
                
                case "enable" :
                    if(eos.core.is.array(value)) {
                        
                    } else {
                        $(".DTouchPages_corner_"+value).show();
                        $(this).data("DTouchPagesSettings")["pageDisable"] = false;
                    }
                    return true;
                break;
                
                case "disable" :
                    if(eos.core.is.array(value)) {
                    
                    } else {
                        $(".DTouchPages_corner_"+value).hide();
                        $(this).data("DTouchPagesSettings")["pageDisable"] = true;
                    }
                    return true;
                break;
			}
	}
	
    // opcoes do objeto
	var settings = $.extend({
		postFunctionLeft 	: '',       // ao mover pagina para esquerda
		postFunctionRight	: '',       // ao mover pagina para direita
		postFunctionCenter	: '',       // ao mover pagina para o centro
        onChange		    : '',       // funcoes executadas no momento da troca da pagina
		onCreate		    : '',       // funcoes executadas no momento de criacao das paginas
		pageChange			: 'center', // pagina inicial
		pageLeft            : false,    // DOM object
		pageRight           : false,    // DOM object
		pageCenter          : false,    // DOM object
        pageDisable         : false     // inicia com paginas desabilitadas  
	}, settings);
	
	// facilita trabalho com objeto
	settings.pg = $(this);
	settings.pg_id = $(this).prop("id");

	return this.each(function() {
        
		// salva opcoes setadas do objeto para uso futuro
		if(isObject(settings) === true) {
			$(this).data("DTouchPagesSettings", settings);	
        }
        
		// prepara container pai
		$(this).addClass("DTouchPages");
        
        /** 
         *  Paginas 
         *      ajusta paginas se nao setadas procura
         */
        if(!settings.pageLeft) { // left page
            if($("#"+settings.pg_id+"_left").length > 0) {
                settings.pageLeft = $("#"+settings.pg_id+"_left").addClass("DTouchPages_left DTouchPages_pages");
            }
        } else {
            settings.pageLeft.addClass("DTouchPages_left");
        }
        
        if(!settings.pageRight) { // right page
            if($("#"+settings.pg_id+"_right").length > 0) {
                settings.pageRight = $("#"+settings.pg_id+"_right").addClass("DTouchPages_right DTouchPages_pages");
            }
        } else {
            settings.pageRight.addClass("DTouchPages_right");
        }
        
        if(!settings.pageCenter) { // center
            if($("#"+settings.pg_id+"_center").length > 0) {
                settings.pageCenter = $("#"+settings.pg_id+"_center").addClass("DTouchPages_center DTouchPages_pages");
            } else { // se pagina central nao existir erro
                console.log("DTouchPages, página central deve ser definida !")
            }
        } else {
            settings.pageCenter.addClass("DTouchPages_center");
        }
		
		/**
         *  Hot Corners
         *      cantos para troca de pagina
		 */
        var corner = {
            right : "<div class='DTouchPages_corner DTouchPages_corner_right'></div>",
            left  : "<div class='DTouchPages_corner DTouchPages_corner_left'></div>"
        }
		
		// add hot corners no corpo do sistema
		$(".DTouchPages_corner").remove();
        $("#corpo").append(corner.left);
        $("#corpo").append(corner.right);	
        
        // se desabilitado
        if(settings.pageDisable) {
            $(".DTouchPages_corner").hide();
        }	

        // adiciona clique
		$(".DTouchPages_corner").click(function(){
            
            // pagina esquerda / direita ativa e clique no corner
            if($("body").find(".DTouchPages_left_active").length > 0 || $("body").find(".DTouchPages_right_active").length > 0) {
                pg = "center";
            } else if($(this).hasClass("DTouchPages_corner_left")) { // se corner esquerdo clicado
                pg = "left";
            } else {
                pg = "right";
            }      

            settings.pg.DTouchPages("page",pg); // troca pagina
		});

		// Roda funcao on create
		if(isFunction(settings.onCreate)) {
			settings.onCreate.call(this);
		}
        
		// ajusta pagina inicial
		if(settings.pageChange) {
            DTouchPagesChange(settings.pg);
		}
        
		/* 
         *  fast click 
         *      remove delay do clique em dispositivos touch 
         */
		new FastClick(document.getElementById(settings.pg_id));
	}); 
};
	
})( jQuery );


/**
 *  DTouchPagesChange
 *      troca de pagina swipe pages
 */
function DTouchPagesChange(obj,pg) {	
    
	var settings = obj.data("DTouchPagesSettings"); // acesso as configuracoes atuais do objeto
        settings.pg_id = obj.prop("id");
        
    if(pg) {
        settings.pageChange = pg;
        
    	if(isFunction(settings.onChange)) { // on change
    		settings.onChange.call(this);
    	}
        
    } else { // pagina inicial SEM efeito
        
        if(settings.pageChange !== "center") {
            $("#"+settings.pg_id+"_"+settings.pageChange).addClass("DTouchPages_pages_noeffect");
        }
    }
    
    // salva low level pagina que sera trocada
    obj.data("DTouchPagesSettings")["pageChange"] = settings.pageChange;
    
	$(".DTouchPages_corner").fadeOut("fast"); // esconde hot corners
    
    // se desabilitado
    if(settings.pageDisable) {
        // $(".DTouchPages_corner").hide();
        return true;
    }
    
	if(settings.pageChange === "left"){ // esquerda
            
		$(".DTouchPages_corner_right").fadeIn("fast"); // mostra hot corner direita
        $("#"+settings.pg_id+"_right").removeClass("DTouchPages_right_active");
        $("#"+settings.pg_id+"_left").addClass("DTouchPages_left_active", function(){
    		if(isFunction(settings.postFunctionLeft)) { // postFunction Left
    			settings.postFunctionLeft.call(this);
    		}
        });
        
	} else if(settings.pageChange === "right") { // direita
        
		$(".DTouchPages_corner_left").fadeIn("fast"); // mostra hot corner esquerda
        $("#"+settings.pg_id+"_left").removeClass("DTouchPages_left_active");
        
        $("#"+settings.pg_id+"_right").addClass("DTouchPages_right_active", function(){
    		if(isFunction(settings.postFunctionRight)) { // postFunction Right
    			settings.postFunctionRight.call(this);
    		}
        });
        
	} else {
        
        $("#"+settings.pg_id+"_left").removeClass("DTouchPages_left_active");
        $("#"+settings.pg_id+"_right").removeClass("DTouchPages_right_active");
        
        if(settings.pageLeft) { // left corner
		    $(".DTouchPages_corner_left").fadeIn("fast");
        }
        
        if(settings.pageRight) { // right corner
		    $(".DTouchPages_corner_right").fadeIn("fast");
        }
        
		if(isFunction(settings.postFunctionCenter)) { // postFunction Center
			settings.postFunctionCenter.call(this);
		}
	}
    
    // remove no effects from pages
    $("#"+settings.pg_id+"_"+settings.pageChange).removeClass("DTouchPages_pages_noeffect");
    // $(".DTouchPages_pages").removeClass("DTouchPages_pages_no_effects");
    
}
