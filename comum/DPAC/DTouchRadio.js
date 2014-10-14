/**
 * 
 * Cria Grupos de rádio para uso Touch: 
 * Suporte a organização Horizontal / Vertical
 * Suporte a Accordion
 *
 * @example $("#ID").DTouchRadio({ addItem: "[{val:value,descrp:'description',img:'image'}]" });
 * @desc Uso Básico
 * @example $("#ID").DTouchRadio({ addItem: "[{val:(valor de retorno),descrp:(descrição do item),img:(imagem do item)}]" });
 * @desc addItem, img é opcional
 * @example $('#accordion').activate(1);
 * @desc Activate the second content of the Accordion contained in &lt;div id="accordion"&gt;.
 *
 * @param addItem Array (obrigatório) Ver: Exemplo addItem
 *
 * @type jQuery
 *
 * @name DTouchRadio
 * @cat Plugins/Accordion
 * @author DONE Tecnologia - Adriano Karkow Gaiatto Leal (http://gaiattos.com/akgleal.com)
 */

/* [INI]  DTouchRadio (by http://gaiattos.com/akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
		Javascript:
	
		CSS:
			/css/DPAC/DPAC.css
			/css/DPAC/DTouchRadio.css

    Opcoes:
		Enable			(Habilita / Desabilita)
		Button More		(Mostra botao mais)
		Orientation		(Horizontal / Vertical)
		Editable  		(opcao de icone de remocao de item)
		add Item 		(adiciona item /items and reload obj)
		Visible Items 	(0 = todos)
		
		***** localSource usar campos hidden com classe DTouchRadioLocalSourceValue / DTouchRadioLocalSourceDescrp *****
	
	Exemplo de uso:
		Javascript:
			$("#ID").DTouchRadio();
			$(".Class").DTouchRadio();
			
			$("#ID")..DTouchRadio(
				{
				options:values
				});
							
		HTML:
			<div id=ID class=Class></div>
*/

