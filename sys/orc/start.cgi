#!/usr/bin/perl

$nacess = "81";
require "../cfg/init.pl";

# vars
$ID  = &get('ID');
$COD = &get('COD');

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
	
<script>
/**
 *   Usuario
 *       obj usuario
 */
function Orcamento(){
    
    var oc = this;
    
    /* initialize */
    this.initialize = function() {
        
        // menus
        oc.form.menu();
        
        // touch pages
		\$("#orcamento_page").DTouchPages({
            // pageChange : "right",
            pageCenter : \$("#orcamento_page_center"),
            pageLeft   : \$("#orcamento_page_left"),
			postFunctionCenter : function() {                
               
                // icones
                eos.menu.action.hideAll();
                eos.menu.action.show(["icon_orcamento_new","icon_orcamento_save"]);
                
                // mostra btn edit
                if(\$("#COD").val()) {
                    eos.menu.action.show(["icon_orcamento_print","icon_orcamento_aprovar","icon_orcamento_cancelar","icon_orcamento_recusar"]);
                }
            },
			postFunctionLeft : function() {
                
                // icones
                eos.menu.action.hideAll();
                eos.menu.action.show(["icon_orcamento_new"]);
                
                // mostra btn edit
                if(\$("#orcamento_list").DTouchRadio("value")) {
                    eos.menu.action.show(["icon_orcamento_edit"]);    
                }
            },
			onCreate : function() {
                
                // solicitacao / solicitante
                \$("#solicitacao_container").DTouchBoxes({ 
                    title : "Solicitação",
                    postFunction : function(){
                        
            			\$("#cliente").fieldAutoComplete({ 
            				// type : "empresa"
            				sql_tbl      : "empresa",
                            localFile    : "fieldAutoComplete.cgi",
                            postFunction : function(x) { 
                                // adiciona endereco
                                \$("#cliente_endereco").val(\$("#cliente").data("fieldAutoCompleteSettings").item.endereco.codigo);
                            }
            			});
                        
                        eos.template.field.text(\$("#responsavel"));
                    }
                });
                
                // dados
                \$("#dados_container").DTouchBoxes({ 
                    title : "Dados",
                    postFunction : function(){
            			\$("#validade").fieldDateTime({ 
            				type : "date"
            			});
                    }
                });
                
                // valores
                \$("#valores_container").DTouchBoxes({ 
                    title : "Valores",
                    postFunction : function(){
                        
                        
            			\$("#servico").fieldAutoComplete({ 
            				sql_tbl      : "servicos",
                            localFile    : "fieldAutoComplete.cgi",
                            clearOnExit  : true,
                            itemAdd      : true,
                            postFunction : function(x) { 
                                // novo cadastro
                                if(x.item.id === "new"){
                                    x.value  = ""
                                }
                                                  
                                orc.servico.add({
                                    value  : x.item.id, 
                                    descrp : x.item.value,
                                    valor  : x.item.valor
                                });
                            }
            			});
                        
            			\$("#produto").fieldAutoComplete({ 
            				sql_tbl      : "produtos",
                            localFile    : "fieldAutoComplete.cgi",
                            clearOnExit  : true,
                            postFunction : function(x) { 
                                orc.produto.add({
                                    value  : x.item.id, 
                                    descrp : x.item.value,
                                    valor  : x.item.valor,
                                    unidade : x.item.unidade,
                                    marca   : x.item.marca,
                                    partnumber : x.item.partnumber,
                                    modelo  : x.item.modelo
                                });
                            }
            			});
                        
            			\$("#despesa").fieldAutoComplete({ 
            				sql_tbl      : "despesas",
                            localFile    : "fieldAutoComplete.cgi",
                            clearOnExit  : true,
                            itemAdd      : true,
                            postFunction : function(x) { 
                                // novo cadastro
                                if(x.item.id === "new"){
                                    x.value  = ""
                                }
                                                     
                                orc.despesa.add({ 
                                    value  : x.item.id, 
                                    descrp : x.item.value
                                    // valor  : \$("#servico").data("fieldAutoCompleteSettings").item.valor
                                });
                            }
            			});
                        
                        // inicia tabs
                        \$("#valores_tabs").tabs();
                        
                        
                        //
                        \$("#servico_list").DTouchRadio({ 
                            orientation : "vertical",
                            unique      : true,
                            itemDel     : true,
                            click       : "off",
                            pick        : false,
                            unique      : false
                        });
                        
                        //
                        \$("#produto_list").DTouchRadio({ 
                            orientation : "vertical",
                            unique      : true,
                            itemDel     : true,
                            click       : "off",
                            pick        : false
                        });
                        
                        //
                        \$("#despesa_list").DTouchRadio({ 
                            orientation : "vertical",
                            unique      : true,
                            itemDel     : true,
                            click       : "off",
                            pick        : false,
                            unique      : false
                        });
                        
                        
                        
                        // totais
                        \$("#totais_despesa").fieldMoney();
                        \$("#totais_despesa").fieldMoney("disable");
                        \$("#totais_servico").fieldMoney();
                        \$("#totais_servico").fieldMoney("disable");
                        \$("#totais_produto").fieldMoney();
                        \$("#totais_produto").fieldMoney("disable");
                        \$("#totais_geral").fieldMoney();
                        \$("#totais_geral").fieldMoney("disable");
                    }
                });
                
                // listagem
                orc.list("$COD");
                
                // inicia formulario inclusao
                // orc.form.reset();
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
        
        \$.DActionAjax({
            action : "print.pdf",
            loader : \$("#orcamento_page_center")
        });
    };
    
    
    /** 
     *  aproval, aprovacao / cancelamento do orcamento
     */
    this.aproval = function(x) {
        
        var title, field;
        
        // cancelar
        if(x === "cancel"){
            title = "Deseja Cancelar ?";
            field = "<textarea name='cancelar' placeholder='Motivo Cancelamento ?'\></textarea>";
        // aprovar
        } else if(x === true) {
            title = "Orçamento Aprovado ?";
            field = "<textarea name='cancelar' placeholder='Nome responsável pela aprovação ?'\></textarea>";
        // recusar
        } else if(x === false) {
            title = "Orçamento Recusado ?";
            field = "<textarea name='cancelar' placeholder='Motivo Recusa ?'\></textarea>";
        }
        
        // janela de confirmacao
        \$.DDialog({
            type    : "confirm",
            title   : title,
            message : field,
            btnYes  : function(){
            
                // verifica se motivo foi preenchido
                var txt = \$(this).parent().find("textarea[name=cancelar]").val();
                if(!txt){
                    \$.DDialog({
                        type    : "error",
                        title   : "Erro",
                        message : "Você deve preencher o motivo !"
                    });
                    return false;
                }
                                
                // gera vars
                var req  = "aproval="+x;
                    req += "&aproval_descrp="+txt;
                    req += "&COD="+\$("#COD").val();
                
                // atualiza db
                \$.DActionAjax({ 
                    action : "submit.cgi",
                    req    : req,
                    postFunction : function(r) { 
                
                        if(r){
                            try {   
                                var r = JSON.parse(r);
                                
                                // cancelar
                                if(x === "cancel"){
                                    title = "Deseja Cancelar ?";
                                    field = "<textarea name='cancelar' placeholder='Motivo Cancelamento ?'\></textarea>";
                                // aprovar
                                } else if(x === true) {
                                    eos.menu.action.hide(["icon_orcamento_aprovar"]);
                                    eos.menu.action.show(["icon_orcamento_aprovar","icon_orcamento_cancelar"]);
                                // recusar
                                } else if(x === false) {
                                    eos.menu.action.hide(["icon_orcamento_recusar"]);
                                    eos.menu.action.show(["icon_orcamento_aprovar","icon_orcamento_cancelar"]);
                                }
                                
                            } catch(e) {
                                return false;
                            } 
                        }
                    }
                });
            },
        });
        
    };
    
    
    /* list */
    this.list = function(x) {
        \$.DActionAjax({
            action : "list.cgi",
            loader : \$("#orcamento_page_left"),
            postFunction : function(){ 
                if(x) {
                    \$("#orcamento_list").DTouchRadio("value",x);
                    
                    // se for edicao direto
                    if("$COD" !== ""){
                        \$("#COD").val("");
                        oc.edit();
                    }
                }
            }
        });
    };
    
    /* editar */
    this.edit = function(){
        
        // ajusta codigo
        var x = \$("#orcamento_list").DTouchRadio("value");
        if(x === \$("#COD").val()) { // se codigo ja selecionado ignora
            return true;
        } else {
            // limpa
            oc.form.reset();
            
            \$("#COD").val(x);
        }
        
        // desloca pagina
        \$("#orcamento_page").DTouchPages("page","center");
        
        // icones
        // eos.menu.action.hideAll();
        
        /* edita formulario */
        \$.DActionAjax({
            action : "edit.cgi",
            req    : "COD="+x,
            loader : \$("#orcamento_page_center"),
            postFunction : function(x){ 
                
                var x = JSON.parse(x);  // console.log(x);

                \$("#descrp").val(x.descrp);
                \$("#obs").val(x.obs);
                \$("#responsavel").val(x.responsavel);
                \$("#validade").fieldDateTime("value",x.validade);
                \$("#cliente").fieldAutoComplete("value", {
                    codigo : x.cliente.codigo,
                    descrp : x.cliente.descrp+" "+x.endereco.descrp
                });
                \$("#cliente_endereco").val(x.endereco.codigo);
                
                \$("#totais_geral").fieldMoney("value",x.total);
                
                
                // adiciona item
                x.itens.forEach(function(i){
                    
                    // servicos
                    if(i.link_tbl === "prod_serv") {
                        orc.servico.add({
                            value  : i.link_codigo, 
                            descrp : i.descrp,
                            valor  : i.valor,
                            codigo : i.codigo,
                            quantidade : i.quantidade,
                            total      : i.total
                        });
                        
                    // produtos
                    } else if(i.link_tbl === "prod_mercadorias") {
                        orc.produto.add({
                            value      : i.link_codigo, 
                            descrp     : i.descrp,
                            valor      : i.valor,
                            quantidade : i.quantidade,
                            total      : i.total,
                            unidade    : i.unidade,
                            marca      : i.marca,
                            partnumber : i.partnumber,
                            modelo     : i.modelo,
                            codigo     : i.codigo
                        });
                        
                    // despesas
                    } else if(i.link_tbl === "prod_despesas") {
                        orc.despesa.add({
                            value      : i.link_codigo, 
                            descrp     : i.descrp,
                            valor      : i.valor,
                            codigo     : i.codigo,
                            quantidade : i.quantidade,
                            total      : i.total
                        });
                    } 
                    
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
        
            eos.menu.action.new({ // novo
                id       : "icon_orcamento_new",
                title    : "novo",
                subtitle : "orça.",
                click    : function(){
                    orc.form.new();
                }
            });
            
            eos.menu.action.new({ // salvar
                id       : "icon_orcamento_save",
                title    : "salvar",
                subtitle : "orça.",
                click    : function(){
                    orc.form.save();
                }
            });
            
            
            eos.menu.action.new({ // editar
                id       : "icon_orcamento_edit",
                title    : "editar",
                subtitle : "orça.",
                click    : function(){
                    orc.edit();
                }
            });
            
            
            eos.menu.action.new({ // aproval
                id       : "icon_orcamento_aprovar",
                title    : "aprovar",
                subtitle : "orça.",
                group    : "icon_orc_aproval",
                click    : function(){
                    orc.aproval(true);
                }
            }); 
            
            eos.menu.action.new({ // cancelar
                id       : "icon_orcamento_recusar",
                title    : "recusar",
                subtitle : "orça.",
                group    : "icon_orc_aproval",
                click    : function(){
                    orc.aproval(false);
                }
            }); 
            
            eos.menu.action.new({ // cancelar
                id       : "icon_orcamento_cancelar",
                title    : "cancelar",
                subtitle : "orça.",
                group    : "icon_orc_aproval_",
                click    : function(){
                    orc.aproval("cancel");
                }
            }); 
        
            
            eos.menu.action.new({ // print
                id       : "icon_orcamento_print",
                title    : "imprimir",
                subtitle : "orça.",
                group    : "icon_orc",
                click    : function(){
                    orc.print();
                }
            }); 
        
            // esconde icones
            eos.menu.action.hideAll();
        },
    
        /* salvar */
        save : function(){
        
            // valida formulario       
            var msg = "";
        
            if(!\$("#cliente").val() || !\$("#cliente_descrp").val()) {
                msg += "Cliente <br>";
            }
            
            if(!\$("#descrp").val()) {
                msg += "Descrição <br>";
            }    
        
            if(!\$("#validade").fieldDateTime("value")) {
                msg += "Validade <br>";
            }
                
            if(msg) {
                \$.DDialog({
                    type    : "error",
                    message : "Campos obrigatórios <br><br>"+msg 
                });
            
                return false;
            }
        
            // envia form
            \$.DActionAjax({
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
                            \$.DDialog({
                               type    : x.status,
                               message : x.message
                            });
                        } else {
                        
                            // retorna o codigo para formulario
                            if(x.COD){
                                \$("#COD").val(x.COD);
                            }
                        
                            // atualiza lista em segundo plano e mantem selecionado
                            oc.list(\$("#COD").val());
                        }
                    }
                }
            });
        },
        
        /* novo */
        new : function(){
            this.reset();
            \$("#orcamento_page").DTouchPages("page","center");
        },
    
        /* reset */
        reset : function(){  
        
            // this.enable(); // habilita formulario
        
            // reseta campos
            \$("#servico_list").DTouchRadio("reset","content");
            \$("#produto_list").DTouchRadio("reset","content");
            \$("#despesa_list").DTouchRadio("reset","content");
            \$("#cliente").fieldAutoComplete("reset");
            \$("#validade").fieldDateTime("reset");
            
            \$("#COD, #descrp, #cliente_endereco, #obs, #responsavel").val("");
            
            // valores
            \$("#totais_geral").fieldMoney("reset");
            \$("#totais_total").empty();
            oc.servico.reset();
            oc.despesa.reset();
            oc.produto.reset();
            
            // listagem
            \$("#orcamento_list").DTouchRadio("reset");
            
            // icones
            eos.menu.action.hideAll();
            eos.menu.action.show(["icon_orcamento_new","icon_orcamento_save"]);
        }
    };
    
    
    /** 
     *  servicos 
     */
    this.servico = {
        
        /* adiciona */
        add : function(x){ 
            
            if(!x.total){
                x.total = x.valor;
            }
        
            if(!x.quantidade){
                x.quantidade = 1;
            }
            
            var id = eos.core.genId();
            var item  = "<div class='DTouchRadio_list_line'>";
                item += "   <div style='width:40%'>";
                item +=         x.descrp;
                item += "       <input type='hidden' name='servico_id' value='"+id+"'>";
                item += "       <input type='hidden' name='servico_descrp_"+id+"' value='"+x.descrp+"'>";
                item += "       <input type='hidden' name='servico_codigo_"+id+"' value='"+x.value+"'>";
                item += "       <input type='hidden' name='servico_codigo_item_"+id+"' value='"+x.codigo+"'>";
                item += "   </div>";
                item += "   <div style='width:60%'>";
                item += "       <div style='width:10%'>";
                item += "           <input type='text' name='servico_qtd_"+id+"' id='servico_qtd_"+id+"' value='"+x.quantidade+"' placeholder='Quantidade'>";
                item += "       </div>";
                item += "       <div style='width:40%'>";
                item += "           <input type='text' name='servico_valor_"+id+"' id='servico_valor_"+id+"' value='"+x.valor+"' placeholder='Valor'>";
                item += "       </div>";
                item += "       <div style='width:40%'>";
                item += "           <input type='text' name='servico_valor_total_"+id+"' id='servico_valor_total_"+id+"' value='"+x.total+"' placeholder='Valor' class='servico_valores'>";
                item += "       </div>";
                item += "   </div>";
                item += "</div>";
            
            // adiciona item
            \$("#servico_list").DTouchRadio("addItem",{
                val    : x.value,
                descrp : item
            });  
            
            function somaUnitario(){
                var qtd = parseFloat(\$("#servico_qtd_"+id).fieldNumber("value"))
                ,   val = money(\$("#servico_valor_"+id).fieldMoney("value"),1);
                
                \$("#servico_valor_total_"+id).fieldMoney("value", money(qtd * val));
                oc.servico.total();
            }
            
            // ajusta campo
            \$("#servico_valor_"+id)
                .keyup(function(){ // soma totais ao sair do campo
                    somaUnitario();
                })
                .fieldMoney();
            
            
            \$("#servico_qtd_"+id)
                .keyup(function(){ // soma totais ao sair do campo
                    somaUnitario();
                })
                .fieldNumber();
            
            \$("#servico_valor_total_"+id)
                .keyup(function(){ // soma totais ao sair do campo
                    somaUnitario();
                })
                .fieldMoney();
                
            // desabilita campo valor total
            \$("#servico_valor_total_"+id).fieldMoney("disable");
            
            // atualiza totais
            this.total();
        },
        
        /* Totais */
        total : function() {
            var soma = 0;
            
            \$(".servico_valores").each(function(){
                soma += money(\$(this).val(),1);
            });
            
            // atualiza totais
            \$("#servico_total").html(" R\$ "+money(soma));
            \$("#totais_servico").fieldMoney("value",money(soma));
            
            // total geral
            oc.total();
        },
        
        /* Reset */
        reset : function() {
            \$("#servico_total").empty();
            \$("#totais_servico").fieldMoney("reset");
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
            \$("#despesa_list").DTouchRadio("addItem",{
                val    : x.value,
                descrp : item
            });  
            
            // ajusta campo
            \$("#despesa_valor_"+id)
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
            
            \$(".despesa_valores").each(function(){
                soma += money(\$(this).val(),1);
            });
            
            // atualiza totais
            \$("#despesa_total").html(" R\$ "+money(soma));
            \$("#totais_despesa").fieldMoney("value",money(soma));
            
            // total geral
            oc.total();
        },
        
        /* Reset */
        reset : function() {
            \$("#despesa_total").empty();
            \$("#totais_despesa").fieldMoney("reset");
        }
    };
    
    
    /** 
     *  Produtos / Mercadorias
     */
    this.produto = {
        
        /* adiciona */
        add : function(x){ 
            
            
            if(!x.total){
                x.total = x.valor;
            }
            
            if(!x.quantidade){
                x.quantidade = 1;
            }
            
            var id = eos.core.genId();
            var item  = "<div class='DTouchRadio_list_line'>";
                item += "   <div style='width:40%'>";
                item +=         x.descrp;
                item += "       <span>("+x.modelo+"  "+x.marca+"  "+x.partnumber+")</span>";
                item += "       <input type='hidden' name='produto_id' value='"+id+"'>";
                item += "       <input type='hidden' name='produto_descrp_"+id+"' value='"+x.descrp+"'>";
                item += "       <input type='hidden' name='produto_codigo_"+id+"' value='"+x.value+"'>";
                item += "       <input type='hidden' name='produto_codigo_item_"+id+"' value='"+x.codigo+"'>";
                item += "   </div>";
                item += "   <div style='width:60%'>";
                item += "       <div style='width:10%'>";
                item += "           <input type='text' name='produto_qtd_"+id+"' id='produto_qtd_"+id+"' value='"+x.quantidade+"' placeholder='Quantidade'>";
                item += "       </div>";
                item += "       <div style='width:40%'>";
                item += "           <input type='text' name='produto_valor_"+id+"' id='produto_valor_"+id+"' value='"+x.valor+"' placeholder='Valor'>";
                item += "       </div>";
                item += "       <div style='width:40%'>";
                item += "           <input type='text' name='produto_valor_total_"+id+"' id='produto_valor_total_"+id+"' value='"+x.total+"' placeholder='Valor Total' class='produto_valores'>";
                item += "       </div>";
                item += "   </div>";
                item += "</div>";
            
            // adiciona item
            \$("#produto_list").DTouchRadio("addItem",{
                val    : x.value,
                descrp : item
            });  
            
            function somaUnitario(){
                var qtd = parseFloat(\$("#produto_qtd_"+id).fieldNumber("value"))
                ,   val = money(\$("#produto_valor_"+id).fieldMoney("value"),1);
                
                \$("#produto_valor_total_"+id).fieldMoney("value", money(qtd * val));
                oc.produto.total();
            }
            
            // ajusta campo
            \$("#produto_valor_"+id)
                .keyup(function(){ // soma totais ao sair do campo
                    somaUnitario();
                })
                .fieldMoney();    
            
            \$("#produto_qtd_"+id)
                .keyup(function(){ // soma totais ao sair do campo
                    somaUnitario();
                })
                .fieldNumber();
                
            \$("#produto_valor_total_"+id)
                .keyup(function(){ // soma totais ao sair do campo
                    somaUnitario();
                })
                .fieldMoney();
                
            // desabilita campo valor total
            \$("#produto_valor_total_"+id).fieldMoney("disable");
            
            // atualiza totais
            this.total();
        },
        
        /* Totais */
        total : function() {
            var soma = 0;
            
            \$(".produto_valores").each(function(){
                soma += money(\$(this).val(),1);
            });
            
            // atualiza totais
            \$("#produto_total").html(" R\$ "+money(soma));
            \$("#totais_produto").fieldMoney("value",money(soma));
            
            // total geral
            oc.total();
        },
        
        /* Reset */
        reset : function() {
            \$("#produto_total").empty();
            \$("#totais_produto").fieldMoney("reset");
        }
    };
    
    
    
    /** 
     *  Totais Orcamento
     */
    this.total = function() {
        var soma = 0;
        
        \$(".totais_valores").each(function(){
            soma += money(\$(this).val(),1);
        });
        
        // atualiza totais
        \$("#totais_total").html(" R\$ "+money(soma));
        \$("#totais_geral").fieldMoney("value",money(soma));        
    }
    
}


 
/**
 *   Document Ready
 */
\$(document).ready(function() { 
    orc = new Orcamento();
    orc.initialize();    
});

</script>
</head>
<body>

    <!-- Formulario -->
    <form >
	
        <!-- Paginas -->
        <div id="orcamento_page">
            
                <!-- pagina esquerda -->
                <div id="orcamento_page_left">
                    <!-- listagem -->
                    <div id="orcamento_list_container">
                        <div id="orcamento_list"></div>
                    </div>
                </div>
                
                <!-- pagina central -->
                <div id="orcamento_page_center">
                        <div class="orcamento_page_line">
                            
                            <div id="solicitacao_container">
                                <div id="cliente_container">
                                    <input type="text" id="cliente" name="cliente" placeholder="Cliente" />
                                    <input type="hidden" id="cliente_endereco" name="cliente_endereco" />
                                </div>
                                <div id="responsavel_container">
                                    <input type="text" id="responsavel" name="responsavel" placeholder="Responsável" />
                                </div>
                                <div id="descrp_container">
                                    <textarea id="descrp" name="descrp" placeholder="Descrição Solicitação"></textarea>
                                </div>
                            </div>
                            
                            <div id="dados_container">
                                <div id="validade_container">
                                    <input type="text" id="validade" name="validade" placeholder="Válido até" />
                                </div>
                                <div class="totais_line_">
                                    <div class="totais_descrp">
                                        Total Geral
                                    </div>
                                    <div class="totais_valor">
                                        <input type="text" id="totais_geral" name="totais_geral" placeholder="Total Geral" />
                                    </div>
                                </div>
                                <div id="obs_container">
                                    <textarea id="obs" name="obs" placeholder="Observações para o cliente"></textarea>
                                </div>
                            </div>
                                                        
                        </div>
                        
                        <div class="orcamento_page_line">
                            
                            <div id="valores_container">
                                <div id="valores_tabs">
                                	<ul>
                                        <li><a href="#servico_tab">Serviços <span id="servico_total"></span></a></li>
                                		<li><a href="#produto_tab">Produtos <span id="produto_total"></span></a></li>
                                        <li><a href="#despesa_tab">Despesas <span id="despesa_total"></span></a></li>
                                        <li><a href="#totais_tab">Totais    <span id="totais_total"></span></a></li>
                                	</ul>
                                
                                    <div id="servico_tab" class="val_tabs">
                                        <div id="servico_container">
                                            <input type="text" id="servico" name="servico" placeholder="Serviço" />
                                        </div>
                                        <div id="servico_list_container">
                                            <div id="servico_list_title">
                                                <div style='width:40%'>Descrição</div>
                                                <div style='width:55%'>Valor Total</div>
                                            </div>
                                            <div id="servico_list"></div>
                                        </div>
                                    </div>
                                    <div id="produto_tab" class="val_tabs">
                                        <div id="produto_container">
                                            <input type="text" id="produto" name="produto" placeholder="Produto" />
                                        </div>
                                        <div id="produto_list_container">
                                            <div id="produto_list_title">
                                                <div style='width:37%'>Descrição</div>
                                                <div style='width:60%'>
                                                    <div style='width:15%'>Quantidade</div>
                                                    <div style='width:40%'>Valor Unitário</div>
                                                    <div style='width:30%'>Valor Total</div>
                                                </div>
                                            </div>
                                            <div id="produto_list"></div>
                                        </div>
                                    </div>
                                    <div id="despesa_tab" class="val_tabs">
                                        <div id="despesa_container">
                                            <input type="text" id="despesa" name="despesa" placeholder="Despesa" />
                                        </div>
                                        <div id="despesa_list_container">
                                            <div id="despesa_list_title">
                                                <div style='width:40%'>Descrição</div>
                                                <div style='width:55%'>Valor Total</div>
                                            </div>
                                            <div id="despesa_list"></div>
                                        </div>
                                    </div>
                                    <div id="totais_tab" class="val_tabs">
                                        <div class="totais_line">
                                            <div class="totais_descrp">
                                                Despesas
                                            </div>
                                            <div class="totais_valor">
                                                <input type="text" id="totais_despesa" name="totais_despesa" placeholder="Total Despesa" class="totais_valores" />
                                            </div>
                                        </div>
                                        <div class="totais_line">
                                            <div class="totais_descrp">
                                                Serviços
                                            </div>
                                            <div class="totais_valor">
                                                <input type="text" id="totais_servico" name="totais_servico" placeholder="Total Servico" class="totais_valores" />
                                            </div>
                                        </div>
                                        <div class="totais_line">
                                            <div class="totais_descrp">
                                                Produtos
                                            </div>
                                            <div class="totais_valor">
                                                <input type="text" id="totais_produto" name="totais_produto" placeholder="Total Produto" class="totais_valores" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>  
                        </div>       
                        
                        
                       
                </div>               

        </div>
        
        
        <input type="hidden" name="COD" id="COD" value="$COD">
    </form>
    
</body>
</html>

HTML

