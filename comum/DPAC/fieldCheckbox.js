/* [INI]  CHECK.BOX field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	
	CSS necessario:
	.fieldCheck { }
	.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:
	
	Exemplo de uso:
	var campoCheck = new fieldCheck("campo_checkbox");
	<input type="checkbox" id='campo_checkbox' name='campo_checkbox'>
	
	Todo
	- adicionar suporte a array para criacao de multiplos checks ??
		$( "#format" ).buttonset();
		<div id="format">
			<input type="checkbox" id="check1" /><label for="check1">B</label>
			<input type="checkbox" id="check2" /><label for="check2">I</label>
			<input type="checkbox" id="check3" /><label for="check3">U</label>
		</div>
*/

(function($){
    
$.fn.fieldCheckbox = function(settings,value){
    
	// setter
	if(isObject(settings) || !settings){
        
    	var settings = $.extend({
    		postFunction : false,           // executa funcao apos criar o objeto
            valueUncheck : false,           // valor quando nao selecionado
            valueCheck   : true,            // valor quando selecionado
            label        : "Selecione",     // label quando nao selecionado
            labelCheck   : "Selecionado",   // label quando selecionado
            onCheck      : false,           // executa funcao ao marcar
            onUncheck    : false            // executa funcao ao desmarcar
    	}, settings);
        
    } else { // getter
        
		switch(settings){
            // check
            case "check": 
                $(this).trigger("click");
                return true;
            break;
            
            // is checked
            case "isChecked": 
                if($("#radio_"+$(this).prop("id")).prop("checked")){
                    return true;
                } else {
                    return false;
                }
            break;
                    
            // habilita
            case "enable":
                console.log("nothing defined for this action");
                return true;
            break;
            
            // desabilita
            case "disable":
                $(this).off("click");
                return true;
            break;
        }
    }
    
	return this.each(function(){
        
        settings.obj           = $(this).clone();            // clona obj original
        settings.obj_name      = settings.obj.prop("name");  // pega nome do objeto se existir
        settings.obj_id        = settings.obj.prop("id");    // pega nome do objeto se existir
        settings.obj_container = "fieldCheckbox_"+settings.obj_id;
        settings.obj_input     = "input_"+settings.obj_id;
        // settings.obj_value = settings.obj.val();         // pega valor objeto se existir
        
        // ajusta nome do antigo checkbox e oculta
        settings.obj.prop("name", "");
        settings.obj.prop("id", "radio_"+settings.obj_id);
        
        // adiciona objeto novo na tela
        $(this).replaceWith("<div class='fieldCheckbox' id='"+settings.obj_container+"'><span class='fieldCheckbox_label'>"+settings.label+"</span></div>"); // troca pelo container  
        $("#"+settings.obj_container).append(settings.obj);                                          // adiciona objeto dentro do container
        $("#"+settings.obj_container).append("<input id='"+settings.obj_input+"' name='"+settings.obj_name+"' value='"+settings.valueUncheck+"'/>");               // adiciona objeto dentro do container
        
        // esconde seletores
        $("#"+settings.obj_input).hide();
        settings.obj.hide();

        // adiciona suporte ao click do checkbox
        $("#"+settings.obj_container)
            .click(function(event){
                event.preventDefault(); // cancela propagacao do click
            
                // checkbox unchecked
        		if(settings.obj.prop("checked")){
                
                    $("#"+settings.obj_input).val(settings.valueUncheck);
                    settings.obj.prop("checked",false);
                    $(this).find(".fieldCheckbox_label").text(settings.label);
                    $(this).removeClass("fieldCheckbox_selected");
                    
                    // executa funcao ao clicar
                    if(isFunction(settings.onUncheck)){
                        settings.onUncheck.call(this, $(this));
                    }
                
        		} else { // checkbox checked
                
                    $("#"+settings.obj_input).val(settings.valueCheck);
                    settings.obj.prop("checked",true);
                    $(this).find(".fieldCheckbox_label").text(settings.labelCheck);
                    $(this).addClass("fieldCheckbox_selected");
                    
                    // executa funcao ao clicar
                    if(isFunction(settings.onCheck)){
                        settings.onCheck.call(this, $(this));
                    }
                
        		}
            })
            .prop('unselectable', true)
            .on('selectstart', false);


        // coloca id do objeto original no container 
        $("#"+settings.obj_container).prop("id", settings.obj_id);

    });

};
})( jQuery );