(function($){
	
$.fn.DTouchRadio = function(settings,value)
	{
	// se for um array ou estiver vazio ajusta variaveis
	if(isObject(settings) || !settings) {
        
		var settings = $.extend({
			orientation		: "horizontal",
            
            itemAdd         : "",           // adiciona itens no momento da inclusao
            itemEdit		: false,        // edita item
			itemDel         : false,        // remove item
            itemDelCheck    : true,         // pergunta se remove
            tbl             : false,        // gera apartir da tabela
            tblCache        : false,        // gera cache apartir da tabela 
            pick            : true,         // seleciona item clicado
            DTouchBox       : false,        // adiciona box depois da criacao DTouchBox : { box : DOM OBJ, title : 'text' }
            cacheFromFile   : false,        // adiciona cache apartir de uma tabela makeCache : { key : txt, value : txt / html }
            postFunction    : false,        // executa funcao apos gerar objeto
            
            type			: "",           // radio / select / 
            
			localSource		: false,        // busca dentro do html padroes pre definidos. ver *****
            enable			: true,
            buttonMore		: "",
            
            /* apos transicao para v3 remover editable, delNocheck */
            editable        : false,         // modificado para itemEdit
            delNoCheck		: false,        // modificado para itemDelCheck
            
            
            addItem			: "",
			editableItems	: false,
			visibleItems	: 5,            // padrao 5 itens se quiser mostrar tudo usar 0
			uncheck			: true,         // uncheck, executa funcao ao desmarcar item
			sortable		: false,
			title			: false,
			search			: false,    // pesquisa local
            searchFile      : false,    // pesquisa no banco: adiciona capacidade de buscar no banco de dados atraves do arquivo setado dentro do modulo 
            searchAdvanced  : false,    // adiciona botao para pesquisa avancada
			mw				: "80", 	// largura minima
            table           : false,    // gera lista a partir de uma tabela pre definida
            name            : "",       // AINDA NAO IMPLEMENTADO seta nome para o grupo de radios diferente do id
            unique          : false,    // nao permite adicionar mais de um item igual
            
			// opcoes 
			DTouchRadioClick	: '',   // clique, ao clicar no item DTouchRadioClick (deprecated remover as soon is possible)
			click				: '',   // clique, ao clicar no item
			postFunction		: '',   // executa funcao apos criar objeto
			DTouchRadioDblClick	: '',   // duplo clique, controle do clique duplo
            dblClick			: '',   // duplo clique, controle do clique duplo
			DTouchRadioUncheck	: '',   // uncheck, executa funcao ao desmarcar item
            // uncheck             : '',   // uncheck, executa funcao ao desmarcar item
			DTouchRadioValue	: '',
			DTouchRadioGetValue	: '',
			DTouchRadioSetValue	: '',
			value				: '',
			DTouchRadioReset	: '',
			DTouchRadioAddItems	: '',
			DTouchRadioAccordionContent	: '',
			DTouchRadioRefresh		: ''
			}, settings || {});
			
		}
	else
		{
        /*
        *   Settings Getter
        *       ajusta opcoes do objeto ja pronto
        */    
		switch(settings.lc())
			{
			// DTouchRadioSetValue: Seta Valor ---------------------------
			case "setval":
			case "setvalue":
			case "dtouchradiosetvalue":
				
			case "val":
			case "getval":
			case "value":
			case "getvalue":
			case "dtouchradiogetvalue":
				
				// retorna o valor do radio grupo se segunda opcao for vazia
                // return $(this).each(function() {
				if(!value) {
					try {
                        return $(this).data("DTouchRadioSettings")["value"];
                    } catch(err) { 
                        return "";
                    }
                }
                    // });
                
				// soma contador de vezes que foi modificado o objeto on the fly
				$(this).data("DTouchRadioSettings")["DTouchRadioSetValue"] = $(this).data("DTouchRadioSettings")["DTouchRadioSetValue"] + 1;
			
				// modifica valor do objeto low-level
				$(this).data("DTouchRadioSettings")["DTouchRadioValue"] = value;
				$(this).data("DTouchRadioSettings")["value"] = value;

				// altera o valor visual
				DTouchRadioSetValue($(this));
				return true;
				
			break;

			// DTouchRadioReset: Limpa Radio Group ---------------------------
			case "reset":
			case "dtouchradioreset":
				
				// soma contador de vezes que foi modificado o objeto on the fly
				// $(this).data("DTouchRadioSettings")["DTouchRadioSetValue"] = parseInt($(this).data("DTouchRadioSettings")["DTouchRadioSetValue"]) + 1;
				
				// remover todos os itens do radio group
				if(value == "hard") {
					// remove itens
					$(this).removeData("DTouchRadioSettings");
					
					// limpa conteudo visual
					$(this).html("");
					
					return true;
				} else if(value == "content") {
					// remove itens
					try {
                        $(this).data("DTouchRadioSettings")["DTouchRadioAddItems"] = "";
                    } catch(err) { 
                        console.log(err);
                    }
                    
					// remove itens
					try {
                        $(this).data("DTouchRadioSettings")["itemAdd"] = "";
                    } catch(err) { 
                        console.log(err);
                    }
					
					// limpa conteudo visual
					$(this).empty();
					
					return true;
				}
                
				
				// altera o valor visual
				DTouchRadioReset($(this));
				return true;
			
			break;
			
			// DTouchRadioAccordionContent: Adiciona conteudo ao radio especifico ---------------------------
			case "dtouchradioaccordioncontent":
			
				// se valor for vazio
				if(value == "")
					{
					alert("Devil's: valor nao pode ser vazio !!");
					return false;
					}

				// retorna o valor do radio grupo
				$(this).data("DTouchRadioSettings")["DTouchRadioAccordionContent"] = value;
				
				// adiciona conteudo ao accordion especifico
				DTouchRadioAccordionContent($(this));
			
			break;
			
			// DTouchRadioRefresh: Refresh no grupo de radio frequente usado em tables -----------------------
			case "refresh":
			case "dtouchradiorefresh":

				if($(this).data("DTouchRadioSettings")["type"] == "table")
					$('#'+$(this).prop("id")+'_tb').dataTable().fnDraw();
				else
					{
					console.log("Opção usada somente para TABLES");
					alerta("Devils: Opção usada somente para TABLES");
					}
				
			break;
			
			// add Item, adiciona item
			case "additem":
			
                // console.log($(this).data("DTouchRadioSettings")["DTouchRadioAddItems"]);
                // console.log(value);
            
				// se objeto nao vazio
				if($(this).data("DTouchRadioSettings")["DTouchRadioAddItems"] !== "") {
                    
                    // se for item unico testa consistencia 
                    if($(this).data("DTouchRadioSettings")["unique"]){
                        var yep = false;
                        var a = $(this).data("DTouchRadioSettings")["DTouchRadioAddItems"];
                        a.forEach(function(i){
                           if(i.val === value.val || i.descrp.lc() === value.descrp.lc()){
                               yep = true;
                           }
                        }); 
                                                
                        if(yep) {
                            $.DDialog({
                                type    : "error",
                                message : "Item já adicionado"
                            });
                            
                            return true;
                        }
                    }
                                    
                    /* recupera itens modificados do objeto
                    var items_changed = [];
                    $(this).find(".DTouchRadio_items").each(function(){
                        items_changed.push({
                            val    : $(this).find(".input_hidden").val(),
                            descrp : $(this).find(".DTouchRadio_descrp").html(),
                        });
                        // console.log($(this));
                    });
                    // input_hidden
                    // DTouchRadio_descrp
                    $(this).data("DTouchRadioSettings")["DTouchRadioAddItems"] = items_changed;
                    
                    
                    console.log($(this).data("DTouchRadioSettings")["DTouchRadioAddItems"]);
                    
                    */
                    // adiciona item
                    $(this).data("DTouchRadioSettings")["DTouchRadioAddItems"].push(value);
                    
                    
                    // adiciona o item sem mexer no resto do radio
                    DTouchRadioAddItemsNew($(this),value);
                    return true;
                    
				} else {
					$(this).data("DTouchRadioSettings")["DTouchRadioAddItems"] = [value];
                }
				
				// limpa variavel de adicao de itens
				$(this).data("DTouchRadioSettings")["addItem"] = "";
				
                // limpa container
                $(this).empty();
                
				// adiciona itens
				DTouchRadioAddItems($(this));

				// aguarda o retorno da criacao para gerar o objeto
				return true;
				
			break;
            
            
			// add Item, adiciona item
			case "itemadd":
                
        		/**
                 *  itemAdd
                 *      adiciona item(s)
                 */
                /*
        		if(settings.itemAdd) {
        			itemAdd($(this), settings.itemAdd);
        			return true;
        		}
                */
                
				// se objeto nao vazio
				if($(this).data("DTouchRadioSettings")["itemAdd"] !== "") {
                    
                    // se for item unico testa consistencia 
                    if($(this).data("DTouchRadioSettings")["unique"]){
                        var yep = false;
                        var a = $(this).data("DTouchRadioSettings")["itemAdd"];
                        a.forEach(function(i){
                           if(i.val === value.val || i.descrp.lc() === value.descrp.lc()){
                               yep = true;
                           }
                        }); 
                                                
                        if(yep) {
                            $.DDialog({
                                type    : "error",
                                message : "Item já adicionado"
                            });
                            
                            return true;
                        }
                    }
                    // adiciona item
                    $(this).data("DTouchRadioSettings")["itemAdd"].push(value);
				} else {
					$(this).data("DTouchRadioSettings")["itemAdd"] = [value];
                }
				
				// limpa variavel de adicao de itens
				$(this).data("DTouchRadioSettings")["itemAdd"] = "";
				
                // limpa container
                $(this).html("");
                
				// adiciona itens
				DTouchRadioAddItems($(this));

				// aguarda o retorno da criacao para gerar o objeto
				return true;
				
			break;
			
            case "slider" :
            case "slide" :
                	var settings = $(this).data("DTouchRadioSettings"); // acesso as configuracoes atuais do objeto
                	var val = $(this).data("DTouchRadioSettings")["value"]; // acesso as configuracoes atuais do objeto
	                var obj = $(this);
                    
                    if(!value) {
                        value = 0;
                    }
                    
                	// remove marcacao 
                	obj.children("div").removeClass("DTouchRadio_selected");
    
                	// verifica qual objeto sera marcado
                	var i = 0;
                	var it = obj.find("input[type=radio]").length - 1;
                	obj.find("input[type=radio]").each(function(){
        
                    	if($(this).val().toString() === val.toString()){
                			$(this).prop("checked", true); // marca radio escondido
            
                            // elemento clicado
                			$(this).parent("div")
                                .addClass("DTouchRadio_selected")  // marca linha selecionada
                                .focus();                          // seta focus para objeto marcado para funcionamento da navegacao por setas
				
                			// slide slider
                			if(settings.orientation === "horizontal") {
                				var m   = $(this).parent("div")[0].offsetWidth,
                                    max = $("#DTouchSlider_"+obj.prop("id")).slider("option", "max");
                			} else {
                				var m   = $(this).parent("div")[0].offsetHeight,
                                    max = $("#DTouchSlider_"+obj.prop("id")).slider("option", "max");
                			}
                            
                			$("#DTouchSlider_"+obj.prop("id")).slider("value", (max - (i * (max / it))).toFixed());
			
                            return false; // para laco for
                		}
            
                		i++;
                	});	
            break;
            
			// ao redimensionar a tela
			case "resize": 
				DTouchRadioResize($(this));
			break;
            
            // disable
            case "disable" :
                $(this).data("DTouchRadioSettings")["click"] = "off";
                return true;
            break;
            
            // enable
            case "enable" :
                $(this).data("DTouchRadioSettings")["click"] = "";
                return true;
            break;
			}
		
		
		// retorna / seta demais opcoes que nao necessitam de tratamento
		if(value == "")
			{
			return $(this).data("DTouchRadioSettings")[settings];
			}
		else
			{
			$(this).data("DTouchRadioSettings")[settings] = value;
			return true;
			}
		}
	
    
        /* V3 [INI] ______________________________________________________________________________  */
        /** 
         *  itemAdd (function)
         *      Adiciona item
         */
        function itemAdd(obj,items) {
            
            // limpa controles
            obj.html("");
            obj.data("DTouchRadioSettings")["itemAdd"] = "";
            
            // adiciona itens
            items.forEach(function(i){ 
                
                if(i.img) { // imagem, se existir
                    var img = "<img src='" +i.img +"' />";
                } else {
                    var img = "";
                }
                            
                var r  = "<div class='DTouchRadio_items' tabindex='0'>";
                    r += "   <input type='radio' name='"+ obj.prop("id") +"_radios' value='"+ i.val +"' class='input_hidden' />";
                    r +=     img;
                    r += "   <span class='DTouchRadio_descrp'>"+ i.descrp +"</span>";
                    r += "</div>";
               
               obj.append(r);
            });
            
        	// atualiza radio
        	obj.DTouchRadio(obj.data("DTouchRadioSettings"));
        }
    
        /** 
         *  itemDel (function)
         *      Deleta item
         */
        function itemDel(obj,item) { 
            
            var items    = obj.data("DTouchRadioSettings")["DTouchRadioAddItems"]
            ,   item_val = item.find(".input_hidden").val();
            
            // remove item
            var c = 0;
            items.forEach(function(i){  
                                
                if(i.val.toString() === item_val) {
                    delete items[c];  // low level
                    item.remove();    // html 
                }
                
                c += 1;
            });
        }
        
        
        
        
        
        
        /* ****
            funcao para adicionar mais itens sem perder nenhuma propriedade de campos 
                internos que possam estar na linha do radio, 
        
            converter para versa 3 do core
        ***** */
        function DTouchRadioAddItemsNew(obj,item) {
        	var showImg  = "";
        	var settings = obj.data("DTouchRadioSettings"); // acesso as configuracoes atuais do objeto
        	// var items    = settings.DTouchRadioAddItems; 

         
        		if(item['descrp'] === "") { // descricao, se nao tiver descricao adiciona valor do item como 
        			item['descrp'] = item['val'];
                }
        
        		if(item['img']) { // imagem, se existir
        			showImg = "<img src='"+item['img']+"' />";
                }
        

        		obj.append("<div class='DTouchRadio_items DTouchRadio_items_new' tabindex='0'><input type='radio' name='"+obj.attr("id")+"_radios' value='"+item['val']+"' class='input_hidden' />"+showImg+"<span class='DTouchRadio_descrp'>"+item['descrp']+"</span></div>");
                //}
        
        
        
        
        		// ao selecionar
        		obj.find(".DTouchRadio_items_new").addClass("DTouchRadio").click(function() {
                    // nao faz nada ao clicar
                    if(settings.click !== "off") {
                
        				// uncheck item
        				if($(this).hasClass("DTouchRadio_selected") === true && settings.uncheck !== false) {
        					DTouchRadioReset(settings.radios);
				
        					// executa funcao de uncheck 
        					if(isFunction(settings.uncheck)) {
        						settings.uncheck.call(this);
                            }
				
        					return true;
        				}
				        
                        // console.log($(this));
                        
        				// remove classe de todos os radios
        				settings.radios.children("div").removeClass("DTouchRadio_selected");	
			    
        				// marca radio clicado
        				$(this).addClass("DTouchRadio_selected").find(":radio").attr("checked", true);
                        
                        //console.log($(this).addClass("DTouchRadio_selected").find(":radio").prop("checked"));
                        
        				// seta valor
                        // console.log($(this).addClass("DTouchRadio_selected").find(":radio").val());
                        settings.radios.data("DTouchRadioSettings")["value"] = $(this).addClass("DTouchRadio_selected").find(":radio").val();
                        settings.radios.data("DTouchRadioSettings")["DTouchRadioValue"] = $(this).addClass("DTouchRadio_selected").find(":radio").val();
        				// settings.radios.DTouchRadio("DTouchRadioSetValue",DTouchRadioGetValue(settings.radios));
            
        				// Clique unico
                        if(isFunction(settings.click)) {
        					settings.click.call(this, settings.radios.data("DTouchRadioSettings"));
                        }
                    }
        		});
        
        
        
        
        		/**
                 *  itemDel
                 *      remove item
                 */
        		if(settings.itemDel) {
            
        			// botao
        			obj.find(".DTouchRadio_items_new").each(function() { 
                        $(this).append("<p class='DTouchRadioRemoveItem'></p>");
        			});
			
        			// acao
        			obj.find(".DTouchRadioRemoveItem")
                        .off("click")
                        .click(function(event) {
    				
            				event.stopPropagation(); // stop click propagation
					
                            // item
            				var item       = $(this).parents(".DTouchRadio_items");
				
                            // confirmacao de exclusao
            				if(settings.itemDelCheck) {
            					$.DDialog({
            					    type    : "confirm",
                                    message : "Deseja remover o item selecionado? <br><br> essa ação é irreversível !",
                                    btnYes  : function(){ 
                            
                    					if(isFunction(settings.itemDel)) { // funcao se delecao positiva
                    						settings.itemDel.call(this, item.find(".input_hidden").val());
                    					}
                            
                    					itemDel(settings.radios,item);
                                    }
            					})
                    
            				} else {
                        
            					if(isFunction(settings.itemDel)) { // funcao se delecao positiva
            						settings.itemDel.call(this, item.find(".input_hidden").val());
            					}
                        
            					itemDel(settings.radios,item);
                            }
            		});
        		}
                
        		// Adiciona classe DTouchRadioContainer na div PAI
        		// obj.addClass("DTouchRadioContainer DTouchRadioContainer_"+settings.orientation);
		
        		// Ajuste da orientacao do objeto
        		obj.find(".DTouchRadio_items_new").addClass(" DTouchRadio_"+settings.orientation);
		
        		// pega a largura do item para rolagem horizontal
        		settings.radios_item_width = obj.children("div:first-child").width();
		
        		// seta valor largura minima do objeto
        		if(obj.children("div:first-child").css("min-width"))
        			{
        			settings.mw = obj.children("div:first-child").css("min-width");
        			obj.data("DTouchRadioSettings")["mw"] = settings.mw.replace("px","");
        			}
		
        		// dimensoes, ajusta
        		DTouchRadioResize(obj);
                
                
                // remove classe apos ajustes
                obj.find(".DTouchRadio_items_new").removeClass("DTouchRadio_items_new");

        }
        /* V3 [END] ______________________________________________________________________________  */
    
    
    
    
    
    
    	
	/**
     *   Retorno do Objeto 
     *       retorna objeto pronto
     */
	return this.each(function()
		{ 
        // ajustes para novo padrao de opcoes
        // (deprecated remover as soon is possible)
        if(settings.click === ""){
            settings.click = settings.DTouchRadioClick;
        }
        /*
        if(isFunction(settings.dblClick)){
            settings.DTouchRadioDblClick = settings.dblClick;
        }
        */
        if(isFunction(settings.DTouchRadioUncheck)){
            settings.uncheck = settings.DTouchRadioUncheck;
        }
        
        /*
        *   ajuste da orientacao do objeto acusando erro ???
        *   erro posivelmente identificado
        *
        console.log("DTouchRadio settings.orientation "+settings.orientation); 
        if(!settings.orientation){
            settings.orientation = "horizontal";
        }
        */
        
		// se nao tiver id gera aleatorio
		if(!$(this).prop("id")) {
			$(this).prop("id", $("div").length+1);
		}
        
		settings.radios = $(this);
		settings.radios_id = $(this).prop("id");
		settings.radios_qtd = $(this).children("div").length; // quantidade de itens do radio
		
		/**
         *   Title 
         *       adiciona titulo ao objeto
         */
		if(settings.title !== false){
			settings.radios.prepend("<div class='DTouchRadio_title DTouchRadio_nosearch'>"+settings.title+"</div>"); 
		}
        
        
        /**
         *  Gera objeto apartir de tabela pre definida
         */
        if(settings.table !== false){
            settings.addItem = eos.core.getList(settings.table);
            settings.table = false; // limpa variavel para evitar loop
        }
        
		/**
         *   search
         *       pesquisa nos itens 
         *       capacidade de pesquisa avancada
         */
		if(settings.search !== false){
            
			var fieldSearch  = "<div class='DTouchRadio_nosearch DTouchRadio_search'>";
                fieldSearch += "    <div>";
				// fieldSearch += "	    <div class='icon_clear DTouchRadio_search_icon_clear'></div>";
				fieldSearch += "	    <input type='text' id='"+settings.radios_id+"_search_field' placeholder='Pesquisar'>";
				// fieldSearch += "	    <div>pesquisa local: </div>";
                fieldSearch += "    </div>";
                fieldSearch += "    <div class='DTouchRadio_search_adv_form'></div>";
				fieldSearch += "</div>";
				fieldSearch += "<div class='DTouchRadio_nosearch icon_search DTouchRadio_search_icon'></div>";
                // fieldSearch += "<div class='DTouchRadio_nosearch icon_search DTouchRadio_search_icon'></div>";
				
			settings.radios.prepend(fieldSearch); // adiciona campo de pesquisa
            
            // ajusta botoes da linha da pesquisa
            if(settings.searchAdvanced !== false) { // se existir pesquisa avancada (formulario)
                var opts  = "<div class='DTouchRadio_search_icon_container'>";
                    opts += "   <div class='DTouchRadio_search_icon_clean' title='Limpar'><span></span></div>";
                    opts += "   <div class='DTouchRadio_search_icon_clear DTouchRadio_search_icon_clear_adv' title='Fechar'><span></span></div>";
                    opts += "   <div class='DTouchRadio_search_icon_adv' title='Pesquisa avançada'><span></span></div>";
                    opts += "</div>";
                    
                // adiciona campo de pesquisa e botoes de funcionamento da pesquisa avancada
                eos.template.field.search($("#"+settings.radios_id+"_search_field"), opts); // ajusta campo      
                    
                // ao clicar na pesquisa avancada  mostra formulario !
                settings.radios.find(".DTouchRadio_search_icon_adv").click(function(e){   
                    settings.radios.find(".DTouchRadio_search").toggleClass("DTouchRadio_search_adv");
                    $(this).find("span").toggleClass("DTouchRadio_search_icon_adv_arrow_up");
                    
                    if(isFunction(settings.searchAdvanced)){ // se vier uma funcao na pesquisa
                        settings.searchAdvanced.call(this,settings.radios.find(".DTouchRadio_search .DTouchRadio_search_adv_form"));
                    }
                });
                
                // adiciona tooltip
                settings.radios.find(".DTouchRadio_search_icon_container div").tooltip();
                
                // formulario de pesquisa avancada
                if(isObject(settings.searchAdvanced)){ 
                    // settings.radios.find(".DTouchRadio_search .DTouchRadio_search_adv_form")
                      //  .html(settings.searchAdvanced.show());
                }
                
                // adiciona botao de pesquisar no banco
                eos.menu.action.new({ // executar
                    id       : "icon_DTouchRadio_search_adv",
                    title    : "pesquisar",
                    subtitle : "db",
                    super    : true,
                    click    : function(){
                		$.DActionAjax({
                			action: settings.searchFile+".cgi",
                			req: "&search="+$("#"+settings.radios_id+"_search_field").val(),
                		});
                    }
                });  
                eos.menu.action.hide("icon_DTouchRadio_search_adv"); // esconde botao apos criar
                
            } else { // pesquisa simples local e banco se for o caso
                var opts  = "<div class='DTouchRadio_search_icon_container'>";
                    opts += "   <div class='DTouchRadio_search_icon_clear'><span></span></div>";
                    opts += "</div>";
                    
                // adiciona campo de pesquisa e botoes de funcionamento da pesquisa avancada
                eos.template.field.search($("#"+settings.radios_id+"_search_field"), opts); // ajusta campo      
            }
            
            // inicializa pesquisa
			$(this).DSearch({
				linha:'DTouchRadio',
				campo: $("#"+settings.radios_id+"_search_field"),
				exclude: "DTouchRadio_nosearch"
			});
			
			// mostra pesquisa
			$(this).find(".DTouchRadio_search_icon").click(function(){
				// settings.radios.find(".DTouchRadio_search").toggle("slide", { direction: "right" }, 500);
                settings.radios.find(".DTouchRadio_search")
                    .addClass("DTouchRadio_search_visible");
                
                eos.menu.action.show("icon_DTouchRadio_search_adv"); // mostra botao
                
                // settings.radios.find(".DTouchRadio_search input[type=text]:first").focus();
                
                // $(this).delay(1000,function(){ settings.radios.find(".DTouchRadio_search input[type=text]:first").focus(); });
			});
				
			// esconde pesquisa
			$(this).find(".DTouchRadio_search_icon_clear").click(function(){
                
                settings.radios.find(".DTouchRadio_search").removeClass("DTouchRadio_search_visible");
                settings.radios.find(".field_search").val("").trigger("keyup"); // limpa pesquisa
                
                eos.menu.action.hide("icon_DTouchRadio_search_adv"); // esconde botao apos criar
                
                /*
				settings.radios.find(".DTouchRadio_search").toggle("slide", { direction: "right" }, 500, function()
					{
					// limpa pesquisa
					settings.radios.find(".field_search").val("").trigger("keyup");
					});
                */
			});
            
            // busca dados no arquivo setado
            $("#"+settings.radios_id+"_search_field").keydown(function(e){
                if(e.keyCode === 13 && settings.searchFile !== false){
                    e.preventDefault();
                    
            		$.DActionAjax({
            			action: settings.searchFile+".cgi",
            			req: "&search="+$("#"+settings.radios_id+"_search_field").val(),
            		});        
                }
            });
		}
		// [END] search, pesquisa local nos itens -----
			
            
            
            
		/** 
         *   Data
         *       salva low level opcoes setadas do objeto para uso futuro
         */
		if(isObject(settings)) {
			$(this).data("DTouchRadioSettings", settings);
		}
        
        
		/** 
         *   Items
         *       adicionar item / items
         */
		if(isArray(settings.addItem) && settings.addItem.length === 0) { // se for um array vazio passado limpa o radio
			// remove itens
			$(this).removeData("DTouchRadioSettings");
			
			// limpa conteudo visual
			$(this).html("");
			
			return true;
            
		} else if(settings.addItem) {
			
			$(this).html(""); // limpa DRadio para atualizar conteudo 
			
			// se for um accordion destroy objeto
			if($(this).hasClass('ui-accordion')) 
			    $(this).accordion('destroy');
			
			// ajusta para criacao
			$(this).data("DTouchRadioSettings")["DTouchRadioAddItems"] = settings.addItem;
			
			// limpa variavel de adicao de itens
			$(this).data("DTouchRadioSettings")["addItem"] = "";
			
			// adiciona itens
			DTouchRadioAddItems($(this));
			
			// aguarda o retorno da criacao para gerar o objeto
			return true;
            
		} else {
            
			if(settings.localSource === true)	
				{
				console.log(settings.localSource);
				}
			// obj.append("<div><input type='radio' name='"+obj.attr("id")+"_radios' value='"+items[f]['val']+"' />"+showImg+"<span class='DTouchRadio_descrp'>"+items[f]['descrp']+"</span></div>");
		}
		
        
		// corrige largura do container ao iniciar (bug: conhecido quando regera o objeto que ja foi setado com largura maxima)
		$(this).css("width","auto");
		
		// se habilitado botao mais
		if(isFunction(settings.buttonMore) === true)
			{
			$(this)
				.append("<div class='DTouchRadioButtonMore'>Limpar Seleção</div>")
				.show();
			
			settings.buttonMore.call(this);
			}
			
		// Adiciona classe DTouchRadioContainer na div PAI
		$(this).addClass("DTouchRadioContainer DTouchRadioContainer_"+settings.orientation);
		
		// Ajuste da orientacao do objeto
		$(this).children("div").addClass(" DTouchRadio_"+settings.orientation);
		
		// pega a largura do item para rolagem horizontal
		settings.radios_item_width = $(this).children("div:first-child").width();
		
		// seta valor largura minima do objeto
		if($(this).children("div:first-child").css("min-width")) {
			settings.mw = $(this).children("div:first-child").css("min-width");
			$(this).data("DTouchRadioSettings")["mw"] = settings.mw.replace("px","");
		}
		
		// dimensoes, ajusta
		DTouchRadioResize($(this));
		
        
        
		/**
         *  Editable
         */
		if(settings.editable) {
            
			// insere botao de exclusao se nao existir
			$(this).find(".DTouchRadio_descrp").each(function() { 
				// pega ultima div 
				radio_del = $(this).find("div").last();
								
				// se nao achar ultima div ajusta para mostrar botao de deletar mesmo assim
				if(radio_del.length == 0) {
					radio_del = $(this);
                }
				
				if(radio_del.find(".DTouchRadioRemoveItem").length == 0) {
					radio_del.append("<p class='DTouchRadioRemoveItem'></p>");
                }
			});
			
			// Remove Radio Item 
			$(this).find(".DTouchRadioRemoveItem")
                .off("click")
                .click(function(event) {
    				// evita que o trigger click da linha seja executado
    				event.stopPropagation();
							
    				// ajusta obj (item linha) para exclusao
    				var obj      = $(this);
				
    				// confirmacao de exclusao
    				if(!settings.delNoCheck) {
    					$.DDialog({
    					    type    : "confirm",
                            message : "Deseja remover o item selecionado? <br><br> essa ação é irreversível !",
                            btnYes  : function(){ 
                            
            					if(isFunction(settings.editable)) { // envia o valor do objeto clicado para delecao
            						settings.editable.call(this, obj.parents(".DTouchRadio_items").find("input:radio[name='"+settings.radios_id+"_radios']").val());
            					}
                            
            					// remove objeto low level e html
            					DTouchRadioDelItems(obj);
                            }
    					})
                    
    				} else {
    					DTouchRadioDelItems(obj);
                    }
    		});
		}
        
        
        
        /* V3 [INI] ______________________________________________________________________________  */
        /**
         *  Gera objeto apartir de tabela pre definida
         */
        if(settings.tbl){
            settings.itemAdd = eos.core.getList(settings.tbl);
            settings.tbl     = false; // limpa variavel para evitar loop
        }
        
        /**
         *  Gera objeto + cache apartir de arquivo predefinido
         */
        if(settings.cacheFromFile){
            settings.itemAdd       = eos.core.getList(settings.cacheFromFile);
            settings.cacheFromFile = false; // limpa variavel para evitar loop
        }
        
		/**
         *  itemAdd
         *      adiciona item(s)
         */
		if(settings.itemAdd) {
			itemAdd($(this), settings.itemAdd);
			return true;
		}
        
        
		/**
         *  itemDel
         *      remove item
         */
		if(settings.itemDel) {
            
			// botao
			$(this).find(".DTouchRadio_descrp").each(function() { 
                $(this).append("<p class='DTouchRadioRemoveItem'></p>");
			});
			
			// acao
			$(this).find(".DTouchRadioRemoveItem")
                .off("click")
                .click(function(event) {
    				
    				event.stopPropagation(); // stop click propagation
					
                    // item
    				var item       = $(this).parents(".DTouchRadio_items");
				
                    // confirmacao de exclusao
    				if(settings.itemDelCheck) {
    					$.DDialog({
    					    type    : "confirm",
                            message : "Deseja remover o item selecionado? <br><br> essa ação é irreversível !",
                            btnYes  : function(){ 
                            
            					if(isFunction(settings.itemDel)) { // funcao se delecao positiva
            						settings.itemDel.call(this, item.find(".input_hidden").val());
            					}
                            
            					itemDel(settings.radios,item);
                            }
    					})
                    
    				} else {
                        
    					if(isFunction(settings.itemDel)) { // funcao se delecao positiva
    						settings.itemDel.call(this, item.find(".input_hidden").val());
    					}
                        
    					itemDel(settings.radios,item);
                    }
    		});
		}
        /* V3 [END] ______________________________________________________________________________  */
        
        

		// seta valor inicial
		if(settings.value != "")
			{
			// settings.radios.data("DTouchRadioSettings")["value"] = settings.value
			DTouchRadioSetValue(settings.radios);
			}
		
		// TYPE, ajusta configuracao com base no tipo
		switch(settings.type) {
            
			/**
             *  list / vazio / lista de radios
             */
			case "":
            case "single":
				// ao selecionar
				$(this).children("div").not(".DTouchRadio_nosearch").addClass("DTouchRadio").click(function() {
                    // nao faz nada ao clicar
                    if(settings.click !== "off") {
                        
    					// uncheck item
    					if($(this).hasClass("DTouchRadio_selected") === true && settings.uncheck !== false) {
    						DTouchRadioReset(settings.radios);
						
    						// executa funcao de uncheck 
    						if(isFunction(settings.uncheck)) {
    							settings.uncheck.call(this);
                            }
						
    						return true;
    					}
						
    					// remove classe de todos os radios
    					settings.radios.children("div").removeClass("DTouchRadio_selected");	
					    
        				// marca radio clicado
        				$(this).addClass("DTouchRadio_selected").find(":radio").attr("checked", true);
                        
        				// seta valor
        				settings.radios.DTouchRadio("DTouchRadioSetValue",DTouchRadioGetValue(settings.radios));
                    
    					// Clique unico
                        if(isFunction(settings.click)) {
    						settings.click.call(this, settings.radios.data("DTouchRadioSettings"));
                        }
                    }
				});
			
				// se for sortable entre os radios
				if(settings.sortable === true) {
					$(".DTouchRadio_items").parent()
						.sortable(
							{
							connectWith: $(".DTouchRadio_items").parent(),
							dropOnEmpty: true,
							receive: function(event, ui) 
								{
								ui.item.find("input:radio").prop("name", $(this).prop("id")+"_radios");								
								}
							})
						.disableSelection();
				}
                /*
                // nao faz nada ao clicar
                if(settings.click === "off") {
                    settings.radios.children("div").off("click"); // desabilita click
                }
                */
			break;
            
            
			// Table: adiciona tabela ---------------------------
			case "table":
			
				$(this).find("table").DGrid();
				
				// setta Click ao selecionar
				$(this).find("table tbody tr").click(function()
					{ 					
					// marca radio
					$(this).find(":radio").attr("checked", true);
					
					// seta valor
					settings.radios.DTouchRadio("DTouchRadioSetValue",$(this).find("td:first").html());
					
					// executa funcao ao clicar se funcao existir
					if(isFunction(settings.click))
						settings.click.call(this, settings.radios.data("DTouchRadioSettings"));
					else if(isFunction(settings.click) === true) // ajustar -> DTouchRadioClick para click (futuro)
						settings.click.call(this, settings.radios.data("DTouchRadioSettings"));
					});
				
				// setta Duplo Click ao selecionar
				$(this).find("table tbody tr").dblclick(function()
					{ 					
					// marca radio
					$(this).find(":radio").attr("checked", true);
					
					// seta valor
					settings.radios.DTouchRadio("DTouchRadioSetValue",$(this).find("td:first").html());
					
					// executa funcao ao clicar se funcao existir
					if(isFunction(settings.click))
						settings.click.call(this, settings.radios.data("DTouchRadioSettings"));
					else if(isFunction(settings.click) === true) // ajustar -> DTouchRadioClick para click (futuro)
						settings.click.call(this, settings.radios.data("DTouchRadioSettings"));
					});
					
			break;
			}
            
            
            
            
    		/** 
             *   post Function
             *       executa funcao apos criar objeto
             */
    		if(isFunction(settings.postFunction)){
    			// settings.postFunction.call(this, settings.radios.data("DTouchRadioSettings"));
                settings.postFunction.call(this, settings.radios);
    		}
            
            
    		/** 
             *   DTouchBox
             *       cria box depois de gerar o radio
             */
            if(isObject(settings.DTouchBox)){
                
                settings.DTouchBox.box.DTouchBoxes({
                    title : settings.DTouchBox.box.title,
                    postFunction : function(){
                        settings.radios.DTouchRadio("resize");
                    }
                });
                // settings.radios.DTouchRadio("resize");
                // $(this).DTouchRadio("resize");
            }
            
            
    		/** 
             *  Post Function
             *       executa funcao apos criar o objeto
             */
            if(isFunction(settings.postFunction)){
                settings.postFunction.call(this);
            }
            
            
    		/** 
             *  ajusta radio
             
            console.log($(this));
            DTouchRadioResize($(this));
            */
		});
	};

})( jQuery );


