
/**
 *   arquivo padrao JS (encapsulamento)
 *       obj principal
 */
function Modulo(){
    
    // short cut do objeto para acesso interno
    var mg = this;
    
    
    
    /* initialize */
    this.initialize = function() {
        
        
        
        // menus
        md.form.menu();
        
        
        
        // touch pages
		$("#pagamentos_page").DTouchPages({
            pageChange : "left",
            pageCenter : $("#pagamentos_page_center"),
            pageLeft   : $("#pagamentos_page_left"),
			postFunctionCenter : function() {                
               
                // icones
                eos.menu.action.hideAll();
                eos.menu.action.show(["icon_pagamento_save"]);
                
                // mostra btn edit
                if($("#COD").val()) {
                    eos.menu.action.show(["icon_pagamento_print","icon_pagamento_aprovar","icon_pagamento_cancelar","icon_pagamento_recusar"]);
                }
            },
			postFunctionLeft : function() {
                
                // icones
                eos.menu.action.hideAll();
                
                // mostra btn edit
                if($("#pagamento_list").DTouchRadio("value")) {
                    eos.menu.action.show(["icon_pagamento_edit"]);    
                } else {
                    md.list();
                }
            },
			onCreate : function() {
                $("#dados_container").DTouchBoxes({ title: "Plano / Features" });
                $("#pagamentos_container").DTouchBoxes({ title: "Modulos" });
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
    
    /** 
     *  list 
     *      listagem
     */
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
    
    /** 
     *  editar 
     */
    this.edit = function(item){
        
        
        // desloca pagina
        $("#pagamentos_page").DTouchPages("page","center");
        
        
        /* edita formulario */
        $.DActionAjax({
            action : "edit.cgi",
            loader : $("#pagamentos_page_center"),
            postFunction : function(x){ 
                
            }
        });
    };
    
    
    
    /**
     *   Formulario modulo
     */
    this.form = {
        
        /* menu */
        menu : function(){       
        
           
            eos.menu.action.new({ // salvar
                id       : "icon_pagamento_save",
                title    : "salvar",
                subtitle : "plan.",
                click    : function(){
                    pagto.form.save();
                }
            });
            
            eos.menu.action.new({ // cancelar
                id       : "icon_pagamento_cancelar",
                title    : "cancelar",
                subtitle : "plan.",
                group    : "icon_pagto_aproval_",
                click    : function(){
                    pagto.aproval("cancel");
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
        
            // reseta campos
            $("#validade").fieldDateTime("reset");
            
            $("#COD, #descrp, #cliente_endereco, #obs, #responsavel").val("");
            
            // listagem
            $("#pagamento_list").DTouchRadio("reset");
            
            // icones
            eos.menu.action.hideAll();
            eos.menu.action.show(["icon_pagamento_save"]);
        }
    };
    

    
}
