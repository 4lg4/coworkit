#!/usr/bin/perl

$nacess = "51";
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
function Servicos(){
    
    /* initialize */
    this.initialize = function() {
        this.list();
    };
    
    /* list, lista de usuarios */
    this.list = function() {
        \$.DActionAjax({
            action : "edit_list.cgi",
            loader : \$("#servicos_list")
        });
    }
    
    /* editar */
    this.edit = function(){
        
        \$("#servicos_page").DTouchPages("page","right");
        
        // icones
        // eos.menu.action.hideAll();
        
        /* edita formulario */
        \$.DActionAjax({
            action : "edit_edit.cgi",
            req    : "COD="+\$("#COD").val(),
            loader : \$("#servicos_page_right"),
            postFunction : function(x){ 
                
                var plano = JSON.parse(x);
                
                \$("#descrp").val(plano.descrp);
                \$("#status").DTouchRadio("value",plano.status);
                \$("#valor").fieldMoney("value",plano.valor);
                                
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
		\$("#servicos_page").DTouchPages({
            // pageChange : "right",
            pageCenter : \$("#servicos_page_center"),
            pageRight  : \$("#servicos_page_right"),
			postFunctionCenter : function() {                
               
                servicos.list();
                
                eos.menu.action.hideAll();
                eos.menu.action.show(["icon_servicos_new"]);
            },
			postFunctionRight : function() {
                
                
                // icones
                eos.menu.action.hideAll();

                //if(form.locked()) {
                  //  eos.menu.action.show(["icon_servicos_new"]);
                    // } else {
                    eos.menu.action.show(["icon_servicos_new","icon_servicos_save"]);
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
                
                // valor
                \$("#valor").fieldMoney();
                
                // dados
                \$("#dados_container").DTouchBoxes({ title : "Dados" });
                eos.template.field.text(\$("#descrp"));

                
                // inicializa servicos
                servicos = new Servicos();
                servicos.initialize();
             
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
            id       : "icon_servicos_save",
            title    : "salvar",
            subtitle : "serviço",
            click    : function(){
                form.save();
            }
        });        
        
        eos.menu.action.new({ // novo
            id       : "icon_servicos_new",
            title    : "novo",
            subtitle : "serviço",
            click    : function(){
                // if(eos.core.limit.servicos.verify()){ // dentro do limite
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
        
        if(!\$("#valor").fieldMoney("value")) {
            msg += "Valor <br>";
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
                        
                        \$("#valor").fieldMoney("refresh");
                        
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
        servicos.edit();
    };
    
    /* novo */
    this.new = function(){
        this.reset();
        \$("#servicos_page").DTouchPages("page","right");
    };
    
    /* reset */
    this.reset = function(){  
        
        this.enable(); // habilita formulario
        
        // reseta campos
        \$("#status").DTouchRadio("value",1);
        \$("#valor").fieldMoney("reset");
        \$("#COD, #descrp").val("");
                
        // icones
        eos.menu.action.hideAll();
        eos.menu.action.show(["icon_servicos_new","icon_servicos_save"]);
    };
    
    /* enable */
    this.enable = function(){  
        \$("#status").DTouchRadio("enable");
        \$("#valor").fieldMoney("enable");
        
        eos.template.field.unlock(\$("#descrp"));
        
        // icones
        eos.menu.action.hideAll();
        eos.menu.action.show(["icon_servicos_new","icon_servicos_save"]);
        
        this.locked(false); // trava do formulario
    };
    
    /* disable */
    this.disable = function(){  
        \$("#status").DTouchRadio("disable");
        \$("#valor").fieldMoney("disable");
        
        eos.template.field.lock(\$("#descrp"));
        
        // icones
        eos.menu.action.hideAll();
        eos.menu.action.show(["icon_servicos_new"]);
        
        this.locked(true); // trava do formulario
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
        <div id="servicos_page">
            
                <!-- pagina central -->
                <div id="servicos_page_center">
                    <div id="servicos_container_center">
                    
                        <!-- lista de usuarios -->
                        <div id="servicos_list"></div>
                    
                    </div>
                </div>
                
                <!-- pagina direita -->
                <div id="servicos_page_right">
                        <div class="servicos_page_line">
                                
                                <div id="dados_container">
                                    <div id="descrp_container">
                                        <input type="text" id="descrp" name="descrp" placeholder="Descrição" />
                                    </div>
                                    <div id="valor_container">
                                            <input type="text" id="valor" name="valor" />
                                    </div>
                                </div>
                                
                                <div id="status_container" >
                                    <div id="status"></div>
                                </div>
                            
                        </div>              
                </div>               

        </div>
        
        
        <input type="hidden" name="COD" id="COD" value="$COD">
    </form>
    
</body>
</html>

HTML