/* 
*   DTouchRadioSetValue
*       Set Value 
*           Seta valor do grupo de radio e marca o item clicado
*/
function DTouchRadioSetValue(obj){
	var settings = obj.data("DTouchRadioSettings"); // acesso as configuracoes atuais do objeto
	var val = obj.data("DTouchRadioSettings")["value"]; // acesso as configuracoes atuais do objeto
	    
	// remove marcacao 
	obj.children("div").removeClass("DTouchRadio_selected");
    
	// verifica qual objeto sera marcado
	var i = 0;
	var it = obj.find("input[type=radio]").length-1;
	obj.find("input[type=radio]").each(function(){
        
    	if($(this).val().toString() === val.toString()){
			$(this).prop("checked", true); // marca radio escondido
            
            // elemento clicado
			$(this).parent("div")
                .addClass("DTouchRadio_selected")  // marca linha selecionada
                .focus();                          // seta focus para objeto marcado para funcionamento da navegacao por setas
				
			// slide slider
			if(settings.orientation === "horizontal") {
				var m   = $(this).parent("div")[0].offsetWidth,
                    max = $("#DTouchSlider_"+obj.prop("id")).slider("option", "max");
			} else {
				var m   = $(this).parent("div")[0].offsetHeight,
                    max = $("#DTouchSlider_"+obj.prop("id")).slider("option", "max");
			}
                
			// $("#DTouchSlider_"+obj.prop("id")).slider("value", ((it * m) - ((i+1) * m)));
			$("#DTouchSlider_"+obj.prop("id")).slider("value", (max - (i * (max / it))));
			
            
            return false; // para laco for
		}
            
		i++;
	});	
}


