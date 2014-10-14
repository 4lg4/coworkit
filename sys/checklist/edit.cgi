#!/usr/bin/perl

$nacess = "70";
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
function checklist(){
    
    /* initialize */
    this.initialize = function() {
        // this.list();
    };
    
    /* list, lista de usuarios */
    this.list = function() {
        \$.DActionAjax({
            action : "edit_list.cgi",
            loader : \$("#checklist_list")
        });
    }
    
    /* editar */
    this.edit = function(x){
        var chk = this;
        
        form.reset();
        
        \$("#checklist_page").DTouchPages("page","right");
        
        // icones
        // eos.menu.action.hideAll();
        
        \$("#TKT").val(x);
        
        /* edita formulario */
        \$.DActionAjax({
            action : "edit_edit.cgi",
            req    : "tkt="+x,
            loader : \$("#checklist_page_right"),
            postFunction : function(x){ 
                // console.log(x);
                var checklist = JSON.parse(x);
                
                \$("#COD").val(checklist.COD);
                \$("#descrp").val(checklist.descrp);
                \$("#dtag").val(checklist.dtag);
                \$("#tkt").text("#"+checklist.tkt);
                \$("#cliente").text(checklist.cliente);
                
                // inventario
                if(checklist.inventario){
                    checklist.inventario.forEach(function(i){
                        chk.inventario.add(i);
                    });
                }
                
                // servico
                if(checklist.servico){
                    checklist.servico.forEach(function(i){
                        chk.servico.add(i);
                    });
                }

            }
        });
    };
    
    
    
    /* inventario */
    this.inventario = {
        
        add : function(x){
            /*
            var c       = document.createElement("div")     // container
            ,   f       = document.createElement("input");  // campo hidden
                f.type  = "hidden";
                f.name  = "inventario";
                f.value = x.value;
                
            c.appendChild(f);
            c.innerHTML = x.descrp;
            
            \$("#inventario_list").append(c);
            */
            
            \$("#inventario_list").DTouchRadio("addItem",{
                val    : x.value,
                descrp : x.descrp
            });
            
        },
        
        list : function(){
            
        }
    };
    
    
    /* inventario */
    this.servico = {
        
        add : function(x){  
            var id = eos.core.genId();
            var item  = "<div class='DTouchRadio_list_line'>";
                item += "   <div style='width:40%'>";
                item +=         x.descrp;
                item += "       <input type='hidden' name='usuario_ini' value='"+x.usuario_ini+"'>";
                item += "       <input type='hidden' name='usuario_end' value='"+x.usuario_end+"'>";
                item += "   </div>";
                item += "   <div style='width:60%'>";
                item += "       <div style='width:40%'><input type='text' name='hora_ini' id='hora_ini_"+id+"' value='"+x.hora_ini+"' placeholder='Início'></div>";
                item += "       <div style='width:40%'><input type='text' name='hora_end' id='hora_end_"+id+"' value='"+x.hora_end+"' placeholder='Fim'></div>";
                item += "       <div style='width:10%'></div>";
                item += "   </div>";
                item += "</div>";
            
            // adiciona item
            \$("#servico_list").DTouchRadio("addItem",{
                val    : x.value,
                descrp : item
            });  

            // ajusta campo
            \$("#hora_ini_"+id).fieldDateTime({ 
                type : "date-time",
                placeholder : "Início"
            });
            
            // ajusta campo
            \$("#hora_end_"+id).fieldDateTime({ 
                type : "date-time",
                placeholder : "Fim",
            });
        }
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
		\$("#checklist_page").DTouchPages({
            // pageChange : "right",
            pageCenter : \$("#checklist_page_center"),
            pageRight  : \$("#checklist_page_right"),
			postFunctionCenter : function() {                
               
                checklist.list();
                
                eos.menu.action.hideAll();
            },
			postFunctionRight : function() {
                
                /*
                if(!\$("#TKT").val()){
                    \$("#checklist_page").DTouchPages("page","center");
                }
                */
                
                // icones
                eos.menu.action.hideAll();
                eos.menu.action.show(["icon_checklist_new","icon_checklist_save"]);
                
            },
			onCreate : function() {

                // DTag
                \$("#dtag").fieldNumber({
                    placeholder : "DTag"
                });
                                
                // dados
                \$("#dados_container").DTouchBoxes({ title : "Dados" });
                eos.template.field.text(\$("#descrp"));
                
                // inventario
                \$("#inventario_container").DTouchBoxes();
                \$("#inventario_list").DTouchRadio({ 
                    orientation : "vertical",
                    unique      : true,
                    itemDel     : true,
                    click       : "off",
                    pick        : false
                });
                \$("#inventario_field").fieldAutoComplete({
                    sql_tbl      : "checklist_inventario",
                    // placeholder  : "Itens de Inventário",
                    postFunction : function(x) {
                        checklist.inventario.add({
                            value  : x.value, 
                            descrp : x.descrp
                        });
                    }
                });
                
                // servico
                \$("#servico_container").DTouchBoxes();
                \$("#servico_list").DTouchRadio({ 
                    orientation : "vertical",
                    unique      : true,
                    itemDel     : true,
                    click       : "off",
                    pick        : false
                });
                \$("#servico_field").fieldAutoComplete({
                    sql_tbl      : "checklist_servico",
                    clearOnExit  : true,
                    // placeholder  : "Itens de Serviço",
                    postFunction : function(x) {                        
                        checklist.servico.add({
                            value  : x.value, 
                            descrp : x.descrp
                        });
                    }
                });
                
                // inicializa checklist
                checklist = new checklist();
                checklist.initialize();
             
                
                // inicia formulario inclusao
                form.reset();
            }
        });
    }
    
    /* menu */
    this.menu = function(){
        eos.menu.action.new({ // salvar
            id       : "icon_checklist_save",
            title    : "salvar",
            subtitle : "check",
            click    : function(){
                form.save();
            }
        });        
        
        eos.menu.action.new({ // novo
            id       : "icon_checklist_new",
            title    : "novo",
            subtitle : "check",
            click    : function(){
                form.new();
            }
        });
        
        // esconde icones
        eos.menu.action.hideAll();
    };
    
    /* salvar */
    this.save = function(){
        
        // ajusta radios para salvar
        document.getElementById("inputs").innerHTML = "";
        
        // servico
        \$("input[name=servico_list_radios]").each(function(){
            var f = document.createElement("input");
                f.type  = "hidden";
                f.name  = "servico";
                f.value = \$(this).val();
                
            document.getElementById("inputs").appendChild(f);
        });
        
        // inventario
        \$("input[name=inventario_list_radios]").each(function(){
            var f = document.createElement("input");
                f.type  = "hidden";
                f.name  = "inventario";
                f.value = \$(this).val();
                
            document.getElementById("inputs").appendChild(f);
        });
                
                
        // envia form
        \$.DActionAjax({
            action : "edit_submit.cgi",
            postFunction : function(x) {
                
                console.log(x);
                return;
                
                
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
        checklist.edit(x);
    };
    
    /* novo */
    this.new = function(){
        this.reset();
        \$("#checklist_page").DTouchPages("page","center");
    };
    
    /* reset */
    this.reset = function(){  
        
        // this.enable(); // habilita formulario
        
        // reseta campos
        \$("#dtag").fieldNumber("reset");
        \$("#COD, #descrp, #TKT").val("");
        
        \$("#servico_field").fieldAutoComplete("reset");
        \$("#inventario_field").fieldAutoComplete("reset");
        
        \$("#inventario_list").DTouchRadio("reset","content");
        \$("#servico_list").DTouchRadio("reset","content");
                
        // icones
        eos.menu.action.hideAll();
        eos.menu.action.show(["icon_checklist_new"]);
    };
    
    /* enable */
    this.enable = function(){  
        this.locked(false); // trava do formulario
    };
    
    /* disable */
    this.disable = function(){  
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
    
    
    
    // \$('#dtag').datepicker({ changeYear: false, changeMonth: false, dateFormat: 'dd' });
});

</script>
</head>
<body>

    <!-- Formulario -->
    <form >
	
        <!-- Paginas -->
        <div id="checklist_page">
            
                <!-- pagina central -->
                <div id="checklist_page_center">
                    <div id="checklist_container_center">
                    
                        <!-- lista de usuarios -->
                        <div id="checklist_list"></div>
                    
                    </div>
                </div>
                
                <!-- pagina direita -->
                <div id="checklist_page_right">
                        <div class="checklist_page_line">
                                
                                <div id="dados_container">
                                    <div id="dados_principais">
                                        <div id="tkt"></div>
                                        <div id="cliente"></div>
                                    </div>
                                    <div id="dados_principais2">
                                        <div id="dtag_container">
                                            <input type="text" id="dtag" name="dtag" />
                                        </div>
                                        <div id="descrp_container">
                                            <input type="text" id="descrp" name="descrp" placeholder="Descrição" />
                                        </div>
                                    </div>
                                </div>                                
                                
                        </div>
                        
                        <div class="checklist_page_line">
                            
                            <div id="inventario_container">
                                <div id="inventario_field_container">
                                    <input id="inventario_field" name="inventario_field" placeholder="Itens de Inventário">
                                </div>
                                <div id="inventario_list"></div>
                            </div>
                            
                            <div id="servico_container">
                                <div id="servico_field_container">
                                    <input id="servico_field" name="servico_field" placeholder="Itens de Serviço">
                                </div>
                                <div id="servico_list"></div>
                            </div>
                        </div>              
                </div>               

        </div>
        
        
        <input type="hidden" name="COD" id="COD" value="$COD">
        <input type="hidden" name="TKT" id="TKT" value="$TKT">
        <div id="inputs"></div>
    </form>
    
</body>
</html>

HTML

