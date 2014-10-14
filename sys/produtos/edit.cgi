#!/usr/bin/perl

$nacess = "76";
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
function Produtos(){
    
    /* initialize */
    this.initialize = function() {
        this.list();
    };
    
    /* list, lista de usuarios */
    this.list = function() {
        \$.DActionAjax({
            action : "edit_list.cgi",
            loader : \$("#produtos_list")
        });
    }
    
    /* editar */
    this.edit = function(){
        
        \$("#produtos_page").DTouchPages("page","right");
        
        // icones
        // eos.menu.action.hideAll();
        
        /* edita formulario */
        \$.DActionAjax({
            action : "edit_edit.cgi",
            req    : "COD="+\$("#COD").val(),
            loader : \$("#produtos_page_right"),
            postFunction : function(x){ 
                
                var produto = JSON.parse(x);
                
                \$("#descrp").val(produto.descrp);
                \$("#status").DTouchRadio("value",produto.status);
                \$("#unidade").DTouchRadio("value",produto.unidade);
                \$("#preco").fieldMoney("value",produto.preco_custo);
                \$("#preco_venda").fieldMoney("value",produto.preco_venda);
                \$("#modelo").val(produto.modelo);
                \$("#link").val(produto.link);
                \$("#partnumber").val(produto.partnumber);
                \$("#obs").val(produto.obs);
                \$("#marca").fieldAutoComplete("value",produto.marca);
            }
        });
    };
}


/**
 *   Form
 *       obj formulario
 */
function Form(){
    
    var l = false;
    
    /* controla form */
    this.locked = function(x){
        if(!x) {
            return l;
        } else {
            l = x;
            return x;
        }
    }
    
    /* initialize */
    this.initialize = function(postFunction){
        
        this.menu(); // inicia menus
        
        
        // touch pages
		\$("#produtos_page").DTouchPages({
            // pageChange : "right",
            pageCenter : \$("#produtos_page_center"),
            pageRight  : \$("#produtos_page_right"),
			postFunctionCenter : function() {                
               
                produtos.list();
                
                eos.menu.action.hideAll();
                eos.menu.action.show(["icon_produtos_new"]);
            },
			postFunctionRight : function() {
                
                
                // icones
                eos.menu.action.hideAll();

                //if(form.locked()) {
                  //  eos.menu.action.show(["icon_produtos_new"]);
                    // } else {
                    eos.menu.action.show(["icon_produtos_new","icon_produtos_save"]);
                    //}
                
            },
			onCreate : function() {
                
                
                // status
                \$("#status_container").DTouchBoxes({ 
                    title : "Status",
                    // uncheck : "off",
                    postFunction : function(){
                        
                        \$("#status").DTouchRadio({
                            orientation : "vertical",
                            itemAdd     : [
                                {
                                    val    : 1,
                                    descrp : "Ativo"
                                },
                                {
                                    val    : 0,
                                    descrp : "Inativo"
                                }
                            ],
                            postFunction : function(x){
                            }
                        });
                    }
                });
                
                // preco
                \$("#preco").fieldMoney();
                \$("#preco_venda").fieldMoney();
                
                // dados
                \$("#dados_container").DTouchBoxes({ title : "Dados" });
                eos.template.field.text(\$("#descrp"));

            	// marca
            	\$("#marca").fieldAutoComplete({ 
            		sql_tbl:"prod_marca"
            	});
                
            	// unidades
            	\$("#unidade_container").DTouchBoxes({ 
            		title : "Tipo de Unidade"
            	});
            	\$("#unidade").DTouchRadio({ 
            		tbl:"prod_unidade",
                    orientation : "vertical"
            	});
                
                // other
                \$("#other_container").DTouchBoxes({ title : "Mais Dados" });
                eos.template.field.text(\$("#modelo"));
                eos.template.field.text(\$("#partnumber"));
                eos.template.field.text(\$("#link"));
                
                
                
                // inicializa produtos
                produtos = new Produtos();
                produtos.initialize();
             
                if(isFunction(postFunction)){
                    postFunction.call(this);
                    // console.log('call');
                }
                
                
                // inicia formulario inclusao
                form.reset();
            }
        });
    }
    
    /* menu */
    this.menu = function(){
        eos.menu.action.new({ // salvar
            id       : "icon_produtos_save",
            title    : "salvar",
            subtitle : "produto",
            click    : function(){
                form.save();
            }
        });        
        
        eos.menu.action.new({ // novo
            id       : "icon_produtos_new",
            title    : "novo",
            subtitle : "produto",
            click    : function(){
                // if(eos.core.limit.produtos.verify()){ // dentro do limite
                    form.new();
                    //} else {
                    //\$.DDialog({
                    //    type    : "error",
                    //    message : "Limite de usuários excedido ! <br><br> Become a premium !" 
                    //});
                    //}
            }
        });
        
        // esconde icones
        eos.menu.action.hideAll();
    };
    
    /* salvar */
    this.save = function(){
        
        // valida formulario       
        var msg = "";
        
        
        if(!\$("#descrp").val()) {
            msg += "Descrição <br>";
        }
        
        if(!\$("#preco").fieldMoney("value")) {
            msg += "Valor Custo <br>";
        }
        
        if(!\$("#preco_venda").fieldMoney("value")) {
            msg += "Valor Venda <br>";
        }
        
        if(parseFloat(\$("#preco_venda").fieldMoney("value")) < parseFloat(\$("#preco").fieldMoney("value"))){
            msg += "Valor Venda menor que Valor Custo <br>";
        }
        
        
        if(!\$("#status").DTouchRadio("value")) {
            msg += "Status <br>";
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
            action : "edit_submit.cgi",
            postFunction : function(x) { 
                
                if(x){
                    try {   
                        var x = JSON.parse(x);
                    } catch(e) {
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
                        
                        \$("#preco").fieldMoney("refresh");
                        \$("#preco_venda").fieldMoney("refresh");
                        
                        // atualiza limites
                        // eos.core.limit.user.get(function(x){
                        //       \$("#users_limit").html(x);
                        // });
                    }
                }
            }
        });
    };
    
    /* editar */
    this.edit = function(x){ 
        \$("#COD").val(x);
        produtos.edit();
    };
    
    /* novo */
    this.new = function(){
        this.reset();
        \$("#produtos_page").DTouchPages("page","right");
    };
    
    /* reset */
    this.reset = function(){  
        
        // this.enable(); // habilita formulario
        
        // reseta campos
        \$("#status").DTouchRadio("value",1);
        \$("#unidade").DTouchRadio("reset");
        \$("#preco").fieldMoney("reset");
        \$("#preco_venda").fieldMoney("reset");
        \$("#marca").fieldAutoComplete("reset")
        
        \$("#COD, #descrp, #modelo, #link, #obs, #partnumber").val("");
                
        // icones
        eos.menu.action.hideAll();
        eos.menu.action.show(["icon_produtos_new","icon_produtos_save"]);
    };
    
    /* enable */
    this.enable = function(){  
        /*
        \$("#status").DTouchRadio("enable");
        \$("#preco").fieldMoney("enable");
        \$("#preco_venda").fieldMoney("enable");
        
        eos.template.field.unlock(\$("#descrp"));
        
        // icones
        eos.menu.action.hideAll();
        eos.menu.action.show(["icon_produtos_new","icon_produtos_save"]);
        
        this.locked(false); // trava do formulario
        */
    };
    
    /* disable */
    this.disable = function(){  
        /*
        \$("#status").DTouchRadio("disable");
        \$("#preco").fieldMoney("disable");
        \$("#preco_venda").fieldMoney("disable");
        
        eos.template.field.lock(\$("#descrp"));
        
        // icones
        eos.menu.action.hideAll();
        eos.menu.action.show(["icon_produtos_new"]);
        
        this.locked(true); // trava do formulario
        */
    };
}

 
/**
 *   Document Ready
 */