/* 
*   DTouchRadioGetValue
*       Get Value
*         Pega valor atual do grupo
*/
function DTouchRadioGetValue(obj){
	return $("input:radio[name='"+obj.prop("id")+"_radios']:checked").val();
}



/* 
*   DTouchRadioReset
*       Reset
*           Reseta valor do objeto, desmarca o objeto selecionado
*/
function DTouchRadioReset(obj){
	var settings = obj.data("DTouchRadioSettings"); // acesso as configuracoes atuais do objeto
	
	// modifica valor do objeto low-level
	obj.data("DTouchRadioSettings")["DTouchRadioValue"] = "";
	obj.data("DTouchRadioSettings")["value"] = "";
	
	// remove marcacao 
	obj.children("div").removeClass("DTouchRadio_selected");
	
	// remove checked do grupo
	$("input:radio[name='"+obj.prop("id")+"_radios']:checked").prop("checked",false);
    
    document.activeElement.blur(); // remove focus
}

// [INI] DTouchRadioDelItem: Deleta itens no radio group ----------------------------------------------------------------
function DTouchRadioDelItems(obj)
	{
	// ajusta variaveis
	var radio_id = obj.parents(".DTouchRadioContainer").prop("id");
	var radio_item = obj.parents(".DTouchRadio_items");
	var valor = radio_item.find("input:radio[name='"+radio_id+"_radios']").val();
		
	// remove item low level
	var items = $("#"+radio_id).data("DTouchRadioSettings")["DTouchRadioAddItems"];
	for(var i in items)
		{
		if(items[i].val == valor)
			{
			delete items[i];
			radio_item.remove();
			}
		}
	}



