#!/usr/bin/perl

$nacess = "2";
require "../cfg/init.pl";

# vars
$ID  = &get('ID');
$COD = &get('COD');
$TBL = &get('TBL');

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
function Defaultmod(){
    
    /* initialize */
    this.initialize = function() {
        this.list();
    };
    
    /* list, lista de usuarios */
    this.list = function() { 
        \$.DActionAjax({
            action : "edit_list.cgi",
            req    : "TBL="+\$("#TBL").val(),
            loader : \$("#defaultmod_list"),
            postFunction : function(x){
               //  console.log(x);
            }
        });
    }
    
    /* editar */
    this.edit = function(x){
        var chk = this;
        
        // form.reset();
        
        \$("#defaultmod_page").DTouchPages("page","right");
        
        // icones
        // eos.menu.action.hideAll();
        
        /* edita formulario */
        \$.DActionAjax({
            action : "edit_edit.cgi",
            req    : "COD="+x+"&TBL="+\$("#TBL").val(),
            loader : \$("#defaultmod_page_right"),
            postFunction : function(x){ 
                
                // form.reset();
                
                // console.log(x);
                // return;
                
                var r = JSON.parse(x);
                
                console.log(r);
                
                \$("#COD").val(r.COD);
                \$("#descrp").val(r.descrp);
                

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
		\$("#defaultmod_page").DTouchPages({
            // pageChange : "right",
            pageCenter : \$("#defaultmod_page_center"),
            pageRight  : \$("#defaultmod_page_right"),
			postFunctionCenter : function() {                
               
                eos.menu.action.hideAll();
                eos.menu.action.show(["icon_defaultmod_new"]);
            },
			postFunctionRight : function() {
                
                // icones
                eos.menu.action.hideAll();
                eos.menu.action.show(["icon_defaultmod_new","icon_defaultmod_save"]);
                
                
            },
			onCreate : function() {            
                // dados
                \$("#dados_container").DTouchBoxes({ title : "Dados" });
                eos.template.field.text(\$("#descrp"));
                
                // inicializa defaultmod
                defaultmod = new Defaultmod();
                defaultmod.initialize();
                
                // ajusta descricao no menu topo (alpha)
                \$("#menu_top_modules").html("<a onclick='eos.core.call.modules.default(\\\""+\$("#TBL").val()+"\\\");'>"+\$("#TBL").val()+"</a>");
            }
        });
    }
    
    /* menu */
    this.menu = function(){
        eos.menu.action.new({ // salvar
            id       : "icon_defaultmod_save",
            title    : "salvar",
            subtitle : "",
            click    : function(){
                form.save();
            }
        });        
        
        eos.menu.action.new({ // novo
            id       : "icon_defaultmod_new",
            title    : "novo",
            subtitle : "",
            click    : function(){
                form.new();
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
                        
                        // apos salvar retorna para lista atualizada
                        form.reset();
                        defaultmod.list();
                        \$("#defaultmod_page").DTouchPages("page","center");
                        
                        // retorna o codigo para formulario
                        // if(x.COD){
                        //    \$("#COD").val(x.COD);
                        // }
                        
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
        defaultmod.edit(x);
        \$("#COD").val(x);
    };
    
    /* novo */
    this.new = function(){
        this.reset();
        \$("#defaultmod_page").DTouchPages("page","right");
    };
    
    /* reset */
    this.reset = function(){  
        // this.enable(); // habilita formulario
        
        // reseta campos
        \$("#COD, #descrp, #codigo").val("");
                
        // icones
        eos.menu.action.hideAll();
       //  eos.menu.action.show(["icon_defaultmod_new"]);
    };
    
    /* enable */
    this.enable = function(){  
     //   this.locked(false); // trava do formulario
    };
    
    /* disable */
    this.disable = function(){  
     //   this.locked(true); // trava do formulario
    };
}


/**
 *   Document Ready
 */
\$(document).ready(function() { console.log("loaded");
    form = new Form();
    form.initialize(function(){
        // console.log("aqui");
        // \$("#area_tipo").width();
        // \$("#area_tipo").DTouchRadio("resize");
    });
    
    
    
    // \$('#dtag').datepicker({ changeYear: false, changeMonth: false, dateFormat: 'dd' });
});

</script>
</head>
<body>

    <!-- Formulario -->
    <form >
	
        <!-- Paginas -->
        <div id="defaultmod_page">
            
                <!-- pagina central -->
                <div id="defaultmod_page_center">
                    <div id="defaultmod_container_center">
                    
                        <!-- lista de usuarios -->
                        <div id="defaultmod_list"></div>
                    
                    </div>
                </div>
                
                <!-- pagina direita -->
                <div id="defaultmod_page_right">
                        <div class="defaultmod_page_line">
                                
                                <div id="dados_container">
                                    <div id="dados_principais">
                                        <div id="descrp_container">
                                            <input type="text" id="descrp" name="descrp" placeholder="Descrição" />
                                        </div>
                                    </div>
                                </div>                                
                                
                        </div>
                        
                        <div class="defaultmod_page_line">
                        </div>              
                </div>               

        </div>
        
        
        <input type="hidden" name="COD" id="COD" value="$COD">
        <input type="hidden" name="TBL" id="TBL" value="$TBL">
    </form>
    
</body>
</html>

HTML

