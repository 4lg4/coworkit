
/**
 *   Pagamento
 *       obj pagamento
 */
function Pagamento(){
    
    var pg = this;
    
    /* initialize */
    this.initialize = function() {
        
        // menus
        pg.form.menu();
        
        // touch pages
		$("#pagamentos_page").DTouchPages({
            pageChange : "left",
            pageCenter : $("#pagamentos_page_center"),
            pageLeft   : $("#pagamentos_page_left"),
			postFunctionCenter : function() {                
               
                // icones
                eos.menu.action.hideAll();
            },
			postFunctionLeft : function() {
                
                // icones
                eos.menu.action.hideAll();
                
                // mostra btn edit
                if($("#pagamento_list").DTouchRadio("value")) {
                    eos.menu.action.show(["icon_pagamento_edit"]);    
                } else {
                    pg.list();
                }
            },
			onCreate : function() {
                $("#dados_container").DTouchBoxes({ 
                    title: "Dados",
                    postFunction : function(){
                        
                        // features radio
                        var ftitle  = "<div class='DTouchRadio_list_title'>";
                            ftitle += "   <div style='width:40%'>Descrição</div>";
                            ftitle += "   <div style='width:30%'>Valor Customizado</div>";
                            ftitle += "   <div style='width:30%'>Valor Padrão</div>";
                            ftitle += "</div>";
                            
                        $("#features").DTouchRadio({ 
                            orientation : "vertical",
                            unique      : true,
                            click       : "off",
                            pick        : false,
                            unique      : false,
                            title       : ftitle
                        });
                        
                        
                        
                        // pagamentos radio
                        var ftitle  = "<div class='DTouchRadio_list_title'>";
                            ftitle += "   <div style='width:20%'>Plano</div>";
                            ftitle += "   <div style='width:30%'>Data vencimento</div>";
                            ftitle += "   <div style='width:30%'>Data pagamento</div>";
                            ftitle += "   <div style='width:20%'>Valor</div>";
                            ftitle += "</div>";
                            
                        $("#pagamentos").DTouchRadio({ 
                            orientation : "vertical",
                            unique      : true,
                            click       : "off",
                            pick        : false,
                            unique      : false,
                            title       : ftitle
                        });
                        
                    }
                 });
                 
                $("#features_container").DTouchBoxes({ title: "Features" });
                
                $("#pagamentos_container").DTouchBoxes({ title: "Pagamentos" });
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
            loader : $("#pagamentos_page_center")
        });
    };
    
    /* list */
    this.list = function(x) {
        $.DActionAjax({
            action : "list.cgi",
            loader : $("#pagamentos_page_left"),
            postFunction : function(){ 
                if(x) {
                    $("#pagamento_list").DTouchRadio("value",x);
                }
            }
        });
    };
    
    /* editar */
    this.edit = function(item){
        
        // ajusta codigo
        var item = {
                    empresa : {
                        codigo : $("#pagamento_list").DTouchRadio("value"),
                        descrp : $("#pagamento_list .DTouchRadio_selected input[name=empresa_nome]").val()
                    },
                    plano : {
                        codigo : $("#pagamento_list .DTouchRadio_selected input[name=plano]").val(),
                        descrp : $("#pagamento_list .DTouchRadio_selected input[name=plano_descrp]").val()
                    }
        };
        
        
        x = item.empresa.codigo;
        
        // desloca pagina
        $("#pagamentos_page").DTouchPages("page","center");
        
        
        if(x === $("#COD").val()) { // se codigo ja selecionado ignora
            return true;
        } else {
            // limpa
            // pg.form.reset();
            
            $("#COD").val(x);
        }
        
        // icones
        // eos.menu.action.hideAll();
        
        $("#cliente").text(item.empresa.descrp);
        $("#plano").text(item.plano.descrp);
        
        /* edita formulario */
        $.DActionAjax({
            action : "edit.cgi",
            req    : "COD="+x+"&empresa="+x+"&plano="+item.plano.codigo,
            loader : $("#pagamentos_page_center"),
            postFunction : function(x){ 
                
                //console.log(x);
                //return;
                
                var x = JSON.parse(x); console.log(x);
                
                // adiciona item
                x.features.forEach(function(i){ 
                    
                    var item  = "<div class='DTouchRadio_list_line'>";
                        item += "   <div style='width:40%'>";
                        item +=         i.descrp+" ("+i.tipo+")";
                        item += "   </div>";
                        item += "   <div style='width:30%'>";
                        item +=         i.custom;
                        item += "   </div>";
                        item += "   <div style='width:30%'>";
                        item +=         i.default;
                        item += "   </div>";
                        item += "</div>";
            
                    // adiciona item
                    $("#features").DTouchRadio("addItem",{
                        val    : x.value,
                        descrp : item
                    });  
                    
                    
                    // $("#features").append("<div>"+i.descrp+" - "+i.default+"</div>");
                    
                    
                    
                    
                    /*
                        pagto.produto.add({
                            value      : i.link_codigo, 
                        });                    
                    */
                });
                
                
                
                
                // pagamentos
                x.pagamentos.forEach(function(i){
                    
                    var item  = "<div class='DTouchRadio_list_line'>";
                        item += "   <div style='width:20%'>";
                        item +=         i.plan_descrp;
                        item += "   </div>";
                        item += "   <div style='width:30%'>";
                        item +=         i.data_vencimento;
                        item += "   </div>";
                        item += "   <div style='width:30%'>";
                        item +=         i.data_pagamento;
                        item += "   </div>";
                        item += "   <div style='width:20%'>";
                        item +=         i.valor;
                        item += "   </div>";
                        item += "</div>";
            
                    // adiciona item
                    $("#pagamentos").DTouchRadio("addItem",{
                        val    : x.value,
                        descrp : item
                    });  
                    
                    
                    // $("#features").append("<div>"+i.descrp+" - "+i.default+"</div>");
                    
                    
                    
                    
                    /*
                        pagto.produto.add({
                            value      : i.link_codigo, 
                        });                    
                    */
                });
            }
        });
    };
    
    
    
    /**
     *   Formulario modulo
     */
    this.form = {
        
        /* menu */
        menu : function(){       
            
            eos.menu.action.new({ // editar
                id       : "icon_pagamento_edit",
                title    : "editar",
                subtitle : "plan.",
                click    : function(){
                    pagto.edit();
                }
            });
        
            // esconde icones
            eos.menu.action.hideAll();
        },
    
        /* salvar */
        save : function(){
        
            // valida formulario       
            var msg = "";
        
            if(!$("#cliente").val() || !$("#cliente_descrp").val()) {
                msg += "Cliente <br>";
            }

            if(msg) {
                $.DDialog({
                    type    : "error",
                    message : "Campos obrigatórios <br><br>"+msg 
                });
            
                return false;
            }
        
            // envia form
            $.DActionAjax({
                action : "submit.cgi",
                postFunction : function(x) { 
                
                    // console.log(x);
                    // return;
                
                    if(x){
                        try {   
                            var x = JSON.parse(x);
                        } catch(e) {
                            console.log(x);
                            console.log(e);
                            return false;
                        } 
                    
                        if(x.status === "error") {
                            $.DDialog({
                               type    : x.status,
                               message : x.message
                            });
                        } else {
                        
                            // retorna o codigo para formulario
                            if(x.COD){
                                $("#COD").val(x.COD);
                            }
                        
                            // atualiza lista em segundo plano e mantem selecionado
                            pg.list($("#COD").val());
                        }
                    }
                }
            });
        },
        
        /* novo */
        new : function(){
            this.reset();
            $("#pagamentos_page").DTouchPages("page","center");
        },
    
        /* reset */
        reset : function(){  
        
            // this.enable(); // habilita formulario
        }
    };
    
    
    
    
    
    
    /** 
     *  Totais Pagamento
     */
    this.total = function() {
        var soma = 0;
        
        $(".totais_valores").each(function(){
            soma += money($(this).val(),1);
        });
        
        // atualiza totais
        $("#totais_total").html(" R$ "+money(soma));
        $("#totais_geral").fieldMoney("value",money(soma));        
    }
    
}