/* 
*   DTouchRadioAddItem: 
*
*       Adiciona itens no radio group
*          items = {
*               val    : $id,
*               descrp : '$descrp' // aceita html 
*               img    : $imagem   // imagem se existir
*               }
*
*/
function DTouchRadioAddItems(obj) {
	var showImg  = "";
	var settings = obj.data("DTouchRadioSettings"); // acesso as configuracoes atuais do objeto
	var items    = settings.DTouchRadioAddItems; 

	// variaveis para opcao tabela
	var table_count   = 1; // controle para header e footer da tabela
	var table_content = "";
	var table_line    = "";
	
	// monta itens e adiciona no objeto
	for(var f in items) {
         
		if(items[f]['descrp'] == "") { // descricao, se nao tiver descricao adiciona valor do item como 
			items[f]['descrp'] = items[f]['val'];
        }
        
		if(items[f]['img']) { // imagem, se existir
			showImg = "<img src='"+items[f]['img']+"' />";
        }
        
		// adiciona objeto no radio on the fly
		// TYPE, ajusta configuracao com base no tipo
		switch(settings.type) {
			// padrao
			case "": 
				obj.append("<div class='DTouchRadio_items' tabindex='0'><input type='radio' name='"+obj.attr("id")+"_radios' value='"+items[f]['val']+"' class='input_hidden' />"+showImg+"<span class='DTouchRadio_descrp'>"+items[f]['descrp']+"</span></div>");
				
                $("#DTouchSlider_"+obj.prop("id")).slider("value", $("#DTouchSlider_"+obj.prop("id")).slider("option", "max"));
                
				// $(this).DTouchSlider({ orientation: settings.orientation });
				
				/*
				if(settings.visibleItems > 0)
					if(settings.radios_qtd > settings.visibleItems)
						$(this).css("width",(settings.radios_item_width * settings.visibleItems)+"px");
				*/
			break;
			
			// Accordion: adiciona accordion ---------------------------
			case "accordion":
				obj.append("<h3><div><input type='radio' name='"+obj.attr("id")+"_radios' value='"+items[f]['val']+"' />"+showImg+"<span class='DTouchRadio_descrp'>"+items[f]['descrp']+"</span></div></h3>");
				obj.append("<div id='"+obj.attr("id")+"_radios_accordion_content_"+items[f]['val']+"'></div>");
			break;
			
			// Table: adiciona tabela ---------------------------
			case "table":
			
				// ajusta array para laco
				var i = items[f]['descrp'];
				
				// inicia tabela
				if(table_count == 1)
					{
					table_line += "<table id='"+settings.radios_id+"_tb' class='DTouchRadio_table'><thead><tr><th class='DTouchRadio_table_first_cell'>cod</th>";
					
					// monta headers
					for(var ff in i)
						{					
						table_line += "<th>"+ff+"</th>";
						}
					
					table_line += "</tr></thead><tbody>";
					}
				
				
				// monta radio group
				table_content += "<input type='radio' name='"+obj.attr("id")+"_radios' value='"+items[f]['val']+"' class='DTouchRadio_table_radios' />";
				
				// monta linha da tabela
				table_content += "<tr><td class='DTouchRadio_table_first_cell'>"+items[f]['val']+"</td>";
				for(var ff in i)
					{					
					table_content += "<td>"+i[ff]+"</td>";
					}
				table_content += "</tr>";
				
				
				// finaliza tabela
				if(table_count == items.length)
					{
					table_line += table_content+"</tbody></table>";
					
					// adiciona tabela no objeto
					obj.append(table_line);
					}
										
				// soma variavel de controle de adicao de itens
				table_count++;
			break;
		}
	}
		
	// atualiza radio
	obj.DTouchRadio(settings);
}