\$(document).ready(function() { 
    form = new Form();
    form.initialize(function(){
        // console.log("aqui");
        // \$("#area_tipo").width();
        // \$("#area_tipo").DTouchRadio("resize");
    });
    
    
    
    // \$('#cob_day').datepicker({ changeYear: false, changeMonth: false, dateFormat: 'dd' });
});

</script>
</head>
<body>

    <!-- Formulario -->
    <form >
	
        <!-- Paginas -->
        <div id="produtos_page">
            
                <!-- pagina central -->
                <div id="produtos_page_center">
                    <div id="produtos_container_center">
                    
                        <!-- lista de usuarios -->
                        <div id="produtos_list"></div>
                    
                    </div>
                </div>
                
                <!-- pagina direita -->
                <div id="produtos_page_right">
                        <div class="produtos_page_line">
                                
                                <div id="dados_container">
                                    <div id="descrp_container">
                                        <input type="text" id="descrp" name="descrp" placeholder="Descrição" />
                                    </div>
                                    <div id="marca_container">
                                        <input type="text" id="marca" name="marca" placeholder="Marca" />
                                    </div>
                                    <div id="preco_container">
                                            <input type="text" id="preco" name="preco" placeholder="Valor Custo" />
                                    </div>
                                    <div id="preco_venda_container">
                                            <input type="text" id="preco_venda" name="preco_venda" placeholder="Valor Venda" />
                                    </div>
                                </div>
                                
                                <div id="unidade_container" >
                                    <div id="unidade"></div>
                                </div>
                                                            
                                <div id="status_container" >
                                    <div id="status"></div>
                                </div>
                        </div>              
    
                
                
                    <div id="other_container">
                        <div id="modelo_container">
                            <input type="text" id="modelo" name="modelo" placeholder="Modelo" />
                        </div>
                        <div id="partnumber_container">
                            <input type="text" id="partnumber" name="partnumber" placeholder="Partnumber / Número de Série" />
                        </div>
                        <div id="link_container">
                            <input type="text" id="link" name="link" placeholder="Link" />
                        </div>
                        <div id="obs_container">
                                <textarea id="obs" name="obs" placeholder="Observações" />
                        </div>                
                    </div>
                    
                    
                </div>      

        </div>
        
        
        <input type="hidden" name="COD" id="COD" value="$COD">
    </form>
    
</body>
</html>

HTML

