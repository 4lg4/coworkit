/** 
 *  Auto Complete  
 *      field Auto Complete
 *      campo auto complete

	*** funcao funciona somente com ID e nao com a classe
	*** verificar a possibilidade de trabalhar com a classe

	Dependencias:
		CGI
			
		Javascript
		
		CSS

	opcoes:
	
	Exemplo de uso:
		Javascrip
				
		HTML


 * @author: http://adriano.gaiattos.com
 */

(function($){
	
$.fn.fieldAutoComplete = function(settings,value) {
    
	// executa funcoes com objeto criado
	if(!isObject(settings)) {
        
		switch(settings.lc()) {
            
			// Reset: Zera valores
			case "reset":				
				$(this).val("");
				$("#"+$(this).prop("id")+"_descrp").val("");

				$(this).data("fieldAutoCompleteSettings")["value"] = "";
				$(this).data("fieldAutoCompleteSettings")["descrp"] = "";
				
				// executa post Reset
                if(isFunction($(this).data("fieldAutoCompleteSettings")["onReset"])){
				    $(this).data("fieldAutoCompleteSettings")["onReset"].call(this);
                }
				return true;
			break;
            
            // seta values
            case "value" :
            case "val" :
                
                    var codigo, descrp;
                
                    if(value.codigo) {
                        codigo = value.codigo;
                        descrp = value.descrp;
                    } else {
                        codigo = value.id;
                        descrp = value.val;
                    }
                
                    $(this).val(codigo);
                    $("#"+this.prop("id")+"_descrp").val(descrp);
                    return true;
            break;
            
            // habilita campo para uso 
            case "enable" :
                eos.template.field.unlock($("#"+this.prop("id")+"_descrp"));
                $("#"+this.prop("id")+"_descrp").autocomplete("enable");
                return true;
            break;
            
            // somente leitura
            case "disable" :
                eos.template.field.lock($("#"+this.prop("id")+"_descrp"));
                $("#"+this.prop("id")+"_descrp").autocomplete("disable");
                return true;
            break;
            
            // show
            case "show" :
                eos.template.field.show($(this));
                return true;
            break;
            
            // hide
            case "hide" :
                eos.template.field.hide($(this));
                return true;
            break;
		}
	}
		
		
	var settings = $.extend({
    		sql_tbl			: '',		// tabela que sera procurado
    		sql_sfield		: 'descrp',	// campo de pesquisa
    		sql_rfield		: 'descrp',	// campo com o retorno do sql 
    		sql_order		: 'descrp',	// campo de ordenacao
    		qtd				: '2', 		// quantidade minima de caracteres a ser usado
    		notab			: true,		// desabilita tab
    		postFunction	: '',		// executa funcao ao finalizar tudo
    		createFunction	: '',		// executa funcao na criacao do objeto
    		enable			: true,		// habilidado
            readonly		: false,	// somente leitura false
    		autocomplete	: false,	// autocomplete do browser desabilitado
    		maxlength		: '',		// tamanho maximo do campo
    		allowEmpty		: false,	// permitir ficar vazio campo
    		filled			: '',		// iniciar campo preenchido { id:$id, val:'$val' }
    		delay			: 300, 		// tempo de espera para pesquisa
    		placeholder		: 'Pesquisar ',
            type            : '',        // tipos predefinidos exemplo usuarios / empresas
            show_img        : false,     // mostrar imagem ou nao
            clearOnExit     : false,     // reseta campo ao escolher
            localFile       : false,     // define se arquivo de pesquisa global ou local 
            itemAdd         : false,     // botao para adicionar item
		}, settings);
	
			
	// Return 
	return this.each(function(){
        
        $(this).addClass('DFields'); // adiciona identificador para campos EOS DFields
        
        // se html tiver place holder
        if($(this).prop("placeholder")) {
            settings.placeholder = $(this).prop("placeholder");
        }
        
        
		// guarda opcoes em low level
		$(this).data("fieldAutoCompleteSettings", settings);
		
		// ajusta variaveis
		var field = $(this)
        ,   field_id = $(this).prop("id")
        ,   field_input_descrp = "<input type='text' id='"+field_id+"_descrp' name='"+$(this).prop("name")+"_descrp' maxlength='"+settings.maxlength+"' placeholder='"+settings.placeholder+"' class='DFields'>"
        ,   return_data = "";
		
		// remove campo descrp se existir
		$('#'+field_id+'_descrp').remove();
		
		// esconde campo com o id
		$(this).hide();
		
		// adiciona campo descricao
		$(this).parent().append(eos.template.field.autocomplete(field_input_descrp));
		
        var field_descrp = $("#"+field_id+"_descrp");
        
		/**
         *   Search path / Type
         *       Ajusta o arquivo de resposta da pesquisa
         */
        if(settings.sql_tbl === "empresa" || settings.sql_tbl === "usuario") {
			settings.type = settings.sql_tbl;
		}
        
        // controla o caso da pesquisa
        search_path = "/sys/DPAC/search/";
        switch(lc(settings.type)) {
            // usuario tbl
            case "usuarios":
            case "usuario":
            case "user":
            case "users":
                search_path += "usuario.cgi";
        		settings.show_img = true;
            break;
            // empresa tbl
            case "empresas":
            case "empresa":
                search_path += "empresa.cgi";
        		// settings.show_img = true;
            break;
            
            // padrao 
            case "":
                search_path = "/sys/cfg/DPAC/fieldAutoComplete.cgi";
            break;
        }
        
        // arquivo local
        if(settings.localFile !== false) {
            search_path = $('#AUX input[name="MODULO_PATH"]').val()+"/"+settings.localFile;
        }
        
        /**
         *  Source 
         *      cache or DB
         */
		if(DListCache[settings.sql_tbl]){ // cache
		    settings.source = DListCache[settings.sql_tbl];
		} else { // DB
		    settings.source  = search_path;
            settings.source += "?ID="+$('#AUX input[name="ID"]').val()+"&tbl="+settings.sql_tbl;
            // settings.source += "&sql="+settings.sql+"&order="+settings.sql_order;
            settings.source += "&order="+settings.sql_order;
            settings.source += "&rfield="+settings.sql_rfield+"&sfield="+settings.sql_sfield;
            // settings.source += "&term="+field_descrp.val();
            
            
            /* pode adicionar itens novos */
            if(settings.itemAdd) {
    			var url     = settings.source;
            
    			settings.source = function( request, response ) {
				
                    var add = {
                        "label" : "Adicionar novo item \""+field_descrp.val()+"\" ?",
                        "value" : field_descrp.val(),
                        "id"    : "new"
                    };
                   
    				$.ajax({
    					url      : url+"&term="+field_descrp.val(), // url+"?ID="+$('#AUX input[name="ID"]').val()+"&tbl="+settings.sql_tbl+"&sql="+settings.sql+"&order="+settings.sql_order+"&rfield="+settings.sql_rfield+"&sfield="+settings.sql_sfield+"&term="+field_descrp.val(),
    					dataType : "json",
    					success  : function( data ) { 
                        
                            var control = true;                        
                            // adiciona botao de novo item com o texto digitado
                            if(settings.itemAdd && data) {
                            
                                function clear(s){
                                    return s.toLowerCase().trim().replace(/\s+/g," ");
                                }
                                data.forEach(function(i){
                                    if(clear(i.label) === clear(field_descrp.val()) || clear(i.value) === clear(field_descrp.val())){
                                        control = false;
                                    }
                                });
                            
                                if(control) {
                                    data.push(add);
                                }
                            } else {
                                var data = [];
                        
                                // adiciona botao de novo item com o texto digitado
                                if(settings.itemAdd) {
                                    data.push(add);
                                }
                            }
                        
    						response( data );
    					},
    					error: function() { 
                                                
    						response( [] );
    					}
    				});
                };
            }
        
		}
    	
        
		/* configura campo descricao */
		field_descrp
			.prop({
				'autocomplete' : settings.autocomplete,
				'readonly'     : settings.readonly
			})
			/** 
             *  Auto Complete
             *      inicia o autocomplete (jquery)
             */
			.autocomplete({
				delay     : settings.delay,
				source    : settings.source,
				method    : "POST",
				minLength : settings.qtd,
                // autoFocus : true,
                
    			/* quando retornado da pesquisa */
                open: function( event, ui ) {
                    // console.log("open");
                },
                
    			/* quando retornado da pesquisa */
                search: function( event, ui ) {
                    // console.log("search");
                },
                
    			/* quando retornado da pesquisa */
                response: function( event, ui ) {
                    // console.log("search");
                },
                
    			/** 
                 *  Change
                 *      ao modificar
                 */
				change: function(event, ui) {
                    // console.log("change");
					/*
					if($(this).val() != "")
						$(this).removeClass("search").addClass("searchAdd"); // change icon for add
					else
						$(this).removeClass("searchAdd").addClass("search"); // change icon for search	
					*/
				},
    			/** 
                 *  Select
                 *      ao selecionar um item
                 */
				select: function(event, ui) { 
					// salva dados para acesso futuro
					field.data("fieldAutoCompleteSettings")["value"]  = ui.item.id;
					field.data("fieldAutoCompleteSettings")["descrp"] = ui.item.value;
                    field.data("fieldAutoCompleteSettings")["item"]   = ui.item;
					
					if(ui) {
						// retorno do id no campo hidden
						field.val(ui.item.id);
						
						// retorno da descricao
						field_descrp.val(ui.item.value);
                        
                        // jump next field
						if(settings.sql_nfield != "") {
							$("#"+settings.sql_nfield).focus();
                        }
					}		
                     
                    // se aceitar incluir itens limpa o valor dos campos
                    if((settings.allowEmpty || settings.clearOnExit) && event.which === 13) { 
                        event.preventDefault();
                    
                        field.fieldAutoComplete("reset");                    
                    } 
                    
                    // postFunction
        			if(isFunction(settings.postFunction)) { 
        				settings.postFunction.call(this, field.data("fieldAutoCompleteSettings"));
        			}
				}
                /* ,
				close: function(event, ui) { 
                    
					if(field.val()) {
        				if(isFunction(settings.postFunction)) { // postFunction
        					settings.postFunction.call(this,field.data("fieldAutoCompleteSettings"));
        				}
					}
                    
                } */
			})
			/** 
             *  Key Down
             *      quando alguma tecla é pressionada 
             
			.keydown(function(event) {
                
				if(settings.notab) { // Tab
					if(event.which === 9) {
						event.preventDefault();
                    }
				}
                    
				if(!field.val() && settings.allowEmpty && event.which === 13 && field_descrp.val()) { // enter
                    event.preventDefault();
                    
					if(isFunction(settings.postFunction)) {
						settings.postFunction.call(this,{ value : field_descrp.val(), descrp : field_descrp.val() });
					}
				}
                
                if((settings.allowEmpty || settings.clearOnExit) && event.which === 13) { // se aceitar incluir itens limpa o valor dos campos
                    event.preventDefault();
                    
                    field.fieldAutoComplete("reset");                    
                }
                            
			});
            */
                
            // adiciona imagem ao item
            if(settings.show_img) {
                field_descrp.data("autocomplete")._renderItem = function (ul, item) {
                        // var show_img = "/sys/cfg/DPAC/view_avatar.cgi?MD5="+item.img; // src das imagens dos usuarios
                        var show_img = "/img/usuario/"+item.img+".png"; // src das imagens dos usuarios
                        
                        var inner_html  = '<a>';
                            inner_html += ' <div class="fieldAutoComplete_list_item">';
                            inner_html += '     <div class="fieldAutoComplete_list_item_img">';
                            inner_html += '        <img src="' + show_img + '" style="height:30px">';
                            inner_html += '     </div>';
                            inner_html += '     <div class="fieldAutoComplete_list_item_descrp">' + item.label + '</div>';
                            // inner_html += '     <div class="description">' + item.DisplayName + '</div>';
                            inner_html += ' </div>';
                            inner_html += '</a>';
                            
                        return $("<li></li>")
                            .data("item.autocomplete", item)
                            .append(inner_html)
                            .appendTo(ul);
                };
            }
			// add class
			// .addClass("search"); 
            
            

		/**
         *  Create Function
         *      executa funcao apos criacao do objeto
         */
		if(isFunction(settings.createFunction)) {
			settings.createFunction.call(this);
        }

			
		/**
         *  Filled
         *      preenchido (filled), preenche campo ao criar
         */
		if(settings.filled != "") {
			field.val(settings.filled.id);
			$("#"+field_id+"_descrp").val(settings.filled.val);
		}	
			
			
	});	

};

})( jQuery );

