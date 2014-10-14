#!/usr/bin/perl

$nacess = "55";
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
function Planos(){
    
    /* initialize */
    this.initialize = function() {
        this.list();
    };
    
    /* list, lista de usuarios */
    this.list = function(cod) {
        \$.DActionAjax({
            action : "edit_list.cgi",
            loader : \$("#planos_list"),
            postFunction : function(){
                if(cod){
                    \$("#planos_list").DTouchRadio("value",cod);
                }
            }
        });
    };
    
    /* list edit  */
    this.listedit = function() {
        eos.menu.action.show(["icon_planos_new","icon_planos_edit","icon_planos_duplicate"]);
    };
    
    /* duplicate */
    this.duplicate = function(){
        this.edit(true);
    };
    
    /* editar */
    this.edit = function(duplicate){
        
        \$("#planos_page").DTouchPages("page","right");
        
        // icones
        // eos.menu.action.hideAll();
        
        /* edita formulario */
        \$.DActionAjax({
            action : "edit_edit.cgi",
            req    : "COD="+\$("#COD").val(),
            loader : \$("#planos_page_right"),
            postFunction : function(x){ 
                
                var plano = JSON.parse(x);
                
                \$("#descrp").val(plano.descrp);
                \$("#obs").val(plano.obs);
                \$("#cobranca").DTouchRadio("value",plano.cobranca);
                \$("#area_tipo").DTouchRadio("value",plano.area);
                \$("#status").DTouchRadio("value",plano.status);
                \$("#cob_day").val(plano.cobranca_dia);
                \$("#hora").val(plano.hora);
                
                \$("#vigencia_ini").val(plano.vigencia_ini);
                \$("#vigencia_fim").val(plano.vigencia_fim);
                
                \$("#empresa").val(plano.empresa);
                \$("#empresa_descrp").val(plano.empresa_nome);
                
                // se for para duplicar
                if(duplicate) {
                    \$("#COD").val("");
                    eos.menu.action.hide(["icon_planos_duplicate"]);
                    \$("#planos_list").DTouchRadio("reset");
                    
                    \$("#descrp").val("Cópia "+\$("#descrp").val());
                    \$("#obs").val("Cópia "+\$("#obs").val());
                }
                
                
                // plano generico
                \$("#lock").val(plano.lock);
                
                if(plano.lock === "1") {
                    // \$("#empresa_container").DTouchBoxes("hide");
                    \$("#empresa_container, #vigencia_container, #cobranca_container, #dados_last_line").hide();
                } else {
                    \$("#empresa_container, #vigencia_container, #cobranca_container, #dados_last_line").show();
                }
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
		\$("#planos_page").DTouchPages({
            // pageChange : "right",
            pageCenter : \$("#planos_page_center"),
            pageRight  : \$("#planos_page_right"),
			postFunctionCenter : function() {                
               
                // planos.list();
                
                // eos.menu.action.hideAll();
                // eos.menu.action.show(["icon_planos_new"]);
                eos.menu.action.hide(["icon_planos_save"]);
                
                if(\$("#planos_list").DTouchRadio("value")) {
                    eos.menu.action.show(["icon_planos_edit"]);
                }
                    
            },
			postFunctionRight : function() {
                
                
                // icones
                // eos.menu.action.hideAll();

                eos.menu.action.show(["icon_planos_save"]);
                eos.menu.action.hide(["icon_planos_edit"]);
                
                // if(form.locked()) {
                    // eos.menu.action.show(["icon_planos_new"]);
                    // } else {
                    // eos.menu.action.show(["icon_planos_new","icon_planos_save"]);
                    // }
                
                
                \$("#area_tipo").DTouchRadio("resize");
            },
			onCreate : function() {
                
                
                // status
                \$("#status_container").DTouchBoxes({ 
                    title : "Status",
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
                
                // tipos de area
                \$("#area_tipo_container").DTouchBoxes({ 
                    title : "Área",
                    postFunction : function(){
                        
                        \$("#area_tipo").DTouchRadio({
                            orientation : "horizontal",
                            tbl : "empresa_area_tipo",
                            postFunction : function(x){
                                // x.DTouchRadio("disable");
                                // ajusta dimensoes
                                // $(this).DTouchRadio("resize");
                            }
                        });
                    }
                });
                
                
                // cobranca
                \$("#cobranca_container").DTouchBoxes({ 
                    title : "Cobrança",
                    postFunction : function(){
                        
                        \$("#cobranca").DTouchRadio({
                            /*
                            DTouchBox   : {
                                box : \$("#cobranca_container"),
                                title : "Cobrança"
                            },
                            */
                            orientation : "vertical",
                            tbl : "prod_cobranca",
                            postFunction : function(x){
                                // x.DTouchRadio("disable");
                        
                            }
                        });
                    }
                });
                
                // dia cobranca
                \$("#cob_day").fieldNumber({
                    placeholder : "Dia da Cobrança",
                    maxlength   : 2,
                    range       : {
                        min : 1,
                        max : 31
                    }
                });
                
                // horas plano
                \$("#hora").fieldDateTime({
                    type        : "time-hour",
                    placeholder : "Horas do Plano"
                });
                
                // dados
                \$("#dados_container").DTouchBoxes({ title : "Dados" });
                eos.template.field.text(\$("#obs"));
                eos.template.field.text(\$("#descrp"));
                // \$("input[type=text]").each(function(){
                //eos.template.field.text(\$(this));
                    // });
                
                // inicializa planos
                planos = new Planos();
                planos.initialize();
             
                if(isFunction(postFunction)){
                    postFunction.call(this);
                    // console.log('call');
                }
                
                
                // cria campos
    			\$("#empresa").fieldAutoComplete({ 
    				type : "empresa"
    			});
                \$("#empresa_container").DTouchBoxes();
                
                
                // vigencia
                \$("#vigencia_container").DTouchBoxes({
                    title : "Vigência"
                });
                \$("#vigencia_ini").fieldDateTime({
                    type : "date"
                });
                \$("#vigencia_fim").fieldDateTime({
                    type : "date"
                });
                
                // inicia formulario inclusao
                form.reset();
                
                // inicia lista
                planos.list();
            }
        });
    }
    
    /* menu */
    this.menu = function(){

        eos.menu.action.new({ // novo
            id       : "icon_planos_new",
            title    : "novo",
            subtitle : "plano",
            click    : function(){
                // if(eos.core.limit.planos.verify()){ // dentro do limite
                    form.new();
                    //} else {
                    //\$.DDialog({
                    //    type    : "error",
                    //    message : "Limite de usuários excedido ! <br><br> Become a premium !" 
                    //});
                    //}
            }
        });
        
        eos.menu.action.new({ // salvar
            id       : "icon_planos_save",
            title    : "salvar",
            subtitle : "plano",
            click    : function(){
                form.save();
            }
        });
        
        eos.menu.action.new({ // editar
            id       : "icon_planos_edit",
            title    : "editar",
            subtitle : "plano",
            click    : function(){
                planos.edit();
            }
        });
        
        eos.menu.action.new({ // duplicar
            id       : "icon_planos_duplicate",
            title    : "duplicar",
            subtitle : "plano",
            click    : function(){
                planos.duplicate();
            }
        });
        
        // esconde icones
        eos.menu.action.hideAll();
    };
    
    /* salvar */
    this.save = function(){
        
        // valida formulario       
        var msg = "";
        
        // se nao for generico
        if(!\$("#lock").val()) {
            if(!\$("#empresa").val()) {
                msg += "Empresa <br>";
            }
        
            if(!\$("#cobranca").DTouchRadio("value")) {
                msg += "Cobrança <br>";
            }
        
            if(!\$("#hora").val()) {
                msg += "Hora do Plano <br>";
            }
            
            var ini = \$("#vigencia_ini").fieldDateTime("value")
            ,   fim = \$("#vigencia_fim").fieldDateTime("value")
            if(ini.replace(/\-/g,'') > fim.replace(/\-/g,'') || (!\$("#vigencia_ini").fieldDateTime("value") && !\$("#vigencia_fim").fieldDateTime("value"))) {
                msg += "Vigência Inválida <br>";
            }
        }
        
        if(!\$("#area_tipo").DTouchRadio("value")) {
            msg += "Área <br>";
        }
        
        if(!\$("#descrp").val()) {
            msg += "Título <br>";
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
                            
                            planos.list(x.COD);
                        } else {
                            planos.list(\$("#COD").val());
                        }
                        
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
        planos.listedit();
        // planos.edit();
    };
    
    /* novo */
    this.new = function(){
        this.reset();
        \$("#planos_page").DTouchPages("page","right");
    };
    
    /* reset */
    this.reset = function(){  
        
        this.enable(); // habilita formulario
        
        // desfaz formulario generico
        \$("#lock").val("");        
        \$("#empresa_container, #vigencia_container, #cobranca_container, #dados_last_line").show();
        
        // reseta campos
        \$("#cobranca").DTouchRadio("reset");
        \$("#area_tipo").DTouchRadio("reset");
        \$("#status").DTouchRadio("reset");
        \$("#status").DTouchRadio("value",1);
        \$("#cob_day").fieldNumber("reset");
        \$("#hora").fieldDateTime("reset");
        \$("#vigencia_ini").fieldDateTime("reset");
        \$("#vigencia_fim").fieldDateTime("reset");
        \$("#COD, #descrp, #obs, #empresa, #empresa_descrp").val("");
                
        // icones
        eos.menu.action.hideAll();
        eos.menu.action.show(["icon_planos_new"]);
        // eos.menu.action.show(["icon_planos_new","icon_planos_save"]);
    };
    
    /* enable */
    this.enable = function(){  
        \$("#cobranca").DTouchRadio("enable");
        \$("#area_tipo").DTouchRadio("enable");
        \$("#status").DTouchRadio("enable");
        \$("#cob_day").fieldNumber("enable");
        \$("#hora").fieldDateTime("enable");
        
        eos.template.field.unlock(\$("#descrp"));
        eos.template.field.unlock(\$("#obs"));
        
        // icones
        eos.menu.action.hideAll();
        eos.menu.action.show(["icon_planos_new","icon_planos_save"]);
        
        this.locked(false); // trava do formulario
    };
    
    /* disable */
    this.disable = function(){  
        \$("#cobranca").DTouchRadio("disable");
        \$("#area_tipo").DTouchRadio("disable");
        \$("#status").DTouchRadio("disable");
        \$("#cob_day").fieldNumber("disable");
        \$("#hora").fieldDateTime("disable");
        
        eos.template.field.lock(\$("#descrp"));
        eos.template.field.lock(\$("#obs"));
        
        // icones
        eos.menu.action.hideAll();
        eos.menu.action.show(["icon_planos_new"]);
        
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
        <div id="planos_page">
            
                <!-- pagina central -->
                <div id="planos_page_center">
                    <div id="planos_container_center">
                    
                        <!-- lista de usuarios -->
                        <div id="planos_list"></div>
                    
                    </div>
                </div>
                
                <!-- pagina direita -->
                <div id="planos_page_right">
                        <div class="planos_page_line">
                                <!-- empresa -->
                                <div id="empresa_container">
                                    <input type="text" id="empresa" name="empresa" placeholder="Cliente" />
                                </div>
                                
                                
                                <div id="dados_container">
                                    <div id="descrp_container">
                                        <input type="text" id="descrp" name="descrp" placeholder="Título" />
                                    </div>
                                    <div id="obs_container">
                                        <input type="text" id="obs" name="obs" placeholder="Observações" />
                                    </div>
                                    <div id="dados_last_line">
                                        <div id="cob_day_container">
                                            <input type="text" id="cob_day" name="cob_day" />
                                        </div>
                                        <div id="hora_container">
                                            <input type="text" id="hora" name="hora" />
                                        </div>
                                    </div>
                                </div>
                                
                                <div id="area_tipo_container" >
                                    <div id="area_tipo"></div>
                                </div>
                                
                        </div>
                        <div class="planos_page_line">
                            
                                <div id="vigencia_container">
                                    <div id="vigencia_ini_container"><input type="text" name="vigencia_ini" id="vigencia_ini" placeholder="Início"></div>
                                    <div id="vigencia_fim_container"><input type="text" name="vigencia_fim" id="vigencia_fim" placeholder="Fim"></div>
                                </div>
                            
                                <div id="cobranca_container">
                                    <div id="cobranca"></div>
                                </div>
                                
                                <div id="status_container" >
                                    <div id="status"></div>
                                </div>
                            
                        </div>              
                </div>               

        </div>
        
        
        <input type="hidden" name="COD" id="COD" value="$COD">
        <input type="hidden" name="lock" id="lock" >
    </form>
    
</body>
</html>

HTML