/* [INI] ----------------------------------------------------------------------------------------
 *
 *	@description DTouchRadioAccordionContent: Adiciona valor ao conteudo do accordion
 *	@param obj
 *  @param min-width setar largura minima via css
 * 
 * ------------------------------------------------------------------------------------------- */
function DTouchRadioResize(obj)
	{
	var settings = obj.data("DTouchRadioSettings"); // acesso as configuracoes atuais do objeto
	// var obj_id = obj.prop("id")+"_radios_accordion_content_"+DTouchRadioGetValue(obj); // monta id do conteudo
	
	// $("#"+obj_id).html(settings.DTouchRadioAccordionContent);

	// ajuste da largura do radio se for horizontal
	if(settings.orientation == "horizontal" && settings.type != "accordion")
		{
		// se a quantidade de itens for maior que o padrao visivel
		if(settings.visibleItems > 0)
			{
			if(settings.radios_qtd > settings.visibleItems)
				{
				obj.css("min-width",(settings.radios_item_width * settings.visibleItems)+"px");
				}
			else
				{					
				// largura proposta -1 para fix da borda dotted right
				var wp = ((obj.width() / settings.radios_qtd)-1);
				
				if(wp < settings.mw)
					{
					obj.children("div").css("width",obj.width()+"px");
					}
				else
					{
					obj.children("div").css("width",wp+"px");
					}
			
				// ajusta a borda do ultimo elemento
				obj.children("div:last-child").css(
					{
					"border-right":"none"
					});
				}
			
			}
		}

	// adiciona slider
	if(settings.orientation == "horizontal")
		{
		if((obj.children("div:first-child").width() * settings.radios_qtd) > obj.width())
			{
			// obj.DTouchSlider({ orientation: settings.orientation });
			DTouchRadioSlider(obj);
			}
		else
			{
			DTouchRadioSlider(obj,false);
			}
		}
	else
		{
		DTouchRadioSlider(obj);
		}
	}
