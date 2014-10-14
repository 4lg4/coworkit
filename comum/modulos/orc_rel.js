
/**
 *   Usuario
 *       obj usuario
 */
function OrcamentoRel(){
    
    var oc = this;
    
    /* initialize */
    this.initialize = function() {
        
        // menus
        oc.form.menu();
        
        // touch pages
		$("#orcamento_rel_page").DTouchPages({
            // pageChange : "right",
            pageCenter : $("#orcamento_rel_page_center"),
            pageRight   : $("#orcamento_rel_page_right"),
			postFunctionCenter : function() {                
               
                // icones
                // eos.menu.action.hideAll();
                eos.menu.action.show(["icon_orcamento_new","icon_orcamento_save"]);
                
                // mostra btn edit
                if($("#COD").val()) {
                    eos.menu.action.show(["icon_orcamento_print","icon_orcamento_aprovar","icon_orcamento_cancelar","icon_orcamento_recusar"]);
                }
            },
			postFunctionRight : function() {
                console.log("right");
                // icones
                // eos.menu.action.hideAll();
                eos.menu.action.show(["icon_orcamento_new"]);
                
                // mostra btn edit
                if($("#orcamento_list").DTouchRadio("value")) {
                    eos.menu.action.show(["icon_orcamento_edit"]);    
                }
            },
			onCreate : function() {
                
                // search range 
                $("#search_container").DTouchBoxes({ 
                    title : "Filtro",
                    postFunction : function(){
            			$("#dt_ini").fieldDateTime({ 
            				type : "date"
            			});
                        
            			$("#dt_end").fieldDateTime({ 
            				type : "date"
            			});
                        
                        
                        $("#filter_cat").DTouchRadio({ 
                            orientation : "horizontal",
                            uncheck : false,
                			addItem:[
                				{
                                    val    : 'orc',
                                    descrp : 'Orçamento'
                                },
                				{
                                    val    : 'item',
                                    descrp : 'Cateoria Itens'
                                }
                			], 
                            postFunction : function(x){ console.log(x);
                                $("#filter_cat").DTouchRadio("value","orc");
                            }
                        });
                    }
                });
                
                
                
                /*
                // valores
                $("#list_container").DTouchBoxes({ 
                    title : "Listagem",
                    postFunction : function(){
                */
                
                var title  = "<div class=\"DTouchRadio_list_title\">";
                    title += "	<div style=\"width:5%\">Cod.</div> ";
                    title += "	<div style=\"width:10%\">Data</div> ";
                    title += "	<div style=\"width:15%\">Cliente</div> ";
                    title += "	<div style=\"width:28%\">Descrição</div> ";
                    title += "	<div style=\"width:20%\">Valor</div> ";
                    title += "</div>";
                
                        //
                        $("#list").DTouchRadio({ 
                            orientation : "vertical",
                            title       : title,
                            unique      : true,
                            itemDel     : true,
                            click       : "off",
                            pick        : false,
                            unique      : false
                        });
                        $("#list").hide();
               /*         
                    }
                });
               */
                
                // listagem
                // orc_rel.list("$COD");
                
                // inicia formulario inclusao
                // orc_rel.form.reset();
            }
        });
        
    };
    
    /** 
     *  print 
     */
    this.print = function(x) {
        // impressao inicial usando jsPDF
        // print.js         
        //
        
        $.DActionAjax({
            action : "print.pdf",
            loader : $("#orcamento_rel_page_center")
        });
    };
    

    
    
    /* filter */
    this.filter = function() {
        
        if(!$("#dt_ini").fieldDateTime("value") || !$("#dt_end").fieldDateTime("value")) {
            $.DDialog({
                type    : "alert",
                message : "Você deve escolher a data de inicio e fim para filtrar"
            });
            
            return false;
        }
        
        $.DActionAjax({
            action : "list.cgi",
            // loader : $("#orcamento_rel_page_left"),
            postFunction : function(x){ 
                
                var x = JSON.parse(x);  // console.log(x);
                
                $("#list").show();

                // gera linha
                function genLine(i){
                    var item  = "<div class='DTouchRadio_list_line'>";
                        item += "   <div style='width:20%'>";
                        item +=         i.codigo;
                        item += "   </div>";
                        item += "   <div style='width:30%'>";
                        item +=         i.descrp;
                        item += "   </div>";
                        item += "   <div style='width:30%'>";
                        item +=         i.valor;
                        item += "   </div>";
                        item += "</div>";
                        
                    // adiciona item
                    $("#list").DTouchRadio("addItem",{
                        val    : i.codigo,
                        descrp : item
                    });
                }
            
                // print lines
                if(x.length == 0) {
                    genLine({
                            codigo : "0",
                            descrp : "Nenhum Item encontrado",
                            valor  : ""
                    });
                } else {

                    x.forEach(function(i){
                        genLine(i);
                    });
                }                      
                
                /*
                if(x) {
                    $("#orcamento_list").DTouchRadio("value",x);
                    
                    * se for edicao direto
                    if("$COD" !== ""){
                        $("#COD").val("");
                        oc.edit();
                    }
                    *
                }
                */
            }
        });
    };    
    
    /**
     *   Formulario modulo
     */
    this.form = {
        
        /* menu */
        menu : function(){       
        
            eos.menu.action.new({ // novo
                id       : "icon_orcamento_new",
                title    : "novo",
                subtitle : "orça.",
                click    : function(){
                    orc_rel.form.new();
                }
            });
            
            eos.menu.action.new({ // list
                id       : "icon_orcamento_rel_list",
                title    : "filtrar",
                subtitle : "rel.",
                group    : "icon_orc_rel",
                click    : function(){
                    orc_rel.filter();
                }
            }); 
            
            // esconde icones
            // eos.menu.action.hideAll();
            
        },
    
        /* salvar */
        save : function(){
        
        },
        
        /* novo */
        new : function(){
            this.reset();
            $("#orcamento_rel_page").DTouchPages("page","center");
        },
    
        /* reset */
        reset : function(){  
        
            // this.enable(); // habilita formulario
        
            // reseta campos
            $("#servico_list").DTouchRadio("reset","content");
            $("#produto_list").DTouchRadio("reset","content");
            $("#despesa_list").DTouchRadio("reset","content");
            $("#cliente").fieldAutoComplete("reset");
            $("#validade").fieldDateTime("reset");
            
            $("#COD, #descrp, #cliente_endereco, #obs, #responsavel").val("");
            
            // valores
            $("#totais_geral").fieldMoney("reset");
            $("#totais_total").empty();
            oc.servico.reset();
            oc.despesa.reset();
            oc.produto.reset();
            
            // listagem
            $("#orcamento_list").DTouchRadio("reset");
            
            // icones
            // eos.menu.action.hideAll();
            eos.menu.action.show(["icon_orcamento_new","icon_orcamento_save"]);
        }
    };
    

    
    
    /** 
     *  Despesas 
     */
    this.despesa = {
        
        /* adiciona */
        add : function(x){ 
            var id = eos.core.genId();
            var item  = "<div class='DTouchRadio_list_line'>";
                item += "   <div style='width:40%'>";
                item +=         x.descrp;
                item += "       <input type='hidden' name='despesa_id' value='"+id+"'>";
                item += "       <input type='hidden' name='despesa_descrp_"+id+"' value='"+x.descrp+"'>";
                item += "       <input type='hidden' name='despesa_codigo_"+id+"' value='"+x.value+"'>";
                item += "       <input type='hidden' name='despesa_codigo_item_"+id+"' value='"+x.codigo+"'>";
                item += "   </div>";
                item += "   <div style='width:60%'>";
                item += "       <div style='width:80%'>";
                item += "           <input type='text' name='despesa_valor_"+id+"' id='despesa_valor_"+id+"' value='"+x.valor+"' placeholder='Valor' class='despesa_valores'>";
                item += "       </div>";
                item += "   </div>";
                item += "</div>";
            
            // adiciona item
            $("#despesa_list").DTouchRadio("addItem",{
                val    : x.value,
                descrp : item
            });  
            
            // ajusta campo
            $("#despesa_valor_"+id)
                .keyup(function(){ // soma totais ao sair do campo
                    oc.despesa.total();
                })
                .fieldMoney();
            
            // atualiza totais
            this.total();
        },
        
        /* Totais */
        total : function() {
            var soma = 0;
            
            $(".despesa_valores").each(function(){
                soma += money($(this).val(),1);
            });
            
            // atualiza totais
            $("#despesa_total").html(" R$ "+money(soma));
            $("#totais_despesa").fieldMoney("value",money(soma));
            
            // total geral
            oc.total();
        },
        
        /* Reset */
        reset : function() {
            $("#despesa_total").empty();
            $("#totais_despesa").fieldMoney("reset");
        }
    };
            
}


 