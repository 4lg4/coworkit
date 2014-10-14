/* 
@description gera selects
@author     http://adriano.gaiattos.com / Done Tecnologia Ltda
*/

// form selects
include("/comum/select2/select2.js");


(function($){
	
$.fn.fieldSelect = function(settings,value){
    
	// setter
	if(isObject(settings)){
        
    	var settings = $.extend({
    		postFunction  : false,
    		filled        : false,
            table         : false,
            placeholder   : "Selecione...",
            type          : false
    	}, settings);
        
    } else { // getter
        
		switch(settings){
            // seta valor
			case "val":
            case "value":
                if(value){
                    $(this).select2("val",value);
                    return true;
                } else {
                    return $(this).select2("val");
                }
            break;
            
            // abre e fecha select
            case "open":
            case "close":
                $(this).select2("open");
                return true;
            break;
            
            // habilita
            case "enable":
                eos.template.field.unlock($(this));
                $(this).find(".select2-chosen").removeClass("EOS_template_field_lock"); // ajuste cor do campo usando plugin select2
                $(this).select2("readonly", false);
                return true;
            break;
            
            // desabilita
            case "disable":
                eos.template.field.lock($(this));
                $(this).find(".select2-chosen").addClass("EOS_template_field_lock"); // ajuste cor do campo usando plugin select2
                $(this).select2("readonly", true);
                return true;
            break;
            
            // readonly
            case "readonly":
                eos.template.field.readonly($(this));
                // $(this).find(".select2-chosen").addClass("EOS_template_field_lock"); // ajuste cor do campo usando plugin select2
                // $(this).select2("readonly", true);
                return true;
            break;
        }
        
    }
	
    
	return this.each(function(){
        settings.obj = $(this);
        $(this).addClass("fieldSelect");
        
		// salva opcoes setadas do objeto para uso futuro
		if(isObject(settings) === true)
			$(this).data("fieldSelectSettings", settings);

        
        // create select
        if(settings.type !== "simple") { // adiciona aparencia se NAO simple
            eos.template.field.select($(this));
        }
        
        // popula
        if(settings.table){
            settings.obj.empty();
            var items = eos.core.getList(settings.table);
            items.forEach(function(i){
                
                var img = "";
                if(i.img){
                    img = "style='background-image:url("+i.img+");' class='empresa_endereco_dados_select_option'";
                }
                
                settings.obj.append("<option value='"+i.codigo+"' "+img+">"+i.descrp+"</option>");
            });
            
            // trick para funcionamento do place holder
            settings.obj.prepend("<option selected></option>");
            
            
            if(settings.type !== "simple") { // adiciona aparencia se NAO simple
             //   fieldSelectApparence($(this)); // aparencia
            }
        }


    // fieldSelectApparence(); // aparencia;
    });
};
})( jQuery );


/* 
*   Apparence
*       ajusta aparencia dos selects
*/
function fieldSelectApparence(obj){   
	var settings = obj.data("fieldSelectSettings"); // acesso as configuracoes atuais do objeto
	// var val = obj.data("DTouchRadioSettings")["value"]; // acesso as configuracoes atuais do objeto
    
    if(!obj){
        // $(".select2-drop-mask").select2("destroy");
        // select2-drop-mask
        $(".fieldSelect").select2({
            width                   : "93%", // "resolve"
            placeholder             : settings.placeholder,
            minimumResultsForSearch : 10,
             allowClear: true // habilida selecionar nada
        });
        
       return true; 
    }
    
    obj.select2({
        width                   : "93%", // "resolve"
        placeholder             : settings.placeholder,
        minimumResultsForSearch : 10,  // mostra filtro acima de 10 itens
        allowClear: true // habilida selecionar nada
    });
}