// [END] DTouchRadioAccordionContent: -------------------------------------------------------------------------------------


// [INI] DTouchRadioSlider: Adiciona Slider ao grupo ---------------------------------------------
function DTouchRadioSlider(obj, enable)
	{
	if(!enable)
		enable = true;
		
	var settings = {
			slider_id 	: "DTouchSlider_"+obj.prop("id"),
			enable		: enable,
			type		: 'boxes', 	// boxes / pages
			handler		: 'left',	// left / right
			orientation	: obj.data("DTouchRadioSettings")["orientation"], // vertical / horizontal
			rolltotal	: 0,
			width		: '',
			height		: ''
		}
	
	// var settings = obj.data("DTouchRadioSettings"); // acesso as configuracoes atuais do objeto
	// var obj_id = obj.prop("id")+"_radios_accordion_content_"+DTouchRadioGetValue(obj); // monta id do conteudo
	
	// objeto
	settings.container = obj;

	// remove slider se existir
	$("#"+settings.slider_id).remove();

	// inicia obejto
	settings.container
		.css("overflow","hidden") // esconde overflow
		.prepend('<div id="'+settings.slider_id+'" class="DTouchSlider"></div>'); // adiciona elemento slider


	// ajusta CSS para boxes se for o caso
	if(lc(settings.type) == "boxes")
		{
		$("#"+settings.slider_id).addClass('DTouchSliderBoxes');
	
		// ajusta css da orientacao vertical / horizontal
		if(lc(settings.orientation) == "horizontal")
			{
			$("#"+settings.slider_id).addClass('DTouchSliderBoxesHorizontal');
			settings.container_scroll = settings.container[0].scrollWidth;
			settings.container_view = settings.container.width();
			}
		else
			{
			$("#"+settings.slider_id).addClass('DTouchSliderBoxesVertical');
			settings.container_scroll = settings.container[0].scrollHeight;
			settings.container_view = settings.container.height();
			}
		}


	// adiciona slider somente se o tamanho exceder
	var forshow_scroll = settings.container_scroll; 
	var forshow_view  =  settings.container_view;
	
	// if(settings.container_scroll > settings.container_view)
	//	{
		// calculo do tamanho do slider
		settings.rolltotal = settings.container_scroll - settings.container_view;

		// cria slider
		$("#"+settings.slider_id).slider(
			{
			orientation: settings.orientation,
			range: "min",
			min: 0,
			max: settings.rolltotal,
			value: settings.rolltotal,
			change: function( event, ui ) 
				{
				// executa scroll 
				if(settings.orientation == "horizontal")
					{
					settings.container.scrollLeft(settings.rolltotal - ui.value);
					}
				else
					{
					settings.container.scrollTop(settings.rolltotal - ui.value);
					}
				},
			slide: function( event, ui ) 
				{
				// executa scroll 
				if(settings.orientation == "horizontal")
					{
					settings.container.scrollLeft(settings.rolltotal - ui.value);
					}
				else
					{
					settings.container.scrollTop(settings.rolltotal - ui.value);
					}
				},
			});
	// }
		if(forshow_scroll > forshow_view)
			$("#"+settings.slider_id).show();
		else
			$("#"+settings.slider_id).hide();
	}
// [END] DTouchRadioSlider: Adiciona Slider ao grupo ---------------------------------------------




/*
*   DTouchRadioNavigation
*       Navigation
*           controla a navegacao usando setas
*/
function DTouchRadioNavigation(obj,key){
    // proximo item
    if(key === 39 || key === 40){
        $(obj).next().trigger("click");
    } else { // anterior
        $(obj).prev().trigger("click");
    }
}










